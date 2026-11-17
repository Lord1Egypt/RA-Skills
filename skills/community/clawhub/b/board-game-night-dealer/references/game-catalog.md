# Game Catalog & Selection Reference

How the dealer thinks: the catalog schema, the selection algorithm,
and the teaching doctrine.

## Catalog Schema

Every game entry carries:

- `players` (min, max) and `best` (the sweet-spot count)
- `minutes` — realistic playtime including setup, NOT box marketing
- `cx` — complexity 1-5: 1 party, 2 filler/family, 3 mid-weight
  strategy, 4 heavy euro, 5 marathon
- `cat` — party / card / family / strategy / heavy / cooperative /
  abstract / auction / war / roll-and-write
- teach kit: `pitch` (30-second elevator), `first_turn` script,
  `gotchas` (the 3 common mistakes)

The "best" count matters more than the range: 7 Wonders plays 2-7 but
is best at 4-5; Patchwork is exactly 2. Selection scores distance from
`best`, not just in-range.

## Selection Algorithm

1. Hard filters (any failure = eliminated):
   - player count within [min, max]
   - playtime <= budget
   - complexity <= ceiling
   - name not in exclusions
2. Fit score:
   - player fit = 1/(1 + |group - best|)
   - time fit = 1.0 if playtime <= budget, else decays by overage/60
   - teach-time check: short sessions (<60 min) penalize long teaches
   - repeat damping: last-3-session picks score ×0.5
3. Rank, and print WHY for each pick ("supports 5 (best 5); 30 min").

This is deliberately simple and explainable — a recommendation you
can't argue with is a recommendation you ignore.

## Teaching Doctrine

- **Elevator before rules.** People learn the shape first ("we're
  building an engine and racing to 15 points"), then the mechanics
  have somewhere to attach.
- **First-turn script.** "On your turn you'll do exactly this." The
  first turn teaches the turn; the second turn teaches the strategy.
- **Three gotchas max.** The mistakes every new player makes with this
  game — stated as prohibitions, because that's how they're remembered.
- **Teach time scales with complexity:** cx 1 ≈ 7 min, cx 2 ≈ 11,
  cx 3 ≈ 15, cx 4 ≈ 19, cx 5 ≈ 23. Budget it inside the session or
  pick something lighter.
- **Reference the rulebook for edge cases only.** If the table needs
  the rulebook mid-game, look up the ONE rule, read it aloud, move on.

## Session Planning Heuristics

- 60 minutes + mixed experience = two short games, not one medium.
- New player + cx 3 game = teach kit + open first hand face-up.
- 5+ players: favor simultaneous-play games (7 Wonders, Just One) —
  downtime kills large groups otherwise.
- 2 players: the duel shelf (Jaipur, Patchwork, 7 Wonders Duel,
  Lost Cities, Battle Line) is a different catalog from the party
  shelf; don't cross them.
- End the night on a 20-minute filler, not a 90-minute closer —
  people remember the last game when they decide to come back.

## Rotation Fairness

The rotation file (game_night.json) tracks the order of pickers.
Everyone picks before anyone picks twice. The dealer computes the
least-recent picker among present players and logs each night's pick
for the repeat-damping feature. Fair rotation is the cheapest
retention tool a game group has.
