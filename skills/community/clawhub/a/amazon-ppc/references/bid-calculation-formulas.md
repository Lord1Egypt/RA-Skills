# Amazon PPC Bid Calculation Formulas

A reference sheet for deriving bids from unit economics rather than guessing.

---

## Core Formulas

### Maximum CPC (the ceiling)
```
Max CPC = Average Selling Price × Target ACoS × Estimated Conversion Rate
```

This is the highest you can bid before your advertising cost exceeds your target. Never consistently bid above this number.

### Break-even CPC
```
Break-even CPC = Average Selling Price × Gross Margin % × Estimated CVR
```

At this bid level, advertising cost equals gross profit. Every click costs you your entire margin. Use as an absolute hard ceiling — any campaign consistently spending at or above this number is destroying contribution margin.

### Target CPC (starting point for bids)
```
Target CPC = Max CPC × 0.8
```

Start bids at 80% of maximum to leave room for error in CVR estimates. Increase toward Max CPC as actual CVR data confirms your assumptions.

---

## Quick Reference Table

| ASP | Gross Margin | CVR | Max CPC (30% ACoS) | Break-even CPC |
|---|---|---|---|---|
| $15 | 35% | 8% | $0.36 | $0.42 |
| $25 | 40% | 10% | $0.75 | $1.00 |
| $35 | 45% | 10% | $1.05 | $1.58 |
| $50 | 40% | 12% | $1.80 | $2.40 |
| $75 | 35% | 8% | $1.80 | $2.10 |
| $100 | 30% | 6% | $1.80 | $1.80 |

---

## Bid Adjustment Formulas

### When ACoS is above target (bids too high)
```
New Bid = Current Bid × (Target ACoS / Actual ACoS)

Example: Target 30%, Actual 45%, Current Bid $1.00
New Bid = $1.00 × (30/45) = $0.67
```

### When ACoS is below target (room to increase)
```
New Bid = Current Bid × (Target ACoS / Actual ACoS) × Scaling Factor

Where Scaling Factor = 1.1 to 1.2 (be conservative — never increase by more than 20% at a time)

Example: Target 30%, Actual 18%, Current Bid $0.60
New Bid = $0.60 × (30/18) × 1.1 = $1.10 (cap at Max CPC)
```

### Match type bid ratios
Starting bids relative to exact match:
```
Exact Match: 100% (baseline)
Phrase Match: 75-85%
Broad Match: 55-70%
Auto (manual bid): 40-60%
```

---

## Placement Multiplier Math

Amazon allows you to increase bids for specific placements. The platform bid × (1 + multiplier%) = effective bid at that placement.

```
Effective Bid at Top of Search = Base Bid × (1 + Top of Search Multiplier)

Example: $0.80 base bid, +30% top-of-search multiplier
Effective Bid = $0.80 × 1.30 = $1.04
```

Ensure the effective bid at premium placements still stays below your Max CPC.

```
Required Base Bid for Top of Search Max CPC = Max CPC / (1 + Multiplier)

Example: Max CPC = $1.00, Multiplier = 30%
Required Base Bid = $1.00 / 1.30 = $0.77
```

---

## Budget Formulas

### Minimum daily budget per campaign
```
Minimum Daily Budget = Max CPC × 10

At a minimum of 10 clicks per day, you get actionable data within 7-14 days.
Running a campaign at 2-3 clicks per day means weeks before you have enough data to optimize.
```

### Monthly budget projection
```
Monthly Spend = Daily Budget × 30 × Budget Utilization Rate

Budget Utilization Rate: 70-95% depending on keyword volume and bid competitiveness
```

### Break-even sales volume for ad spend
```
Orders Needed to Break Even on Ad Spend = Daily Ad Budget / (ASP × Gross Margin %)

Example: $20/day budget, $25 ASP, 40% margin → need 2 orders/day to cover ad cost
```

---

## CVR Estimation Guidelines

Conversion rate varies significantly by category, review count, and price point. Use these ranges as starting assumptions until real data is available:

| Category / Situation | Estimated CVR Range |
|---|---|
| New product, 0 reviews | 3-6% |
| Established product, 50+ reviews, 4.0+ stars | 8-15% |
| Consumables / repeat-purchase | 10-18% |
| High-ticket items ($100+) | 3-8% |
| Highly competitive category | 5-10% |
| Branded search terms | 15-30% |

**Important:** Recalculate Max CPC every 30 days using actual CVR from campaign data. Estimated CVR errors compound into significant bid mistakes over time.
