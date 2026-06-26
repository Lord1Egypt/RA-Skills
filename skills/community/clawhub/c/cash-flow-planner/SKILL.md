---
name: Cash Flow Planner
description: Build 13-week cash flow forecasts, identify liquidity gaps, and design capital allocation plans for ecommerce businesses navigating inventory cycles and seasonal demand.
version: 1.1.0
---

# Cash Flow Planner

Cash flow is the oxygen of ecommerce. Unlike traditional retail, DTC brands face a brutal timing mismatch: you buy inventory today, pay suppliers in 30-60 days, hold stock for weeks or months, then finally collect cash from customers—often with payment processing delays adding 2-3 more days. This cash conversion cycle creates dangerous liquidity gaps that can strangle growth. The difference between a thriving brand and one that collapses during a successful sales surge often comes down to whether founders saw the cash crunch coming and planned for it. This skill helps you build rigorous 13-week cash flow forecasts, stress-test multiple scenarios, and design capital allocation strategies that prevent cash surprises from derailing your business.

## Solves

**Inventory financing blindness** — You buy stock based on sales forecasts, but you don't know when that cash will return. Without a weekly cash flow model, you can't calculate how much working capital you need or negotiate better payment terms with suppliers. A 13-week forecast shows exactly when payables come due versus when customer cash arrives, exposing the size and timing of your financing need.

**Seasonal cash traps** — Q4 inventory builds create massive cash drains weeks before revenue materializes. Many brands buy holiday stock in August but don't sell through until October-November, leaving them cash-poor in September. Scenario planning around seasonal demand lets you model different inventory timing strategies and calculate exactly how much capital you need to bridge the gap without blowing through reserves.

**Liquidity blindness during growth** — Growing 200% year-over-year sounds great until you realize it requires 2-3x working capital. Paid advertising creates a cash float problem: you spend $50k on ads today, collect revenue over the next 30 days, then wait 2-3 more days for payment processing. Without a cash reserve target tied to your cash conversion cycle, you can run out of money while growing.

**Bad capital allocation decisions** — Founders often overspend on paid acquisition, skip inventory buys for safe products, or over-hold cash reserves when that cash could fund faster growth. Without a disciplined capital allocation waterfall (operations first, then inventory for proven winners, then marketing, then growth), you'll either run out of cash or leave growth on the table.

**Supplier payment term negotiation failure** — Net 30 is standard, but brands with leverage—those with $50k+ monthly orders or strong year-round demand—often don't ask for Net 45 or Net 60. You can't negotiate terms effectively without a cash flow forecast showing your capacity to support extended payables. A 30-day extension on a $100k inventory buy gives you weeks of cash breathing room.

**Inability to stress-test before crises** — You can't manage what you don't measure. Without scenario analysis (base, optimistic, pessimistic), you're flying blind into downside risk. When a marketing channel underperforms, ad costs spike, or inventory sits longer than expected, you have no playbook. A scenario model built in advance lets you pull the trigger on cost cuts or inventory draws before you're desperate.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|----------|--------|-----------|------|
| **Forecast horizon** | 13 weeks rolling (quarter ahead) | 8-12 weeks | < 8 weeks or annual only |
| **Cash buffer target** | 8-12 weeks operating expenses | 6-8 weeks | 4-6 weeks (minimum) or > 16 weeks (capital locked up) |
| **Inventory financing method** | Mix of terms (Net 45/60 + RBF for spikes) | Consistent Net 30 with one supplier | Cash on delivery or over-reliance on credit lines |
| **Payment terms strategy** | Negotiated based on order volume ($50k+) | Standard Net 30 with tier discounts | Cash on delivery or paying early without discount |
| **Reorder point calculation** | Tied to cash conversion cycle + safety stock | Lead time + average weekly sales | Ad hoc restocks based on "feeling low" |
| **Seasonal reserve timing** | Built 8-12 weeks before peak (Aug for Q4) | Built 4-6 weeks before | Built during peak season or not built at all |
| **Break-even and cap allocation visibility** | Contribution margin break-even + cash burn waterfall | Gross profit break-even tracked weekly | No break-even analysis or only profit-based |

## Workflow

### Step 1: Audit Your Cash Conversion Cycle

Start by calculating your current cash conversion cycle (CCC): the number of days between when you pay suppliers and when you collect cash from customers. CCC = Days Inventory Outstanding (DIO) + Days Sales Outstanding (DSO) – Days Payable Outstanding (DPO). Pull 12 weeks of transaction data: supplier payment dates (for DIO: how long inventory sits before sale), customer purchase dates and payment settlement dates (for DSO: how long after sale until cash arrives), and supplier invoice dates (for DPO: how long you hold cash before paying suppliers). If you're on Shopify + Stripe, export your orders and payouts to calculate exact timelines. For a supplement brand with 30-day inventory turns, 2-day payment processing, and Net 30 supplier terms, your CCC might be 32 days—meaning you need to fund 32 days of operations, COGS, and ad spend simultaneously. This audit is your baseline for everything that follows.

### Step 2: Build Your 13-Week Baseline Forecast

Create a weekly cash flow forecast for the next 13 weeks using the output template provided. For each week, calculate: (1) Opening Balance (closing balance from previous week), (2) Cash Inflows (customer revenue settled to your bank account—not sales recognized, but actual cash), (3) Cash Outflows (COGS payables, payroll, platform fees, ad spend, overhead), and (4) Closing Balance. The key is using settlement timelines, not transaction dates. If you process $20k in Shopify sales on Monday, that cash hits your bank Wednesday or Thursday depending on your payment processor. Use actual payment settlement dates from your bank statements or payment processor dashboard, not order dates. Build this with last year's data (same weeks, adjusted for growth), recent trend data, and known commitments (payroll, bulk ad buys, planned inventory purchases). Most teams build this in a spreadsheet or use cash flow software; the format matters less than accuracy. Flag any week where Closing Balance dips below your minimum cash buffer (typically 4-6 weeks of operating expenses).

### Step 3: Map Inventory and Payables Timing

Layer in your inventory purchases and supplier payables. For each planned inventory buy, identify: (1) Order date, (2) Expected arrival date, (3) Payment due date (based on your supplier terms), and (4) Estimated sell-through timeline. If you buy $50k of inventory on Net 45 terms, you don't pay until day 45—but that $50k cash outflow will hit your forecast on that specific date. Then model when that inventory sells based on historical velocity or conservative projections. This step surfaces timing mismatches: a Q4 inventory build paid on Net 30 requires cash in early August; if your cash buffer is only $30k and the inventory buy is $80k, you'll need to: negotiate Net 60, pre-buy with RBF or a capital line, or delay/reduce the buy. Most cash crises come from poor alignment between payables timing and revenue timing—this step prevents that.

### Step 4: Scenario Test Base, Optimistic, and Pessimistic Cases

Build three versions of your forecast: (1) Base case (your best estimate, likely based on recent performance), (2) Optimistic (+20-30% revenue, lower COGS per unit, faster inventory turns), and (3) Pessimistic (-20-30% revenue, higher COGS, slower turns). For each scenario, recalculate cash inflows and outflows and the impact on your Closing Balance trajectory. The pessimistic case matters most: a 30% revenue miss during a seasonal ramp-up could wipe your buffer or require an emergency credit line. Run sensitivity on key variables: if your CAC increases by 20%, ad spend in week 7 goes up by $10k—does that break your buffer? If a customer refund surge hits 15% (instead of 5%), how deep do you go? Build a simple sensitivity table: 1-2 variables down the left, scenarios across the top, ending cash balance in each cell. This lets you see which variables matter most and where to focus your risk management.

### Step 5: Identify Liquidity Gaps and Capital Needs

Review your three scenarios and identify any week where Closing Balance falls below your minimum cash buffer (4-6 weeks of operating expenses). That's your liquidity gap. For each gap, calculate the size and timing: if your pessimistic case shows a $40k shortfall in week 8, you need $40k in capital by week 7. Then decide how to fill it: (1) Extend payables with suppliers (negotiate Net 60 instead of Net 30), (2) Raise capital (venture, revenue-based financing, or a bank line of credit), (3) Reduce cash outflows (trim ad spend, delay hires), (4) Accelerate inflows (run a sale, pre-order campaign, or offer early-bird discounts). Most founders wait until they're desperate; smart founders raise capital 6-8 weeks before they need it, when they're negotiating from a position of strength. If your forecast shows a $150k seasonal shortfall, pitch that thesis to a lender or RBF provider in week 4 or 5, not week 9 when you're 2 weeks from zero.

### Step 6: Design Your Capital Allocation Waterfall

With your cash position and liquidity gaps clear, build a capital allocation plan: the priority order for how you deploy available cash. Standard waterfall: (1) Operations & payroll (this is sacred), (2) Payables to suppliers (maintain relationships and leverage for better terms), (3) Inventory buys for proven products (products with >50% gross margin and confirmed demand), (4) Paid acquisition (only after you've proven unit economics at current scale), (5) Overhead, hiring, and growth experiments. This forces discipline: you won't overspend on Facebook ads or hire a new role if it puts your payables at risk or delays a high-margin inventory restock. Many brands fail because they allocate capital backwards—overspendinv on acquisition, underfunding inventory, or holding excess cash reserves. A waterfall locks in the right sequence and prevents heroic firefighting.

### Step 7: Review and Reforecast Weekly

Cash flow planning is not a once-a-quarter exercise. Set a recurring weekly review: every Monday, update your forecast with last week's actual revenue and spend, adjust the forward weeks based on new data (new ad campaigns, delayed shipments, supplier changes), and check if your liquidity position has improved or deteriorated. A weekly rhythm keeps your forecast accurate and gives you early warning of changes. If your pessimistic revenue miss appears to be tracking true, you'll see it in week 2 or 3, not week 8 when you're out of options. Most sophisticated brands reforecast every Sunday evening: 30 minutes with a spreadsheet or dashboard. This discipline is cheap insurance against cash surprises.

## Examples

### Example 1: Supplement Brand Building a 13-Week Forecast

**Business profile:** A DTC supplement brand with $120k monthly revenue (growing 15% month-over-month), 65% COGS, 8% platform fees (Shopify, payment processing), $25k monthly fixed overhead (payroll, rent, software), and $40k monthly paid media spend. Payment settlement: Stripe payouts 2 days after sale. Inventory: turns every 4 weeks (28 days), purchased with Net 30 terms from suppliers. Current cash balance: $75k.

**Inputs:**
- Week 1-4 revenue: $120k, $138k, $159k, $183k (15% growth)
- Week 5-8 revenue: $211k, $243k, $279k, $322k (continued 15% growth, no constraints)
- Week 9-13 revenue: $370k, $426k, $490k, $564k, $649k (aggressive growth, testing)
- COGS: 65% of revenue
- Platform fees: 8% of revenue
- Fixed overhead: $25k/week
- Paid media: $40k/week (scaling slightly with revenue: +$2k/week in week 5+)
- Payables: Net 30 (pay in week 2 for week 1 purchase, week 3 for week 2 purchase, etc.)
- Cash buffer target: $50k minimum (6 weeks of ($25k overhead + $40k media), assumes COGS and platform fees tracked to payables separately)

**13-Week Forecast Summary Table:**

| Week | Opening Balance | Revenue Inflow | COGS Payable (Prior Week) | Platform Fees | Overhead | Paid Media | Closing Balance |
|------|-----------------|----------------|--------------------|---------------|----------|-----------|-----------------|
| 1    | $75,000         | $120,000       | $0                 | $9,600        | $25,000  | $40,000   | $120,400        |
| 2    | $120,400        | $138,000       | $78,000            | $11,040       | $25,000  | $40,000   | $104,360        |
| 3    | $104,360        | $159,000       | $89,700            | $12,720       | $25,000  | $40,000   | $95,940         |
| 4    | $95,940         | $183,000       | $103,350           | $14,640       | $25,000  | $40,000   | $95,950         |
| 5    | $95,950         | $211,000       | $119,000           | $16,880       | $25,000  | $42,000   | $104,070        |
| 6    | $104,070        | $243,000       | $137,150           | $19,440       | $25,000  | $44,000   | $121,480        |
| 7    | $121,480        | $279,000       | $157,950           | $22,320       | $25,000  | $46,000   | $149,210        |
| 8    | $149,210        | $322,000       | $181,350           | $25,760       | $25,000  | $48,000   | $191,100        |
| 9    | $191,100        | $370,000       | $209,300           | $29,600       | $25,000  | $50,000   | $237,200        |
| 10   | $237,200        | $426,000       | $240,500           | $34,080       | $25,000  | $52,000   | $311,720        |
| 11   | $311,720        | $490,000       | $276,900           | $39,200       | $25,000  | $54,000   | $405,620        |
| 12   | $405,620        | $564,000       | $318,700           | $45,120       | $25,000  | $56,000   | $524,800        |
| 13   | $524,800        | $649,000       | $366,600           | $51,920       | $25,000  | $58,000   | $672,280        |

**Analysis:**
- **Liquidity health**: This brand stays well above the $50k buffer throughout the 13 weeks, ending with $672k. No capital need for the base case.
- **Key risk**: In week 2, cash dips to $104k—still healthy, but the tightest point. This is where inventory payables hit for the week 1 buy.
- **Inventory reorder timing**: With 28-day turns, they're reordering in week 5, 9, and 13. Payables from week 5 reorder hit in week 6 ($137k+ outflow), but revenue is accelerating, so cash still grows.
- **Paid media scaling**: Spend increases from $40k to $58k/week as revenue grows—disciplined scaling. If this brand doubles their ad spend, the trajectory changes significantly.
- **Downside scenario (pessimistic, -20% revenue)**: Week 1-4 revenue drops to $96k, $110k, $127k, $147k instead of base case. Week 2 payables still hit ($78k COGS) while inflows drop, and closing balance in week 2 falls to $71k. By week 5-6, the pessimistic case shows $32-40k balances, below the $50k target. **Action**: Negotiate extended terms with suppliers (Net 45 instead of Net 30), or pre-arrange a $75k RBF line to cover downside risk.

---

### Example 2: Apparel Brand Planning a Seasonal Inventory Buy

**Business profile:** A $200k/month apparel DTC brand with 55% COGS, 5% payment processing fees, $30k monthly overhead, $50k monthly paid acquisition spend, and cyclical demand (flat summer, strong fall/winter). Current cash balance: $120k. Planning a Q4 inventory buy for holiday season.

**Situation:** The brand wants to buy $200k of inventory in August (5 months before peak demand) to be ready for BFCM and holiday shopping. Their suppliers require payment on delivery (terms cannot be extended). They're projecting a $100k weekly revenue bump in November-December (up from $50k/week baseline), but inventory might not sell through until January. They want to know: (1) Can we fund this buy with current cash? (2) What financing should we pursue? (3) How much cash do we end the year with under different scenarios?

**Analysis Approach:**

**Base Case Assumptions:**
- August: Buy $200k inventory (payment on delivery = cash out in week 1 of August)
- Revenue Sept-Oct: $200k/month ($50k/week baseline, modest growth)
- November-December: Revenue spikes to $100k/week (Q4 surge)
- January-February: Revenue normalizes to $75k/week (post-holiday)
- COGS: 55% of revenue (but already paid in advance for Q4 inventory)
- Inventory sell-through: 60% of $200k ($120k) by end-December, remaining $80k in January
- Current cash: $120k

**Forecast Impact:**

| Period | Revenue | COGS Payables | Processing Fees | Fixed Overhead | Ad Spend | Inventory Buy | Closing Balance |
|--------|---------|------------------|-----------------|----------------|----------|------------------|-----------------|
| Start of August | — | — | — | — | — | — | $120,000 |
| August (weeks 1-4) | $200k | $110k (prior July buys) | $10k | $30k | $50k | $200k | -$100,000 |
| Sept (weeks 5-8) | $200k | $110k | $10k | $30k | $50k | — | -$60,000 |
| Oct (weeks 9-12) | $200k | $110k | $10k | $30k | $50k | — | -$20,000 |
| Nov (weeks 13-16) | $400k | $110k | $20k | $30k | $50k | — | $190,000 |
| Dec (weeks 17-20) | $400k | $110k | $20k | $30k | $50k | — | $400,000 |
| Jan (weeks 21-24) | $300k | $110k | $15k | $30k | $50k | — | $505,000 |

**Problem identified**: Without external capital, this brand goes cash-negative by September. They cannot fund the $200k inventory buy from current cash while paying ongoing operations.

**Capital Solution Scenarios:**

**Option 1: Revenue-Based Financing (RBF)**
- Borrow $200k; repay 8% of monthly revenue (capped at 18 months or $300k total repayment)
- Cost: $24k/month in Nov-Dec (8% of $300k), then $18k/month in Jan-Feb
- Total cost: ~$84k for the $200k draw
- Result: August cash stays positive ($120k - $200k buy + $200k RBF = $120k). No cash crisis. **Best option for this scenario.**

**Option 2: Trade Financing / Supplier Terms**
- Negotiate Net 90 with suppliers instead of cash on delivery
- Buys 90 days before payment due (buy in August, pay in November)
- Requires supplier agreement and strong relationship; possible with $200k+ orders
- Result: August buy doesn't drain cash until November when revenue surges. **Works if suppliers agree; saves financing cost.**

**Option 3: Bank Line of Credit**
- Establish $300k revolver at 8-10% APR
- Draw $200k in August, repay starting November from strong cash flow
- Cost: ~$4-5k/month in interest (August-October), then repay principal
- Requires business financials and personal guarantee; typical for established brands
- Result: Similar to RBF, but lower cost. **Good if credit already exists.**

**Pessimistic Scenario (Q4 revenue up only +50% instead of +100%):**
- November-December weekly revenue: $75k instead of $100k
- Closing balance in December: $250k instead of $400k
- Still positive, but tighter; RBF repayment obligation ($24k/month) is tighter against available cash
- Conclusion: RBF works, but tight. Might have preferred supplier terms or a higher financing line

**Key Decision for this Brand:**
Given their cash balance ($120k) and the size of the inventory buy ($200k), they **cannot self-fund**. They need to commit to financing before August (not in August when they're desperate). RBF is the fastest option (1-2 weeks approval) and aligns repayment with revenue. The brand should: (1) Lock in RBF by June ($200-250k capacity), (2) Negotiate Net 60 with suppliers as a backup, and (3) Execute the buy with confidence knowing cash won't constrain their ability to invest in paid media or manage the holiday surge.

---

## Common Mistakes

1. **Using profit instead of cash flow.** A $100k month of revenue with 60% COGS and $20k overhead looks profitable (+$20k gross profit). But if you're on Net 60 terms and haven't collected customer payments yet, you've actually spent $60k on COGS and $20k on overhead with zero cash inflow. Profit and cash are not the same. Always forecast cash settlement dates, not just revenue recognition.

2. **Ignoring payment processing float.** Stripe and Shopify Payments settle 2-3 days after transaction. PayPal holds 10% or more for 21 days. If you process $50k Monday, you don't have $50k Wednesday—you have $35-40k after fees and settlement delays. Many founders treat sales as instant cash and get shocked on Thursday when their bank balance doesn't match sales.

3. **Treating inventory as a sunk cost after purchase.** Once you've bought $100k of inventory, founders often stop thinking about it as a cash risk. But inventory sitting in a warehouse for 90 days is $100k of working capital that could have been deployed elsewhere. Model inventory turns explicitly: when does it sell, when does that cash hit your bank, and are you happy with that timeline?

4. **Overspending on paid acquisition without a cash buffer.** A brand with $30k cash spending $20k/week on ads is insane. If something breaks (supplier delays, inventory arrives damaged, payment processor holds funds), they're out of money in 1.5 weeks. A safe rule: never spend more than 25-30% of your cash buffer on weekly ad spend. With $50k cash, max weekly ad spend is $12-15k.

5. **Not building scenario analysis until crisis hits.** Most founders forecast once a quarter or once a year. When something changes—a sales miss, a supplier delay, new competition—they have no playbook. By then, it's too late. Building a pessimistic scenario (revenue -20-30%) forces you to think through downside risk when you still have time to act.

6. **Negotiating terms too late.** Asking a supplier for Net 60 when you're already late on a payment is useless. Negotiate terms before you buy, using your order size as leverage. Once you've ordered, you've lost leverage. Start supplier conversations in month 2-3 of a relationship, before any issues arise.

7. **Keeping too much cash as a buffer.** Founders often hold 16-20+ weeks of operating expenses in cash out of fear. That's $200-300k sitting idle that could buy inventory, fuel paid acquisition, or be invested. A data-driven buffer (8-12 weeks operating expenses based on your cash conversion cycle) is smarter than fear-based hoarding.

8. **Assuming inventory will always turn on schedule.** A supplement that normally turns in 4 weeks might sit for 8 weeks if a competitor launches, ad costs spike, or seasonality shifts. Always model slower turns in your pessimistic scenario. If your cash forecast assumes 28-day turns but inventory might sit for 42 days, that's a 2-week cash gap.

9. **Forgetting about payment reserves, refunds, and chargebacks.** Shopify takes a 2.9% platform fee. Stripe holds 1-5% for chargebacks. You might have a 15% return rate for apparel, paid back out of gross profit. None of these reduce your revenue recognition, but all reduce cash inflow. If your forecast shows $100k revenue and assumes $100k cash inflow, you're overestimating by $10-20k.

10. **Not stress-testing ad spend assumptions.** Most forecasts assume ad spend stays flat or grows at a fixed percentage. But if iOS 14+ attribution breaks a channel, CAC spikes 40%, or a major competitor enters your space, ad spend might double. Stress-test your forecast with a +50% ad spend scenario and see what happens to your cash buffer in week 6-8. If you go negative, that's your real risk threshold.

## Resources

- **Output Template** (`references/output-template.md`) — The exact structure for presenting your 13-week forecast, scenario analysis, and capital allocation plan to investors, lenders, or your board.
- **Cash Flow Metrics Guide** (`references/cash-flow-metrics-guide.md`) — Deep dive into cash conversion cycle, DSO/DIO/DPO, cash buffer benchmarks, and payment processing timelines for every major platform (Stripe, Shopify, PayPal, Amazon).
- **Scenario Planning Guide** (`references/scenario-planning-guide.md`) — Framework for building base, optimistic, and pessimistic scenarios, stress-testing sensitivity, and designing downside protection playbooks.
- **Quality Checklist** (`assets/cash-flow-quality-checklist.md`) — 40+ item checklist to validate that your forecast is complete, accurate, and ready for investor or lender review.
