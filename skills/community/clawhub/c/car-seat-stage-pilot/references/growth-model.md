# Growth Model — Transition-Date Projection

The script projects transition dates from a crude piecewise growth model. It exists to answer
"how long do we have?" — a planning aid, not a pediatric growth chart.

## Rates Used

| Age band | Weight gain | Height gain |
|---|---|---|
| 0–12 mo | ~1.0 lb/month | ~0.5 in/month |
| 12–24 mo | ~0.5 lb/month | ~0.4 in/month |
| 24 mo+ | ~0.25 lb/month | ~0.2 in/month |

## Behavior

- If the child's current measurement already exceeds a limit → transition date = today.
- If a measurement isn't supplied, that driver contributes no candidate (age-only fallback).
- The NEXT TRANSITION shown is the EARLIEST of all candidate dates (age / weight / height).
- Dates are computed as `today + (limit − current) / rate × 30.4375 days`.

## Error Bars — Read the Output as a Window

CDC growth-chart variation at age 3 spans roughly the 3rd–97th percentile: 26–42 lb and
35–40 in. That means projected dates carry real uncertainty:

- Weight-driven projections: ±6 months is normal.
- Height-driven projections: ±9 months is normal.
- The verdict for TODAY is based on today's measurements and is unaffected.

Practical rule: when a projected transition is within 3 months, re-measure the child and check
the seat manual's exact limit — the projection is a calendar reminder, not a switch date.

## Why Not Percentile Curves

Full CDC/WHO LMS percentile tracking would make the skill heavy and would still not beat a tape
measure. The model deliberately trades precision for a single number parents will act on:
"re-check around <date>".
