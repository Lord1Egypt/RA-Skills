# Event Seating Orchestra

**The seating chart is a constraint-satisfaction problem disguised as a family drama.**

Every wedding, rehearsal dinner, and big holiday table has the same constraints living in hosts' heads: divorced parents, the ex who's still invited, four couples who must stay together, three loud talkers who can't share a table, kids who need seating with patient adults. Planners charge hundreds for the chart; relatives burn the night before the wedding on a spreadsheet and still seat the feuding pair together.

## What this skill does

- **Guest graph model**: parties (must-together), keep-apart vetoes, prefer-near wishes, know-well edges for actual mixing, flags (talker / kid / needs-aisle).
- **Simulated annealing optimizer** (30k iterations, party-block moves, deterministic seed) with a scoring model tuned to real social physics: talker overload is quadratic, kids belong together with adults, already-close guests get gently split to make new connections.
- **Printable per-table rosters** with headcount, talker/kid counts, aisle flags.
- **Hard-constraint audit**: the run fails loudly if any keep-apart pair shares a table, a party is split, or a table is overfull.
- **Re-run discipline**: same seed + edited guest list → sane diffs for late RSVPs.

## Quick start

```bash
# 24-guest demo wedding: 3 tables of 8, exes apart, 3 talkers, 4 kids
python3 scripts/seating_optimizer.py --demo

# Your event
python3 scripts/seating_optimizer.py --guests guests.json          # see reference for schema
python3 scripts/seating_optimizer.py --guests guests.json --seed 42
```

## Why it matters

- A bad chart is remembered for years ("they seated me with HER"); a good one is invisible — and invisible is the goal.
- 100+ guests × relationship constraints exceeds what humans can hold; an optimizer holds them all, every time.
- Deterministic re-runs turn the late-RSVP panic from "redo everything" into a 30-second diff.

## What's inside

```
SKILL.md                       triggers, constraint encoding table, pitfalls
references/seating-model.md    scoring math, annealing params, schema, special cases
scripts/seating_optimizer.py   the optimizer (stdlib-only, offline, deterministic)
```

## Scope & honesty

The optimizer handles social constraints, not physical ones — venue map, sightlines, service lanes need a human pass after the run (see reference §7). Sweetheart-table pre-seating and language grouping are documented patterns, not built-in toggles.
