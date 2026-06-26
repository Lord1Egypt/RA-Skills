# LTV Calculation Comprehensive Guide

## Overview

Lifetime Value (LTV) quantifies the total profit (or revenue) a customer is expected to generate over their entire relationship with your company. It's the most critical metric for determining customer acquisition cost (CAC) budgets, retention marketing investment, and segment-specific marketing strategies.

Two calculation approaches dominate ecommerce:
1. **Historical LTV** — based on actual past customer spending
2. **Predictive LTV** — forecasts future spending using cohort analysis and decay modeling

This guide covers both methods, benchmark data, and implementation across tools.

---

## Historical LTV Formula

The simplest LTV calculation uses three components:

```
LTV = Average Order Value (AOV) × Purchase Frequency × Customer Lifespan
```

**Example:**
- AOV: $85
- Purchase Frequency: 3 purchases per year
- Customer Lifespan: 4 years
- LTV = $85 × 3 × 4 = $1,020

**Calculation Details:**

### Average Order Value (AOV)
- Definition: Total revenue ÷ total orders
- Lookback period: Last 12 months (or full customer history if customer age <12 months)
- Exclusions: Discounts applied to orders should NOT be excluded from AOV (AOV reflects net revenue)
- Formula: `SUM(order_value) / COUNT(orders)`

### Purchase Frequency
- Definition: Total orders per customer ÷ customer age in years
- Interpretation: How many times per year does a customer purchase?
- Lookback: Full customer history (or last 12 months for lestablished customers)
- Formula:`COUNT(orders) / (days_since_first_purchase / 365)`
- Example: Customer with 8 orders over 24 months = 4 orders/year frequency

### Customer Lifespan
- Definition: Expected number of years a customer will remain active (continue purchasing)
- Calculation: 1 / annual_churn_rate
- Example: If annual churn is 25%, lifespan = 1 / 0.25 = 4 years
- Alternative: Use median customer tenure (if churn rate is unknown)
- Conservative estimate: Use 3–5 years for established ecommerce brands

**Limitations of Historical LTV:**
- Assumes future behavior matches past (may not account for product launches, market changes, seasonality)
- Sensitive to cohort age (new customers appear lower LTV than mature customers)
- Requires 12+ months of data to be reliable
- Does not account for declining engagement curves (active customers may slow purchases over time)

---

## Predictive LTV Using Cohort Analysis

Cohort analysis enables more sophisticated LTV prediction by grouping customers by acquisition month and analyzing their spending curves over time.

### Cohort Construction Methodology

**Step 1: Define Cohorts**
Group customers by first-purchase month. Example:
- Cohort "Jan 2024": All customers whose first purchase occurred Jan 1–31, 2024
- Cohort "Feb 2024": All customers whose first purchase occurred Feb 1–28, 2024
- Continue for 18–24 months of historical data

**Step 2: Create Revenue Lookback Table**
For each cohort, calculate cumulative revenue at fixed intervals: 30-day, 60-day, 90-day, 180-day, 365-day post-first-purchase.

**Example Cohort Table (Jan 2024):**

| Cohort | Cohort Size | Revenue @ Day 30 | Revenue @ Day 90 | Revenue @ Day 180 | Revenue @ Day 365 | Avg LTV @ 365d |
|---|---|---|---|---|---|---|
| Jan 2024 | 1,200 | $127,500 (avg $106.25/customer) | $318,750 (avg $265.63) | $528,000 (avg $440) | $867,500 (avg $722.92) | $722.92 |
| Feb 2024 | 980 | $104,580 (avg $106.70) | $262,140 (avg $267.49) | $441,200 (avg $450.20) | $701,750 (avg $716.07) | $716.07 |
| Mar 2024 | 1,050 | $113,400 (avg $108.00) | $287,250 (avg $273.57) | $483,750 (avg $460.71) | $801,000 (avg $763.81) | $763.81 |

**Step 3: Validate Monotonic Growth**
Ensure revenue grows consistently across lookback periods. If Day 90 revenue < Day 60 revenue, investigate data quality issues (refunds, returns, data gaps).

**Step 4: Identify Spending Curves**
Analyze the delta between lookback periods to identify decay patterns:

| Cohort | 30–90d Growth | 90–180d Growth | 180–365d Growth | Growth Rate |
|---|---|---|---|---|
| Jan 2024 | +150% ($265.63 vs $106.25) | +66% ($440 vs $265.63) | +64% ($722.92 vs $440) | Decelerating |
| Feb 2024 | +150% | +69% | +59% | Decelerating |
| Mar 2024 | +153% | +69% | +66% | Decelerating |

Key insight: All cohorts show a decelerating growth curve (growth rate slows after Day 90). This is typical for ecommerce.

**Step 5: Project 365+ Day LTV (for newer cohorts)**
If a cohort is <365 days old, you need to project its eventual LTV. Use historical cohort decay rates:

Projection formula:
```
Projected LTV @ 365d = Observed LTV @ 180d × (Avg growth rate 180–365d for mature cohorts)
```

Example: Q1 2025 cohort has $450 LTV @ 180 days. Historical cohorts grow 64% from Day 180 to Day 365.
- Projected 365d LTV = $450 × 1.64 = $738

**Step 6: Calculate Percentile Thresholds**
Once all cohorts have 365-day LTV calculated (or projected), sort by LTV and identify percentile breakpoints:

```
Top 1% LTV Threshold = 99th percentile of all customer LTVs
Top 10% LTV Threshold = 90th percentile of all customer LTVs
Top 20% LTV Threshold = 80th percentile of all customer LTVs
Mid 60% LTV = 20th–80th percentile (between top 20% and bottom 20%)
Bottom 20% LTV = Bottom 20th percentile
```

---

## Category-Specific LTV Benchmarks (90-Day, 180-Day, 365-Day)

These benchmarks are based on SaaS benchmarking reports, Shopify data, and industry surveys. Use these to validate your LTV calculations and set segment targets.

### Fashion & Apparel
| Lookback | LTV | Repeat Rate | AOV | Notes |
|---|---|---|---|---|
| 90-day | $150–$250 | 15–25% | $70–$100 | High volume, lower margins |
| 180-day | $280–$420 | 25–35% | $85–$120 | Seasonality (spring/summer, fall/winter) |
| 365-day | $450–$700 | 35–50% | $90–$130 | Loyalty programs lift retention significantly |

### Beauty & Skincare
| Lookback | LTV | Repeat Rate | AOV | Notes |
|---|---|---|---|---|
| 90-day | $180–$350 | 25–40% | $65–$110 | Subscription-friendly category |
| 180-day | $380–$650 | 40–55% | $80–$140 | Natural repeat cycle (resupply) |
| 365-day | $650–$1,200 | 50–70% | $90–$160 | Highest repeat rates in DTC |

### Home & Furniture
| Lookback | LTV | Repeat Rate | AOV | Notes |
|---|---|---|---|---|
| 90-day | $200–$400 | 8–15% | $150–$300 | Lower frequency, high AOV |
| 180-day | $350–$550 | 12–20% | $200–$350 | Longer purchase cycle |
| 365-day | $500–$900 | 15–28% | $250–$400 | Gift-giving and seasonal spikes |

### Vitamins & Supplements
| Lookback | LTV | Repeat Rate | AOV | Notes |
|---|---|---|---|---|
| 90-day | $120–$200 | 30–50% | $35–$60 | Subscription-dominant; high repeat |
| 180-day | $280–$450 | 50–70% | $40–$75 | Resupply cycle every 30–45 days |
| 365-day | $500–$900 | 60–80% | $45–$85 | Longest repeat lifecycle in DTC |

### Luxury Goods
| Lookback | LTV | Repeat Rate | AOV | Notes |
|---|---|---|---|---|
| 90-day | $500–$1,500 | 10–20% | $300–$800 | Very low frequency; high AOV |
| 180-day | $1,000–$2,500 | 15–28% | $400–$1,000 | Extended consideration cycle |
| 365-day | $1,800–$4,500 | 20–40% | $500–$1,200 | Gift-giving and occasion-based buying |

### Electronics & Tech
| Lookback | LTV | Repeat Rate | AOV | Notes |
|---|---|---|---|---|
| 90-day | $250–$600 | 8–15% | $200–$500 | Low frequency; high AOV; long upgrade cycle |
| 180-day | $450–$900 | 12–22% | $250–$600 | Accessories drive repeat rate |
| 365-day | $700–$1,400 | 15–30% | $300–$700 | Warranty and extended service lift LTV |

**How to Use These Benchmarks:**
1. Calculate your own LTV by cohort (using methodology above)
2. Compare your results to category benchmark
3. If your LTV is 20%+ below benchmark, investigate: weak repeat rate? High AOV but low frequency? Cohort contamination?
4. If above benchmark, validate data quality and document your competitive advantage (loyalty program, better retention playbooks)

---

## Cohort-Based LTV Percentile Thresholds

Once you have calculated LTV for all customers (using historical or cohort-projected methods), identify percentile breakpoints for segmentation. These breakpoints determine segment size and strategy allocation.

### Standard Breakpoints (Ecommerce)

```
Champions        = Top 1% LTV
VIP              = Top 10% LTV (includes Champions)
High-Value       = Top 20% LTV (includes VIP + Champions)
Mid-Tier         = 20th–80th percentile LTV (mid 60%)
Low-Value        = Bottom 20% LTV
```

### Example Threshold Table (Cohorts Jan 2023–Dec 2024, sorted by LTV percentile):

| Percentile | LTV Threshold | Example Count | Revenue Contribution |
|---|---|---|---|---|
| 99th–100th (Top 1%) | $3,500+ | 450 customers | 28% of revenue |
| 90th–99th (9%) | $2,200–$3,500 | 4,050 customers | 22% of revenue |
| 80th–90th (10%) | $1,400–$2,200 | 4,500 customers | 18% of revenue |
| 20th–80th (60%) | $250–$1,400 | 27,000 customers | 28% of revenue |
| Bottom 20% | <$250 | 9,000 customers | 4% of revenue |

**Key Insight:** In most ecommerce businesses, top 20% of customers drive 60–80% of revenue. This justifies concentrated marketing investment in VIP and High-Value segments.

### Validation Rule
If top 20% of customers drive <50% of revenue, or if bottom 20% drives >10% of revenue, re-examine:
- Is your LTV calculation including low-margin or promotional orders that shouldn't be counted?
- Are you including product returns/refunds correctly (should reduce LTV)?
- Is there cohort contamination (new customers mixed with mature)?

---

## Data Requirements & Minimum History Needed

### Minimum Dataset Structure

```
customer_id | first_purchase_date | last_purchase_date | total_orders | total_revenue | product_categories | email | cohort_month
```

### Minimum History Needed by Calculation Method

| Calculation Method | Minimum History | Data Points Per Customer | Lookback Window |
|---|---|---|---|---|
| Historical LTV (simple formula) | 12 months | 1 year of transactions | Last 12 months |
| Cohort-based LTV (mature segments) | 18 months | 18 months of post-purchase data | First-purchase month + 12+ months |
| Cohort-based LTV (projected, newer) | 6 months | 6 months of post-purchase + projection model | 6 months observed + 6 months projected |
| Predictive LTV (ML-based) | 24 months | 24 months of transactions | Full customer history |

**Practical Rule:** Do not segment customers acquired <6 months ago (insufficient data). If building segments, either:
- Exclude customers <6 months old and segment established customers only, OR
- Create separate "New Customer" segment with different playbooks (focus on second-purchase conversion vs. retention)

### Data Quality Checks

Before calculating LTV, validate:

| Check | Rule | Action if Failed |
|---|---|---|
| No duplicate customer IDs | Each customer_id appears once per transaction | Deduplicate; investigate data source |
| No future dates | All purchase_dates ≤ today | Remove; investigate source |
| AOV >$0 | Revenue > $0 per order | Exclude $0 orders (gift cards, returns) |
| Plausible order frequency | No customer has >100 orders per year (typical ecommerce max = 12) | Flag for fraud review; may indicate bot or data error |
| Cohort age validation | first_purchase_date to last_purchase_date should match orders | Recalculate; verify transaction log |
| No extreme outliers | LTV >10x category median should be investigated | Review for fraud, bulk orders, B2B sales |

---

## Tools & Implementation

### Shopify Analytics
**Native Capability:** Shopify's built-in Customer Lifetime Value metric (Shopify Analytics > Customers > LTV)
- Pros: No setup required; updates daily; available in Shopify mobile app
- Cons: Limited customization; cannot adjust lookback window; no percentile thresholds
- Recommendation: Use as validation check; export to CSV for deeper analysis

**Export Method:**
1. Shopify Admin → Analytics → Customers
2. Click "Export" button
3. Download CSV with customer-level LTV

**Limitations:**
- LTV includes all-time revenue (no cohort normalization)
- Does not account for seasonality or product mix changes
- Cannot segment by acquisition channel

### Klaviyo Predictive Analytics
**Native Capability:** Klaviyo's Predictive LTV score (if using Klaviyo Enterprise plan)
- Pros: Integrates with email performance; updates in real-time; enables dynamic segmentation
- Cons: Requires Klaviyo Enterprise; requires 30+ days of behavioral data per customer
- Recommendation: Use for active customer segments; combine with custom cohort analysis for full picture

**Implementation:**
1. Klaviyo Account → Settings → Predictive Analytics
2. Enable "Lifetime Value Predictor"
3. Define monetization events (purchases, subscriptions)
4. Klaviyo calculates predicted LTV for each customer every 24 hours

### Google Sheets / Excel (DIY)
**Method:** Pivot table approach using exported transaction data

**Steps:**
1. Export customer transaction data from Shopify / payment processor
   - Columns: customer_id, purchase_date, order_value
2. Create "Cohort Lookup" table
   - For each customer_id, find first_purchase_date
   - Assign to cohort month (Jan 2024, Feb 2024, etc.)
3. Pivot table: Group by cohort_month, sum revenue @ 30d, 90d, 180d, 365d post-acquisition
4. Calculate percentiles using `PERCENTILE()` function

**Formula Example (Excel):**
```
=PERCENTILE(array_of_ltv_values, 0.90)  [returns 90th percentile LTV]
```

### SQL Query (Custom Database)

**Cohort-Based LTV Calculation:**

```sql
WITH cohorts AS (
  SELECT
    customer_id,
    DATE_TRUNC(MIN(order_date), MONTH) AS cohort_month,
    MIN(order_date) AS first_purchase_date,
    SUM(order_value) AS total_lifetime_revenue,
    COUNT(DISTINCT order_id) AS total_orders
  FROM orders
  GROUP BY customer_id
),
ltv_90d AS (
  SELECT
    c.customer_id,
    c.cohort_month,
    SUM(CASE WHEN DATE_DIFF(o.order_date, c.first_purchase_date, DAY) <= 90 THEN o.order_value ELSE 0 END) AS ltv_90d
  FROM cohorts c
  LEFT JOIN orders o ON c.customer_id = o.customer_id
  GROUP BY c.customer_id, c.cohort_month
),
ltv_365d AS (
  SELECT
    c.customer_id,
    c.cohort_month,
    SUM(CASE WHEN DATE_DIFF(o.order_date, c.first_purchase_date, DAY) <= 365 THEN o.order_value ELSE 0 END) AS ltv_365d
  FROM cohorts c
  LEFT JOIN orders o ON c.customer_id = o.customer_id
  GROUP BY c.customer_id, c.cohort_month
),
final_ltv AS (
  SELECT
    l365.customer_id,
    c.cohort_month,
    l90.ltv_90d,
    l365.ltv_365d,
    PERCENT_RANK() OVER (ORDER BY l365.ltv_365d) AS ltv_percentile
  FROM ltv_365d l365
  JOIN ltv_90d l90 ON l365.customer_id = l90.customer_id
  JOIN cohorts c ON l365.customer_id = c.customer_id
)
SELECT
  customer_id,
  cohort_month,
  ltv_90d,
  ltv_365d,
  CASE
    WHEN ltv_percentile >= 0.99 THEN 'Champions'
    WHEN ltv_percentile >= 0.90 THEN 'VIP'
    WHEN ltv_percentile >= 0.80 THEN 'High-Value'
    WHEN ltv_percentile >= 0.20 THEN 'Mid-Tier'
    ELSE 'Low-Value'
  END AS segment
FROM final_ltv
WHERE DATEDIFF(CURRENT_DATE(), cohort_month) >= 365
ORDER BY ltv_365d DESC;
```

### Iterable / Segment
**Recommended For:** Advanced teams with data infrastructure

**Method:** Use custom attributes and real-time calculation
1. Connect transaction data to Iterable
2. Create custom user attribute "ltv_365d"
3. Update daily via batch import
4. Build segments using LTV attribute
5. Use in dynamic send-time optimization and personalization

---

## Discount & Refund Handling

### Include or Exclude?

| Item | Include in LTV? | Rationale |
|---|---|---|
| Base order value | YES | Core transaction |
| Applied discounts/coupons | Include as net revenue | Reflects actual margin |
| Refunded orders | EXCLUDE | Customer didn't keep product; no long-term value |
| Returns (keep one item, return one) | INCLUDE as net | Account for split refunds |
| Free products (gift with purchase) | EXCLUDE | Zero revenue; separable promotion |
| Shipping | EXCLUDE (standard) | Include only if shipping is a material revenue line |
| Taxes | EXCLUDE | Tax is pass-through to government |

**Formula Adjustment:**
```
LTV = (Revenue – Refunds + [shipping if included]) × (Purchase Frequency) × (Customer Lifespan)
```

**Example:**
- Total revenue (before refunds): $1,000
- Refunds: $200
- Net revenue: $800
- Purchase frequency: 2x/year
- Lifespan: 4 years
- LTV = $800 × 2 × 4 = $6,400

---

## Seasonality Normalization

ecommerce LTV calculations are prone to seasonal distortion. Q4 (holiday) cohorts appear much higher LTV than Q1 (post-holiday) cohorts simply due to high volume, not quality.

### Seasonality Adjustment Method

**Step 1: Identify Seasonal Multiplier by Cohort**

```
Q4 2024 cohort = 1,200 customers acquired, $1,435 avg LTV 365d
Q1 2025 cohort = 650 customers acquired, $485 avg LTV @ day 180 (projected $850)

Seasonal multiplier = Q4 cohort avg / Non-Q4 cohort avg
= $1,435 / $850 = 1.69x (Q4 is 69% higher)
```

**Step 2: Normalize Future Cohorts**
When comparing Q1 2025 cohort to historical average, apply seasonal deflator:
```
Normalized LTV = Observed LTV / Seasonal Multiplier
= $850 / 1.69 = $503 (normalized to non-seasonal baseline)
```

**Step 3: Use Normalized LTV for Segmentation**
If using normalized LTV:
- Ensures segments remain comparable across seasons
- Prevents over-allocation to Q4-acquired customers during Q1 budget planning
- Alternatively, re-segment monthly to account for seasonal shifts (simpler, but requires more frequent updates)

---

## Checklist: Ready to Segment

Before building segment playbooks, validate:

- [ ] LTV calculated using cohort methodology (not point-in-time)
- [ ] Minimum 12 months post-purchase history for all customers in base
- [ ] Customers <6 months old excluded or in separate "New" segment
- [ ] Discounts, refunds, and outliers handled consistently
- [ ] Seasonality documented and accounted for in threshold interpretation
- [ ] Percentile breakpoints validated (top 20% drives 60%+ revenue)
- [ ] Data quality checks passed (no duplicates, no future dates, plausible frequency)
- [ ] Percentile thresholds match your business model (luxury brand may have different distribution than mass-market)
- [ ] Recalculation schedule defined (monthly refresh recommended)
- [ ] Tools selected and tested (Shopify exports, Klaviyo segments, SQL queries, etc.)
