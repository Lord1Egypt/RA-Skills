---
name: diet-plateau-decoder
description: "Use when the scale hasn't moved in 2+ weeks: separates TRUE plateaus (real energy-balance stalls) from water-retention masks (sodium, cortisol, menstrual phase, new training damage) and logging drift, using 7-day rolling averages, trend-vs-noise statistics, and expected-rate physics. Verdicts: NOT A PLATEAU / TRUE PLATEAU / LOG BROKEN with a per-verdict action plan."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [weight-loss, plateau, trend-analysis, health, fitness, statistics]
---

# Diet Plateau Decoder

## Overview

"Week 3 and the scale hasn't moved" kills more diets than craving ever did.
But most 2–3 week "plateaus" are not stalls — they are **masks**: the fat is
still going, and the water holding it on the scale came from sodium, stress
cortisol, a new training program (muscle repair holds water), menstrual
phase, or a carb refeed refilling glycogen (each gram binds ~3 g water).

The decoder runs the scale data through three tests:

1. **Trend test** — linear regression slope over the window vs the expected
   rate from your stated deficit. If fat should be leaving at 0.5 kg/wk and
   the 7-day-average slope says it is (−0.45 kg/wk) while raw weight is
   flat, the stall is cosmetic.
2. **Noise test** — daily scale noise is ±1–2 kg (water, gut content,
   clothing). A "flat" week inside noise with a negative slope underneath is
   a mask; the plateau only becomes real when the smoothed trend itself
   flattens for 3+ weeks.
3. **Context test** — flags from your log (high-sodium day, new workout
   program, period week, poor sleep, alcohol, constipation) that predict
   water retention of exactly the magnitude observed.

Verdicts:

| Verdict | Meaning | Action |
|---|---|---|
| **NOT A PLATEAU** | trend still negative; water is masking it | keep executing; trust the trend line |
| **TRUE PLATEAU** | smoothed trend flat ≥3 weeks | deficit audit (see below) |
| **LOG BROKEN** | data too noisy/missing to judge | fix logging first; weekend binges are the usual culprit |

## When to Use

- Scale flat 2+ weeks despite consistent eating
- Before cutting calories further (the reflex that creates metabolic and
  psychological damage — usually the wrong move on a mask)
- Deciding whether a diet break / refeed is warranted
- Reviewing a client's stall (coach mode)
- Post-holiday "I gained it all back?" — same water physics in reverse

**Don't use for:** eating-disorder context (obsessive trend-watching is
harmful there — this tool is deliberately coarse), or medical edema
(pitting, asymmetric swelling → doctor, not statistics).

## The Physics

```
expected_rate = deficit_kcal_per_day × 7 / 7700   kg/week
  (7700 kcal ≈ 1 kg fat; 3500 kcal ≈ 1 lb)

water masks (typical magnitudes):
  sodium spike (restaurant/processed day)   +0.3 – 1.2 kg for 1–3 days
  new training program (repair edema)       +0.5 – 2 kg for 1–2 weeks
  menstrual luteal phase                    +0.5 – 2 kg, resolves with menses
  carb refeed after low-carb                +0.5 – 1.5 kg (glycogen 3:1 water)
  alcohol                                   diuretic then rebound +0.3–1 kg
  cortisol (sleep<6h, life stress)          +0.3 – 1 kg, diffuse
  constipation                              +0.2 – 0.8 kg of the obvious
```

Adaptive thermogenesis is real but modest at first: NEAT drops and TDEE
eases down ~5–15% over months, not weeks. A week-3 stall is almost never
"starvation mode"; it is water or arithmetic (weekend surpluses erasing
weekday deficits — a 1400-kcal weekend overshoot halves a 500/day deficit).

## Using the Script

```bash
# weights in kg, one per day (also accepts JSON log, see --help)
python3 scripts/plateau_decoder.py --weights 82.1,81.8,82.4,81.6,81.9,81.4,81.7,81.5,81.6,81.3,81.4,81.2,81.3,81.1 \
    --expected-loss 0.5 --unit kg

# lb user, 3 weeks flat, logging weekend overeats
python3 scripts/plateau_decoder.py --weights "180,179.5,180.2,..." --expected-loss 1 --unit lb --flag weekend-overshoot

# with context flags
python3 scripts/plateau_decoder.py --weights ... --expected-loss 0.6 \
    --flag new-training --flag high-sodium --flag luteal
```

Output: regression slope vs expected, per-week trend table, noise band,
flag-weighted water budget, verdict, and the matched action plan.

## Per-Verdict Action Plans

### NOT A PLATEAU (mask)
1. Change nothing for 7 days. Weigh daily, same conditions (morning,
   post-bathroom, pre-food).
2. Judge only the 7-day rolling average, never a single day.
3. If flags were sodium/training: expect the whoosh when the water clears.

### TRUE PLATEAU
1. **Audit the log for 2 weeks** — weigh food again; portions creep 10–20%;
   weekends are the usual leak.
2. **Recompute TDEE** at current weight (a 90 kg person losing to 75 kg has
   a smaller engine: −10 to −15 kcal/day per kg lost).
3. Raise NEAT before cutting calories (steps 8k→10k) — cheaper than eating
   less.
4. Only then trim 100–200 kcal, or take a 1–2 week diet break at maintenance
   (evidence: MATADOR/intermittent-dieting studies show break periods
   preserve lean mass and adherence).
5. Measure beyond the scale: waist, photos, gym numbers — recomposition
   hides fat loss behind muscle gain, especially in returning lifters.

### LOG BROKEN
1. 14 days of honest logging, including weekends, before any decision.
2. Daily weighing is not obsessive — it's higher-quality data (research:
   daily weighers maintain loss better; the trend, not the day, is the unit).

## Common Pitfalls

1. **Judging a plateau on raw daily weights.** ±1–2 kg of water noise sits
   on top of a 0.5 kg/week signal — you need 2–3 weeks of smoothed trend to
   see anything.
2. **Cutting calories on week 2 of a new training program.** The repair
   edema mask is near-universal; the scale "whooshes" in week 3–4.
3. **Ignoring weekends.** Five good days at −500 and two at +900 average to
   −180/day: a third of the intended deficit, gone invisibly.
4. **Using the "whoosh" as a plan.** Water masks resolve on their own
   schedule; chasing them with sauna/diuretics just adds noise.
5. **Panicking at maintenance+500 refeed gains.** That's glycogen+water,
   mostly gone in 2–4 days; the fat fraction is 500/7700 of a kg.
6. **Forgetting menstrual phase.** Luteal water of 1–2 kg resolves with
   menses; comparing to the same phase last cycle, not yesterday.

## Verification Checklist

- [ ] ≥14 consecutive daily weights (same conditions) before running
- [ ] Expected-loss number comes from an honest deficit, not a wish
- [ ] Flags match the log (training started? sodium spike? cycle week?)
- [ ] Verdict read together with waist/photos, not the scale alone
- [ ] If TRUE PLATEAU: log audit happened before any calorie cut
