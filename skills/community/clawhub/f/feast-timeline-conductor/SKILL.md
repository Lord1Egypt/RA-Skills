---
name: feast-timeline-conductor
description: Use when cooking a multi-dish meal that must all land on the table at one time (holiday dinners, dinner parties, big Sunday roasts) — backward-schedules every dish from your serve time across limited oven shelves and burners, temp-tolerance co-baking (±25°F), rest/hold windows, make-ahead splits, and a minute-by-minute kitchen timeline with hands-busy conflict warnings.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [cooking, meal-planning, thanksgiving, scheduling, holiday-dinner, kitchen, timeline]
---

# Feast Timeline Conductor

## Overview

Every host knows the disaster: turkey still resting, potatoes boiling over,
the gratin went in late, and dinner "at 19:00" becomes 20:15 with cold sides.
The problem is not cooking skill — it is **scheduling**. A holiday meal is a
resource-constrained project (one oven, four burners, two hands) that people
run from memory.

This skill turns a dish list into a **backward-scheduled timeline** anchored
to your serve time:

1. Every dish gets stages `prep → cook → rest`, laid out *backwards* from
   the serve time, using each dish's hold window as slack.
2. **Oven as a shared resource** — dishes co-bake only if temperatures are
   within 25°F and shelf capacity allows; conflicting dishes are shifted
   earlier into their hold slack automatically.
3. **Burner capacity** — limited slots, same greedy resolution.
4. **Make-ahead detection** — dishes marked `make_ahead` move to a
   "day-before" list instead of competing on the day.
5. **Hands-busy audit** — if two prep tasks collide, you are told *before*
   you're standing there with two knives.
6. **Feasibility check** — if the serve time is impossible, the earliest
   feasible time is computed instead of a silently broken plan.

## When to Use

- "Dinner is at 19:00, I have 7 dishes, one oven — when does everything go in?"
- Planning a holiday meal (Thanksgiving, Christmas, Easter, Eid, Seder)
- Dinner parties where dishes have different oven temperatures
- "Can I still serve at 18:30 if I start now?" → feasibility check
- Deciding what to make ahead the day before

**Don't use for:** single-dish cooking, industrial kitchens, or dishes you
can't describe with prep/cook/rest minutes. It schedules; it does not cook.

## Quick Start

```bash
# 1. Generate a sample dishes.json to copy from
python3 scripts/feast.py example --out dishes.json

# 2. Get the full timeline for a 19:00 serve
python3 scripts/feast.py plan --serve 19:00 --dishes dishes.json

# 3. ...when you're starting later than planned
python3 scripts/feast.py plan --serve 19:00 --dishes dishes.json --now 15:40

# 4. Different kitchen: 3 shelves, 6 burners
python3 scripts/feast.py plan --serve 18:30 --dishes dishes.json --shelves 3 --burners 6
```

## The Dish File

```json
[
  {
    "name": "Roast turkey",
    "prep_min": 30,
    "cook_min": 180,
    "rest_min": 45,
    "equipment": "oven",
    "temp_f": 350,
    "hold_min": 20,
    "shelves": 2
  },
  {
    "name": "Green bean casserole",
    "prep_min": 15,
    "cook_min": 35,
    "rest_min": 10,
    "equipment": "oven",
    "temp_f": 375,
    "hold_min": 15,
    "shelves": 1
  },
  {
    "name": "Mashed potatoes",
    "prep_min": 25,
    "cook_min": 30,
    "equipment": "burner",
    "rest_min": 0,
    "hold_min": 30
  }
]
```

- `temp_f` optional; oven dishes without temps are treated as
  temperature-agnostic (co-bake with anything).
- `hold_min` = how long the finished dish stays good. This is your slack —
  the scheduler consumes it to resolve conflicts.
- `make_ahead: true` → dish is moved to the day-before list entirely.

## How Scheduling Works

1. Sort dishes by cook time descending (the big roast claims its slot first).
2. Latest cook end = `serve + hold − rest`. Work backwards from there.
3. An oven slot is valid during `[start, start+cook]` only if, at every
   minute, either the oven is free, or every co-baking dish's temperature is
   within 25°F **and** total shelves ≤ capacity.
4. If the latest slot conflicts, slide the start earlier minute-by-minute
   (into hold slack) until it fits.
5. Prep is laid immediately before the cook start, so knife-work naturally
   staggers across dishes.
6. After scheduling, prep windows are pairwise-checked for overlap —
   overlapping hands-on work is flagged as a **conflict warning**, not
   silently accepted.
7. If any prep would have to start before `--now`, the plan is infeasible;
   the tool searches forward (5-minute steps) for the earliest feasible
   serve time and reports it.

## Common Pitfalls

1. **Optimistic hold times.** A soufflé has ~0 min hold; a braised dish has
   60+. If you lie in `hold_min`, the scheduler happily builds a plan that
   ruins food. Be honest per dish.
2. **Forgetting rest matters.** Big roasts need 20–45 min rest, which is
   *free scheduling space* — another dish can finish the oven in that window.
3. **Two things at ±300°F cannot co-bake.** The 25°F tolerance is real
   physics of doneness, not bureaucracy. Dishes far apart in temperature
   must be sequenced, and the tool sequences them.
4. **Prep collisions.** If the plan says you're dicing onions while whipping
   cream at 18:05, the warning is the plan working — move one prep earlier
   by hand or simplify a dish.
5. **Not using make_ahead.** Cranberry sauce, stock, pies, and casseroles
   assembled ahead don't belong in day-of competition at all.

## Verification Checklist

- [ ] Every dish appears in the timeline exactly once (plus rest/serve lines)
- [ ] No oven interval over capacity or over temp tolerance
- [ ] Prep windows don't overlap (or warnings are acknowledged)
- [ ] Everything lands within `[serve, serve + hold]` of its own window
- [ ] If `--now` was given, the plan starts in the future

## One-Shot Recipes

**Classic Thanksgiving for 8, serve 18:00:**
```bash
python3 scripts/feast.py example --out dishes.json
python3 scripts/feast.py plan --serve 18:00 --dishes dishes.json --now 09:00
```

**Two-oven household:** run twice with different dish files, or set
`--shelves 4` and let co-baking rules approximate it.

**"When could I possibly serve?"** — drop `--serve`, add `--now`:
```bash
python3 scripts/feast.py plan --dishes dishes.json --now 16:00
```
The tool reports the earliest feasible serve time for that start.
