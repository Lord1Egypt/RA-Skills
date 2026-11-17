---
name: car-seat-stage-pilot
description: "Use when a parent asks which car seat their child needs, when to turn the seat forward, move to a booster, or ditch the booster — converts birthday + weight/height into rear-facing/forward-facing/harness/booster verdicts, limit warnings, next-transition dates, and a lifetime stage timeline."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [parenting, car-seat, child-safety, stages, milestones]
---

# Car Seat Stage Pilot

## Overview
Car-seat stages (rear-facing → forward-facing harness → booster → adult belt) are governed by
THREE clocks at once: the child's **age**, **weight**, and **height** — plus the specific seat's
limits. Parents get this wrong constantly: turning the seat at age 1 because "their legs look
cramped", boosting a 3-year-old because "she's tall for her age", or dropping the booster at 6
because "the belt looks fine". Mis-staging is one of the most common — and most dangerous —
usage errors found in car-seat check events.

This skill converts a birthday (or age in months) plus optional measurements into a definitive
stage verdict: what position, what seat type, what harness rule applies right now, which limits
are close, and when the next transition is projected.

## When to Use
- "My son just turned 2 — can I turn his seat around now?"
- "She's 4 and 42 lb — is it booster time?"
- "When can my kid stop using a booster?"
- "The seat manual says RF to 40 lb — my toddler is 38 lb, how long do we have?"
- "New baby arriving — what seat stage do we buy?"
- Any request involving child age + car seat position/type/transition.

**Don't use for:** installation help for a specific vehicle (angle, tightness, anchor locations) —
that's a certified Child Passenger Safety Technician job; direct the user to a local check station.

## How It Works — Numbered Steps
1. Collect inputs: birthday (best) or age in months; weight in lb; height in inches; current seat
   type if known (typical vs extended-rear-facing convertible).
2. Run the stage engine:
   `python3 scripts/car_seat_pilot.py --birthday 2024-03-15 --weight-lb 24 --height-in 31`
   Add `--json` for machine output, `--belt-fit` to force the 5-step belt-fit checklist.
3. Read the verdict block: POSITION NOW / SEAT NOW / HARNESS NOW.
4. Check `WARNING:` lines — they fire when a measurement is at/over a seat limit (transition now).
5. Use NEXT TRANSITION to answer "when": earliest of age-, weight-, and height-driven dates from
   a crude growth model (see references/growth-model.md).
6. For booster-age children, run through the 5-step belt-fit test verbatim — all five must pass.

## The Four Stages (quick reference)

| Stage | Position | Age guide | Size gate | Key rule |
|---|---|---|---|---|
| 1. Infant/convertible | Rear-facing | birth–2+ y | RF to seat max (often 40–50 lb) | Max out the seat, don't race the birthday |
| 2. Harness | Forward-facing | ~2–4+ y | ≥40 lb typical floor | Straps AT/ABOVE shoulders + top tether |
| 3. Booster | Forward-facing | ~4–10 y | until 4'9" + belt-fit pass | Lap+shoulder belt only, never lap-only |
| 4. Adult belt | Back seat | 8–12 y | 5-step test passes | Back seat until age 13 |

## Common Pitfalls
1. **Treating age 2 as the goal for turning.** Age 2 is the FLOOR, not the target — keep
   rear-facing until the seat's RF limits are exhausted (many seats go to 40–50 lb).
2. **Strap height direction.** Rear-facing: at or BELOW shoulders. Forward-facing: at or ABOVE.
   This is the #1 harness error and flips at the transition.
3. **Forgetting the top tether.** Forward-facing installs need the tether even with lower anchors.
4. **Boostering on height alone.** A tall 3-year-old stays in the harness; maturity (sitting the
   whole ride) gates the booster as much as size does.
5. **Mixing belt + lower anchors** unless the seat manual explicitly permits both.
6. **Expiring seats.** Seats expire 6–10 years from manufacture (plastic fatigue) — check the label.
7. **After any crash** most manufacturers (and NHTSA) say replace the seat, even if it looks fine.

## Example
```
Parent: "Daughter is 30 months, 24 lb, 31 in — grandma says she can face forward now."

$ python3 scripts/car_seat_pilot.py --birthday 2024-03-15 --weight-lb 24 --height-in 31
POSITION NOW: FORWARD-FACING  (age floor passed at 24 mo)
SEAT NOW:     convertible or combination seat installed FF
HARNESS NOW:  5-point harness + top tether
NEXT TRANSITION: Booster window opens (age ~4 + 40 lb) — 2028-03-15

Answer: yes, she may face forward (age floor passed), but she is ONLY 24 lb —
the harness stage continues for years; booster talk is ~2 years early.
```

## Safety Note
Guidance basis: AAP 2018 policy statement, NHTSA, Safe Kids Worldwide. The child's seat manual
and state law always supersede this tool. When in doubt, direct to a free certified car-seat
inspection station (NHTSA's "car seat inspection station" locator).

## References
- `references/stage-rules.md` — full rule set per stage, strap-position tables, tether rules,
  state-law variability, expiry and post-crash rules.
- `references/growth-model.md` — the crude lb/month and in/month growth curves used for
  transition-date projection, and their error bars.
