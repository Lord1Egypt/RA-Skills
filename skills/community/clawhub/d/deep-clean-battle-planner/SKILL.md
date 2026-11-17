---
name: deep-clean-battle-planner
description: "Use when planning a whole-house deep clean (spring cleaning, move-out, post-illness, before-guests) — turns rooms + available hours into ordered cleaning waves (dusty-first, top-down, machines working while you do), maps waves onto real weekend time blocks with a 15% buffer, matches surfaces x soils to the correct cleaner chemistry with never-mix warnings (bleach+acid, bleach+ammonia), and prints per-room zone playbooks with running time markers and upkeep recurrence cadences."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [cleaning, home, housekeeping, schedule, chemistry]
---

# Deep-Clean Battle Planner

## Overview
Deep cleaning fails the same way every time: people start in the wrong room
(mopping before dusting), underestimate by 2× (no dwell-time buffer), run
out of energy mid-house with the worst rooms untouched, and improvise
cleaner chemistry that damages surfaces (vinegar on stone) or actually
harms them (bleach + acid = chlorine gas; the US poison centers log tens of
thousands of cleaning-substance exposures a year).

This skill treats the deep clean as a schedulable project:

1. **plan** — rooms + hours → ordered waves. Dust-generating and high
   traffic zones first; top-down inside every room; machines (washer,
   oven cleaner) started at T-0 so they clean in parallel; 15% buffer.
2. **schedule** — waves mapped onto your real time blocks
   ("Sat 3h, Sun 2h") with leftovers explicitly deferred, plus the upkeep
   cadence table that keeps the deep clean from relapsing in 3 weeks.
3. **products** — surface × soil → the correct cleaner, dwell time, and
   warnings; always prints the never-mix danger table.
4. **zone** — one-room playbook: ordered tasks with running time marks.

Pure stdlib, offline.

## When to Use
- "This weekend I'm finally deep cleaning" — plan + schedule
- Spring cleaning / seasonal reset
- Move-out cleaning (deposit stakes)
- Post-illness household reset, before-guests blitz
- "What do I actually clean WITH?" — surface chemistry questions
- Building a recurring upkeep routine from the cadence table

**Don't use for:** hoarding-level remediation (professional help),
post-flood/post-fire restoration (insurance + remediation contractors),
or commercial/janitorial contracts (different standards and products).

## How It Works — Numbered Steps
1. Inventory the rooms and honest hours:
   ```
   python3 scripts/clean_planner.py plan --rooms kitchen,bathroom-main,livingroom --hours 4
   ```
   → waves with per-task minutes; what fits is planned, what doesn't is
   DEFERRED (a rushed room is worse than a planned one).
2. Map to actual calendar blocks:
   ```
   python3 scripts/clean_planner.py schedule --blocks "Sat 3h,Sun 2h,Mon 1h" \
       --rooms-list kitchen,bathroom-main,livingroom,bedroom,hallway,entry
   ```
   → each block loaded to 85% capacity, leftovers named, upkeep cadence
   per room (kitchen 7d, bathroom 5d, hallway 30d...).
3. Check every unfamiliar surface before spraying:
   ```
   python3 scripts/clean_planner.py products --surface hardwood --soil general
   python3 scripts/clean_planner.py products --surface tile-grout --soil mold
   ```
4. Execute a room with the zone playbook (running time marks keep pace
   honest):
   ```
   python3 scripts/clean_planner.py zone --room kitchen
   ```
5. After the deep clean, adopt the upkeep cadences — recurrence (5d
   bathroom, 7d kitchen) prevents the next 8-hour marathon.

## Ordering Rules (why the waves sort the way they do)
1. **Dusty work first** — dust falls; cleaning under falling dust is
   rework. Entry and kitchen (grease+traffic soil) lead.
2. **Top-down in-room** — fans → shelves → surfaces → floors, always.
3. **Machines at T-0** — washer, dishwasher, oven-cleaner dwell, hood
   filter soaking: they clean unattended while your hands do other work.
4. **Dwell chemistry** — spray the tub, let it work 10 min WHILE doing the
   toilet and sink; scrubbing un-dwelt cleaner is 3× the effort.
5. **15% buffer** — supplies hunt, labels, phone. A plan at 100% capacity
   is a plan to fail by 4 PM.

## Common Pitfalls
1. **Mixing cleaners.** Bleach + vinegar/acid → chlorine gas; bleach +
   ammonia → chloramine; peroxide + vinegar → peracetic acid. One cleaner
   at a time, rinsed between. The danger table prints on every `products`
   run for a reason.
2. **Vinegar on stone/marble/granite** etches permanently — pH-neutral
   only on natural stone (same for hardwood finishes long-term).
3. **Starting with floors.** Floors are LAST in every room, after all
   dust has settled and been removed above them.
4. **No dwell time.** Degreaser needs 5-10 min, oven cleaner needs
   overnight, mold gel 15 min. Spray-then-immediately-scrub wastes most
   of the chemical's work.
5. **Planning 100% of hours.** The 85% capacity rule: 4h block = 204
   planned minutes, not 240.
6. **The relapse cycle.** Deep clean once, no cadence → back to start in
   a month. The recurrence table (bathroom 5d, kitchen 7d, hallway 30d)
   is the actual product of the deep clean.
7. **Magic eraser on glossy paint/sheen** — it's micro-abrasive; test in a
   corner first (hallway task list warns).
8. **Boiling-water drains or caustic + plunger sequences** — drain
   cleaners are exothermic; follow label timing exactly, full flush
   between different products.

## Example
```
Saturday-Sunday plan, 6 rooms, blocks "Sat 3h, Sun 2h, Mon 1h":

$ plan --rooms kitchen,bathroom-main,livingroom --hours 4
→ WAVE1 kitchen 90m (8 tasks) → WAVE2 bathroom 60m (7 tasks);
  livingroom DEFERRED.

$ schedule --blocks "Sat 3h,Sun 2h,Mon 1h" \
    --rooms-list kitchen,bathroom-main,livingroom,bedroom,hallway,entry
→ Sat: entry+kitchen+hallway (135m of 153m usable)
  Sun: bathroom+bedroom (100m of 102m usable)
  Mon: catch-up block; livingroom left over → next weekend's wave 1.

$ products --surface tile-grout --soil mold
→ chlorine bleach gel, 15m dwell, ventilate, never-mix table.

Upkeep cadence printed at the bottom — bathroom every 5 days is what
keeps grout mold from ever coming back.
```

## References
- `references/wave-method.md` — the theory: soil types, ordering proofs,
  dwell chemistry, parallelizing machines, pace data behind task minutes.
- `references/cleaning-chemistry.md` — full surface × soil matrix, pH
  reasoning, the danger-mix table with symptoms and first response.
