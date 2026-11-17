---
name: board-game-night-dealer
description: Use when planning a board game night — ranked game picks for the group's exact player count, time budget, and complexity ceiling with WHY-explanations, a 70-game catalog with teach kits (30-second elevator pitch, first-turn script, common rules mistakes), fair pick rotation tracking, and an interactive preference survey.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [board-games, game-night, selection, teaching, party, catalog]
---

# Board Game Night Dealer

Game night fails in predictable ways: the game needs 3 players and 6
showed up; it's a 120-minute euro and everyone has 45 minutes; the
person who owns the games always picks their favorite; and the teach
takes 40 minutes because nobody read the rules first. This skill is
the dealer that fixes all four: hard filters (players, time,
complexity) then fit scoring, a teach kit per game so the rules
explanation is 5 minutes instead of 40, and a rotation so picking
is fair instead of habitual.

## When to Use

- Planning a game night: "what should we play with 5 people, 90
  minutes, nothing heavier than a 3?"
- Teaching a game tonight you haven't taught before — elevator pitch,
  first-turn script, the three mistakes new players always make
- Rotating who picks the game fairly across a regular group
- Deciding what to buy next from a wishlist against your group's
  real player count and session length

## The Method

```bash
# Ranked picks: players, minutes, complexity ceiling, exclusions
python3 scripts/game_night.py pick --players 5 --minutes 90 \
    --complexity-max 3 --exclude 'Codenames,Catan'

# Teach kit: pitch + first-turn script + common mistakes
python3 scripts/game_night.py teach "Wingspan"
python3 scripts/game_night.py teach "7 Wonders"

# Fair rotation: who picks next (state persists in game_night.json)
python3 scripts/game_night.py rotation --people "Anna,Ben,Caro,Dave"
python3 scripts/game_night.py rotation --people "Anna,Ben,Caro,Dave" \
    --picked "Cascadia"

# Interactive survey: 4 questions -> weighted recommendations
python3 scripts/game_night.py survey
```

## Selection Algorithm

1. **Hard filters first.** Player count must fit (min-max), playtime
   must fit the budget, complexity must be under the ceiling, excluded
   titles drop out. No amount of scoring rescues a game you can't play.
2. **Fit scoring.** Player-count fit (distance from the game's best
   count), time fit (underage bonus, overage penalty), teach-time
   check for short sessions.
3. **Repeat damping.** Games picked in the last 3 sessions score at
   half weight — variety without banning.
4. **Explain every pick.** Output says WHY: "supports 5 (best 5);
   30 min; party-light rules".

## Teach Kit Doctrine

- **The 30-second elevator** comes BEFORE rules details — people
  need the shape of the game before the pieces.
- **First-turn script**: what the first player physically does on
  turn one. Concrete beats abstract; the second turn teaches itself.
- **Common mistakes**: the 3 rules new players always get wrong,
  stated as don't-do-this.
- Teaching time scales with complexity: ~7 min for a party game,
   ~15+ for a heavy euro — budget it inside the session length.

## Common Pitfalls

1. **Picking by BGG rank.** A #5-ranked heavy euro is a terrible
   pick for 6 casual players with an hour. Filter by group, not by
   fame.
2. **Forgetting teach time.** A 60-min game with a 20-min teach is
   an 80-min game. The pick command shows both numbers.
3. **Same picker every week.** Rotation rots silently; the rotation
   command tracks it so it can't.
4. **Teaching from the rulebook.** Read it before, teach from the
   kit: elevator, first turn, mistakes. Questions answer themselves
   by round two.
5. **One long game vs two short ones.** For mixed groups, two
   40-minute games beat one 90-minute game — everyone resets,
   late arrivals slot in.

## Verification Checklist

- [ ] Player count hard-filtered before scoring
- [ ] Time budget includes teach time, not just play time
- [ ] Recent picks damped (variety check)
- [ ] Teach kit read by the teacher BEFORE the night
- [ ] Rotation logged after the pick, not from memory
