import re
cardsUndo = []
cardsUndoRef = []
CounterMarker =("Damage", "0f74413d-45d6-4c52-b584-201b99af4125")

####################################################
def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} taps {}.'.format(me, card))
    else:
        notify('{} untaps {}.'.format(me, card))	

def untapAll(group, x = 0, y = 0): #Modified it to account for Energy which will be played upside down
	mute()
	for card in group:
            if not card.owner == me:
                continue
            if card.orientation == Rot90:
                card.orientation = Rot0
            if card.orientation == Rot270:
                card.orientation = Rot180
	notify("{} untaps all their cards.".format(me))			

def switchModes(card, x = 0, y = 0): 
	mute()
	alt_count = len(card.alternates)
	if alt_count == 0:
            whisper("{} has no other sides to flip to.".format(card.name))
            return
        side = 0
        for alternate in card.alternates:
            if alternate == card.alternate:
                break
            else:
                side += 1
        if side < alt_count -1:
            card.alternate = card.alternates[side +1]
        else:
            card.alternate = card.alternates[0]
        notify("{}'s {} switches to its {}.".format(me, card, card.type.split('- ')[-1]))


def wish(group, x = 0, y = 0):
    mute()
    if group == me.characters:
        guid, quantity = askCard({"Type":["Character - Head Mode", "Character - Bot Mod", "Character - Alt Mode", "Character - Alt1 Mode", "Character - Alt2 Mode", "Character - Body Mode", "Character - Combiner Mode"]}, "or")
    else:
        guid, quantity = askCard({"Type":["Upgrade - Weapon", "Upgrade - Armor", "Upgrade - Utility", "Action", "Secret Action", "Upgrade - Weapon Armor"]}, "or")
        group = me.hand
    if quantity == 0:
        return
    if quantity < 10:
        card = group.create(guid)
        notify("{} pulled {} from outside the game.".format(me, card))

def combiner(card, x = 0, y = 0):
    mute()
    try:
        card.alternate = "combiner"
        notify("{}'s {} switches to its Combiner Mode.".format(me, card))
    except:
        whisper("I'm sorry, it appears {} has no Combiner Mode.".format(card))

def reshuffle(verbose=True):
    mute()
    if verbose == False:
        for card in me.Scrap:
            card.moveTo(me.Deck)
        shuffle(me.Deck)
        notify("{} reshuffles their Scrap pile into their Deck!".format(me))
    elif confirm("Are you sure you want to reshuffle your Scrap pile into your deck?"):
        for card in me.Scrap:
            card.moveTo(me.Deck)
        shuffle(me.Deck)
        notify("{} reshuffles their Scrap pile into their Deck!".format(me))

def botFaceDown(group = me.Deck, card=''):
    mute()
    card = me.Deck.bottom()
    card.moveToTable(0, 0, forceFaceDown = True)
    notify("{} places the bottom card of their deck on the table face down.".format(me))
    
	
def clearAll(group, x = 0, y= 0):
    notify("{} clears all targets and combat.".format(me))
    for card in group:
##        if card.controller == me:
            card.target(False)
            card.highlight = None

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))
		  
def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

def discard(card, x = 0, y = 0): #Renamed
    card.moveTo(me.piles['Scrap'])
    notify("{} discards {}".format(me, card))

def addCounter(card, x = 0, y = 0):
    mute()
    notify("{} adds 1 counter to {}.".format(me, card))
    card.markers[CounterMarker] += 1

def addCounterX(card, x = 0, y = 0):
    mute()
    quantity = askInteger("How many counters", 0)
    notify("{} adds {} counter to {}.".format(me, quantity, card))
    card.markers[CounterMarker] += quantity

def removeCounter(card, x = 0 , y = 0):
    mute()
    notify("{} removes 1 counter to {}.".format(me, card))
    card.markers[CounterMarker] -= 1

def removeCounterX(card, x = 0, y = 0):
    mute()
    quantity = askInteger("How many counters", 0)
    notify("{} removes {} counter from {}.".format(me, quantity, card))
    card.markers[CounterMarker] -= quantity
	  
def setCounter(card, x = 0, y = 0):
    mute()
    quantity_prior = card.markers[CounterMarker]
    quantity = askInteger("How many counters", 0)
    notify("{} changes {}'s counters from {} to {}.".format(me, card, quantity_prior, quantity))
    card.markers[CounterMarker] = quantity	
		
def flip1(count=1):
    mute()
    flipMany(0,1)

def flipMany(group, count=None, w=0, o=0, u=0, b=0, g=0):
    mute()
    x = 0
    try:
        group + 1
        x = 1
    except:
        pass
    if count == None: count = askInteger("Flip how many cards?", 0)
    try:
        count += 1
        count -= 1
    except:
        return
    if len(me.Deck) == 0:
        reshuffle(False)
    while count > 0:
        card = me.Deck[0]
        if len(card.properties["White Pips"]) > 0 and w == 0 and x != 1:
            count += 2
        flipBattle(1, card)
        try:
            w += int(card.properties["White Pips"])
        except:
            pass
        try:
            o += int(card.properties["Orange Pips"])
        except:
            pass
        try:
            u += int(card.properties["Blue Pips"])
        except:
            pass
        try:
            g += int(card.properties["Green Pips"])
        except:
            pass
        try:
            b += int(card.properties["Black Pips"])
        except:
            pass
        if len(me.Deck) == 0:
            reshuffle(False)
        count -= 1
    notify("{} flips {} orange, {} blue, {} white, {} green and {} black pips!".format(me, o, u, w, g, b))
        
def flipBattle(count=1, card=None):
    mute()
##    card.moveToTable(0,0)
    testing(card)
    card.orientation = Rot270        

def testing(card):
    mute()
    cardsInTable = [c for c in table if c.controller == me and c.orientation != Rot270 and c.orientation != Rot180]
    flippedCardsInTable = [c for c in table if c.controller == me and c.orientation == Rot270]
    if me._id == 1:
        x = 400
        for c in cardsInTable:
            if c.position[0] >= (x - 125):
                x = c.position[0] + 125
    else:
        x = -475
        for c in cardsInTable:
            if c.position[0] < (x+125):
                x = c.position[0] - 125
    if me._id == 1:
        y = 0
        for c in flippedCardsInTable:
            if c.position[1] >= y:
                y = c.position[1] + 10
    else:
        y = -75
        for c in flippedCardsInTable:
            if c.position[1] <= y:
                y = c.position[1] - 10
    try:
        card.moveToTable(x, y)
        if not me._id == 1:
            card.sendToFront()
    except:
        pass

def KO(card, x=0, y=0):
    mute()
    if ("Battle Master" in card.traits or "Sergeant Cog - Artillery, Mechanic" in card.name) and card.alternate == "":
        switchModes(card)
        card.markers[CounterMarker] = 0
        card.orientation = Rot0
        return
    cardsInTable = [c for c in table if c.controller == me and c.orientation != Rot270 and c.orientation != Rot180]
    KOCardsInTable = [c for c in table if c.controller == me and c.orientation == Rot180]
    if me._id == 1:
        x = -500
        for c in cardsInTable:
            if c.position[0] <= (x + 100):
                x = c.position[0] - 150
    else:
            x = 400
            for c in cardsInTable:
                if c.position[0] > (x-150):
                        x = c.position[0] - 150
    if me._id == 1:
        y = 50
        for c in KOCardsInTable:
            if c.position[1] >= y:
                y = c.position[1] + 20
    else:
        y = -175
        for c in KOCardsInTable:
            if c.position[1] <= y:
                y = c.position[1] - 20
    if KOCardsInTable:
        x = KOCardsInTable[0].position[0]
    card.moveToTable(x, y)
    card.orientation = Rot180
    card.filter = '#88ee0000'
    card.sendToBack()

def unKO(card, x=0, y=0):
    mute()
    card.orientation = 0
    card.filter = None

def randomDiscard(group):
    mute()
    card = group.random()
    if card == None: return
    if group==me.piles["VP"]:
        notify("{} randomly discards {} from VP.".format(me,card.name))
    else:
        notify("{} randomly discards {}.".format(me,card.name))
    card.moveTo(me.piles['Scrap'])

def randomDraw(group):
    mute()
    card = group.random()
    if card == None: return
    notify("{} takes a random VP.".format(me))
    card.moveTo(card.owner.hand)

def draw(group, conditional = False, count = 1, x = 0, y = 0): #Added draw function to include choice
    mute()
    for i in range(0,count):
        if len(group) == 0:
            if group == me.Deck:
                reshuffle(False)
            else:
                return
        if conditional == True:
            choiceList = ['Yes', 'No']
            colorsList = ['#FF0000', '#FF0000']
            choice = askChoice("Draw a card?", choiceList, colorsList)
            if choice == 0 or choice == 2:
                return 
        card = group[0]
        card.moveTo(card.owner.hand)
        notify("{} draws a card.".format(me))

def drawMany(group, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("Draw how many cards?", 0)
    if count == None: count = 0
    for card in group.top(count):
        if group == me.Deck:
            if len(me.Deck) == 0:
                reshuffle(False)
        card.moveTo(me.hand)
    notify("{} draws {} cards.".format(me, count))

def drawBottom(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group.bottom().moveTo(me.hand)
    notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
    group.shuffle()
  
def lookAtTopCards(num, targetZone='hand'): #Added function for looking at top X cards and take a card
    mute()
    notify("{} looks at the top {} cards of their deck".format(me,num))
    cardList = [card for card in me.Deck.top(num)]
    choice = askCard(cardList, 'Choose a card to take')
    toHand(choice, show = True)
    me.Deck.shuffle() 
	
def lookAtDeck(): #For Automation
    mute()
    notify("{} looks at their Deck.".format(me))
    me.Deck.lookAt(-1)

def sideboard(group=me.Deck, x = 0, y = 0):
    mute()
    topCards = []
    for c in me.Deck.top(100):
        topCards.append(c)
        c.peek()
    dlg = cardDlg(topCards)
    botCards = []
    for c in me.sideboard:
        botCards.append(c)
        c.peek()
    dlg = cardDlg(topCards, botCards)
    dlg.title = "Sideboarding"
    dlg.label = "Deck"
    dlg.bottomLabel = "Sideboard"
    dlg.text = "Move cards between your deck and sideboard."
    cards = dlg.show()
    for c in reversed(dlg.list):
        c.moveTo(me.Deck)
    for c in dlg.bottomList:
        c.moveTo(me.sideboard)
    me.Deck.visibility = "none"
    me.Sideboard.visibility = "Me"

def playCharacters(group, x = 0, y = 0):
    mute()
    stars = 0
    charactersWorking = me.characters
    if len(me.characters) > 0:
        for card in me.characters:
            try:
                stars += int(card.stars)
            except:
                pass
        if stars > 25:
            whisper("Sorry, you have too many stars to play your characters automatically.")
            charactersWorking = pickCharacters()
    heads = []
    characters = []
    stratagems = []
    for card in charactersWorking:
        if "Head Mode" in card.type:
            heads.append(card)
        else:
            characters.append(card)
        if "Stratagem" in card.type:
            stratagems.append(card)
        else:
            characters.append(card)
    count = len(characters)
    if me._id == 1:
        if count == 1:
            characters[0].moveToTable(-50, 40)
            return
        i = 0
        for card in characters:
            x = round(600/(count-1))*i - 350
            card.moveToTable(x, 40)
            i += 1
    else:
        i = 0
        if count == 1:
            characters[0].moveToTable(-50, -170)
            return
        for card in characters:
            x = round(600/(count-1))*i + 250
            card.moveToTable(x, -170)
            i -= 1
    if len(heads) > 0:
        playHeads(heads)
    if len(stratagems) > 0:
        playStratagems(stratagems)

def playHeads(heads, *args):
    mute()
    for card in heads:
        pickBody(card)

def pickBody(card, *args):
    mute()
    characters = [c for c in table if c.controller == me and "Character" in c.type]
    bodyCharacters =[]
    for c in characters:
        try:
            if c.alternateProperty('bot', 'type') == "Character - Body Mode":
                bodyCharacters.append(c)
        except:
            pass
    dlg = cardDlg(bodyCharacters)
    dlg.title = "Choosing a Bot to Put Your {} on.".format(card.name)
    dlg.text = "Please select a body to put your {} on".format(card.name)
    dlg.min = 1
    dlg.max = 1
    cardSelected = dlg.show()
    try:
        cardSelected = cardSelected[0]
    except:
        pass
    if cardSelected:
        x = cardSelected.position[0]
        y = cardSelected.position[1]
        if me._id == 1:
            card.moveToTable(x+35, y-12)
            card.sendToBack()
        else:
            card.moveToTable(x, y+60)
            card.sendToBack()
    else:
        return
    
def playStratagems(stratagems, *args):
    mute()
    i = 0
    if me._id == 1:
        x = -450
        for card in stratagems:
            card.moveToTable(x, 40 + i * 15)
            i += 1
    else:
        x = 375
        for card in stratagems:
            card.moveToTable(x, -130 - i * 15)
            card.sendToFront()
            i += 1

def playUpgrade(card, *args):
    mute()
    i = 0
    characters = [c for c in table if c.controller == me and "Character" in c.type and "Head" not in c.type and c.orientation != Rot180]
    dlg = cardDlg(characters)
    dlg.title = "Upgrade a Bot With Your {}.".format(card.name)
    dlg.text = "Please select a bot to put your {} on".format(card.name)
    dlg.min = 1
    dlg.max = 1
    cardSelected = dlg.show()
    try:
        cardSelected = cardSelected[0]
    except:
        pass
    if cardSelected:
        x = cardSelected.position[0]
        y = cardSelected.position[1]
        upgrades = [c for c in table if c.controller == me and cardSelected.name in c.filler]
        if len(upgrades) > 0:
            dlg = cardDlg([card], upgrades)
            dlg.title = "Play an Upgrade"
            dlg.text = "Bottom box is equipped upgrades, top box is upgrades to be scrapped."
            dlg.label = "Upgrades to be Scrapped"
            dlg.bottomLabel = "Equipped Upgrades"
            ph = dlg.show()
            for c in dlg.list:
                c.moveTo(me.scrap)
                notify("{} replaces their {}".format(me, c))
            upgrades = dlg.bottomList
        else:
            upgrades.append(card)
        i = 0
        notify("{} plays {} on {}".format(me, card, cardSelected))
        if me._id == 1:
            for card in upgrades:
                card.moveToTable(x-35 + 50*(i%3), y + cardSelected.height + 12*(i//3))
                card.filler = cardSelected.name
                i += 1
        else:
            for card in upgrades:
                card.moveToTable(x+65 - 50*(i%3), y + cardSelected.height - 80 - 12*(i//3))
                card.filler = cardSelected.name
                i += 1
    else:
        return


def scoop(prompt = False, *args):
    mute()
    if prompt != False:
        if not confirm("Are you sure you want to scoop up your cards?  Current setup will be lost"):
            return
    for card in table:
        if card.owner == me: findCharacter(card)
    for card in me.hand: findCharacter(card)
    for card in me.piles['Scrap']: findCharacter(card)
    notify("{} scoops up their cards.".format(me))

def findCharacter(card):
    mute()
    if "Character" in card.Type or len(card.alternates) > 1 or card.Type =="Stratagem":
        card.moveTo(me.characters)
    else:
        card.moveTo(me.Deck)

def pickCharacters(*args):
    dlg = cardDlg(me.Characters)
    dlg.title = "Choosing Cards from Your Character Pile."
    dlg.text = "You have more than 25 stars worth of characters in your Character pile.  Please choose the ones you wish to start the game with."
    dlg.min = 0
    dlg.max = 10
    cardsSelected = dlg.show()
    return cardsSelected

def undo(*args):
    mute()
    global cardsUndo
    if len(cardsUndo) == 0:
        whisper("Sorry, we have no saved card movements to undo.")
        return
    lastMove = cardsUndo.pop()
    index = 0
    for card in lastMove.cards:
        oldCoords = (lastMove.xs[index], lastMove.ys[index])
        newCoords = (card.position[0], card.position[1])
        group = lastMove.fromGroups[index]
        if group == table:
            card.moveToTable(oldCoords[0], oldCoords[1])
        else:
            card.moveTo(group)
        index += 1
        notify("{} undoes their last card movement.".format(me))

def onCardsMoved(args):
    mute()
    global cardsUndo
    global cardsUndoRef
    if args.player != me:
        return
    if args.xs[0] == args.cards[0].position[0] and args.fromGroups[0] == args.cards[0].group:
        return
    i = 0
    for entry in cardsUndoRef:
        try:
            if entry.cards[0].name == args.cards[0].name and entry.fromGroups[0] == args.cards[0].group:
                cardsUndoRef.pop(i)
                return()
            i += 1
        except:
            return
    cardsUndo.append(args)
    cardsUndoRef.append(args)
    if len(cardsUndo) > 10:
        cardsUndo.pop(0)
    if len(cardsUndoRef) > 20:
        cardsUndo.pop(0)
