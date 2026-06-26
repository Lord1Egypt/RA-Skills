# Sensitivity Analysis Template

Use this framework to model how changes in key variables affect break-even.

---

## Single-Variable Sensitivity

Test one variable at a time while holding others constant:

### Price sensitivity
| Price point | CM/unit | CM% | BE Units | BE CPA | Verdict |
|---|---|---|---|---|---|
| $XX (base) | $XX.XX | XX% | XXX | $XX.XX | Base case |
| $XX (-10%) | $XX.XX | XX% | XXX | $XX.XX | [Impact] |
| $XX (-20%) | $XX.XX | XX% | XXX | $XX.XX | [Impact] |
| $XX (+10%) | $XX.XX | XX% | XXX | $XX.XX | [Impact] |
| $XX (+20%) | $XX.XX | XX% | XXX | $XX.XX | [Impact] |

### CPA sensitivity
| CPA | Net margin/order | Monthly profit at X units | Scale verdict |
|---|---|---|---|
| $XX (base) | $XX.XX | $X,XXX | [Verdict] |
| $XX (+25%) | $XX.XX | $X,XXX | [Verdict] |
| $XX (+50%) | $XX.XX | $X,XXX | [Verdict] |
| $XX (+100%) | $XX.XX | $X,XXX | [Verdict] |

### Discount impact
| Discount | Effective price | New CM | CM change | BE shift |
|---|---|---|---|---|
| 0% (base) | $XX.XX | $XX.XX | — | — |
| 10% off | $XX.XX | $XX.XX | -XX% | +XX% more units needed |
| 15% off | $XX.XX | $XX.XX | -XX% | +XX% more units needed |
| 20% off | $XX.XX | $XX.XX | -XX% | +XX% more units needed |
| 25% off | $XX.XX | $XX.XX | -XX% | +XX% more units needed |

---

## Scenario Analysis

Model realistic combined scenarios:

### Optimistic scenario
- Lower COGS (supplier negotiation)
- Higher conversion rate (lower effective CPA)
- Lower return rate (better product/listing)
- Result: [CM, BE, profit projection]

### Base scenario
- Current inputs as-is
- Result: [CM, BE, profit projection]

### Pessimistic scenario
- COGS increase (tariffs, supply chain)
- CPA increase (competition, seasonality)
- Higher return rate
- Result: [CM, BE, profit projection]

---

## Tornado Chart Priority

Rank variables by break-even impact (highest first):

1. **[Variable]** — X% BE change per Y% input change
2. **[Variable]** — X% BE change per Y% input change
3. **[Variable]** — X% BE change per Y% input change

This tells the operator which lever to focus on first.
