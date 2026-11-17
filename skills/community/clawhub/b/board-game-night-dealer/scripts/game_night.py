#!/usr/bin/env python3
"""game_night.py — board game night selector: pick, teach, rotation, survey.
Stdlib only. Exit 0 ok, 2 usage/data error."""

import argparse
import json
import os
import sys
from datetime import date

# ---------------------------------------------------------------------------
# Catalog: name, players (min,max), best (player count), minutes, complexity
# 1-5 (1 = party, 5 = heavy euro), category, teach-kit
GAMES = [
    # --- Party / social (complexity 1) ---
    dict(name="Codenames", players=(2, 8), best=5, minutes=15, cx=1,
         cat="party",
         pitch="Two spymasters give one-word clues to a grid of 25 codename cards; their teams guess which cards belong to them, avoiding the assassin.",
         first_turn="Spymaster says 'ocean, 2'. Team discusses, touches ONE card at a time; a wrong guess ends the turn. Spymasters may not speak or gesture beyond the clue.",
         gotchas=["Clue must be ONE word, no rhymes-with or sounds-like tricks",
                  "Touching a card = final; no take-backs",
                  "The assassin card instantly loses the game"]),
    dict(name="Dixit", players=(3, 6), best=5, minutes=30, cx=1,
         cat="party",
         pitch="The storyteller describes a surreal card vaguely; everyone else plays a card matching the description, and all players vote for the original — score by being subtle, not obvious.",
         first_turn="Storyteller says a phrase for their card, everyone submits one card from hand face-down, shuffle, then vote with the two numbered tokens.",
         gotchas=["Exactly right = no points; be oblique",
                  "Voters: don't vote for your own card",
                  "Storyteller must speak, not just gesture"]),
    dict(name="Just One", players=(3, 7), best=5, minutes=20, cx=1,
         cat="party",
         pitch="Cooperative word guessing: everyone writes a one-word clue for the mystery word, duplicates cancel out, then the guesser sees what survived.",
         first_turn="Guesser closes eyes; each other player writes one clue word on their easel; duplicates erased; guesser gets ONE guess.",
         gotchas=["Identical or same-root words are removed, hurting the guesser",
                  "Illegal clue words: same root as the target",
                  "One guess, then reveal"]),
    dict(name="Telestrations", players=(4, 8), best=6, minutes=30, cx=1,
         cat="party",
         pitch="Telephone meets Pictionary: sketch the word, next player guesses the sketch, next sketches the guess — the mutation is the comedy.",
         first_turn="Roll for your secret word, secretly sketch it in 60 seconds, pass the booklet clockwise.",
         gotchas=["No letters, numbers, or symbols in sketches",
                  "Guessers get one guess, written fully",
                  "Keep it quick — the fun is the reveal at the end"]),
    dict(name="Wavelength", players=(2, 12), best=6, minutes=30, cx=1,
         cat="party",
         pitch="Teams position a dial on a spectrum (hot-cold, overrated-underrated) based on a psychic's cryptic clue, scoring by how close they land.",
         first_turn="Psychic draws a spectrum card, spins the dial secretly behind the shield, gives a clue, team debates and guesses the position.",
         gotchas=["Clue cannot reference the spectrum's endpoints directly",
                  "Left/right scoring pins are set before the guess",
                  "Psychic passes the shield after each round"]),
    dict(name="Monikers", players=(4, 10), best=6, minutes=30, cx=1,
         cat="party",
         pitch="Celebrities-salad-bowl game: describe quirky names in round 1 with any words, round 2 one word, round 3 charades — same deck each round, so memory compounds.",
         first_turn="Everyone writes names into the deck. Describe as many as possible in 60 seconds; a passed card sits out that turn.",
         gotchas=["One pass max per turn",
                  "Round 2: literally ONE word, same word repeatable",
                  "Don't say any part of the name in round 1"]),
    dict(name="Skull", players=(3, 6), best=4, minutes=15, cx=1,
         cat="party",
         pitch="Poker-faced pushing of luck: play flower or skull coasters, then bid how many flowers you can flip without hitting a skull.",
         first_turn="Everyone places one coaster face-down; on your turn add a coaster or start a bid; bids must rise; highest bid flips that many of anyone's coasters.",
         gotchas=["You may bid only what's on the table",
                  "Flipping your own stack first is allowed",
                  "Two losses = you're out"]),
    dict(name="So Clover!", players=(3, 6), best=4, minutes=20, cx=1,
         cat="party",
         pitch="Cooperative clue-weaving: write one clue per edge of your clover relating the two visible words, then teammates must reconstruct your clover's placement.",
         first_turn="Write four edge clues relating adjacent keywords, pass the clover; teammates rotate the four clue tokens onto the clover grid.",
         gotchas=["Clue must relate BOTH words on that edge",
                  "No using the keywords themselves",
                  "Consensus before locking a rotation"]),
    # --- Fillers / light (complexity 1.5) ---
    dict(name="Azul", players=(2, 4), best=2, minutes=40, cx=2,
         cat="abstract",
         pitch="Draft tiles from factory displays to your wall mosaic; completing rows and columns scores, hoarding the wrong tiles shatters your floor.",
         first_turn="Take ALL tiles of one color from a factory display, place one in a pattern line, leftovers go to the center; floor tiles score minus.",
         first="",
         gotchas=["First-center-taker also takes the minus-1 tile",
                  "You must place into ONE pattern line per turn",
                  "Column/majority bonuses dominate — plan 2 rounds ahead"]),
    dict(name="Sushi Go!", players=(2, 5), best=3, minutes=15, cx=1,
         cat="card",
         pitch="Pass-and-pick card drafting: build the best sushi meal by combos (wasabi x nigiri, triple sashimi), pudding counts at the very end.",
         first_turn="Keep one card, pass the rest; three rounds; score after the third.",
         gotchas=["Pudding only scores at game end (most/least)",
                  "Wasabi must be played BEFORE nigiri to triple",
                  "Chopsticks let you take two cards on a later turn"]),
    dict(name="Love Letter", players=(2, 4), best=4, minutes=15, cx=1,
         cat="card",
         pitch="16-card deduction duel: use character powers to knock rivals out or end the round holding the highest card.",
         first_turn="Draw one, play one of your two; the played card's power resolves.",
         gotchas=["Count cards: only one Guard per player memory is key",
                  "King/Prince force discards — Prince on yourself is legal",
                  "Princess discard = instant out"]),
    dict(name="The Crew", players=(3, 5), best=4, minutes=30, cx=2,
         cat="cooperative",
         pitch="Cooperative trick-taking to the moon: communication is locked behind strict token rules, so every trick is a tense inference.",
         first_turn="Lead any suit; you MUST follow suit if you can; trump (rockets) only when void.",
         gotchas=["You can't talk about your cards beyond token placement",
                  "Tokens are one-shot per mission: use or lose",
                  "Task cards must be won by the assigned player specifically"]),
    dict(name="6 nimmt!", players=(2, 10), best=5, minutes=30, cx=1,
         cat="card",
         pitch="Everyone simultaneously picks a card from hand; they slot into ascending rows by tens — the 6th card in a row takes the penalty cattle.",
         first_turn="Reveal chosen cards simultaneously; lowest goes first into the row it extends.",
         gotchas=["Card goes into the row with the closest LOWER value",
                  "Taking a row = your card starts a new one on the right",
                  "Negative points: 66 cattle-heads total, lowest wins"]),
    # --- Family / mid (complexity 2-2.5) ---
    dict(name="Ticket to Ride", players=(2, 5), best=4, minutes=60, cx=2,
         cat="family",
         pitch="Claim railway routes across the map by spending colored card sets; connect your secret destination tickets, block rivals' routes.",
         first_turn="Take 2 train cards (or 1 locomotive), OR claim a route, OR draw destination tickets.",
         gotchas=["Claiming a route = exact color count, face-up wilds count as any",
                  "Longest continuous path is +10 at the end",
                  "When one player hits <=2 trains, everyone gets one final turn"]),
    dict(name="Catan", players=(3, 4), best=4, minutes=90, cx=2,
         cat="family",
         pitch="Collect resources from dice rolls matching your settlements' hexes; build, trade, and race to 10 victory points.",
         first_turn="Roll for production; then trade and/or build one or more things (road, settlement, city, dev card).",
         gotchas=["7 = robber: move it, steal, and everyone over 7 cards loses half",
                  "You may only build on your own road network (except initial placement)",
                  "Longest road / largest army are stealable VP cards"]),
    dict(name="Carcassonne", players=(2, 5), best=3, minutes=40, cx=2,
         cat="family",
         pitch="Draw and place map tiles, then deploy a follower as knight, monk, thief, or farmer to score features as the map grows.",
         first_turn="Place your tile edge-matching somewhere, optionally place one meeple on a feature of that tile.",
         gotchas=["Field (farmer) scoring only at game end — commit wisely",
                  "You may only deploy to an unoccupied feature",
                  "Cloisters score 9 points with all 8 neighbors"]),
    dict(name="Kingdomino", players=(2, 4), best=3, minutes=20, cx=2,
         cat="family",
         pitch="Draft domino-shaped terrain tiles to build a 5x5 kingdom; contiguous crowns-per-terrain multiply for score.",
         first_turn="Take a domino from the next-row display; next turn place it edge-matching into your kingdom.",
         gotchas=["Kingdom must fit 5x5 (or lose the domino)",
                  "Domino order = turn order next round (better domino goes earlier)",
                  "Connecting your castle to a single-terrain bonus (+15) at the end"]),
    dict(name="Splendor", players=(2, 4), best=3, minutes=30, cx=2,
         cat="card",
         pitch="Engine-building gem market: buy cards with gem chips; owned cards discount future purchases; race to 15 prestige.",
         first_turn="Take 3 different-color chips, or 2 of one color (if 4+ remain), or reserve/buy a card.",
         gotchas=["Max 10 chips in hand — spend before taking",
                  "Card discounts are permanent gem income",
                  "Noble visits are automatic at 10 points, don't miss one"]),
    dict(name="7 Wonders", players=(3, 7), best=5, minutes=30, cx=2,
         cat="card",
         pitch="Simultaneous card drafting through three ages; build your wonder, chain structures, balance military vs science vs civilian points.",
         first_turn="Pick a card, pay its cost, pass the rest left; everyone resolves simultaneously.",
         gotchas=["Science sets (3 different) score exponentially — deny neighbors",
                  "Military compares only with your two neighbors",
                  "You may burn any card for 3 coins via wonder stage"]),
    dict(name="Point Salad", players=(2, 6), best=4, minutes=20, cx=1,
         cat="card",
         pitch="Two-sided cards: take vegetables or their scoring cards, and you can flip any card later — score-by-committee chaos.",
         first_turn="Take 2 cards from the market: any mix of veggie and scoring.",
         gotchas=["You may flip ONE of your scoring cards to a veggie per turn",
                  "Scoring conditions can conflict; both count",
                  "No hand limit — everything is on the table"]),
    dict(name="King of Tokyo", players=(2, 6), best=4, minutes=30, cx=1,
         cat="family",
         pitch="Yahtzee-style dice as kaiju: roll punch-energy-hearts, stay in Tokyo for points but eat everyone's attacks.",
         first_turn="Roll 6 dice up to 3 times keeping what you like; resolve attacks (in Tokyo hits everyone outside, and vice versa).",
         gotchas=["Heal doesn't work while in Tokyo",
                  "Entering Tokyo is mandatory when it empties",
                  "First to 20 VP or last monster standing wins"]),
    dict(name="Camel Up", players=(3, 8), best=5, minutes=40, cx=2,
         cat="family",
         pitch="Camel-race betting game where stacked camels move as a unit; bet legs and the overall race, root for pyramid dice chaos.",
         first_turn="Roll the pyramid die (moves a camel), or take a betting/movement/audience tile.",
         gotchas=["Camels in a stack move TOGETHER, top carries all",
                 "End-of-leg bets pay best when placed early",
                  "Overall winner/loser cards locked at game end pay big"]),
    dict(name="Quest for El Dorado", players=(2, 4), best=3, minutes=60, cx=2,
         cat="family",
         pitch="Deck-building race through jungle: buy movement cards, cross terrain, first to El Dorado wins — no points, just speed.",
         first_turn="Play movement cards matching the next hex's terrain; buy one card from the market if you like.",
         gotchas=["Terrain types don't mix within one move",
                 "Blocking a single-hex chokepoint is legal and mean",
                  "Trashing weak cards late-game tightens the deck"]),
    # --- Mid-weight strategy (complexity 3) ---
    dict(name="Wingspan", players=(1, 5), best=3, minutes=70, cx=2,
         cat="strategy",
         pitch="Engine-build a bird preserve: birds chain powers off your three habitats, food engine, egg-laying, and bonus card scoring.",
         first_turn="Choose a habitat row and play a bird (pay food+eggs), or gain food / lay eggs / draw birds — each action activates that row's powers.",
         gotchas=["Powers activate left-to-right only when the row's action is taken",
                  "Bird limits per row: 5, 4, 3 + base",
                  "End-of-round goals vary — check them before turn 1"]),
    dict(name="Terraforming Mars", players=(1, 5), best=3, minutes=120, cx=3,
         cat="strategy",
         pitch="Corporations raise Mars' temperature, oxygen, and oceans; projects chain resources in a sprawling tableau race.",
         first_turn="Play a project card by paying its cost, or take a standard action (plants, heat, city, ocean), or pass for cards.",
         gotchas=["TR raises score AND income — tempo matters",
                 "Placement bonuses on the map are first-come",
                  "Production, not resources, is the real currency"]),
    dict(name="Scythe", players=(1, 5), best=4, minutes=115, cx=3,
         cat="strategy",
         pitch="Alternate-history farming mechs: each faction mat plays asymmetrically; engine, territory, and combat race for $6+ coins.",
         first_turn="Pick your top-row action, then its bottom-row enabler (upgrade, deploy, enlist, build, recruit).",
         gotchas=["Combat cards + power commit secretly — bluff the riverwalk",
                 "Popularity brackets multiply final score — don't tank it",
                 "Mechs unlock moves your workers can't do"]),
    dict(name="Viticulture", players=(1, 6), best=3, minutes=90, cx=3,
         cat="strategy",
         pitch="Run a Tuscan vineyard: plant vines, harvest, build the winery, fill wine orders through hand-built worker placement.",
         first_turn="Place a worker on the wake-up chart or a board space; take that action if you can pay its cost.",
         gotchas=["Wine orders need exact value tokens, not just type",
                 "Visitor cards are free actions, read them",
                  "Winter is short — age the right wine first"]),
    dict(name="Everdell", players=(1, 4), best=3, minutes=80, cx=3,
         cat="strategy",
         pitch="Woodland worker placement + city tableau: gather resources in spring, chain critter/construction pairs across seasons.",
         first_turn="Place workers, or prepare for season (reveal events, gain bonuses).",
         gotchas=["Season jump timing: earlier = more workers but less tempo",
                 "Paired critter+construction discounts are the engine",
                 "Events score end-game, don't forget them"]),
    dict(name="Race for the Galaxy", players=(2, 4), best=2, minutes=45, cx=3,
         cat="card",
         pitch="Phase-selection tableau builder: cards are both currency and planets/techs; the icon-reading race rewards pattern recognition.",
         first_turn="Choose a phase secretly; every player gets the phase, chooser gets the bonus.",
         gotchas=["Discarded cards pay for developments/settlements",
                 "Consume x2 wins if nobody else picks consume",
                  "6-cost developments swing 10+ points"]),
    dict(name="Great Western Trail", players=(2, 4), best=3, minutes=120, cx=3,
         cat="strategy",
         pitch="Drive cattle up the trail, building engine along the way: stations, hazards, and the train tempo puzzle.",
         first_turn="Move up to your hand limit, then act on the tile you land on.",
         gotchas=["Auxiliary spaces are free once per turn",
                 "Certificates multiply delivery value",
                 "The train catching the trail's teepee spaces hurts"]),
    dict(name="Cascadia", players=(1, 4), best=2, minutes=45, cx=2,
         cat="abstract",
         pitch="Draft tile+token pairs to build your Pacific Northwest ecosystem; scoring cards change what 'good placement' means.",
         first_turn="Take one tile-token pair, place the tile adjacent to your terrain, place the token per its rule.",
         gotchas=["Token placement rules differ per animal",
                 "Terrain corridors score big — plan connections",
                 "Nature tokens let you swap pairs; save them"]),
    dict(name="Concordia", players=(2, 5), best=4, minutes=100, cx=3,
         cat="strategy",
         pitch="Hand-driven economy: cards are your actions, map presence is your engine, and final scoring re-prices everything you did.",
         first_turn="Play a card (Tribune, Architect, etc.) from hand; when you take cards back, that's your tempo reset.",
         gotchas=["No dice, no combat — the tension is card tempo",
                 "Buying cards adds actions AND endgame scoring",
                 "Houses multiply the card's scoring category"]),
    dict(name="Brass: Birmingham", players=(2, 4), best=3, minutes=150, cx=4,
         cat="heavy",
         pitch="Industrial revolution network builder: cotton mills, breweries, and canals-to-rails eras with a merciless loan economy.",
         first_turn="Take a loan or build in the canal era; income beats points early.",
         gotchas=["Overbuilding rivals is legal and devastating",
                 "Beer is consumed, not sold, in networks",
                 "Rail era doubles the map — location, location"]),
    dict(name="Agricola", players=(1, 5), best=3, minutes=120, cx=4,
         cat="heavy",
         pitch="17th-century farm survival: feed family each harvest while growing crops, livestock, and the family itself.",
         first_turn="Place a worker on an action space (resources, building, fences); actions vanish when taken.",
         gotchas=["Begging cards are -3 each: never starve",
                 "Renovations unlock occupations and minor improvements",
                 "Family growth without room is impossible"]),
    dict(name="Viticulture Essential Edition", players=(1, 6), best=3, minutes=90, cx=3,
         cat="strategy",
         pitch="The streamlined Viticulture core with structure cards — wake-up order tension plus wine-order fulfillment.",
         first_turn="Place a worker; consider the wake-up chart bonus for going late.",
         gotchas=["Late wake-up bonuses can out-earn early tempo",
                 "Fields need matching vines to your climate",
                 "Fill orders by exact value — cellar planning"]),
    dict(name="Power Grid", players=(2, 6), best=5, minutes=120, cx=3,
         cat="heavy",
         pitch="Auction power plants, buy fuel, wire cities; turn order flips leader/loser each round — being first is a burden.",
         first_turn="Auction a plant from the market; everyone who wins one then buys fuel.",
         gotchas=["Resource prices rise as supplies deplete",
                 "Step 2 opens the third connection tier",
                 "Bidding wars lose more games than they win"]),
    dict(name="Dominion", players=(2, 4), best=3, minutes=30, cx=2,
         cat="card",
         pitch="The original deck-builder: buy action/treasure/victory cards, shuffle, and race to estates in a 17-card kingdom.",
         first_turn="Play treasures, buy one card, one action — read the kingdom before anyone shuffles.",
         gotchas=["Trash the starting Estates/Coppers when the kingdom allows",
                 "Action economy (villages) enables card draw engines",
                 "Green clog: buy victory only when the engine is hot"]),
    dict(name="Lost Ruins of Arnak", players=(1, 4), best=3, minutes=90, cx=3,
         cat="strategy",
         pitch="Deck-building meets worker placement on a jungle expedition: resources, guardian idols, and research tracks.",
         first_turn="Send an assistant to a site, or play a card (its action + maybe its free bonus).",
         gotchas=["Fear cards are dead weight — purge them",
                 "Research tracks pay escalating one-time bonuses",
                 "Idols need to be covered by assistants to score"]),
    dict(name="Root", players=(2, 4), best=4, minutes=90, cx=3,
         cat="strategy",
         pitch="Asymmetric woodland war: cats industrialize, birds zealously decree, vagabond adventures — each faction is its own game.",
         first_turn="Read your faction board's turn structure aloud; then follow it exactly.",
         gotchas=["Each faction breaks a rule; teach one at a time",
                 "Overextending invites coalitions against you",
                 "Dominance cards replace VP victory — watch them"]),
    dict(name="Spirit Island", players=(1, 6), best=2, minutes=120, cx=4,
         cat="cooperative",
         pitch="Anti-colonial coop: you are island spirits driving invaders back with elemental powers, fear, and cascading blight.",
         first_turn="Growth (energy/presence), then pay for power cards by element matching.",
         gotchas=["Blight cascade can flip the island early",
                 "Element timing: innates fire BEFORE card plays resolve",
                 "Fear levels change victory conditions"]),
    dict(name="Patchwork", players=(2, 2), best=2, minutes=30, cx=2,
         cat="abstract",
         pitch="Two-player quilt duel: buy patches with buttons and time, Tetris them onto your board, race the income clock.",
         first_turn="Advance to the next patch and buy it with buttons + time tokens.",
         gotchas=["Time = turn order: lag intentionally for the 1x1 specials",
                 "Button income each time you pass a income space",
                 "7x7 completion bonus is real — race for it"]),
    dict(name="Jaipur", players=(2, 2), best=2, minutes=30, cx=2,
         cat="card",
         pitch="Two-player market bazaar: trade camels and goods, sell sets before the market floods, ride the bonus tiles.",
         first_turn="Take goods, swap with camels, or sell a set of one good.",
         gotchas=["Camels are currency, not goods — herd stays tabled",
                 "Selling big sets grabs the juicy bonus tiles first",
                 "Market refill can hand your rival the win"]),
    dict(name="7 Wonders Duel", players=(2, 2), best=2, minutes=30, cx=2,
         cat="card",
         pitch="Two-player 7 Wonders: pyramid drafting, tug-of-war tokens, and three instant-win paths that keep both players honest.",
         first_turn="Take an available card from the pyramid (uncovered ones first).",
         gotchas=["Military token push can auto-win at the 8th space",
                 "Science pairs = a symbol you own twice, not two pairs",
                 "Discard-for-money is sometimes correct"]),
    dict(name="Star Realms", players=(2, 2), best=2, minutes=20, cx=2,
         cat="card",
         pitch="Space-combat deck-builder: trade authority from bases and blobs, allies chain in-faction bonuses.",
         first_turn="Play your hand, buy one card from the trade row, optionally scrap cards.",
         gotchas=["Ally abilities need another card of that faction in play",
                 "Outposts must be destroyed before anything else",
                 "Scrap-decline: thinning beats buying big"]),
    dict(name="The Quacks of Quedlinburg", players=(2, 4), best=4, minutes=45, cx=2,
         cat="family",
         pitch="Push-your-luck potion brewing: draw ingredients from your bag, stop before the cherry bomb explodes your cauldron.",
         first_turn="Draw and place chips one at a time; rubies let you draw one more; stop before white score tracks overflow.",
         gotchas=["Blue tear upgrades EVERY future drop of that color",
                 "Exploding still scores your placed value minus 1 chip",
                 "The 2-ruby fortune tokens change the game"]),
    dict(name="Century: Spice Road", players=(2, 5), best=4, minutes=45, cx=2,
         cat="family",
         pitch="Straightforward resource engine: upgrade spices, chain caravan cards, claim point tiles before the market empties.",
         first_turn="Play a card (gather/upgrade/trade), rest to take your hand back, or claim a point tile.",
         gotchas=["Hand size limits your combo length — rest timing",
                 "Upgrades are free, trade ratios matter",
                  "Six point tiles ends the game"]),
    dict(name="Coup", players=(2, 6), best=5, minutes=15, cx=1,
         cat="party",
         pitch="Bluffing micro-game: claim Duke, Assassin, Captain powers you may not hold; challenge and lose a card, call right and gain the tempo.",
         first_turn="Take income or foreign aid, or claim a character action.",
         gotchas=["Losing both influence cards = eliminated",
                 "Successful challenges force the claimant to flip a card",
                 "Bluffing Captain to steal is a legal strategy"]),
    dict(name="The Resistance: Avalon", players=(5, 10), best=7, minutes=30, cx=1,
         cat="party",
         pitch="Hidden-identity missions: loyal servants of Arthur vs Minions of Mordred, with Merlin knowing but unable to say.",
         first_turn="Propose a team; everyone votes approve/reject; approved teams go on the mission secretly succeed/fail.",
         gotchas=["5th rejected vote auto-passes — watch the count",
                 "Merlin must steer subtly or be assassinated",
                 "One fail card fails a mission (usually)"]),
    dict(name="Dominant Species", players=(2, 6), best=4, minutes=180, cx=5,
         cat="heavy",
         pitch="Evolutionary warfare on a hex ice age map: action planning, adaptation, and brutal speciation dominance scoring.",
         first_turn="Place action pawns on the planning board; execution resolves in fixed order after all placements.",
         gotchas=["Planning is simultaneous; read the whole board first",
                 "Glaciation deletes hexes — tundra is a safe haven",
                 "Domination cards re-score everything; timing is huge"]),
    dict(name="Twilight Struggle", players=(2, 2), best=2, minutes=180, cx=4,
         cat="heavy",
         pitch="Cold War card-driven duel: every card helps you OR your opponent; manage the hand you're dealt across three decades.",
         first_turn="Play a card for ops (event OR ops, not both) — your rival's event still fires.",
         gotchas=["Playing the rival's event for ops triggers THEIR event",
                 "DEFCON limits war regions — pace the escalations",
                  "Space race is a card-dump valve"]),
    dict(name="Pandemic Legacy Season 1", players=(2, 4), best=4, minutes=60, cx=3,
         cat="cooperative",
         pitch="The campaign that made legacy games famous: your wins and losses permanently scar the board and unlock the story.",
         first_turn="Set up the base game per the campaign book; DO NOT open sealed components early.",
         gotchas=["Open envelopes only when told — no peeking",
                 "Losses carry forward: the game adapts",
                  "Name your characters; you'll remember them"]),
    dict(name="Exit: The Game — The Abandoned Cabin", players=(1, 6), best=4, minutes=90, cx=2,
         cat="cooperative",
         pitch="Tabletop escape room: puzzle book, decoding wheel, and components you're allowed to fold, tear, and destroy.",
         first_turn="Read the intro, examine the starting room, note the help-card order (3 hints per puzzle).",
         gotchas=["Materials are single-use — one play per copy",
                 "Decode carefully: one wrong spin wastes minutes",
                  "Score by time + hint cards used"]),
    dict(name="Sherlock Holmes Consulting Detective", players=(1, 8), best=3, minutes=90, cx=2,
         cat="cooperative",
         pitch="Read the newspaper, pick leads, visit addresses in the directory — beat Sherlock's score if you can.",
         first_turn="Read the case intro, then visit any two addresses from the lead list.",
         gotchas=["Every extra visit costs you points — be selective",
                 "The newspaper is not optional reading",
                 "Discuss before visiting; it's conversation, not racing"]),
    dict(name="Obsession", players=(1, 4), best=2, minutes=90, cx=3,
         cat="strategy",
         pitch="Victorian family reputation duel: host the right activities, court the gentry, renovate the estate one room at a time.",
         first_turn="Play a family/guest card to its matching room tile, gaining reputation and service effects.",
         gotchas=["Deck cycling = reputation engine; guest count matters",
                 "Courtship tile race ends rounds suddenly",
                 "Silence rumors before they spread"]),
    dict(name="Nusfjord", players=(1, 5), best=2, minutes=60, cx=3,
         cat="strategy",
         pitch="Rosenberg's tight fishing-village euro: feed the elders, build the harbor, sneak in buildings before the Shares deck empties.",
         first_turn="Place workers on the action board; reserve the fish you'll need to pay elders.",
         gotchas=["Elders demand fish every round — stockpile or starve",
                 "Public buildings are first-come",
                 "Company shares pay out endgame bonuses"]),
    dict(name="Ra", players=(2, 5), best=4, minutes=45, cx=2,
         cat="auction",
         pitch="Push-your-luck auction: suns bid on lots of tiles; drawing Ra ends the epoch and forces resolution.",
         first_turn="Flip tiles into the lot; call Ra to force an auction, or bid when someone else does.",
         gotchas=["Higher-numbered suns win ties for later position",
                 "Disaster tiles eat your nicest civilization",
                 "Epoch 3 monument double-scoring warps value"]),
    dict(name="Modern Art", players=(3, 5), best=4, minutes=45, cx=2,
         cat="auction",
         pitch="You are both gallery and collector: sell paintings to your rivals, then buy theirs — positioning the market for your holdings.",
         first_turn="Play a card from hand to sell it via its auction type; the seller earns the price.",
         gotchas=["Once-through deck: track which artist is nearly out",
                 "Buying your own sale keeps it cheap but wastes money",
                 "5th painting of an artist triples value"]),
    dict(name="For Sale", players=(3, 6), best=5, minutes=20, cx=1,
         cat="auction",
         pitch="Two-phase property flip: bid coins for houses, then sell houses for checks — matching the market's rhythm.",
         first_turn="Open bidding on a property row; pass = take the cheapest remaining for half your last bid.",
         gotchas=["Coin conservation: leftover coins are wasted",
                 "Sell order is driven by flipped checks; high house not always best",
                  "Passing early gets you a house + a rebate"]),
    dict(name="Cash 'n Guns", players=(4, 8), best=6, minutes=30, cx=1,
         cat="party",
         pitch="Foam-gun loot split: point, bluff, and sometimes take the bullet for the bigger pile of cash.",
         first_turn="Load your bullet (click or bang); everyone aims; cowardice keeps you alive but poor.",
         gotchas=["Shame on targeting the same person every round",
                 "Hero cards need a bullet spent to earn",
                 "Godfather distributes loot on ties"]),
    dict(name="Deception: Murder in Hong Kong", players=(4, 12), best=6, minutes=20, cx=1,
         cat="party",
         pitch="The forensic scientist knows the murder combo but can only communicate via scene boards; investigators deduce, the murderer misdirects.",
         first_turn="Scientist places scene tokens silently; investigators each point ONE finger; murderer wins if missed.",
         gotchas=["Scientist cannot speak or gesture beyond tokens",
                 "The murderer picks their own combo cards",
                  "Accomplice mode: one player secretly helps the killer"]),
    dict(name="Magic Maze", players=(1, 8), best=5, minutes=15, cx=2,
         cat="cooperative",
         pitch="Real-time silent coop: everyone shares one hand of movement abilities, no talking, escape the mall before the timer flips.",
         first_turn="Start the sand timer; move any pawn you're allowed to; pass the 'do something' token when stuck.",
         gotchas=["ABSOLUTE silence — even giggling is cheating",
                 "Anyone can move any eligible pawn",
                 "Losing focus token rules force engagement"]),
    dict(name="The Mind", players=(2, 4), best=3, minutes=15, cx=1,
         cat="party",
         pitch="Play your numbered cards 1-99 in ascending order as a team — without communicating at all. It shouldn't work; it does.",
         first_turn="Deal the round's cards; everyone plays lowest-to-highest by feel; throwing stars discard mistakes.",
         gotchas=["No signals, sounds, or table-talk",
                 "Throwing stars are team-owned — use in silence",
                  "Lives lost never return; level count matters"]),
    dict(name="Welcome To...", players=(1, 100), best=3, minutes=25, cx=2,
         cat="roll-and-write",
         pitch="Flip-and-write suburb planning: street numbers, pools, parks, and temp-boost chaining on everyone's own sheet.",
         first_turn="Flip three card pairs; each player picks ONE pair and writes; rinse, repeat, no waiting for anyone.",
         gotchas=["Streets ascend left to right — plan number gaps",
                  "Fence-building is once per round, use it",
                  "Everyone plays simultaneously — no downtime"]),
    dict(name="Cartographers", players=(1, 100), best=4, minutes=30, cx=2,
         cat="roll-and-write",
         pitch="Map-drawing expedition: trace terrain into your grid, score the season's edicts, survive the monster invasions.",
         first_turn="Flip an explore card; every player draws that shape's terrain into their map.",
         gotchas=["Edges don't wrap; ruins must be adjacent",
                 "Monsters score negative — box them in",
                 "Edict variety: read the season's two before drawing"]),
    dict(name="Railroad Ink", players=(1, 6), best=2, minutes=30, cx=2,
         cat="roll-and-write",
         pitch="Route-laying network puzzle: connect exits through your 7x7 grid, dice by dice, stations and lakes optional.",
         first_turn="Roll the route dice; draw those connections into your grid; repeat 7 rounds.",
         gotchas=["Center spaces double network scoring",
                 "Longest road/rail bonuses pay only if completed",
                 "Special structures are once each — choose wisely"]),
    dict(name="Hadrian's Wall", players=(1, 6), best=1, minutes=90, cx=3,
         cat="roll-and-write",
         pitch="Mega-flip-and-write at the edge of empire: soldiers, buildings, and trade chains across linked grids in a Roman fort.",
         first_turn="Place your meeple to activate a line of Roman life; chain adjacent bonuses.",
         gotchas=["Milecastles link sections — plan the whole fort",
                 "Discipline chains are the scoring engine",
                  "Theft/patrol balance decides the north wall"]),
    dict(name="It's a Wonderful World", players=(1, 5), best=4, minutes=45, cx=2,
         cat="card",
         pitch="Fast card-drafting engine builder: cards are resources or developments, empire piles score in one final sweep.",
         first_turn="Draft a card; keep or recycle it for resources; Empire deck development each turn.",
         gotchas=["Recycling gives kredits to finish bigger cards",
                 "Completion bonuses chain into future turns",
                  "Empire cards score by category coverage"]),
    dict(name="Ark Nova", players=(1, 4), best=2, minutes=150, cx=4,
         cat="heavy",
         pitch="Modern zoo Tycoon-size euro: enclosures, conservation projects, and appeal-vs-reputation dual tracks.",
         first_turn="Play association or builder cards from your 5-card row; action strength grows each round.",
         gotchas=["Reputation x Appeal interplay gates break-ins",
                 "Conservation projects have hard prereqs",
                 "Action upgrades compound — early dirt cheap"]),
    dict(name="Dune: Imperium", players=(1, 4), best=3, minutes=120, cx=3,
         cat="strategy",
         pitch="Deck-building worker placement hybrid: intrigue cards, faction alliances, and the spice must flow to victory points.",
         first_turn="Send an agent to a row space; play cards for perspoin benefits, then purchase from the market row.",
         gotchas=["Agent spaces are exclusive — tempo matters",
                 "Intrigue cards resolve at combat resolution",
                 "High Council slots flip value late game"]),
    dict(name="Lost Cities", players=(2, 2), best=2, minutes=30, cx=2,
         cat="card",
         pitch="Two-player push-your-luck expeditions: commit to color runs, investment multipliers, and the 20-point entry fee.",
         first_turn="Play or discard a card, then draw from deck or discards.",
         gotchas=["Handshake cards multiply wins AND losses",
                 "Discard piles are public draws — deny carefully",
                 "8+ card color runs pay huge; 3-card runs lose"]),
    dict(name="Battle Line", players=(2, 2), best=2, minutes=30, cx=2,
         cat="card",
         pitch="Poker-hand flags in formation: build 3-card fronts, bluff formations, and claim 5 of 9 flags (3 adjacent for blitz).",
         first_turn="Play one card to a flag, then draw.",
         gotchas=["Flags resolve immediately when both sides have 3",
                 "Tactics cards break the standard rules — read twice",
                 "Claim 3 adjacent flags for the sudden win"]),
    dict(name="Hanabi", players=(2, 5), best=4, minutes=25, cx=2,
         cat="cooperative",
         pitch="Cooperative fireworks: you see everyone's cards but your own; spend clue tokens to hint, spend discards to earn them.",
         first_turn="Give a clue (color or number) or discard; then draw; you NEVER look at your own hand.",
         gotchas=["Clues are color OR number, never both",
                 "Misplayed card = permanent loss",
                 "Perfect-score 25 needs table discipline"]),
    dict(name="The Quest for El Dorado", players=(2, 4), best=3, minutes=60, cx=2,
         cat="family",
         pitch="Race across jungle hexes with a deck you improve as you go — terrain-matched movement, blocking chokes, thin decks win.",
         first_turn="Move with cards matching terrain, or buy from the market.",
         gotchas=["Discard to ride the rapids once",
                 "Market refill slides — cheap cards shift value",
                  "Block chokepoints: one hex can stall a rival"]),
    dict(name="Azul: Summer Pavilion", players=(2, 4), best=3, minutes=40, cx=2,
         cat="abstract",
         pitch="Azul's bigger sequel: round-colored wilds, pattern-building toward statues and columns on a mandala board.",
         first_turn="Draft tiles from factory displays; wilds (gold) fill any color line.",
         gotchas=["Scoring statue/-column/windows endgame dominates",
                 "Floor penalties hurt more than base Azul",
                 "Round color tiles double if placed right"]),
    dict(name="Calico", players=(1, 4), best=2, minutes=45, cx=2,
         cat="abstract",
         pitch="Quilting cats: place hex patches to attract cats and button-pop goals in a cozy-but-brutal optimization.",
         first_turn="Pick one of 3 patches, place adjacent; market refills.",
         gotchas=["Cat patterns need EXACT color counts",
                 "Button goals overfill = zero points",
                  "Needle token lets you bank a patch for later"]),
    dict(name="The Gnomes of Nottingham", players=(3, 6), best=4, minutes=30, cx=1,
         cat="party",
         pitch="Absurdist bluffing market: buy junk, sell stories, the sheriff inspects bags of dubious honesty.",
         gotchas=["Bribery is the core mechanic, embrace it",
                 "Bags hold exactly 5 goods",
                 "Set collection pays in multiples"]),
    dict(name="Sheriff of Nottingham", players=(3, 5), best=4, minutes=60, cx=1,
         cat="party",
         pitch="Smuggle goods past the sheriff: declare bags, bribe, bluff; caught contraband is confiscated, honest goods pay out.",
         first_turn="Load your bag (up to 5 goods), declare one type, bribe/negotiate, sheriff opens or passes.",
         gotchas=["Declared goods must be legal — you can't lie about type, only quantity",
                 "Market prices fluctuate by round",
                 "King/Queen bonuses for legal-good majority"]),
    dict(name="Codenames Duet", players=(2, 2), best=2, minutes=15, cx=1,
         cat="party",
         pitch="Two-player cooperative Codenames: both see assassin-adjacent words, timed turns, shared guessing.",
         first_turn="Clue-giver alternates; guess together; unlimited guesses after the first correct.",
         gotchas=["3 assassins end the game",
                 "Timer flips each turn",
                  "Both players share the giver role"]),
    dict(name="Targi", players=(2, 2), best=2, minutes=60, cx=2,
         cat="strategy",
         pitch="Two-player worker placement on a grid of tribal cards: intersections give bonus actions, goods trade for points.",
         first_turn="Place your 3 Targi on the grid edge cards; intersections activate.",
         gotchas=["Robber blocks a row/column each round",
                 "Intersection actions are the engine",
                 "Tribe cards pay endgame if fed"]),
    dict(name="Watergate", players=(2, 2), best=2, minutes=60, cx=3,
         cat="card",
         pitch="Nixon vs Journalists card duel: momentum on the evidence track, one side buries the story, the other impeaches.",
         first_turn="Play a card for its event or movement; initiative token decides who acts first.",
         gotchas=["Evidence momentum swings wildly — track it",
                 "Some events trash the opponent's board state",
                 "Two board sections: campaign + investigation"]),
    dict(name="Undaunted: Normandy", players=(2, 2), best=2, minutes=60, cx=2,
         cat="war",
         pitch="Deck-building WW2 tactical duel: squads gain experience, fog-of-war cards, and casualty-thinning decks.",
         first_turn="Play cards to activate/move/fire; draw back to 4.",
         gotchas=["Casualties go to the top of the discard: clunk hands",
                 "Objectives, not annihilation, win scenarios",
                 "Terrain cover modifies dice heavily"]),
    dict(name="Memoir '44", players=(2, 2), best=2, minutes=60, cx=2,
         cat="war",
         pitch="Scenario-driven WW2 commands: left/center/right order cards, dice combat, and terrain that matters.",
         first_turn="Play an order card activating units in that section.",
         gotchas=["Cards gate WHICH units move — plan sections",
                 "Retreat flags push units off the map",
                 "Scenario special rules override the book"]),
    dict(name="Twilight Imperium 4", players=(3, 6), best=6, minutes=360, cx=5,
         cat="heavy",
         pitch="The 4X epic: galactic politics, trade, tech trees, and plastic dreadnoughts in a six-hour negotiation marathon.",
         first_turn="Strategy phase pick, then action phase: tactical or strategic actions per round.",
         gotchas=["Politics card agenda can flip the game",
                 "Victory points via objectives ONLY — war is a tool",
                 "Table talk is the real core mechanic"]),
    dict(name="Gaia Project", players=(1, 4), best=3, minutes=150, cx=4,
         cat="heavy",
         pitch="Terra Mystica in space: 14 asymmetric factions, tech tracks, and a galaxy of planets to terraform.",
         first_turn="Build a mine on a convertible planet; charge power from neighbors.",
         gotchas=["Power charges are free tempo from rivals' builds",
                 "Round boosters swap each round — timing",
                 "Tech tiles chain into endgame scoring"]),
    dict(name="Terra Mystica", players=(2, 5), best=4, minutes=120, cx=4,
         cat="heavy",
         pitch="Seven factions terraform adjacent terrain: cult tracks, town founding, and the power-bowl economy.",
         first_turn="Transform and build a dwelling; check your terrain ring.",
         gotchas=["Faction terrain dictates expansion path",
                 "Priests to cult tracks pay round bonuses",
                 "Power burns are the tempo lever"]),
    dict(name="Clank!", players=(2, 4), best=3, minutes=60, cx=2,
         cat="card",
         pitch="Deck-building dungeon crawl: delve deep, grab artifacts, and get OUT before the dragon's clank draws blood.",
         first_turn="Play skills/movement/attack; buy from the dungeon row; clank cubes go into the bag.",
         gotchas=["Deeper artifacts pay more but the exit is far",
                 "Dragon draws hurt everyone with clank in bag",
                 "Market cards synergize — engine fast, escape faster"]),
    dict(name="Quacks", players=(2, 4), best=4, minutes=45, cx=2,
         cat="family",
         pitch="Quacks of Quedlinburg core game (see entry above for teach notes).",
         first_turn="Draw chips; stop before explosion.",
         gotchas=["See The Quacks of Quedlinburg"]),
    dict(name="Souq", players=(2, 6), best=4, minutes=30, cx=1,
         cat="party",
         pitch="Simultaneous haggling micro-game: set collection with a rotating market and one-shot special powers.",
         first_turn="Play bid tokens on market stalls; highest takes goods, ties carry over.",
         gotchas=["Bids stay placed until won",
                 "Special powers are once-per-game",
                 "Set multipliers beat singles"]),
]

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "game_night.json")


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"rotation": [], "picks": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def find_game(name):
    target = name.strip().lower()
    for g in GAMES:
        if g["name"].lower() == target:
            return g
    # fuzzy: prefix match
    for g in GAMES:
        if g["name"].lower().startswith(target):
            return g
    return None


def teach_time(g):
    """minutes to teach, from complexity."""
    return int(3 + g["cx"] * 4)


# ---------------------------------------------------------------------------
# Commands


def cmd_pick(args):
    exclude = {x.strip().lower() for x in (args.exclude or "").split(",") if x.strip()}
    state = load_state()
    recent = [p.lower() for p in state.get("picks", [])[-3:]]
    picks = []
    for g in GAMES:
        lo, hi = g["players"]
        if args.players < lo or args.players > hi:
            continue
        if args.complexity_max is not None and g["cx"] > args.complexity_max:
            continue
        if g["name"].lower() in exclude:
            continue
        # fit: distance from best player count
        pfit = 1.0 / (1 + abs(args.players - g["best"]))
        # time fit: penalty if longer than budget, bonus for closeness
        tfit = 1.0 if g["minutes"] <= args.minutes else max(0.0, 1 - (g["minutes"] - args.minutes) / 60)
        # repeat penalty
        rep = 0.5 if g["name"].lower() in recent else 1.0
        # teach budget check
        tt = teach_time(g)
        tpen = 1.0 if args.minutes >= 60 else (1.0 if tt <= 10 else 0.6)
        score = (pfit * 2.0 + tfit * 1.5) * rep * tpen
        why = []
        why.append(f"supports {args.players} (best {g['best']})")
        why.append(f"{g['minutes']} min")
        if g["cx"] == 1:
            why.append("party-light rules")
        picks.append((score, g, why, tt))

    if not picks:
        die("no games in catalog match the constraints — loosen them")

    picks.sort(key=lambda t: -t[0])
    print("=" * 62)
    print(f"  GAME NIGHT PICKS — {args.players} players, {args.minutes} min, "
          f"complexity <= {args.complexity_max}")
    print("=" * 62)
    for i, (score, g, why, tt) in enumerate(picks[: int(args.top)], 1):
        print(f"\n  {i}. {g['name']}  [{g['cat']}]  cx {g['cx']:g}/5")
        print(f"     why: {'; '.join(why)}")
        print(f"     teach time ~{tt} min; play {g['minutes']} min")
        print(f"     {g['pitch']}")
    print()
    print(f"  {len(picks)} candidates matched; showing top {min(args.top, len(picks))}")
    return 0


def cmd_teach(args):
    g = find_game(args.game)
    if not g:
        die(f"game {args.game!r} not in catalog")
    print("=" * 62)
    print(f"  TEACH KIT — {g['name']}")
    print("=" * 62)
    print("\n  ELEVATOR (30 seconds):")
    print(f"    \"{g['pitch']}\"")
    print("\n  FIRST TURN SCRIPT:")
    print(f"    {g.get('first_turn', g.get('first', '(see rulebook setup)'))}")
    print("\n  COMMON MISTAKES:")
    for i, gotcha in enumerate(g["gotchas"], 1):
        print(f"    {i}. {gotcha}")
    print(f"\n  Complexity {g['cx']:g}/5, {g['minutes']} min, "
          f"players {g['players'][0]}-{g['players'][1]}")
    return 0


def cmd_rotation(args):
    state = load_state()
    people = [p.strip() for p in args.people.split(",") if p.strip()]
    if not people:
        die("no people given")
    rot = state.setdefault("rotation", [])
    for p in people:
        if p not in rot:
            rot.append(p)
    # who's next: least recently picked among present people
    counts = {p: (rot.index(p) if p in rot else len(rot)) for p in people}
    nxt = min(people, key=lambda p: counts[p])
    print("=" * 62)
    print("  PICK ROTATION")
    print("=" * 62)
    print(f"  Rotation order : {' -> '.join(people)}")
    print(f"  Next picker    : {nxt}")
    print(f"  History (oldest->newest): {', '.join(rot) if rot else '(none)'}")
    if args.picked:
        g = find_game(args.picked)
        gname = g["name"] if g else args.picked
        state.setdefault("picks", []).append(gname)
        # move picker to the end
        if nxt in rot:
            rot.remove(nxt)
        rot.append(nxt)
        print(f"  Logged pick    : {nxt} picked {gname}")
    save_state(state)
    return 0


SURVEY = [
    ("Aggressive take-that fun?", ("yes", "no"), {"yes": 0.2, "no": 0}),
    ("Cooperative or competitive?", ("cooperative", "competitive"),
     {"cooperative": -0.3, "competitive": 0}),
    ("Brain-burn or light?", ("burn", "light"), {"burn": 0.5, "light": -0.5}),
    ("Group size right now?", ("2", "3-4", "5+"), None),
    ("Minutes available?", ("30", "60", "120"), None),
]


def cmd_survey(args):
    print("=" * 62)
    print("  GAME NIGHT SURVEY — answer 4 quick questions")
    print("=" * 62)
    answers = []
    for q, opts, _ in SURVEY:
        while True:
            a = input(f"  {q} [{'/'.join(opts)}]: ").strip().lower()
            if a in opts:
                answers.append(a)
                break
            print(f"    pick one of: {', '.join(opts)}")
    players = {"2": 2, "3-4": 4, "5+": 6}[answers[3]]
    minutes = {"30": 30, "60": 60, "120": 120}[answers[4]]
    cxmax = 2 if answers[2] == "light" else 4
    cooperative = answers[1] == "cooperative"
    aggressive = answers[0] == "yes"
    # reuse pick with computed constraints + preference nudges
    scored = []
    for g in GAMES:
        lo, hi = g["players"]
        if not (lo <= players <= hi):
            continue
        if g["cx"] > cxmax:
            continue
        if g["minutes"] > minutes:
            continue
        s = 1.0
        if cooperative and g["cat"] != "cooperative":
            s *= 0.7
        if not cooperative and g["cat"] == "cooperative":
            s *= 0.6
        if aggressive and g["cat"] in ("party", "family"):
            s *= 1.1
        scored.append((s, g))
    scored.sort(key=lambda t: (-t[0], t[1]["name"]))
    print()
    print(f"  Based on your answers ({players}p, {minutes} min, "
          f"{'cooperative' if cooperative else 'competitive'}, "
          f"{'brain-burn' if cxmax > 2 else 'light'}):")
    for s, g in scored[:5]:
        print(f"   - {g['name']} ({g['minutes']} min, cx {g['cx']:g}) — {g['pitch'][:70]}...")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="game_night.py",
        description="Board game night: pick, teach, rotation, survey")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("pick", help="ranked picks for the group")
    sp.add_argument("--players", type=int, required=True)
    sp.add_argument("--minutes", type=int, required=True)
    sp.add_argument("--complexity-max", type=float, default=3.0)
    sp.add_argument("--exclude", default="")
    sp.add_argument("--top", type=int, default=5)
    sp.set_defaults(fn=cmd_pick)

    sp = sub.add_parser("teach", help="teach kit for one game")
    sp.add_argument("game")
    sp.set_defaults(fn=cmd_teach)

    sp = sub.add_parser("rotation", help="fair pick rotation")
    sp.add_argument("--people", required=True, help="comma list")
    sp.add_argument("--picked", default="", help="log what was picked")
    sp.set_defaults(fn=cmd_rotation)

    sp = sub.add_parser("survey", help="interactive preferences survey")
    sp.set_defaults(fn=cmd_survey)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
