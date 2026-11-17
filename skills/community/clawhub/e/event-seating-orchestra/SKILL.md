---
name: event-seating-orchestra
description: Use when planning seating for a wedding, dinner party, holiday table, or rehearsal dinner and you must respect keep-apart pairs, balance talkers across tables, seat couples near-but-not-alone, and keep exes/estranged family apart — and need an actual assignment chart, not vibes.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [seating-chart, weddings, dinner-parties, event-planning, optimization]
---

# Event Seating Orchestra

## Overview

The seating chart is the highest-stress artifact of wedding and event planning. The constraints live only in hosts' heads: divorced parents who can't share a table, the two friends who broke up, the uncle who talks over everyone, cousins who only know each other, grandma who needs an aisle-adjacent seat. Professional planners charge real money for this; spreadsheet-savvy relatives drown in it the night before.

This skill encodes the real constraints and runs an actual optimizer (simulated annealing over table assignments) to produce a printable chart, a per-table roster with reasons, and a complaint log for changes ("swap these two and the score improves by X").

## When to Use

- Weddings (the big one: 60–250 guests, family politics, plus-ones).
- Holiday dinners with known friction pairs.
- Rehearsal dinners, retirement parties, milestone birthdays.
- Dinner parties 8–16 where mixing matters ("don't let the two quiet ones end up together").
- Conference-style lunches where you want cross-team mixing.

Don't use for: standing receptions (no seating), classroom training (fixed rows), gala sponsor tables (priority ordering, not social optimization).

## How It Works

1. **Build the guest graph.** Each guest: name, party (couple/family unit that must sit together or near), flags (`talker`, `quiet`, `kid`, `needs-aisle`), and optional `language`. Edges: `must-together` (couples), `keep-apart` (exes, feuding), `prefer-near` (friends), `know-well` (already close — mixing prefers splitting them).
2. **Score function** (what "good" means):
   - +100 per must-together at same table (hard constraint otherwise)
   - −150 per keep-apart pair at the same table (hard veto)
   - talker balance: per-table talker penalty = (talkers − ideal)² × 15
   - party integrity: couples at same table strongly preferred; families with kids at kid-friendly tables
   - mixing bonus: tables whose members have few prior `know-well` edges score better
   - kid tables: kids seated together, not scattered among adults
3. **Optimize.** Simulated annealing: start random (respecting must-together blocks), propose single-guest or block swaps, accept improvements, occasionally accept worse to escape local optima, cool over ~20k iterations. Deterministic seed for reproducibility.
4. **Output.** Per-table rosters with headcount, talker load, kid count, constraint check, and per-table "why" notes. Swap suggestions for manual tweaks with score deltas.
5. **Iterate.** Late RSVP changes? Re-run with the same seed and the new guest list; diff the charts.

## Constraint Encoding Examples

| Real situation | Encoding |
|---|---|
| Divorced parents | `keep-apart` edge between them (and optionally their new spouses) |
| Maid of honor + her new boyfriend | same party (`must-together`) |
| Two work friends who should meet | `prefer-near` |
| The loud cousin | flag `talker` — optimizer spreads talkers one-per-table max |
| Grandma with a walker | flag `needs-aisle` → host marks which seats are aisle seats |
| Kids' table | flag `kid` → grouped at one table (with 1–2 patient adults) |
| "Don't split our family of 5" | party of 5, `must-together` |

## Worked Examples

`python3 scripts/seating_optimizer.py --demo` — 24-guest wedding sample (2 divorced-parent keeps-apart, 4 couples, 3 talkers, 4 kids) across 3 tables of 8 → rosters + balance report in under a second.

`python3 scripts/seating_optimizer.py --guests guests.json --tables "8,8,8"` — your guest file.

## Common Pitfalls

1. **Optimizing before the guest list is frozen.** Every late RSVP invalidates the chart; run final versions, not drafts (or accept re-runs).
2. **Forgetting plus-ones.** A party of 2 must be seated as a block; modeling guests as individuals breaks couples randomly.
3. **Treating all constraints as equal.** keep-apart is a veto; prefer-near is a wish. The tool uses hard/soft classes — respect them when entering data.
4. **One kids' table with zero adults.** Young kids need 1–2 assigned adults; the optimizer flags kid tables without adults.
5. **All the talkers at one table** (usually the "fun" table the host builds by hand). Every other table goes silent; spread the energy.
6. **Chart delivered as a screenshot.** Output rosters as text/table; venue coordinators and caterers need names per table, not graphics.
7. **Hiding the chart from the couple's parents** when they're hosts. A 10-minute review of table rosters surfaces forgotten frictions the graph never knew about.
8. **No aisle-seat map.** `needs-aisle` guests must map to real physical seats; get the venue's table map before finalizing.

## Verification Checklist

- [ ] Every `must-together` party seated at one table (script asserts)
- [ ] Zero `keep-apart` pairs sharing a table (script asserts)
- [ ] Talker load balanced (no table with 2+ talkers unless unavoidable)
- [ ] Kids grouped, each kid table has ≥1 adult
- [ ] Headcounts match venue table capacities exactly
- [ ] Aisle/mobility guests matched to the venue's actual aisle seats
- [ ] Chart printed as text rosters + one review pass with a second host
