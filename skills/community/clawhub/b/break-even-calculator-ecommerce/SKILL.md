# Break-even Calculator Ecommerce

Calculate the real no-loss line before deciding whether to launch harder, discount harder, or scale paid traffic.

This is not a generic margin calculator. It separates variable from fixed costs, models real ecommerce unit economics (returns, payment fees, platform takes), and translates math into actionable launch/hold/scale decisions.

---

## Quick Reference

| Decision | Key Metric | Green | Yellow | Red |
|---|---|---|---|---|
| Launch viability | Contribution margin % | > 40% | 20–40% | < 20% |
| Ad scaling room | Break-even CPA | CPA < 60% of CM | CPA 60–90% of CM | CPA > 90% of CM |
| Discount safety | Margin after discount | > 25% CM remaining | 10–25% CM remaining | < 10% CM remaining |
| Free shipping | Margin absorption | Shipping < 30% of CM | Shipping 30–50% of CM | Shipping > 50% of CM |
| Scale readiness | Break-even units/mo | < 50% of current vol | 50–80% of current vol | > 80% of current vol |

---

## Solves

Ecommerce operators lose money not because they can't calculate margins, but because:

- They use gross margin when they should use contribution margin
- Platform fees, payment processing, returns, and packaging get excluded from "cost"
- Ad scaling decisions are made on ROAS without knowing actual break-even ROAS
- Discount and free-shipping policies are set without modeling margin impact
- "Profitable" products turn unprofitable at scale because fixed costs aren't allocated
- Teams confuse revenue growth with profit growth

Goal: **Give operators a clear, reviewable break-even model that supports real decisions — not just a number.**

---

## Use when

- You need a break-even view before launching or scaling a product
- A team is changing price, discount, bundle, or free-shipping policy
- Paid acquisition is growing but true profitability is unclear
- Margin pressure is increasing and you need a decision baseline fast
- Evaluating whether to run a promotion, flash sale, or bundle offer
- Comparing profitability across SKUs, channels, or fulfillment methods
- Building a case for price changes or cost reductions

## Do not use when

- You need full accounting, tax treatment, or cash-flow modeling
- Core inputs are missing and nobody can provide reasonable assumptions
- The task is valuation, forecasting, or board-level finance reporting
- You only want gross revenue math without cost realism
- Legal or compliance-sensitive financial reporting is required

---

## Inputs

Gather these inputs — mark any assumptions explicitly:

**Revenue side:**
- Selling price (or price range if testing)
- Average order value (AOV) if bundling
- Expected discount % or coupon structure

**Variable costs per unit:**
- COGS / unit cost (landed cost including freight to warehouse)
- Shipping to customer (outbound)
- Packaging & pick-pack-ship labor
- Payment processing fees (typically 2.5–3.5%)
- Platform/marketplace fees (e.g., Amazon 15%, Shopify Payments 2.9%)
- Return/refund rate and cost per return

**Acquisition costs:**
- Ad spend or budget
- Target or actual CPA (cost per acquisition)
- Target or actual ROAS
- Organic vs paid traffic mix if known

**Fixed costs (if relevant):**
- Monthly overhead (warehouse, tools, staff)
- Subscription/platform fees
- Content/creative production costs

See `references/cost-breakdown-guide.md` for detailed cost taxonomy.

---

## Workflow

### 1. Separate variable costs from fixed costs

This is the most common error. Be explicit about what scales with volume and what doesn't.

**Variable (per-unit):**
- COGS, shipping, packaging, payment fees, platform fees, returns

**Fixed (per-period):**
- Rent, salaries, SaaS tools, insurance, loan payments

**Semi-variable (step functions):**
- Warehouse staff (fixed per shift, but add shifts at volume thresholds)
- 3PL fees (often tiered)

Use the cost classification in `references/cost-breakdown-guide.md` to ensure nothing is missed.

### 2. Calculate contribution margin

```
Contribution Margin (CM) = Selling Price - Total Variable Costs per Unit
CM% = CM / Selling Price × 100
```

**Include ALL variable costs:**
- COGS
- Outbound shipping (if seller-paid)
- Packaging + pick-pack
- Payment processing (% of selling price)
- Platform/marketplace fees (% of selling price)
- Return cost allocation = (return rate × cost per return)

### 3. Calculate break-even points

**Break-even units (with fixed costs):**
```
BE Units = Fixed Costs / CM per unit
```

**Break-even CPA:**
```
BE CPA = CM per unit (before ad spend)
```
This is the maximum you can pay to acquire a customer and still break even on first order.

**Break-even ROAS:**
```
BE ROAS = Selling Price / (Selling Price - CM + CPA target)
```
Or more simply:
```
BE ROAS = 1 / (CM% before ad spend)
```

### 4. Run sensitivity analysis

Model how the break-even shifts when key inputs change. Focus on the variables the team can actually control:

| Variable | Test range | Impact on |
|---|---|---|
| Selling price | ±10–20% | CM, BE units, BE ROAS |
| COGS | ±5–15% | CM, BE units |
| Ad CPA | ±20–50% | Profitability, scale room |
| Return rate | ±3–10pp | CM, effective margin |
| Discount depth | 10/15/20/25% off | CM, BE units, BE ROAS |
| Shipping policy | Paid vs free vs threshold | CM, conversion rate |

Use `references/sensitivity-template.md` for structured output.

### 5. Translate to decisions

Don't just output numbers. Frame results as decisions:

| Result | Decision framing |
|---|---|
| CM > 40%, BE CPA has room | **Scale:** Increase ad spend, test new channels |
| CM 20–40%, tight CPA room | **Optimize:** Reduce COGS, improve conversion, test pricing |
| CM < 20% | **Hold:** Don't scale until unit economics improve |
| Discount breaks BE | **Don't discount:** Use value-adds instead of % off |
| Free shipping kills margin | **Set threshold:** Offer free shipping above $X AOV |
| High return rate crushing CM | **Fix product/listing:** Returns are a product/expectation problem |

### 6. Quality-check the model

Before presenting results, verify with `assets/model-checklist.md`:
- Are all variable costs included?
- Are assumptions labeled with confidence levels?
- Does the model account for returns?
- Is payment processing calculated on selling price (not COGS)?
- Are platform fees applied correctly?

---

## Output

Return a structured analysis package (see `references/output-template.md`):

1. **Assumptions table**
   - Every input listed with source (actual data vs estimate vs industry benchmark)
   - Confidence flag: ✅ confirmed / ⚠️ estimated / ❓ assumed

2. **Unit economics breakdown**
   - Revenue per unit → all variable costs → contribution margin
   - Show each cost line, not just totals

3. **Break-even results**
   - Break-even units per month
   - Break-even CPA
   - Break-even ROAS
   - Current margin vs break-even margin

4. **Sensitivity analysis**
   - 2–3 scenarios showing how key variables shift break-even
   - Highlight which variable has the strongest impact

5. **Decision recommendation**
   - Launch / Hold / Scale / Optimize
   - Specific actions based on the numbers
   - Risk flags (e.g., "margin too thin for discounting")

---

## Quality bar

Strong output should:
- Show all math explicitly — no black boxes
- Keep variable and fixed costs clearly separated
- Include return/refund impact (most calculators ignore this)
- Label every assumption with confidence level
- Frame results as decisions, not just numbers
- Help teams avoid "fake-profit" decisions

## What "better" looks like

Better output goes beyond "your break-even is X units." It helps decide:
- Whether the offer is viable at current costs
- How much ad spend room exists before break-even
- Whether discounting breaks the model
- Which cost lever matters most (COGS? Shipping? Returns?)
- Whether the business is near scale-ready or still too fragile
- What would need to change to make the unit economics work

---

## Examples

### Example 1: DTC skincare product

**Inputs:**
- Selling price: $45
- COGS: $8.50
- Shipping: $5.50
- Packaging: $2.00
- Payment processing (3%): $1.35
- Platform fees: $0 (own Shopify store)
- Return rate: 8%, cost per return: $7

**Calculation:**
- Return cost allocation: 8% × $7 = $0.56/unit
- Total variable cost: $17.91
- **Contribution margin: $27.09 (60.2%)**
- Break-even CPA: $27.09
- If actual CPA is $18 → $9.09 profit per order → **Scale**

### Example 2: Amazon marketplace electronics

**Inputs:**
- Selling price: $29.99
- COGS: $11.00
- FBA fees: $5.50
- Amazon referral (15%): $4.50
- Return rate: 12%, cost per return: $9

**Calculation:**
- Return cost allocation: 12% × $9 = $1.08/unit
- Total variable cost: $22.08
- **Contribution margin: $7.91 (26.4%)**
- Break-even CPA: $7.91
- If PPC CPA is $6.50 → only $1.41 profit per order → **Optimize before scaling**

---

## Common mistakes

1. **Forgetting payment processing fees** — 2.5–3.5% of every sale adds up fast
2. **Ignoring return costs** — A 10% return rate with $8 return cost = $0.80/unit drag
3. **Using gross margin instead of contribution margin** — Gross margin excludes shipping, fees, returns
4. **Not modeling discounts through** — A 20% discount on a 30% margin product leaves only 10% margin
5. **Treating CPA as fixed** — CPA rises as you scale (diminishing returns on ad spend)

---

## Resources

- `references/output-template.md` — Structured output format
- `references/cost-breakdown-guide.md` — Comprehensive cost taxonomy for ecommerce
- `references/sensitivity-template.md` — Sensitivity analysis framework
- `assets/model-checklist.md` — Pre-delivery quality checklist
