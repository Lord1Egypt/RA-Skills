# Cash Flow Forecast Quality Checklist

Use this 40+ item checklist to validate that your cash flow forecast is complete, accurate, and ready for investor/lender review. Organized into 10 categories: separate REQUIRED items (must have before sharing) from RECOMMENDED items (best practice).

---

## Category 1: Forecast Completeness & Structure

### REQUIRED

- [ ] **13-week rolling forecast defined.** Forecast covers 13 weeks starting with the week of [DATE] through week of [DATE]. Not more than 13 weeks (too uncertain), not less (too short-term).
- [ ] **All major line items included.** Forecast has columns for: Opening Balance, Revenue Inflows, COGS Payables, Platform Fees, Payroll, Operating Expenses, Paid Acquisition, Other Outflows, Total Outflows, Closing Balance.
- [ ] **Week-by-week granularity.** Each row represents one calendar week (Mon-Sun or consistent definition). Avoid "lumpy" forecasts that skip weeks or combine multiple weeks.
- [ ] **Base, optimistic, and pessimistic scenarios defined.** Three complete forecasts prepared; each with clear assumptions. Not just one "best guess" forecast.
- [ ] **Closing balance tracked for each week.** Formula: Opening Balance + Revenue Inflow − Total Outflows = Closing Balance. No gaps.
- [ ] **Running reserve calculated.** Each week shows Closing Balance vs. Minimum Cash Buffer Target (e.g., "week 1 closing $150k vs. target $120k = +$30k buffer").
- [ ] **Cash minimum buffer defined.** Explicit value in $ (e.g., $150k minimum = 6 weeks of operating expenses at current level). Documented and justified.

### RECOMMENDED

- [ ] **Sensitivity analysis table created.** One-variable stress test for top 5-7 variables (revenue, COGS %, ad spend, inventory turns, payables terms). Shows impact on week 13 closing balance.
- [ ] **Scenario probability assigned.** Base case 60% likely, optimistic 20%, pessimistic 20% (or your best estimate). Helps prioritize risk management.
- [ ] **Forecast vs. actuals comparison.** Prior quarter's forecast shown alongside actual results, with variance % documented. Shows forecast accuracy and credibility.

---

## Category 2: Data Accuracy & Sources

### REQUIRED

- [ ] **Revenue data reconciled.** 13-week revenue forecast backed by: (1) last 12 weeks of actual revenue, (2) known campaigns/events in forecast window, (3) stated growth assumptions. Not arbitrary.
- [ ] **Revenue data from primary source.** Revenue pulled directly from Shopify Analytics, Stripe Dashboard, or accounting system. Not a gut estimate.
- [ ] **Payment settlement timing validated.** DSO (days sales outstanding) calculated from actual settlement data from your payment processor (Stripe, Shopify Payments, PayPal, etc.). Not assumed.
  - [ ] Stripe: Verified 2-3 day settlement from recent deposits in bank statement
  - [ ] PayPal: Verified 1 day settlement + % hold for 21 days (if applicable)
  - [ ] Other processors: Documented and confirmed
- [ ] **COGS % validated.** Percentage based on last 8-12 weeks actual COGS, not estimated. Document variance by product category if applicable.
- [ ] **COGS payables timeline confirmed.** Days Payable Outstanding (DPO) backed by: (1) supplier invoices showing Net 30/45/60 terms, (2) actual payment history showing when you pay.
- [ ] **Operating expenses documented.** Payroll, overhead, software, and other fixed expenses listed with source: (1) current payroll system, (2) vendor invoices, (3) accounting ledger. Not guesses.
- [ ] **Ad spend data from actual accounts.** Facebook Ads Manager, Google Ads, TikTok, etc. showing historical spend and planned spend. Not estimates.

### RECOMMENDED

- [ ] **Revenue by channel broken down.** If revenue comes from multiple channels (Shopify, Amazon, wholesale, etc.), forecast shows each separately with different settlement timelines.
- [ ] **Refund/return reserve modeled.** Historical return rate (e.g., 10% for apparel, 5% for supplements) documented and cash impact calculated.
- [ ] **Chargeback reserve included.** Historical chargeback rate (typically 1-3%) and average chargeback amount documented.
- [ ] **Data quality audit performed.** Spot-check: pick 3 random weeks from forecast, verify revenue/expenses match bank statements or source systems. Should match within 2-3%.

---

## Category 3: Scenario Assumptions & Flags

### REQUIRED

- [ ] **Base case assumptions documented.** For each major line item, write 1-2 sentences explaining the assumption:
  - [ ] Revenue: "Based on last 8-week average of $X/week, plus 3% weekly growth (observed trend in past 12 weeks). No major campaigns planned in forecast window."
  - [ ] COGS: "58% of revenue based on last 12 weeks actual. Current supplier is primary; no major price increases known."
  - [ ] Payroll: "$15k/week, fixed. No hires or severances planned in 13-week window."
  - [ ] Payables terms: "Net 30 with all suppliers, confirmed in recent invoices. No negotiations pending."
  - [ ] Inventory turns: "28-day average based on last 12 weeks. Normal seasonality applies."
- [ ] **Optimistic case assumptions documented.** What has to happen for optimistic to come true?
  - Revenue growth rate, COGS reduction, ad spend scaling, etc. At least 2-3 sentences.
- [ ] **Pessimistic case assumptions documented.** What are the downside triggers?
  - Specific revenue reduction %, COGS increase %, ad spend changes, inventory turn slowdown. At least 2-3 sentences.
- [ ] **Known risks flagged.** Any material uncertainty documented:
  - [ ] "Largest supplier could tighten terms from Net 30 to Net 15" → Cash impact: –$50k in week 5
  - [ ] "iOS 14+ attribution changes could reduce ROAS 30-40%" → Cash impact: +$30k/week ad spend to maintain sales
  - [ ] "Q4 inventory build planned for August, payment due Sept; requires $200k working capital" → Need to pre-arrange financing
  - [ ] "Top 3 products represent 65% of revenue; if one underperforms, revenue miss 15-20%" → Inventory allocation risk
  - [ ] "Payment processor holds 10% of PayPal volume for 21 days" → Affects DSO by ~1 week vs. Stripe baseline

### RECOMMENDED

- [ ] **Confidence level assigned to each assumption.** High / Medium / Low, with brief justification.
- [ ] **Historical accuracy tracked.** "Last quarter's forecast predicted $X revenue; actual was $Y (98% accurate)" or "off by 8%". Shows track record.
- [ ] **Downside trigger points defined.** "If revenue misses by 20% for 2 consecutive weeks, we trigger ad cut playbook." Clear, objective rules.

---

## Category 4: Inventory & Payables Timing

### REQUIRED

- [ ] **Planned inventory builds documented.** For each major purchase in next 13 weeks:
  - [ ] Purchase amount and timing (which week)
  - [ ] Supplier and payment terms (e.g., "Net 45 from ABC Supplier")
  - [ ] Payment due date (calculate from order date + terms)
  - [ ] Expected sell-through timeline (how long inventory will sit before selling)
  - [ ] Impact on cash flow (COGS payable outflow in week X)
- [ ] **Payables aging reviewed.** Do you have accounts payable older than 30-60 days? If so, flag as supplier relationship risk.
- [ ] **Supplier payment terms confirmed.** Contact top 3 suppliers and confirm: Are you on Net 30, Net 45, Net 60? Any changes planned?
  - [ ] Supplier A: [Name], Net [#] days (confirmed [DATE])
  - [ ] Supplier B: [Name], Net [#] days (confirmed [DATE])
  - [ ] Supplier C: [Name], Net [#] days (confirmed [DATE])
- [ ] **Days Payable Outstanding (DPO) calculated.** Formula: (Average Payables / Daily COGS) × 365. Should match your supplier terms.
  - Target DPO: [#] days (based on negotiated terms)
  - Actual DPO: [#] days (based on recent payment history)
  - Variance: [#] days (are you paying faster or slower than terms?)

### RECOMMENDED

- [ ] **Inventory by SKU tracked.** Top 10 SKUs listed with:
  - Current stock (units)
  - Days of stock on hand (units sold per day vs. stock)
  - Reorder status (when will you reorder?)
  - Estimated sell-through date
- [ ] **Inventory financing plan documented.** For large builds (>$100k), how will you finance it?
  - Self-funded (from operating cash): $X
  - Supplier terms (Net 45/60): $X
  - RBF or credit line: $X
  - Pre-orders: $X
- [ ] **Payables negotiation opportunity identified.** Do you have suppliers you should push for better terms?
  - Supplier [Name]: Current Net [#], Target Net [#], Annual volume [$(amount)]

---

## Category 5: Seasonal Adjustments

### REQUIRED

- [ ] **Seasonality identified and modeled.** Does your business have seasonal demand?
  - [ ] If YES: Q1 average revenue, Q2 average, Q3 average, Q4 average documented. Each week in forecast adjusted accordingly.
  - [ ] If NO: Confirm business is stable year-round. Document if demand is typically flat.
- [ ] **Seasonal reserve planned (if applicable).** If your business is seasonal:
  - [ ] Q4 inventory buy timing documented: "Ordered by [DATE], arrives [DATE], payment due [DATE]"
  - [ ] Working capital requirement calculated: $[amount]
  - [ ] Financing plan: Supplier terms, RBF, or capital raise?
- [ ] **Post-peak cliff modeled.** If revenue spikes seasonally:
  - [ ] Peak month revenue: $[amount]
  - [ ] Post-peak month revenue: $[amount]
  - [ ] Cliff percentage: (peak − post-peak) / peak = [%] decline
  - [ ] Cash impact: You've built large inventory, peak revenue doesn't last, cash gets tied up in slow-moving stock?

### RECOMMENDED

- [ ] **Multi-year seasonality trend shown.** Last 3 years of monthly revenue by quarter. Shows if seasonality is consistent or changing.
- [ ] **Seasonal inventory clearance plan created.** How will you clear excess inventory after peak season?
  - Discount strategy, timing, target margin, expected cash recovery

---

## Category 6: Platform & Payment Processing

### REQUIRED

- [ ] **Payment processor settlement verified.** For each payment method used:
  - [ ] Stripe: 2-3 day settlement, 2.9% + 30¢ fee (confirmed from recent deposits)
  - [ ] Shopify Payments: [#] day settlement, [%] fee
  - [ ] PayPal: [#] day settlement, [%] fee, [%] hold for [#] days
  - [ ] Other: [Processor], [#] day settlement, [%] fee, [%] hold (if applicable)
- [ ] **Platform fees calculated and deducted from revenue.**
  - Not assuming 100% of sales = cash. Actual cash inflow = Revenue − Platform Fees.
  - Example: $100k sales on Stripe = $100k − 2.9% fee − 30¢ = $97.07k cash
- [ ] **Shopify account charges reviewed.** Basic Shopify vs. Shopify Plus? Any monthly charges beyond the core plan?
  - Shopify plan: [Plan name], [$/month]
  - Shopify apps: [Apps], [$/month each]
  - Total Shopify+app fees: $[amount]/month
- [ ] **Payment processor holds modeled (if applicable).** If Stripe, PayPal, or other holds funds:
  - Hold percentage: [%]
  - Hold duration: [#] days
  - Impact on DSO: [#] additional days of delayed cash
  - Dollar impact: At $[revenue]/week, hold = $[amount] locked up

### RECOMMENDED

- [ ] **Multi-processor strategy documented (if using multiple).** If you use both Stripe and PayPal:
  - Stripe: [%] of revenue
  - PayPal: [%] of revenue
  - Weighted average settlement time: [#] days
  - Combined fee impact: [%] of total revenue
- [ ] **Processor redundancy plan documented.** What if Stripe account is limited or holds funds?
  - Backup processor: [Processor]
  - Estimated revenue shift: [%] to backup
  - Setup timeline: [#] days
- [ ] **Payment disputes & chargebacks modeled.** Historical chargeback rate documented:
  - Chargeback rate: [%] of transactions
  - Average chargeback amount: $[amount]
  - Monthly chargeback reserve needed: $[amount]

---

## Category 7: Capital Allocation & Waterfall

### REQUIRED

- [ ] **Capital allocation waterfall defined.** Priority order for deploying available cash:
  1. Operations & Payroll (non-negotiable)
  2. Supplier Payables (maintain terms and relationships)
  3. Core Inventory Restocks (high-margin, proven SKUs)
  4. Paid Acquisition (growth channel)
  5. [Optional priorities: overhead, hiring, experiments]
- [ ] **Each tier has explicit allocation rule.** Not vague. Examples:
  - "Operations: 100% of weekly operating expenses ($35k/week) prioritized first"
  - "Payables: 100% of supplier invoices due within 30 days paid on time"
  - "Inventory: Restock only SKUs with >50% gross margin and confirmed demand from prior 4 weeks"
  - "Ads: Only if cash balance > 2x buffer, and ROAS on channel > 3.0"
- [ ] **Any deferral or constraint documented.** Are you deferring any category?
  - [ ] "Ad spend capped at $15k/week until cash hits $150k"
  - [ ] "Hiring freeze: no new hires until Q3"
  - [ ] "Inventory restraint: only restock current bestsellers, no new SKUs"

### RECOMMENDED

- [ ] **Weekly capital allocation review process documented.** "Every Monday, CFO reviews prior week's cash balance and allocates available cash per waterfall rules"
- [ ] **Variance from waterfall flagged.** "In week 3, we spent $10k on growth initiative outside of waterfall. Reason: [explanation]. Impact on baseline: [cash impact]"

---

## Category 8: Risk Flags & Downside Scenarios

### REQUIRED

- [ ] **All liquidity gaps identified.** Any week where Closing Balance < Minimum Buffer?
  - Week [#]: Closing balance $[amount], Buffer target $[amount], Shortfall $[amount]
  - Root cause: [Explanation, e.g., "Large COGS payable from Q3 inventory buy"]
  - Mitigation: [Planned action: negotiate terms, raise capital, cut expenses, etc.]
- [ ] **Pessimistic scenario stress-tested.** Revenue down 20-30%; does business still have 4+ weeks of cash?
  - Pessimistic week 13 closing: $[amount]
  - vs. Minimum buffer: $[amount]
  - Shortfall (if any): $[amount]
  - Finance needed by week [#]: $[amount]
- [ ] **Key variable sensitivities documented.** Which 3-5 variables have biggest impact on cash?
  - Variable 1: Revenue ±20% → Cash impact ±$[amount]
  - Variable 2: COGS ±5% → Cash impact ±$[amount]
  - Variable 3: [Variable] → Cash impact [impact]
- [ ] **Early warning signals defined.** What data points trigger defensive actions?
  - Revenue misses forecast by [%] for [#] consecutive weeks → Trigger ad cut
  - DIO increases by [#] days vs. rolling avg → Investigate overstock
  - Payment processor hold increases from [%] to [%] → Re-plan DSO
  - Supplier delays shipment by [#] weeks → Accelerate backup order

### RECOMMENDED

- [ ] **Downside playbook created.** If pessimistic scenario tracks true, what's the action sequence?
  - Week 1-2 response: [Action]
  - Week 3-4 response: [Action]
  - Week 5-6 response: [Action]
  - Emergency (week 7+): [Action]
- [ ] **Supplier relationship risk assessed.** Any suppliers at risk of tightening terms or failing to deliver?
  - Supplier [Name]: [Risk, e.g., "Financial stress", "Relationship strained by late payment"]
  - Impact: Loss of this supplier would reduce COGS capacity by [%], requiring backup sourcing
  - Mitigation: [Plan, e.g., "Build relationship with backup supplier", "Negotiate longer terms before problem"]

---

## Category 9: Assumptions Validation & Documentation

### REQUIRED

- [ ] **Every number in forecast has a source.** Pick any cell at random; you should be able to explain:
  - Where did this data come from? (Bank statement, vendor invoice, software dashboard, etc.)
  - When was it last updated? (Should be current week data, not old)
  - Is it actual or forecasted? (If forecasted, what's the basis? Historical trend? Known event?)
- [ ] **Assumptions last updated date documented.** "Forecast prepared on [DATE] using data through [DATE]. Last updated [DATE]."
- [ ] **Change log maintained (recommended but listed as required for mature forecasts).** When an assumption changes, document it:
  - [DATE]: Supplier [Name] extended terms from Net 30 to Net 45 → Added $50k week 6 inflow
  - [DATE]: Revenue trend shifted from 5% growth to 2% growth → Reduced weeks 7-13 revenue by 3%
  - [DATE]: Q4 inventory buy pushed back from week 8 to week 6 → Payables now due week 9 instead of week 11

### RECOMMENDED

- [ ] **Forecast accuracy tracked quarterly.** Last quarter's forecast vs. actual:
  - Base case forecast: $[amount] revenue, $[amount] ending cash
  - Actual: $[amount] revenue, $[amount] ending cash
  - Variance: [%] on revenue, [%] on cash
  - What drove the variance? What assumptions were wrong?

---

## Category 10: Output & Delivery Standards

### REQUIRED

- [ ] **Forecast presented in clear format.** Three options:
  - [ ] Spreadsheet (Excel/Google Sheets) with clear row/column labels
  - [ ] Cash flow management software (Foresight, Float, etc.) with exportable summary
  - [ ] Formatted document using the provided output template
- [ ] **Week-by-week table clear and readable.** All numbers formatted consistently:
  - Currency: $ prefix, comma separators (e.g., $1,234,567)
  - Negative numbers: Shown in parentheses or red (-$50,000)
  - Percentages: [%] format (e.g., 58%)
- [ ] **Scenario summary table included.** For each of 3 scenarios:
  - Assumptions (1-2 line summary)
  - Week 13 closing balance
  - Lowest cash balance and when it occurs
  - vs. Buffer target (surplus or deficit)
- [ ] **Key metrics summary on first page.** Any reader should immediately see:
  - Current cash balance: $[amount]
  - 13-week ending cash (base): $[amount]
  - Liquidity gaps (if any): [Description and weeks]
  - Capital need (if any): $[amount] needed by week [#]
- [ ] **Appendices included.**
  - Assumption detail (list all major assumptions)
  - Data sources (where did the data come from?)
  - Calculation methodology (how did you derive DSO, DIO, payables, etc.?)

### RECOMMENDED

- [ ] **Executive summary (1 page) created.** For busy stakeholders:
  - Business summary (revenue, margins, cash position)
  - Forecast at a glance (base, optimistic, pessimistic in one paragraph each)
  - Key risks and mitigation
  - Capital plan (if raising)
- [ ] **Sensitivity analysis table included.** One-page table showing impact of key variable changes on week 13 cash balance.
- [ ] **Updated weekly.** Forecast is no older than [#] days. Not a quarterly or one-time document.

---

## Sign-Off Section

**Forecast creator:** [Name], [Title]
**Date prepared:** [DATE]
**Date last updated:** [DATE]
**Reviewed by:** [Name], [Title] (optional but recommended for mature businesses)
**Approved by:** [Name], [Title] (optional but recommended for investor/lender submission)

**Quality score:**
- Required items completed: [#]/[total required]
- Recommended items completed: [#]/[total recommended]
- **Overall confidence level: [ ] Low (< 70% required) [ ] Medium (70-90% required) [ ] High (> 90% required, > 50% recommended)**

---

## How to Use This Checklist

1. **Before creating forecast:** Review categories 1-3. Gather data sources. Define assumptions.
2. **While building forecast:** Use categories 4-7. Ensure each calculation is sourced and documented.
3. **Before sharing forecast:** Run through categories 8-10. Flag risks. Validate accuracy.
4. **Monthly reforecast:** Use the checklist as quality standard. Aim to improve from month 1 to month 2 to month 3.

**Target:** 100% of REQUIRED items, 70%+ of RECOMMENDED items by month 2. By month 3, you should have a best-in-class cash flow forecast.
