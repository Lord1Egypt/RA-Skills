---
name: basement-dampness-doctor
description: "Use when a basement or crawl space smells musty, shows mold, efflorescence, or wet spots — or when sizing a dehumidifier. Separates condensation from liquid-water intrusion using dew-point physics (deep-soil wall temperature model), ranks the 10 classic moisture sources, sizes dehumidifier capacity in pints/day, and analyzes humidity logs."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [home, basement, moisture, mold, dehumidifier, dew-point, diagnostics]
---

# Basement Dampness Doctor

## Overview

Every damp basement gets one of two wrong treatments: a dehumidifier bought for a *water problem*, or foundation waterproofing sold for an *air problem*. The physics that separates them is simple and checkable: **moisture condenses on any surface colder than the air's dew point**. In summer, basement walls sitting against 13–17°C deep soil chill the air below its dew point — mold on organic surfaces with a dusty-white *absence* of stains on the concrete = condensation. Efflorescence (white salt crystals), staining in vertical streaks, or puddles = **liquid water moving through/along the foundation** — and a dehumidifier will not fix that.

This skill computes dew point (Magnus formula), estimates the wall-surface temperature from a deep-soil seasonal lag model, renders a CONDENSATION vs LIQUID verdict, ranks the classic sources (downspouts, grading, window wells, dryer venting...), and sizes dehumidifier capacity honestly (AHAM pints/day by area × dampness class), plus a humidity-log analyzer.

## When to Use

- Musty smell, mold spots, peeling paint, "sweating" walls or floor in a basement/crawl space
- Deciding between a dehumidifier, a fan, and calling a waterproofing contractor
- Sizing/buying a dehumidifier (how many pints? drain vs bucket? energy cost?)
- Reviewing a contractor's "you need $12k of interior French drains" quote — the source ranking usually finds the $200 fix first
- Don't use for: active flooding (water rising), burst pipes, sewer backup — those are emergency-shutoff problems.

## Quick Start

```bash
# 1. Why are my walls wet? (summer classic: humid air + cold walls)
python3 scripts/dampdoctor.py analyze --air-t 22 --rh 70 --soil-t 14 \
  --wall-t 16 --area 800 --ceiling 2.3 --season summer

# 2. What size dehumidifier do I need?
python3 scripts/dampdoctor.py dehumidifier --area 800 --class wet --energy-rate 0.34

# 3. Is my existing unit keeping up? (bucket math from measured fill rate)
python3 scripts/dampdoctor.py dehumidifier --area 800 --class damp \
  --measured-liters-day 6.5

# 4. Rank the moisture sources / crack the case
python3 scripts/dampdoctor.py sources --grading negative --downspouts 0.5 \
  --gutters clogged --dryer-vent inside --sump none --wall-signs efflorescence

# 5. Analyze a humidity log (CSV: date,RH,Temp)
python3 scripts/dampdoctor.py log --csv basement_log.csv --target 50
```

## The Two-Problem Decision Table

| Observation | Condensation (air problem) | Liquid water (ground problem) |
|---|---|---|
| Wall marks | uniform dust/damp film, mold on organic items, paint peeling in sheets | efflorescence salt lines, streaks from cracks, tide marks, puddles |
| Seasonality | worst in humid summer, gone in winter | worst during/after rain or snowmelt, any season |
| Floor | damp film, condensate on cold-water tank/pipes | standing water at low point, wet around wall-floor joint |
| Fix | dehumidifier + air sealing + stop interior moisture sources | downspouts/grading OUTSIDE, seal cracks, drain tile if hydrostatic |

## Dehumidifier Sizing (AHAM/Energy Star table, 27°C/60% RH test)

| Area (m²) | Moderately damp (60–70% RH) | Very damp (70–80%) | Wet (80–100% / seepage) |
|---|---|---|---|
| 50 | 10 L/day (21 pt) | 12 L (25 pt) | 14 L (30 pt) |
| 100 | 14 L (30 pt) | 17 L (35 pt) | 20 L (40 pt) |
| 150 | 18 L (37 pt) | 21 L (44 pt) | 25 L (50 pt) |
| 250 | 25 L (50 pt) | 30 L (60 pt) | 34 L (70 pt) |
| 350+ | 32 L (65 pt) | 38 L (80 pt) | 44 L (90 pt) |

Rules: buy the class ×1.2 if the space is open to a humid stairwell; a unit that runs constantly at max is undersized; drain-hose mode beats buckets for anything >12 L/day; Energy Star units ≈ 1.6 L/kWh.

## Common Pitfalls

1. **Dehumidifier for a liquid-water problem.** Pulling 20 L/day from a room fed by a downspout dumping at the foundation just runs the meter — fix the water path first.
2. **Closing the basement "to keep humid air out" in summer.** Summer air at 30°C/60% RH holds more moisture than the basement's 18°C air — ventilating with warm humid air *increases* condensation. Keep it closed + dehumidify.
3. **Efflorescence scrubbed with bleach and called mold.** White crystalline powder = salts left by water passing through concrete = liquid path = outside fix.
4. **Sizing by floor area only.** A wet 30 m² crawl space with an open stairwell needs more capacity than a sealed 100 m² basement — use the class column and the ×1.2 openness factor.
5. **Dryer venting or unsealed sump ignored.** One dryer load = 2–4 L of water into the air if vented inside; an unsealed sump lid is a moisture pump. The `sources` audit prices these.

## Verification Checklist

- [ ] Dew point vs wall temperature comparison shown with the verdict (not vibes)
- [ ] Wall-sign reading done (efflorescence/mold/tide marks) before any purchase
- [ ] Source ranking ordered cheap-first (downspout extensions before drain tile)
- [ ] Dehumidifier pints/day from the table × openness factor, with drain recommendation
- [ ] If verdict = LIQUID: no dehumidifier recommended as the primary fix

## Example Session

```
$ python3 scripts/dampdoctor.py analyze --air-t 22 --rh 70 --soil-t 14 \
    --wall-t 16 --area 800 --ceiling 2.3 --season summer

BASEMENT MOISTURE ANALYSIS
══════════════════════════════════════════════════════
Air: 22.0°C @ 70% RH → dew point 16.4°C
Deep-soil estimate: 14.0°C | measured wall: 16.0°C
→ Wall temp (16.0) vs dew point (16.4): wall is BELOW dew point by 0.4°C
VERDICT: CONDENSATION LIKELY — expect moisture film/mold on the coldest
  surfaces (corners, north wall, cold-water tank). Relative risk rises fast:
  every extra 1°C of cooling or +5% RH widens the gap.
Suggested dehumidifier target: 50% RH → extract to dew point ≤ ~11°C.
Dehumidifier class for 74 m² (799 ft²), 'damp': ~17 L/day (35 pt) ×1.2 open
  = 21 L/day class.
```
