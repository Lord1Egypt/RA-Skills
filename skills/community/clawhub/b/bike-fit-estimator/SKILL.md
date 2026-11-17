---
name: bike-fit-estimator
description: Use when buying a bike, setting one up, or diagnosing ride pain — computes frame size and stack/reach from your body (inseam×0.885 saddle height, Holmes 25–35° knee angle, crank length, standover clearance by discipline), dials position by flexibility and ride type, and routes pain symptoms (numb hands, front/back knee, hot foot, saddle numbness, neck) to ranked fit causes with the exact adjustment to try first.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [cycling, bike-fit, sizing, ergonomics, pain, road-bike, commuter]
---

# Bike Fit Estimator

A bad bike fit turns a healthy activity into a pain generator: knees, hands,
neck, perineum. Professional fits cost $150–400; a lot of what they do is
geometry you can compute from two measurements (inseam + height) and a
symptom table you can follow.

This skill sizes the frame, sets the contact points (saddle height, setback,
bar drop/reach, cleat fore-aft), and routes ride pain to its most likely fit
cause with the adjustment to try first.

## When to Use

- Buying a bike (online or used) and decoding size charts
- Setting saddle height/setback on a new or inherited bike
- Diagnosing pain that appears during or after rides
- Adjusting for flexibility changes, aging, or switching ride type
- Deciding crank length and checking standover clearance

**Don't use for:** post-crash pain, pain at rest/night, or any
neurological symptoms (numbness that persists off the bike) — medical.

## The Method

1. **Measure once, properly.** Barefoot, feet ~10 cm apart, hardback book
   pulled into the crotch, measure floor→book top. That's inseam. Height
   without shoes.
2. **`size`** — frame + contact points: saddle height (BB-to-top =
   inseam × 0.885, the LeMond method; cross-check Holmes 25–35° knee angle),
   setback (KOPS starting point), crank length, standover check, estimated
   stack/reach class.
3. **`position`** — bar drop and reach by flexibility × ride type:
   endurance/commute (comfort-first) → sportive → aggressive. Includes
   saddle tilt and transition protocol (change ONE thing, 2–3 rides).
4. **`pain`** — symptom → ranked causes → first fix. Change one variable at
   a time, 2–5 mm increments; log rides.

## Quick Start

```bash
# Frame size + contact points: 178 cm, 84 cm inseam, road bike
python3 scripts/bike_fit.py size --inseam 84 --height 178 --type road

# Position by flexibility
python3 scripts/bike_fit.py position --height 178 --flexibility medium --type road

# Diagnose: hands go numb after 45 minutes
python3 scripts/bike_fit.py pain --symptom numb-hands

# Check a listing: 56cm frame, your 84cm inseam
python3 scripts/bike_fit.py standover --inseam 84 --standover-height 80 --type road
```

Stdlib-only Python 3. Offline.

## Key Numbers (what the script computes)

- **Saddle height** (crank axle to saddle top along seat tube): inseam ×
  0.885. Verify: at bottom-dead-center, knee angle 25–35° (Holmes).
- **Setback**: knee-over-pedal-spindle as STARTING point, then adjust by
  hamstring flexibility; saddle nose behind BB axis 0–3 cm typical.
- **Crank length**: ~ inseam × 2.0 → mm (168 cm → 170 mm); shorter cranks
  (165) for tight hips/close fit or aero positions.
- **Drop** (saddle-to-bar): 0–2 cm low flexibility / endurance, 2–5 medium,
  5–8+ high flexibility / race. Reach: bars at natural elbow-to-hand span.
- **Standover clearance**: road ≥ 2 cm, gravel 3–5, MTB 5+.

## Pain Routing Table (summary)

| Symptom | Most likely (try first) | Then |
|---|---|---|
| Front of knee | saddle too LOW or too far forward | +2–3 mm height |
| Back of knee | saddle too HIGH or too far back | −2–3 mm height |
| Outside of knee | cleat rotation/angle | float check |
| Numb hands | weight too far forward: bars low/reach long, saddle nose down | raise bars, shorten reach, level saddle |
| Numb/lady-parts | saddle width/shape, too much drop | level saddle, wider/cutout saddle, less drop |
| Hot foot | cleat too far forward, shoes tight | move cleat back 2–4 mm |
| Neck/traps | drop too deep for flexibility | raise stem, shorter reach |
| Lower back | reach long, drop deep, saddle nose down | shorten reach, level saddle |
| Hip rocking | saddle too high | lower 2–3 mm until rock stops |

## Common Pitfalls

1. **Changing three things at once.** You fix the pain but learn nothing —
   and can't revert. One variable, 2–3 rides, log it.
2. **Saddle height from the floor or from old muscle memory.** Only
   BB-axis→saddle-top is a stable reference; it survives frame changes.
3. **Level the bike wrong.** Set heights with the bike on a trainer or
   measured against a wall on level ground, tires equal pressure.
4. **Fixing knee pain with a bigger gear / cadence change first.** Geometry
   first: 3 mm of saddle height fixes what a season of "spinning easier"
   won't.
5. **Buying by top-tube size alone.** Modern geometry varies: compare stack
   and reach, not "56 cm" — a 56 from two brands can differ 2 cm in both.
6. **Copying a pro's position.** Their flexibility and weekly hours aren't
   yours. Drop is earned, not chosen.
7. **Ignoring cleats.** Feet are the fixed point the whole chain rotates
   around; cleat rotation causes "mystery" lateral knee pain no saddle
   change touches.

## Verification Checklist

- [ ] Inseam measured with book method, barefoot (±5 mm matters)
- [ ] Saddle height set and marked (tape on seatpost)
- [ ] Knee-angle check at BDC: 25–35°
- [ ] One change at a time, ≥2 rides between changes
- [ ] Pain persisting after 3–4 fit iterations → professional fit / medical

## References

- `references/fit-science.md` — the geometry, angles, formulas, flexibility
  tests, cleat science, and the full pain table with reasoning
- `references/used-bike-buying.md` — decoding listings, stack/reach
  comparison, contact-point refresh budget (bars/saddle/tape are wear items)
