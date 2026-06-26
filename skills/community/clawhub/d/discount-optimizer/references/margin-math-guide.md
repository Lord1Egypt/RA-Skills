# Margin Math Guide

The numbers behind every discount decision. Get these right and the rest of the skill follows.

## 1. The three margins (don't mix them up)

- **Gross margin** = (price − COGS) ÷ price. COGS only — the cost of the goods. Ignores platform fees, shipping, processing, returns.
- **Contribution margin (CM)** = (price − *all variable costs*) ÷ price. Subtracts COGS **and** every per-order variable cost: commission, payment processing, fulfillment, shipping subsidy, affiliate commission, returns reserve. **This is the number that matters for discounting**, because a discount eats into contribution, not gross.
- **Net margin** = profit after *also* allocating fixed costs (overhead, salaries, ad spend, software) ÷ price. Useful for whole-business health, too lagging and too allocated for sizing a single promo.

**Rule:** size discounts off **contribution margin**. Gross margin overstates your headroom (it forgets fees); net margin understates it (it loads fixed costs that don't change with one promo).

**Worked example.** Price $39.90, COGS $11.00, variable costs (commission $2.00 + payment $0.80 + shipping $4.50 + returns $1.20) = $8.50.
- Gross margin = (39.90 − 11.00) ÷ 39.90 = **72.4%**
- Contribution margin = (39.90 − 19.50) ÷ 39.90 = **51.1%**

The 21-point gap is exactly the fee/shipping/returns load. Sizing a discount off the 72% gross figure would let you cut far deeper than you can actually afford.

## 2. The break-even volume-lift formula

For a discount of depth `d` (as a fraction of price) on a product with contribution margin `m` (as a fraction of price), the additional unit volume needed to **hold total contribution flat** is:

> **required-lift = d / (m − d)**

**Why it works.** Per-unit contribution before = `m × price`. After the discount, per-unit contribution = `(m − d) × price` (the price drops by `d×price`, and that whole amount comes out of contribution). To keep total contribution equal: `units_old × m = units_new × (m − d)`, so `units_new / units_old = m / (m − d)`, and the *extra* fraction is `units_new/units_old − 1 = d / (m − d)`.

**Caveat:** the clean formula assumes per-unit variable cost is fixed. In reality, percentage-based fees (commission, payment, affiliate) fall slightly when the price drops, so the *true* break-even lift is a little lower than the formula. The formula is the conservative (safe) estimate; recompute exactly when fees are a large % of price.

### Lookup table: required volume lift to break even

Rows = discount depth `d`. Columns = starting contribution margin `m`. Values = required-lift % from `d/(m−d)`. "—" means impossible (discount ≥ margin → you lose money on every unit no matter the volume).

| d \ m | 30% | 40% | 50% | 60% | 70% |
|---|---|---|---|---|---|
| 5% | 20.0% | 14.3% | 11.1% | 9.1% | 7.7% |
| 10% | 50.0% | 33.3% | 25.0% | 20.0% | 16.7% |
| 15% | 100.0% | 60.0% | 42.9% | 33.3% | 27.3% |
| 20% | 200.0% | 100.0% | 66.7% | 50.0% | 40.0% |
| 25% | 500.0% | 150.0% | 100.0% | 71.4% | 55.6% |
| 30% | — | 300.0% | 150.0% | 100.0% | 75.0% |
| 40% | — | — | 400.0% | 200.0% | 133.3% |
| 50% | — | — | — | 500.0% | 250.0% |

Spot-checks: `d=20%, m=50%` → 0.20/(0.50−0.20)=0.667 → **66.7%** ✓. `d=30%, m=60%` → 0.30/0.30=1.0 → **100%** ✓. `d=15%, m=30%` → 0.15/0.15=1.0 → **100%** ✓. `d=40%, m=70%` → 0.40/0.30=1.333 → **133.3%** ✓.

**Read it like this:** a 20%-off promo on a 50%-margin item needs **two-thirds more units** just to break even. A 40% cut on a 50% item needs **5x the units** — almost never achievable. The diagonal where `d` approaches `m` explodes toward infinity; never discount close to your contribution margin.

## 3. Markdown % vs margin % (the classic trap)

A **markdown** is the discount off the selling price. **Margin** is what's left after cost. They are not complements.

- A 40% markdown does **not** leave 60% margin.
- Remaining margin after a markdown depends on starting margin: `new margin = (m − d) / (1 − d)` as a % of the *new* price.

**Example:** item with 50% margin, take 30% off. New CM as % of new price = (0.50 − 0.30) ÷ (1 − 0.30) = 0.20 ÷ 0.70 = **28.6%** — not 20%. The denominator shrank too. Always state whether a percentage is a markdown (off price) or a margin (off cost), and convert with this formula.

## 4. Platform-fee / commission accounting

Net **every** variable cost before computing `m`:

```
contribution$ = price
              − COGS (landed)
              − platform commission (% of price)
              − payment processing (% of price)
              − fulfillment / pick-pack (per unit)
              − outbound shipping subsidy (per unit)
              − affiliate / creator commission (% of price)
              − returns reserve (% of price)
```

Key points: (1) Commission is charged on the **discounted** price, so it falls when you discount — but so does your contribution. (2) Affiliate/creator commission is *additional* to platform commission; on TikTok Shop a creator promo can add 10–20% on top of the base commission. (3) Coupons/vouchers may be funded by you, the platform, or split — only the portion **you** fund hits your margin; confirm who pays.

## 5. Blended margin across a bundle

For a bundle, compute contribution on the **whole bundle**, not per item — a low-margin filler can drag the basket below the floor.

**Example:** bundle = Item A (price $20, var cost $9 → CM $11) + Item B (price $15, var cost $10 → CM $5), sold together for $30 (a $5 bundle discount off the $35 combined).
- Combined variable cost = $9 + $10 = $19
- Bundle CM$ = 30 − 19 = **$11**
- Blended CM% = 11 ÷ 30 = **36.7%**

Compare to the un-bundled blended margin: (11+5)/(20+15) = 16/35 = 45.7%. The $5 bundle discount cost ~9 margin points. Check the bundle CM clears your floor *after* the bundle discount.

## 6. Inventory holding-cost reasoning

For aging stock the comparison is **discounted contribution now vs salvage value later**, not discounted vs full-price contribution. Carrying cost per unit over a holding window ≈ annual carrying rate × unit cost × (weeks held ÷ 52), where the annual rate bundles capital (~3–5%), storage/handling (~5–10%), and — usually the dominant term — obsolescence/markdown risk (10–25%+ for seasonal goods).

**Decision rule:** discount deeper than your normal floor when
`(extra units sold × their thin CM) > (carrying cost saved + salvage loss avoided on units that would otherwise go unsold)`.
A clearance discount that the `d/(m−d)` test rejects in steady state can still be the profit-maximizing move once obsolescence is racing you to a write-off. See SKILL.md Example 2 for the full worked trade-off.
