---
name: camping-loadout-planner
description: "Use when planning camping or backpacking trips — gear lists from conditions (temp/precip/bugs), sleeping-system temperature rating math, pack weight budgeting by trek style, camp kitchen sizing, and pre-departure loadout audits."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [camping, backpacking, gear, sleeping-bag, packing]
---

# Camping Loadout Planner — Gear From Conditions, Not From Habit

## Overview

Camping gear lists fail in two directions: the car-camper who brings everything twice, and
the backpacker whose "it fit last time" pack turns out to be 35 lb for a 15-mile day. The
correct method is to derive the loadout **upward from the environment** — the coldest
expected night defines the sleep system, the precipitation profile defines shelter, the
water availability defines carry capacity, the trek style defines the weight budget — and
then audit the result against that budget.

This skill generates condition-driven gear lists, computes honest sleeping comfort using
the bag + pad + liner stack (with the bag-rating reality check), enforces pack-weight
budgets by trek class with a ranked cut list when over, and sizes the camp kitchen and
water plan from headcount and water sources.

## When to Use

- Planning any car-camping, tent-camping, or backpacking trip (1–7 nights)
- "What temperature bag do I need?" — comfort rating math from forecast lows
- "My pack is too heavy, what do I cut?" — budget audit + ranked cuts
- Group trips: shared-gear shakedown (who carries the stove/tent/water filter)
- Packing for unpredictable shoulder-season conditions (30°F nights in June at altitude)
- Don't use for: RV/campervan outfitting, day hikes (no overnight system), alpine
  mountaineering technical gear (ropes/pro — different domain), or winter expedition style

## Core Knowledge

### 1. Sleep system math (the coldest night drives everything)

```
comfort ≈ min(limits of the stack): bag comfort + pad R-value contribution + liner boost
```

- Bag ratings: **EN/ISO comfort** (for cold-side sleepers) vs **limit** (warm-side). Women's
  bags quote comfort; unisex often quote limit — always compare comfort numbers.
- Pad R-value is not optional insulation: ground contact drains heat faster than air. R ≥ 2
  for 3-season, R ≥ 4 for freezing nights, R ≥ 5+ for snow. An R-1.5 pool-noodle under a
  20°F bag on frozen ground = cold night regardless of the bag.
- Linear stacking approximation (the script computes it): effective comfort ≈ bag comfort,
  but pad deficit subtracts roughly 10–15°F of protection; a liner adds ~8–10°F.
- Rule of thumb: **bag comfort rating ≈ forecast low − 5°F** (weather forecasts err low at
  night, especially in terrain; radiative cooling under clear skies is real).

### 2. Trek-style weight budgets (base weight = pack minus consumables)

| Class | Base weight | Philosophy |
|---|---|---|
| Traditional | 30–45 lb | comfort-camping; fine for short walks-in |
| Lightweight | 20–30 lb | the sane default for 3-season multi-day |
| Ultralight (UL) | 10–20 lb | bought-or-obsessed, big miles |
| Super-UL | <10 lb | specialist; usually warm/dry routes only |

Body-scaled check: total pack ≤ 20% body weight is the classic comfort ceiling; ≤ 15% for
hot weather or long days. Kids: ≤ 10–15% of body weight, or they hate hiking.

### 3. Condition-driven gear derivation

- **Forecast low** → sleep system (above) + insulated layers (puffy rating vs static hours
  in camp) + beanie/gloves below 40°F nights
- **Precip probability** → shelter + pack cover/liner + camp shoes that aren't cotton socks
- **Bug season** (freeze-out to first frost, roughly) → headnet, tent mesh integrity,
  permethrin-treated clothes; buggy + no-mesh shelter = misery
- **Water sources** (map recon: creeks/lakes every N miles?) → carry capacity: hot/dry
  terrain needs 3–4 L capacity + filter; cold/wet needs 1–2 L + filter
- **Fire rules** (check current restrictions!) → stove as primary; campfire plans are
  conditional, never loadout-critical
- **Bear country** (black/grizzly by region) → canister/bear-hang kit + food discipline;
  in grizzly country the canister isn't optional
- **Group size** → shared gear division: one stove per 3–4, one filter per 2–3, one FAK per
  group + one solo, tent pairing halves shelter weight

### 4. Camp kitchen sizing (per person per day, 3-season)

- Stove fuel: canister ~10–12 g per person-day (2 hot meals + coffee); cold-soak = 0
- Food: 1.5–2.5 lb/person-day (2,500–4,000 kcal depending on mileage)
- Water for cooking: 0.5–1 L/person/day beyond drinking

### 5. The audit that catches real failures

- Weight: measured or manufacturer-quoted per item; sum vs budget → cut list ranked by
  (comfort cost ÷ weight)
- Redundancy check: two of anything? (knives, lights, stoves — cut one)
- Cotton audit: cotton kills in cooling wet weather; synth/wool only above trivial walks
- Battery math: phone GPS + headlamp days vs power bank Wh
- "Just in case" bin: items whose use probability < 10% and weight > 100 g get flagged

## Workflow

1. **Gather conditions**: location + dates, forecast low (and how recent), precip %,
   bug season y/n, water sources map, fire status, bear country, group size, trek style
   (walk-in vs multi-day backpack), body weight for the scaled check.
2. **Generate the loadout:**
   ```bash
   python3 scripts/loadout_planner.py --demo
   python3 scripts/camping_loadout.py --trip trip.json   # see trip.example.json
   ```
3. **Check the sleep system** output: bag comfort vs derived requirement, pad R verdict.
4. **Audit weight**: budget by class, cut list if over, scaled-to-body check.
5. **Divide shared gear** (group mode) and print the carry manifest per person.
6. **Pre-departure run-through** the night before: tent+guylines pitched once at home,
   stove lit once, filter flushed, batteries charged, permit + fire status re-checked.

## Verdicts

| Output | Meaning |
|---|---|
| SLEEP OK / SLEEP RISK | stack comfort vs required rating with °F margin |
| WITHIN BUDGET / OVER by X lb | base weight vs class budget |
| CUT (ranked) | items ordered by comfort-per-ounce sacrifice |
| CAPACITY GAP | water carry vs source spacing |

## Common Pitfalls

1. **Trusting the bag's limit rating as the comfort number.** Limit is "survive the night
   curled up"; comfort is "sleep". Buy/plan on comfort, and compare like with like.
2. **Ignoring pad R-value.** A summer pad under a winter bag loses the night through the
   ground. The stack is bag AND pad AND liner, not bag alone.
3. **Planning to the average forecast.** Use the *nighttime low* with terrain adjustment;
   clear-sky radiative cooling drops tent interiors below the forecast valley number.
4. **Packing by memory instead of conditions.** Last trip's list was for different weather,
   different water, different bugs. Regenerate per trip — it's the point of the skill.
5. **Weight budgeting total pack, not base weight.** Consumables shrink daily; the
   constant misery is base weight. Budget that, then add food/water for day-1 worst case.
6. **"Just in case" stacking.** Every item below 10% use probability gets named and
   defended or cut — 15 of them = 4 lb of nothing.
7. **Fire-dependent cooking plans.** Restrictions, rain, and tiredness all kill campfires;
   the stove is the plan, the fire is the bonus.

## Verification Checklist

- [ ] Forecast low (with date fetched) drives the sleep-system requirement
- [ ] Bag comfort vs requirement margin stated (±5°F)
- [ ] Pad R-value checked against the night temperature
- [ ] Base weight vs class budget, cut list if over
- [ ] Total pack ≤ 20% body weight (≤ 15% hot/long)
- [ ] Water plan: capacity vs source spacing matches terrain
- [ ] Bear/food storage method matches the region's rules
- [ ] Shared gear divided and manifested per person (group mode)

## One-Shot Recipe: 2-night shoulder-season backpack, forecast low 34°F

Requirements: sleep stack for 29°F (low − 5). Your gear: 20°F-limit bag (≈29°F comfort),
R-2 pad, no liner → SLEEP OK, margin ≈ 0°F — tight; add the $30 liner for +8–10°F and
make it comfortable. Base weight 24 lb (lightweight class, within budget), total day-1
pack 31 lb vs 20%-of-body 34 lb — OK. Water: 2 L capacity, sources every 4 mi — OK.
Cut list flags the second knife (0.4 lb) and the steel mug doubling the titanium one
(0.3 lb). Loadout derived, not remembered.
