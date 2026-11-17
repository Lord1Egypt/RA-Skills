# Board Game Night Dealer

Ranked game picks for your exact group, teach kits for the teacher,
and a fair pick rotation — the four ways game night fails, fixed.

## The Real Problem

Every regular game group hits the same failure modes:

- **The count problem.** Six people show up; the chosen game caps at
  4. Or three people and every shortlisted game needs 4+.
- **The time problem.** A "90-minute" euro plus a 25-minute rules
  explanation blows past the evening; someone leaves mid-game.
- **The teaching problem.** The rules-reader opens the rulebook at the
  table and improvises. The teach takes 40 minutes and three players
  zone out permanently.
- **The rotation problem.** The collection owner picks their favorite
  every session; quietly, everyone else stops showing up.

None of these are hard problems individually — but nobody solves them
in the moment, because the decision happens at 7:55 PM with snacks on
the table. This skill makes the decision in ten seconds with filters
and data instead of vibes.

## Who Needs This

- **Household game groups** (2-6 people) choosing tonight's game
- **Game-night hosts** with a shelf of options and rotating guest counts
- **Board game clubs / lunch groups** scheduling around fixed time slots
- **Couples** deciding between two-player duels vs joining a bigger table
- **New owners** of a big collection who bought faster than they learned

## What It Does

- `pick` — hard-filters the embedded 70-game catalog by player count,
  time budget, and complexity ceiling, then ranks by fit (best-player-
  count distance, time fit, repeat damping from recent sessions) and
  explains every pick
- `teach` — per-game teach kit: 30-second elevator pitch, first-turn
  script, the three common mistakes, teach-time estimate by complexity
- `rotation` — persistent fair rotation: who picks next, with history
- `survey` — 4-question interactive preference probe feeding weighted
  recommendations

Everything runs offline, stdlib Python, no dependencies. State lives
beside the script in `game_night.json`.

## Example

```console
$ python3 scripts/game_night.py pick --players 5 --minutes 90 --complexity-max 3
  1. Dixit  [party]  cx 1/5
     why: supports 5 (best 5); 30 min; party-light rules
     teach time ~7 min; play 30 min
  2. Just One  [party]  cx 1/5
  ...
$ python3 scripts/game_night.py teach "Wingspan"
  ELEVATOR: "Engine-build a bird preserve: birds chain powers off your
  three habitats..."
  FIRST TURN: Choose a habitat row and play a bird (pay food+eggs)...
  COMMON MISTAKES:
    1. Powers activate left-to-right only when the row's action is taken
```

The catalog spans party games (Codenames, Wavelength), fillers (Azul,
Love Letter), family euros (Ticket to Ride, Kingdomino), mid-weight
strategy (Wingspan, Terraforming Mars, Dune: Imperium), two-player
duels (Jaipur, Patchwork, 7 Wonders Duel), cooperatives (The Crew,
Hanabi, Spirit Island), roll-and-writes, and heavy euros — each with
players/best-count/playtime/complexity/category and a full teach kit.

MIT license. Data fits in your head never; in this file, always.
