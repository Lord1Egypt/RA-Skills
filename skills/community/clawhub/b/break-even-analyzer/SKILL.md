---
name: Break-Even Analyzer
description: Calculate break-even points for e-commerce products and campaigns including fixed/variable cost analysis, contribution margin optimization, scenario modeling, and profitability timelines for informed pricing and launch decisions.
---

# Break-Even Analyzer

Determine exactly when a product, campaign, or business initiative becomes profitable. This skill walks you through cost classification, contribution margin calculation, scenario modeling, and sensitivity analysis so you can make data-driven launch and pricing decisions.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| **Cost classification** | Every cost mapped to fixed or variable with source documentation | Major costs classified, minor estimated | Lump-sum "total cost" with no breakdown |
| **Contribution margin** | Calculated per SKU with all variable costs included | Calculated at product-line level | Guessed or based on gross margin alone |
| **Break-even units** | Precise calculation with sensitivity ranges | Single-point calculation | "We need to sell a lot" |
| **Scenario modeling** | 3+ scenarios (pessimistic, base, optimistic) with probability weights | Base case only | No scenario analysis |
| **Time horizon** | Monthly cash flow projection to break-even date | Quarterly estimate | No timeline |
| **Sensitivity analysis** | Key variables tested (price ±10-20%, volume ±25%, COGS ±15%) | One variable tested | No sensitivity testing |

## Solves

1. **Blind launches** — Launching products without knowing the minimum sales needed to cover costs
2. **Mispriced products** — Setting prices based on gut feel rather than cost structure analysis
3. **Hidden cost traps** — Overlooking variable costs that erode margins (returns, payment fees, shipping)
4. **Campaign overspend** — Running marketing campaigns without knowing the sales needed to justify the spend
5. **Inventory risk** — Ordering too much inventory before validating demand at the break-even threshold
6. **Scaling miscalculations** — Assuming linear cost scaling when step-fixed costs create new break-even points
7. **Investor misalignment** — Presenting financial projections without rigorous break-even analysis

## Workflow

### Step 1: Classify All Costs

Separate every cost into fixed or variable categories.

**Fixed costs** (don't change with volume):
- Rent/warehouse lease
- Salaries (non-commission)
- Software subscriptions
- Insurance
- Equipment depreciation
- Loan payments

**Variable costs** (change per unit sold):
- Product COGS (materials, manufacturing)
- Shipping & fulfillment per order
- Payment processing fees (typically 2.9% + $0.30)
- Marketplace commissions (e.g., Amazon 15%)
- Returns & refund costs (typically 5-15% of sales)
- Packaging materials per unit
- Customer acquisition cost (if attributable per unit)

**Step-fixed costs** (fixed within ranges, then jump):
- Warehouse staff (1 picker per 200 orders/day)
- Software tiers (e.g., Shopify Basic → Shopify → Advanced)
- Storage fees (per pallet or bin threshold)

### Step 2: Calculate Contribution Margin

```
Contribution Margin per Unit = Selling Price - Total Variable Costs per Unit
Contribution Margin Ratio = Contribution Margin / Selling Price
```

Include ALL variable costs, not just COGS:

| Component | Amount | Notes |
|---|---|---|
| Selling price | $49.99 | After any standard discounts |
| Product COGS | -$12.00 | Manufacturing + materials |
| Shipping cost | -$5.50 | Average across zones |
| Payment processing | -$1.75 | 2.9% + $0.30 |
| Packaging | -$2.00 | Box, insert, tape, label |
| Marketplace fee | -$7.50 | 15% if on Amazon |
| Returns allowance | -$2.50 | 5% return rate × full cost |
| **Contribution margin** | **$18.74** | **37.5% ratio** |

### Step 3: Calculate Break-Even Point

**Basic break-even (units)**:
```
Break-Even Units = Fixed Costs / Contribution Margin per Unit
```

**Break-even (revenue)**:
```
Break-Even Revenue = Fixed Costs / Contribution Margin Ratio
```

**Break-even with target profit**:
```
Units for Target Profit = (Fixed Costs + Target Profit) / Contribution Margin per Unit
```

### Step 4: Build Scenario Models

Create three scenarios minimum:

| Scenario | Price | Volume/mo | Variable Cost | Fixed Cost | Break-Even |
|---|---|---|---|---|---|
| Pessimistic | $44.99 | 150 | $33.25 | $8,000 | 681 units |
| Base | $49.99 | 250 | $31.25 | $8,000 | 427 units |
| Optimistic | $49.99 | 400 | $28.75 | $8,000 | 377 units |

Weight scenarios by probability: Pessimistic 25%, Base 50%, Optimistic 25%.

**Expected break-even** = (681 × 0.25) + (427 × 0.50) + (377 × 0.25) = **478 units**

### Step 5: Run Sensitivity Analysis

Test how break-even changes when key variables shift:

**Price sensitivity** (±10%):
- Price $44.99: Break-even = 582 units (+36%)
- Price $49.99: Break-even = 427 units (base)
- Price $54.99: Break-even = 338 units (-21%)

**Volume sensitivity**: Project months to break-even at different monthly sales rates.

**COGS sensitivity** (±15%):
- COGS +15%: Break-even = 498 units (+17%)
- COGS base: Break-even = 427 units
- COGS -15%: Break-even = 372 units (-13%)

### Step 6: Project Timeline to Break-Even

Map the break-even point to a calendar timeline:

| Month | Units Sold | Cumulative | Revenue | Cumulative Profit |
|---|---|---|---|---|
| Month 1 | 80 | 80 | $3,999 | -$6,501 |
| Month 2 | 150 | 230 | $7,499 | -$4,191 |
| Month 3 | 220 | 450 | $10,998 | -$871 |
| Month 4 | 250 | 700 | $12,498 | $3,814 |

**Break-even month**: Month 3-4 (at ~427 cumulative units)

### Step 7: Document and Present

Compile findings into a one-page executive summary with:
- Break-even units and revenue
- Expected timeline
- Top 3 risks (from sensitivity analysis)
- Recommended pricing strategy
- Go/no-go recommendation with confidence level

## Example 1: New DTC Product Launch

**Scenario**: Launching a premium yoga mat at $89.99. Monthly fixed costs: $12,000 (warehouse, staff, software, marketing base spend).

**Cost classification**:
- COGS: $22.00 (materials + manufacturing)
- Shipping: $8.50 (oversized item surcharge)
- Payment processing: $2.91 (2.9% + $0.30)
- Packaging: $3.50 (custom box + insert)
- Returns (8%): $7.20
- **Total variable**: $44.11/unit

**Contribution margin**: $89.99 - $44.11 = **$45.88 (51.0%)**

**Break-even**: $12,000 / $45.88 = **262 units/month**

**Scenario modeling**:
- Pessimistic (price $79.99, COGS +10%): 384 units/month → 5.5 months
- Base ($89.99): 262 units/month → 3.2 months
- Optimistic ($89.99, COGS -10%): 233 units/month → 2.1 months

**Recommendation**: Launch is viable if marketing can drive 262+ units/month. At $30 CAC, marketing budget needs $7,860/month to hit base case, raising effective fixed costs to $19,860 and break-even to 433 units.

## Example 2: Amazon Marketplace Expansion

**Scenario**: Existing DTC brand ($34.99 product) evaluating Amazon launch. Additional fixed costs: $2,500/month (Amazon advertising base, A+ content, brand registry tools).

**Cost classification (Amazon-specific)**:
- COGS: $8.00
- FBA fee: $5.50
- Referral fee (15%): $5.25
- Shipping to FBA: $1.50
- Payment processing: $0.00 (included in referral)
- Packaging: $1.50
- Returns (12% on Amazon): $4.20
- PPC cost per unit (estimated): $4.50
- **Total variable**: $30.45/unit

**Contribution margin**: $34.99 - $30.45 = **$4.54 (13.0%)**

**Break-even**: $2,500 / $4.54 = **551 units/month**

**Sensitivity analysis**:
- If PPC drops to $3.00/unit: Break-even = 385 units (-30%)
- If returns drop to 8%: Break-even = 439 units (-20%)
- If price increases to $37.99: Break-even = 331 units (-40%)

**Recommendation**: Thin margins make this risky. Recommend testing at $37.99 price point and optimizing PPC to < $3.50/unit before committing to full inventory. Break-even at 331 units is more achievable.

## Common Mistakes

1. **Forgetting payment processing fees** — At 2.9% + $0.30 per transaction, this is $1.75 on a $50 item. Over 10,000 units, that's $17,500 you didn't account for.

2. **Using gross margin instead of contribution margin** — Gross margin only subtracts COGS. Contribution margin includes ALL variable costs (shipping, fees, returns). The difference can be 15-25 percentage points.

3. **Ignoring return costs** — Returns aren't just lost revenue; they include reverse shipping, inspection labor, restocking, and often product write-offs. Budget 5-15% of sales.

4. **Treating marketing as fixed** — If you spend $X per acquired customer, that's a variable cost. Only base marketing spend (brand campaigns, content creation) is fixed.

5. **Linear scaling assumptions** — Costs don't scale linearly. You'll hit step-fixed costs: new warehouse staff at 200 orders/day, higher software tiers, additional customer service reps.

6. **Single-scenario planning** — A single break-even number creates false precision. Always model pessimistic and optimistic cases to understand the range.

7. **Ignoring seasonality** — Monthly break-even assumes steady sales. If 40% of revenue comes in Q4, your break-even timeline looks very different month-by-month.

8. **Mixing product-level and business-level analysis** — Break-even for a single product is different from break-even for the business. Be clear about which fixed costs to allocate.

9. **Forgetting opportunity cost** — Capital tied up in inventory could be earning returns elsewhere. Factor in the cost of capital (typically 8-15% annually).

10. **Not updating the model** — Break-even analysis is not a one-time exercise. Update monthly with actual costs and sales data to track progress and adjust projections.

## Resources

- [Output Template](references/output-template.md) — Break-even analysis report template
- [Cost Classification Guide](references/cost-classification-guide.md) — Comprehensive e-commerce cost taxonomy
- [Scenario Modeling Framework](references/scenario-modeling-framework.md) — How to build weighted scenario models
- [Quality Checklist](assets/quality-checklist.md) — Analysis validation checklist
