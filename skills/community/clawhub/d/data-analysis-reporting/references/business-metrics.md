# Business Metrics Reference

Standard business metrics, how to calculate them, and how to interpret the results. Use this reference when the user's data contains these metrics or when calculating them from raw data.

## Revenue Metrics

### MRR (Monthly Recurring Revenue)
- **Formula:** Sum of all active subscription revenue normalized to monthly
- **Components:**
  - **New MRR** — revenue from new customers acquired this month
  - **Expansion MRR** — revenue increase from existing customers (upgrades, add-ons)
  - **Contraction MRR** — revenue decrease from existing customers (downgrades)
  - **Churned MRR** — revenue lost from customers who cancelled
  - **Net New MRR** = New + Expansion - Contraction - Churned
- **Interpretation:**
  - Healthy SaaS: Net New MRR is positive and growing
  - Warning: Churned MRR exceeding New MRR for 2+ consecutive months
  - Context: Always report components, not just the total — a flat MRR can mask high churn offset by high acquisition

### ARR (Annual Recurring Revenue)
- **Formula:** MRR x 12
- **Caution:** Only valid when MRR is relatively stable month-to-month. Do not annualize a spike month.
- **Use:** Standard for SaaS valuation, fundraising metrics, and annual planning

### Revenue Growth Rate
- **MoM:** (This month - Last month) / Last month x 100
- **QoQ:** (This quarter - Last quarter) / Last quarter x 100
- **YoY:** (This period - Same period last year) / Same period last year x 100
- **CAGR:** (End value / Start value)^(1/years) - 1
- **Best practice:** Always show absolute numbers alongside percentages. A 50% MoM growth from $2K to $3K is very different from $200K to $300K.

### ARPU (Average Revenue Per User/Account)
- **Formula:** Total Revenue / Total Customers (for the same period)
- **Cross-validation:** When a dataset provides Revenue, Customers, and ARPU columns, verify that Revenue / Customers = stated ARPU. Flag any mismatches before proceeding — contradictory data undermines all downstream analysis.
- **Variants:**
  - **ARPU** — per user, common in consumer products
  - **ARPA** — per account, common in B2B where one account has multiple users
- **Interpretation:**
  - Rising ARPU with stable customer count = healthy expansion / upsell
  - Falling ARPU with growing customer count = adding lower-value customers (may be fine strategically)
  - Flat ARPU = stable unit economics, look at volume for growth signal
- **Caution:** ARPU is an average — high variance means the average may be misleading. Report median alongside mean when possible.

## Customer Metrics

### Customer Churn Rate
- **Logo churn:** Customers lost / Customers at start of period x 100
- **Revenue churn (gross):** Churned MRR / MRR at start of period x 100
- **Revenue churn (net):** (Churned MRR - Expansion MRR) / MRR at start of period x 100
- **Important:** Ask the user which definition they use. "Churn" means different things to different businesses.
- **Benchmarks (SaaS):**
  - SMB: 3-7% monthly logo churn is common
  - Mid-market: 1-3% monthly
  - Enterprise: <1% monthly
  - Net negative revenue churn is the gold standard (expansion exceeds churn)

### Retention Rate
- **Formula:** 1 - Churn Rate (for the same period and definition)
- **Cohort retention:** Track what percentage of a signup cohort remains active after N months
- **Dollar retention (NDR/NRR):** Revenue from a cohort after N months / Revenue from that cohort at start. >100% means expansion exceeds churn within the cohort.

### CAC (Customer Acquisition Cost)
- **Formula:** Total sales and marketing spend / New customers acquired (in the same period)
- **Variants:**
  - **Blended CAC** — all spend / all new customers
  - **Paid CAC** — only paid channel spend / customers from paid channels
  - **Fully loaded CAC** — includes salaries, tools, overhead allocated to acquisition
- **Caution:** CAC is only meaningful when compared to LTV and payback period. A high CAC is fine if LTV is proportionally high.

### LTV (Customer Lifetime Value)
- **Simple formula:** Average revenue per customer per month / Monthly churn rate
- **Better formula:** Average revenue per customer per month x Gross margin % / Monthly churn rate
- **Caution:** LTV assumes stable churn and ARPU, which is rarely true for fast-growing companies. Label assumptions.

### LTV:CAC Ratio
- **Formula:** LTV / CAC
- **Benchmarks:**
  - <1:1 — losing money on every customer (unsustainable)
  - 1:1 to 3:1 — breakeven to marginal (may be okay in land-and-expand models)
  - 3:1 to 5:1 — healthy range for most SaaS
  - >5:1 — either very efficient or under-investing in growth
- **Always pair with:** CAC payback period (months to recover CAC from gross margin)

## Profitability Metrics

### Gross Margin
- **Formula:** (Revenue - COGS) / Revenue x 100
- **COGS for SaaS:** hosting, infrastructure, customer support, onboarding costs directly tied to service delivery
- **COGS for product:** raw materials, manufacturing, direct labor, shipping
- **Benchmarks:** SaaS typically 70-85%; physical products 30-60%; services 40-60%

### Net Margin
- **Formula:** Net income / Revenue x 100
- **Includes:** all operating expenses, taxes, interest, depreciation
- **Context:** Negative net margin is normal for growth-stage companies. Flag when burn rate is relevant.

### Operating Margin
- **Formula:** Operating income / Revenue x 100
- **Use:** Better than net margin for comparing operational efficiency (excludes tax and interest effects)

### Contribution Margin
- **Formula:** (Revenue - Variable costs) / Revenue x 100
- **Use:** Per-unit or per-customer profitability before fixed costs. Critical for pricing and unit economics.

## Efficiency Metrics

### Burn Rate
- **Gross burn:** Total monthly cash outflow
- **Net burn:** Total monthly cash outflow - Total monthly cash inflow
- **Runway:** Cash on hand / Net monthly burn = months until cash runs out
- **Warning thresholds:** <6 months runway is urgent; <12 months requires active fundraising or path-to-profitability plan

### Rule of 40
- **Formula:** Revenue growth rate (%) + Profit margin (%) >= 40
- **Use:** SaaS benchmark balancing growth and profitability
- **Context:** Early-stage companies should skew toward growth; mature companies should skew toward margin

### Magic Number (SaaS Sales Efficiency)
- **Formula:** Net New ARR this quarter / Sales & marketing spend last quarter
- **Benchmarks:** <0.5 = inefficient; 0.5-1.0 = decent; >1.0 = strong signal to invest more in S&M

## Calculation Best Practices

1. **State the formula** every time you calculate a metric. Different businesses define metrics differently.
2. **Confirm definitions** with the user before calculating churn, CAC, or LTV — these are the most commonly miscalculated metrics.
3. **Show absolute numbers** alongside percentages. Percentages without context are noise.
4. **Specify the time period** for every rate or ratio. Monthly churn and annual churn are very different numbers.
5. **Flag when sample size is too small** to calculate meaningful rates. 5 churned customers out of 20 is a 25% churn rate, but the confidence interval is enormous.
6. **Do not mix time periods.** Monthly CAC with annual LTV produces a meaningless ratio. Normalize first.
7. **Label benchmarks as context, not targets.** Industry benchmarks vary by segment, stage, and geography.
