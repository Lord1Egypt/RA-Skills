# Scenario Planning Guide for Cash Flow

This guide provides a comprehensive framework for stress-testing your cash flow forecast across multiple scenarios. Scenario planning is how you prepare for uncertainty and avoid being blindsided by cash crises.

---

## The 3-Scenario Framework

Build three versions of your 13-week cash forecast: base case, optimistic, and pessimistic. Each scenario tells a different story about your cash position and where you might need capital.

### Scenario 1: Base Case (Most Likely)

**Definition:** Your best estimate based on recent performance, known commitments, and reasonable assumptions. Not conservative, not aggressive—just honest.

**How to build it:**
1. Pull last 12 weeks of actual revenue, COGS, and operating expenses
2. Calculate rolling 4-week average for each line item
3. Apply your expected growth rate (if any) week-by-week
4. Layer in known events: planned ad campaigns, seasonal patterns, supplier commitments, payroll increases

**Example assumptions:**
- Revenue: $50k/week baseline, +2% weekly growth (based on past 8 weeks)
- COGS: 58% of revenue (consistent with last 8 weeks)
- Payables: Net 30 with all suppliers (confirmed)
- Paid media: $20k/week (current spend, no changes planned)
- Payroll: $12k/week (fixed, no hires planned in 13-week window)

**Key output:** Closing balance in week 13 and the lowest cash balance (low point) during the 13 weeks.

**Use case:** Present this to your team and stakeholders as "this is what we think will happen." It's your north star for planning.

---

### Scenario 2: Optimistic Case (+20-30% Revenue)

**Definition:** Things go well. Your marketing works better than expected, product-market fit improves, or a competitor stumbles. Revenue grows faster, costs are well-controlled, and you're flush with cash.

**How to build it:**
1. Start with your base case revenue
2. Increase by +20-30% (or your best estimate of "things going right")
3. Assume COGS stays flat or improves (economies of scale)
4. Assume ad spend scales proportionally (if revenue is +25%, ad spend is +25%)
5. Assume payroll and overhead stay fixed (leverage those fixed costs)

**Example:**
- Base case: $50k/week revenue → Optimistic: $62.5-65k/week
- Base case COGS: 58% → Optimistic: 57% (better supplier negotiation, bulk discounts)
- Base case ad spend: $20k/week → Optimistic: $25k/week (scaled with revenue growth)
- Payroll: Still $12k/week (no new hires)

**Cash impact:**
- Higher revenue → faster cash inflow
- Better margins → more cash available after COGS
- Scaled ad spend → but only proportional to growth (not an extra drain)
- Fixed overhead → now a smaller % of revenue (leverage)

**Week 13 result:** Likely $100-200k higher than base case (compounding over 13 weeks).

**Use case:** This scenario shows your **upside potential**. It answers: "If we crush it, how much cash can we deploy in growth, inventory, or reserves?" It's also useful for investor conversations ("if we hit X growth, we'll have $500k by month 4").

---

### Scenario 3: Pessimistic Case (-20-30% Revenue)

**Definition:** Things don't go according to plan. A competitor launches, your main marketing channel breaks (iOS tracking changes), or the market cools. Revenue drops 20-30%, and you need to defend your cash position.

**How to build it:**
1. Start with base case revenue
2. Decrease by -20-30% (or your worst-reasonable estimate)
3. Assume COGS stays the same % (worst case: margins compress as revenue falls)
4. Assume payroll and overhead stay fixed (costs don't drop immediately)
5. Assume ad spend stays elevated initially (trying to stabilize revenue), then cuts

**Example:**
- Base case: $50k/week revenue → Pessimistic: $35-40k/week
- Base case COGS: 58% → Pessimistic: 60% (higher landed cost on smaller orders, less negotiating power)
- Base case ad spend: $20k/week → Pessimistic: Week 1-4 $20k (doubling down), Week 5-8 $12k (cutting 40%), Week 9-13 $8k (crisis mode)
- Payroll: Still $12k/week through week 8, then cut to $8k (hiring freeze, one contractor let go)

**Cash impact:**
- Lower revenue → slower cash inflow
- Worse margins → less cash available after COGS
- Ad spend maintained initially (to stabilize), then cuts in crisis mode
- Fixed overhead eventually cuts, but with 4-week lag (hard to change quickly)

**Week 13 result:** Likely $150-300k lower than base case. Possibly negative if not managed.

**Use case:** This scenario shows your **downside risk**. It answers: "If things go wrong, when do we run out of cash? How much capital do we need?" Every serious founder should spend time in this scenario and have a playbook for it.

---

## Sensitivity Analysis: Stress-Test Key Variables

A sensitivity table helps you identify **which variables have the biggest impact** on cash. Instead of just building three fixed scenarios, test how changes to individual variables affect your cash position.

### Template: 1-Variable Sensitivity

| Variable | Base Value | Stressed Value | Impact on Week 13 Cash | Risk Level |
|----------|-----------|---------|-----------|-----------|
| Revenue | $50k/week | $40k/week (-20%) | –$130k | HIGH |
| Revenue | $50k/week | $62.5k/week (+25%) | +$150k | (upside) |
| COGS % | 58% | 60% (+2%) | –$26k | MEDIUM |
| Ad Spend | $20k/week | $26k/week (+30%) | –$78k | MEDIUM |
| Payables Terms | Net 30 | Net 45 (+15 days) | +$60k | LOW |
| Inventory Turns | 28 days | 42 days (-2 weeks) | –$50k | MEDIUM |
| Payroll | $12k/week | $18k/week (+50%) | –$78k | MEDIUM |
| Payment Settlement | 3 days | 7 days (+4 days) | –$40k | LOW |

**How to interpret this table:**
- **HIGH risk variables** (big impact on cash): Revenue, ad spend, inventory turns. Focus your risk management here.
- **MEDIUM risk variables:** COGS, payroll. Monitor and have a playbook for adjustment.
- **LOW risk variables:** Settlement timing, payables terms. Less urgent, but still worth optimizing.

**Create your own sensitivity table:**
1. List every assumption in your forecast (revenue growth, COGS %, ad spend, payroll, DPO, DIO, etc.)
2. For each, stress-test it ±10-20% (or whatever range is realistic)
3. Recalculate week 13 closing balance and capture the delta
4. Rank by impact (biggest deltas = biggest risks)

---

## Inventory Scenario Modeling

Inventory drives cash in ecommerce. Model three inventory scenarios in parallel with your revenue scenarios.

### Scenario A: Sell-Through on Plan

**Assumptions:**
- Inventory bought in week 1: $100k
- Expected weekly sell-through: 15% of inventory ($15k first week, declining as stock depletes)
- Total sell-through by week 8: 100% (inventory fully sold)
- Payables due: Week 5 (Net 30 from week 1 purchase)

**Cash timeline:**
- Week 1: –$100k (inventory purchase, assume payment in week 5)
- Weeks 1-8: Steady revenue from inventory sale ($15k week 1, $13k week 2, $12k week 3, etc.)
- Week 5: –$100k (payables due)
- Result: By week 8, inventory is sold, payables are paid, cash is neutral or positive

---

### Scenario B: Stockout (Sales Exceed Supply)

**Assumptions:**
- Same inventory buy: $100k
- Demand exceeds supply: Selling 20% weekly instead of 15%
- Stockout in week 5 (inventory fully sold)
- Lost sales: $20k unmet demand weeks 6-8
- Must reorder or miss growth opportunity

**Cash impact:**
- Faster cash collection (inventory converts to cash by week 5 instead of week 8)
- But opportunity cost: $20k in weeks 6-8 of unmet revenue
- Must decide: Reorder emergency inventory (likely on worse terms, higher cost) or accept lost revenue?
- If reorder: New $50k purchase in week 4 on rushed terms (Net 15), due in week 5 = cash squeeze

**When this happens:** Your inventory forecast was too conservative. Growth happened faster than expected.
**Playbook:** Pre-arrange a backup supplier or RBF line for emergency reorders. Have a reorder decision point at 50% inventory sold (mid-point).

---

### Scenario C: Overstock (Sales Underperform Supply)

**Assumptions:**
- Same inventory buy: $100k
- Demand is lower: Selling 10% weekly instead of 15%
- Still have $30-40k inventory by week 13 (25-40% unsold)
- Payables due week 5: –$100k due, but you've only recovered $70-80k from sales
- **Cash gap:** $20-30k shortfall

**Cash impact:**
- Slower cash collection (inventory turns in 50+ days instead of 28 days)
- Payables come due before inventory sells (classic cash crisis)
- Forced to carry excess inventory or markdown to clear
- Working capital is locked up

**When this happens:** Demand softened, product underperformed, or seasonality shifted.
**Playbook:** (1) Run a discount/clearance sale to accelerate sell-through (accept lower margin to free cash). (2) Reduce next reorder size by 30-40%. (3) Use RBF or a credit line to bridge the payables-to-sell-through gap. (4) Review product-market fit; if this SKU is a dud, discontinue and reallocate that inventory budget.

---

## Demand Spike Scenarios

Certain events cause sudden revenue spikes. Model the cash impact of each.

### BFCM / Holiday Season Spike

**Event:** Black Friday Cyber Monday (late November) + holiday shopping (December) drive 2-3x normal revenue.

**Timeline:**
- October-November: Revenue ramps 50-75% above baseline (early holiday shoppers)
- Late November: 150-200% above baseline (BFCM peak)
- December: 100-150% above baseline (holiday shoppers)
- January: 20-30% below baseline (post-holiday cliff)

**Cash impact:**
- Positive: Revenue is 3-4x normal = huge cash influx
- Negative: Requires 3-4x inventory investment (bought August-September)
- Timing: Payables due Sept-Oct (before revenue hits)
- Net result: Likely 4-8 week cash squeeze (Sept-Oct) followed by cash surplus (Nov-Dec)

**Planning:**
- **Inventory buy:** Commit by June, order by July, take delivery Aug-Sept
- **Financing:** Negotiate Net 60 with suppliers or pre-arrange $200-300k RBF by August
- **Cash buffer:** Ensure you have 4-6 weeks of operating expenses in buffer before Sept
- **Ad spend:** Scale up in Sept-Oct (ahead of peak) to build traffic for Nov-Dec peak
- **Reserve:** Hold back 10-20% of Nov-Dec cash surplus for Jan cliff and working capital needs

### Product Launch Spike

**Event:** New product launch drives 25-50% revenue uplift for 2-4 weeks, then normalizes.

**Timeline:**
- Week 1: Pre-launch awareness campaign (ad spend increases)
- Weeks 2-3: Launch peak (50% above baseline revenue)
- Weeks 4-5: Sustained uplift (30% above baseline)
- Weeks 6+: Normalization (or sustained if launch is mega-successful)

**Cash impact:**
- Ad spend increases 1-2 weeks before launch (cash drag)
- Revenue follows 1-2 weeks later (cash replenishment with lag)
- If new product has different (usually lower) margins, net cash impact is smaller
- Inventory for new product is separate build (timing risk)

**Planning:**
- **Inventory:** Buy new product inventory 3-4 weeks before launch, plan for 30-day turns (conservative)
- **Ad spend:** Increase budget 2 weeks before launch, with clear ROAS targets (must hit 3.0+ or cut)
- **Cash bridge:** Model the 1-2 week gap where ad spend is elevated but revenue hasn't hit yet
- **Inventory reserve:** If new product underperforms, have a clearance plan to free cash quickly

### Influencer Mention / PR Spike

**Event:** Major influencer/media mentions your brand, causing 2-5x traffic and 20-50% conversion lift for 1-2 weeks.

**Timeline:**
- Day 1: Mention goes live (can't predict timing)
- Days 1-7: Peak traffic and conversion (2-3x normal)
- Days 7-14: Sustained uplift (1.5x normal)
- Beyond: Normalization

**Cash impact:**
- Upside: 2-3x revenue with minimal ad spend increase (organic lift)
- Downside: Potential stockout if inventory is tight
- Timing: Usually unplanned, so inventory might not keep up

**Planning:**
- **Inventory buffer:** Keep 25-30% excess inventory of top 3 SKUs to absorb spikes
- **Scalable logistics:** Have backup fulfillment capacity or drop-ship option if you run out
- **Cash reserve:** This is a bonus; bank 30-50% of spike revenue into buffer rather than spend it (you may not see it again)

---

## Downside Protection Playbook

When the pessimistic scenario is tracking true, you need a playbook for defending cash. Rank these actions by impact and speed.

### Expense Reduction Priority Order

| Priority | Action | Cash Impact | Implementation Time | Pain Level |
|----------|--------|-------------|-----------|-----------|
| 1 | Pause all paid acquisition except proven channels (ROAS > 3.0) | $10-20k/week savings | 1-2 days | Low |
| 2 | Reduce ad spend by 25% across all channels | $5-10k/week savings | 2-3 days | Low |
| 3 | Negotiate payment terms: extend from Net 30 to Net 45 | $50-100k cash relief | 1-2 weeks | Medium |
| 4 | Reduce discretionary spending (software, tools, services) | $2-5k/week savings | 1 week | Low |
| 5 | Hiring freeze: pause all open reqs | $5-15k/week savings | Immediate | Medium |
| 6 | Reduce contractor/freelancer spend | $3-8k/week savings | 1-2 weeks | Medium |
| 7 | Negotiate workforce reduction (temporary, 10% cut) | $15-30k/week savings | 1-3 weeks | High |
| 8 | Reduce marketing/content initiatives to emergency only | $5-10k/week savings | 1 week | High |
| 9 | Renegotiate supplier prices: target 5-10% reduction | $20-50k total savings | 2-4 weeks | High |
| 10 | Full layoff (20-30% workforce reduction) | $30-60k/week savings | 2-4 weeks | Critical |

**Implementation:** You don't execute all of these at once. As cash deteriorates, move down the list. By priority 4-5, you know you're in trouble. By priority 7, it's a real crisis.

**Triggers for each action:**
- **Action 1 (pause low-ROAS ads):** Triggered when cash balance falls 20% below target or revenue misses forecast by 15% for 2 consecutive weeks
- **Action 2 (25% ad cut):** Triggered when cash balance falls 30% below target or revenue misses by 20%
- **Actions 3-4:** Triggered when cash balance is < 6 weeks of operating expenses
- **Actions 5-6:** Triggered when cash balance is < 4 weeks of operating expenses
- **Actions 7-10:** Emergency response (use only if immediate capital raise isn't possible)

---

## Inventory Drawdown Strategy

Inventory is a last-resort source of cash. Only use if capital raise isn't possible.

### Rapid Inventory Clearance Plan

**Approach 1: Aggressive Discounting**
- Mark down slow-moving inventory 30-50%
- Liquidate within 2-3 weeks
- Accept lower margins to free cash fast
- Example: $50k inventory marked at 40% off = $30k recovery (30% realized margin instead of 60%)
- Cash impact: +$30k in 2-3 weeks
- Downside: Trains customers that you discount heavily (future margin risk)

**Approach 2: Flash Sales / Limited-Time Offers**
- Create urgency without permanent markdowns
- "48-hour flash sale" on overstocked SKUs
- Faster conversion, less margin erosion than full clearance
- Example: Run 3-4 flash sales over 3 weeks = $30-40k recovery
- Cash impact: +$30-40k over 3 weeks
- Better: Preserves brand pricing, customers see it as special event

**Approach 3: Bulk Wholesale / Liquidation**
- Sell overstock in bulk to liquidators or wholesalers
- Get 20-40% of retail value
- Convert to cash in days
- Example: $50k inventory → $15-20k from bulk liquidator
- Cash impact: +$15-20k in 1 week
- Lowest margin, but fastest cash

**Approach 4: Donation + Tax Credit**
- Donate unsellable inventory to charity
- Claim tax deduction at FMV (fair market value, not cost)
- Example: $10k unmoving inventory → $10k tax deduction
- Cash impact: $3-4k tax savings (assuming 30-40% tax rate)
- Use only for truly dead inventory, long-term

---

## Break-Even Analysis

Understanding your break-even is critical for downside planning. Different types of break-even matter.

### Contribution Margin Break-Even

**What it is:** The revenue level where you cover all variable costs (COGS + payment fees) but not fixed costs. Contribution margin is your cash engine.

**Formula:**
```
Contribution Margin % = (Revenue − COGS − Payment Fees) / Revenue
Break-Even Revenue = Fixed Costs / Contribution Margin %
```

**Example:**
- Monthly fixed costs: $40k (payroll $25k + overhead $10k + software $5k)
- Revenue assumption: $200k/month
- COGS: 58% of revenue = $116k
- Payment fees: 3% of revenue = $6k
- Contribution margin: ($200k − $116k − $6k) / $200k = 39%
- **Contribution margin $ per dollar of revenue: $0.39**
- Break-even revenue: $40k / 0.39 = **$102.5k/month**

**Interpretation:** At $102.5k/month revenue, you cover fixed costs but have no profit. Below that, you're cash-negative (burning cash). Every dollar above $102.5k contributes $0.39 to profit and growth.

**In a downturn:** If revenue drops from $200k to $120k, you're only $17.5k above break-even. Any further slip and you're burning cash fast. This is why it matters to know your break-even.

### Cash Break-Even

**What it is:** Break-even adjusted for working capital timing. Accounts for inventory float and payables timing, not just contribution margin.

**Formula:**
```
Cash Break-Even = Contribution Margin Break-Even + (CCC-related Cash Drain)
```

**Example (continuing above):**
- Contribution margin break-even: $102.5k/month
- Cash conversion cycle: 25 days = 0.82 months
- COGS: 58% of revenue
- **At break-even revenue ($102.5k), you're holding 0.82 months of COGS in working capital**
- Working capital drain: $102.5k × 58% × 0.82 = **$49k of cash tied up**
- You need an additional $49k cash buffer above break-even revenue to fund the working capital cycle

**Interpretation:** If you're at $102.5k revenue (contribution margin break-even) but only have $30k cash, you're actually cash-negative because you don't have enough working capital to fund the 25-day cycle. You need $49k + ongoing operating expenses.

### Cash Runway Calculation

**What it is:** How many weeks/months of cash you have at current burn rate.

**Formula:**
```
Cash Runway = Current Cash Balance / Weekly Cash Burn
```

**Example:**
- Current cash: $150k
- Weekly cash burn (pessimistic scenario): $25k
- Cash runway: $150k / $25k = **6 weeks**

**Interpretation:** If nothing changes, you have 6 weeks to raise capital or hit break-even. If revenue recovers and burn drops to $15k/week, runway extends to 10 weeks.

**How to use this:** Every week, update your cash runway calculation. If it's dropping (weeks going down), you're deteriorating. If it's stable or improving (weeks going up), you're on the right track.

---

## Capital Raise Timing & Strategy

### When to Raise Capital (The Right Trigger)

**Wrong timing (desperate):**
- Cash runway is 2-3 weeks
- You're in crisis mode, cutting all marketing
- Lenders know you're desperate and offer terrible terms
- You end up with expensive, dilutive capital

**Right timing (prepared):**
- Cash runway is 8-10 weeks
- Your forecast shows a liquidity need in 6-8 weeks
- You're growing and want to accelerate investment
- Lenders see a healthy business and offer good terms
- You're negotiating from strength

### Financing Hierarchy by Scenario

| Scenario | Financing Approach | Timing |
|----------|---|---|
| **Base case** | No external financing needed; reforecast weekly | Ongoing |
| **Optimistic case** | Self-fund growth; hold excess cash in buffer or deploy in inventory | Ongoing |
| **Pessimistic case (light)** | Pre-arrange a $100k credit line as emergency buffer (don't draw unless needed) | Month 2 of quarter |
| **Pessimistic case (medium)** | Negotiate extended supplier terms (Net 45-60) and secure RBF line ($150-250k) | Month 1 of quarter |
| **Pessimistic case (severe)** | Seek venture funding or raise a secondary round; plan for expense cuts | Before crisis point |

### Capital Raise Playbook

**6-8 weeks before liquidity need:**
1. Finalize your base, optimistic, and pessimistic forecasts
2. Identify which scenario requires external capital and how much
3. Reach out to potential lenders (banks, RBF providers, venture)
4. Prepare a 1-page capital request: amount, use of funds, repayment timeline
5. Get term sheets and negotiate

**2-4 weeks before liquidity need:**
6. Execute financing (draw down line, close RBF, etc.)
7. Confirm cash is available before you need it

**After financing closes:**
8. Deploy capital per your capital allocation waterfall
9. Continue weekly reforecasting to confirm capital is sufficient

---

## Scenario Planning Checkpoints

### Weekly Review

Every Monday, answer these questions:
- [ ] Is revenue tracking toward base case, optimistic, or pessimistic?
- [ ] Is cash balance still above minimum buffer?
- [ ] Has any assumption changed materially (supplier terms, ad spend, inventory timing)?
- [ ] Do I need to trigger any defensive actions from the playbook?

### Monthly Review (End of month)

- [ ] Reforecast the next 13 weeks with new actuals
- [ ] Update sensitivity analysis: which variables changed impact?
- [ ] Review scenario outcomes: are we still expecting base case, or should optimistic/pessimistic probabilities shift?
- [ ] Any changes to capital plan?

### Quarterly Review (End of quarter)

- [ ] Full 13-week reforecast for next quarter
- [ ] Update all three scenarios
- [ ] Revise financing strategy (do we need to raise or can we self-fund?)
- [ ] Share forecast and scenario analysis with board/advisors

---

## Real-World Scenario Example: DTC Apparel Brand

**Business context:**
- Monthly revenue: $250k (growing 5% month-over-month)
- Gross margin: 55%
- COGS: 45% of revenue
- Monthly operating expenses: $90k (payroll $50k, overhead $25k, software $15k)
- Inventory turns: 40 days
- Current cash: $200k

### Base Case (Expected)
- Revenue stays at $250k/month, 5% monthly growth
- COGS: 45%, payables Net 30
- Operating expenses: flat
- Inventory: 40-day turns
- **13-week outlook:** Cash rises to $280k (positive cash flow, no issues)
- **Action:** Continue normal operations, plan next inventory build

### Optimistic Case (+30% Revenue)
- Revenue accelerates to $325k/month with strong brand growth
- COGS: 44% (bulk discounts from higher volume)
- Operating expenses: unchanged (leverage)
- Inventory: 35-day turns (faster sell-through)
- **13-week outlook:** Cash rises to $420k (strong cash generation)
- **Action:** Pre-fund Q4 seasonal inventory buy ($200k), accelerate ad spend to capture growth

### Pessimistic Case (-25% Revenue)
- Revenue drops to $187.5k/month (competitive pressure, macro slowdown)
- COGS: 46% (lower volume, higher landed cost)
- Operating expenses: $90k (payroll hard to cut immediately)
- Inventory: 50-day turns (slower sell-through, overstock)
- **13-week outlook:** Cash drops from $200k to $80k by week 10 (below safety threshold)
- **Liquidity gap:** Week 8-10, cash falls below $100k (4 weeks of operating expenses)
- **Triggers:**
  - Week 1-2: Monitor revenue daily; if tracking 20%+ below forecast, trigger action 1 (pause low-ROAS ads)
  - Week 3-4: If revenue still down, trigger action 2 (reduce all ad spend 25%)
  - Week 5-6: Negotiate extended supplier terms (Net 45) to ease payables timing
  - Week 6-8: If still shortfall, activate $150k RBF line as emergency buffer
- **Alternative:** Pre-arrange RBF in month 1 of quarter ($150k available) so it's ready if needed

**Key insight:** For this brand, the pessimistic scenario is realistic and has happened before. Pre-arranging a $150k RBF line as insurance costs ~$2-3k/year (fee) but prevents a $150k crisis if things go wrong. That's smart capital management.
