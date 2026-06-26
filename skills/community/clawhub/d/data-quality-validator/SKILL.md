---
name: cm-data-quality-validator
description: Validate data quality in pipelines by checking completeness, consistency, freshness, accuracy, and distribution anomalies. Define expectations, profile data distributions, detect schema drift, identify outliers, and generate quality reports. Use when asked to validate data quality, audit pipeline data, check data completeness, detect data anomalies, profile datasets, review data freshness, or set up data quality checks. Triggers on "data quality", "data validation", "data completeness", "data freshness", "data profiling", "data anomaly", "data consistency", "data expectations", "pipeline quality", "great expectations", "data audit", "schema drift".
metadata:
  tags: ["data-quality", "data-engineering", "pipeline", "validation", "profiling", "anomaly-detection", "data-governance", "completeness", "consistency", "freshness"]
---

# Data Quality Validator

Validate data quality across pipelines by defining expectations, profiling distributions, detecting anomalies, and generating quality reports. Reviews data completeness, consistency, freshness, accuracy, uniqueness, and schema conformance. Acts as a senior data quality engineer auditing your pipeline data for trustworthiness.

## Usage

Invoke this skill when you need to validate data quality, define quality expectations, detect anomalies, or audit pipeline data.

**Basic invocation:**
> Validate data quality for the orders pipeline
> Set up data quality checks for /path/to/data/
> Audit this dataset for completeness and consistency

**Focused analysis:**
> Check data freshness across all pipeline outputs
> Profile distributions for anomaly detection
> Detect schema drift between pipeline runs
> Generate a data quality scorecard for stakeholders

The agent reads data source definitions, pipeline code, schema files, and sample data, then produces a comprehensive data quality assessment with actionable expectations.

## How It Works

### Step 1: Discover and Profile Data Sources

The agent locates data sources and produces initial profiles:

```bash
# Find data pipeline definitions
find /path/to/pipelines/ -name "*.py" -o -name "*.sql" -o -name "*.yaml" | head -50

# Find schema definitions
grep -rl "CREATE TABLE\|schema\|DataFrame\|Column(" /path/to/src/ --include="*.py" --include="*.sql"

# Find data files
find /path/to/data/ -name "*.csv" -o -name "*.parquet" -o -name "*.json" | head -30

# Check for existing quality frameworks
grep -rl "great_expectations\|dbt_expectations\|soda\|pandera\|pydantic" /path/to/src/ --include="*.py" --include="*.yaml"
```

The agent profiles each data source:

```
Data Source Profile: orders_daily

  Source: PostgreSQL (analytics.orders)
  Format: Table (partitioned by order_date)
  Records: 2.4M (latest partition: 12,847)
  Columns: 18
  Last updated: 2026-04-30 06:15:00 UTC
  Update frequency: Daily (expected by 07:00 UTC)

  Column Profile:
    order_id        INT       NOT NULL  unique=100%   nulls=0%
    customer_id     INT       NOT NULL  unique=8.2%   nulls=0%
    order_date      DATE      NOT NULL  unique=0.1%   nulls=0%
    total_amount    DECIMAL   NOT NULL  min=0.01      max=99999.99  mean=127.43  stddev=284.91
    status          VARCHAR   NOT NULL  distinct=5    top: completed(72%), pending(15%), cancelled(8%)
    email           VARCHAR   NULLABLE  unique=91.2%  nulls=2.3%
    country_code    CHAR(2)   NOT NULL  distinct=47   top: US(42%), GB(18%), DE(12%)
    created_at      TIMESTAMP NOT NULL  min=2024-01-01 max=2026-04-30
    shipping_cost   DECIMAL   NULLABLE  min=0         max=299.99    nulls=12%
    discount_code   VARCHAR   NULLABLE  distinct=234  nulls=68%
    ...
```

### Step 2: Define Completeness Expectations

The agent checks for missing data and coverage:

```
Completeness Analysis: orders_daily

  Column-Level Completeness:
    PASS: order_id       — 0% null (expected: 0%)
    PASS: customer_id    — 0% null (expected: 0%)
    PASS: order_date     — 0% null (expected: 0%)
    PASS: total_amount   — 0% null (expected: 0%)
    PASS: status         — 0% null (expected: 0%)
    FAIL: email          — 2.3% null (expected: < 1%)
      Trend: Was 0.8% last month, increased to 2.3% this month
      INVESTIGATE: New checkout flow may not require email
      IMPACT: Email marketing campaigns miss 2.3% of customers
    PASS: country_code   — 0% null (expected: 0%)
    WARN: shipping_cost  — 12% null (expected: < 5%)
      May be valid for digital products — verify business rule
    PASS: discount_code  — 68% null (expected: high null rate for optional field)

  Row-Level Completeness:
    FAIL: Expected 12,000-15,000 rows for April 30 partition
      Actual: 8,247 rows
      RISK: 35% fewer records than expected — possible ingestion failure
      Previous 7 days: 12,100 | 13,400 | 11,900 | 12,800 | 14,200 | 12,600 | 13,100
      Today is a statistical outlier (> 3 stddev below mean)
      INVESTIGATE: Check source system for extraction errors

  Temporal Completeness:
    PASS: No gaps in order_date sequence (2024-01-01 to 2026-04-30)
    FAIL: Missing data for 2026-03-15 (0 rows)
      Known issue? If not: check pipeline logs for March 15 run
    WARN: Weekend volumes 30% lower — expected business pattern (verified)

  Entity Completeness:
    PASS: All 47 countries represented in latest partition
    FAIL: Country "JP" missing from last 3 days
      Was present before (avg 150 orders/day from JP)
      INVESTIGATE: Possible regional payment gateway issue
```

### Step 3: Validate Consistency Rules

The agent checks cross-field and cross-source consistency:

```
Consistency Analysis: orders_daily

  Intra-Record Consistency:
    FAIL: 847 orders where total_amount = 0 but status = "completed"
      Business rule: Completed orders must have total > 0
      Expectation: total_amount > 0 WHEN status IN ("completed", "shipped")
      IMPACT: Revenue reporting understated by ~$107K (estimated)
      SQL: SELECT * FROM orders WHERE total_amount = 0 AND status = 'completed'

    FAIL: 23 orders where shipping_cost > total_amount
      Shipping exceeds order value — likely data entry or calculation error
      Expectation: shipping_cost <= total_amount * 0.5
      INVESTIGATE: Check order IDs: 892341, 892355, 892412, ...

    WARN: 156 orders where created_at > updated_at
      Temporal paradox — update timestamp before creation
      Likely: Timezone mismatch between source systems
      FIX: Normalize all timestamps to UTC before comparison

    PASS: All status values are in allowed set
      {"pending", "processing", "completed", "cancelled", "refunded"}

  Cross-Source Consistency:
    FAIL: Customer count mismatch between orders and CRM
      Orders source: 198,423 distinct customer_ids
      CRM source: 195,100 customer records
      Delta: 3,323 customers in orders but not in CRM
      INVESTIGATE: Orphaned customer references — possible sync lag

    FAIL: Revenue total mismatch between orders and payments
      Orders SUM(total_amount): $15,847,234.56
      Payments SUM(amount): $15,612,891.23
      Delta: $234,343.33 (1.5% discrepancy)
      Expectation: Delta < 0.1% between sources
      INVESTIGATE: Partial payments, refunds not reflected, or timing differences

    PASS: Product catalog IDs in orders all exist in products table
    PASS: Country codes conform to ISO 3166-1 alpha-2
```

### Step 4: Check Data Freshness

The agent validates timeliness of data:

```
Freshness Analysis:

  Pipeline: orders_daily
    SLA: Data available by 07:00 UTC daily
    Last update: 2026-04-30 06:15:00 UTC
    PASS: Within SLA (45 minutes early)

  Pipeline: inventory_sync
    SLA: Real-time (< 5 minute lag)
    Last update: 2026-04-30 04:23:00 UTC
    FAIL: Data is 2 hours stale
      Expected: Updated every 5 minutes
      Last successful run: 04:23 UTC
      INVESTIGATE: Check sync process health
      IMPACT: Inventory decisions based on 2-hour-old data
      RISK: Overselling on high-demand products

  Pipeline: customer_360
    SLA: Updated by 08:00 UTC daily
    Last update: 2026-04-28 07:45:00 UTC
    FAIL: Data is 2 days stale
      Missed runs on April 29 and April 30
      INVESTIGATE: Pipeline failure — check orchestrator logs
      IMPACT: Customer segmentation using outdated attributes

  Pipeline: analytics_events
    SLA: Near real-time (< 15 minute lag)
    Partition freshness check:
      2026-04-30T06:00 — 12,403 events (PASS)
      2026-04-30T06:15 — 11,892 events (PASS)
      2026-04-30T06:30 — 0 events (FAIL — missing partition)
      2026-04-30T06:45 — 0 events (FAIL — missing partition)
    ALERT: Event pipeline stopped producing after 06:15
    INVESTIGATE: Kafka consumer lag or ingestion failure

  Freshness Summary:
    Sources within SLA: 2/5
    Sources stale: 2/5
    Sources critically stale: 1/5 (customer_360 — 2 days)
```

### Step 5: Detect Schema Drift

The agent compares current schema against baseline:

```
Schema Drift Analysis:

  Dataset: orders_daily
  Baseline: 2026-04-01 schema snapshot
  Current: 2026-04-30

  FAIL: Column added without documentation
    New column: "referral_source" (VARCHAR, nullable)
    Added between April 15-16 (first appeared in April 16 partition)
    Not in data dictionary or pipeline documentation
    IMPACT: Downstream consumers unaware — may ignore this data
    ACTION: Update data dictionary, notify downstream teams

  FAIL: Column type changed
    Column "discount_percentage" was INTEGER, now FLOAT
    Changed between April 20-21
    RISK: Downstream pipelines expecting integer may truncate or error
    IMPACT: Reports may show incorrect discount values
    ACTION: Notify all consumers, update transformation logic

  WARN: Column semantics changed (detected via distribution shift)
    Column "category" — new value "electronics_refurbished" appeared
    Previous distinct values: 12, current: 13
    Not a schema change but a semantic expansion
    ACTION: Update downstream CASE statements and enum validations

  PASS: No columns removed
  PASS: No column renames detected
  PASS: Primary key structure unchanged

  Schema Compatibility Score: BACKWARD COMPATIBLE
    All changes are additive — old consumers still work
    But: type change on discount_percentage may break strict parsers
```

### Step 6: Profile Distributions and Detect Anomalies

The agent uses statistical profiling to find data anomalies:

```
Distribution Analysis: orders_daily

  Numeric Columns:

    total_amount:
      Current mean: $127.43 | Historical mean: $134.89
      Current median: $62.50 | Historical median: $68.20
      WARN: Mean dropped 5.5% vs. 30-day average
        Possible causes: Promotion driving lower AOV, mix shift, or data issue
        CHECK: Is there an active sale/promotion?
        If no promotion: INVESTIGATE data pipeline for missing high-value orders

    quantity:
      FAIL: Max value = 99,999 (historical max = 50)
        Single order with quantity 99,999 — likely test data or input error
        Expectation: quantity BETWEEN 1 AND 100
        ACTION: Flag record for manual review, add validation rule

    shipping_cost:
      FAIL: Negative values detected (3 records)
        shipping_cost should never be negative
        Expectation: shipping_cost >= 0
        Values found: -12.50, -8.99, -15.00
        INVESTIGATE: Refund adjustments leaking into shipping field?

  Categorical Columns:

    status:
      Current distribution vs. 30-day average:
        completed:  72% (avg: 74%)  — OK
        pending:    15% (avg: 12%)  — WARN: 25% increase in pending rate
        cancelled:   8% (avg:  8%)  — OK
        refunded:    3% (avg:  4%)  — OK
        processing:  2% (avg:  2%)  — OK

      WARN: Pending rate spike from 12% to 15%
        Possible causes: Payment gateway issues, fulfillment backlog
        INVESTIGATE: Check payment success rates for correlation

    country_code:
      FAIL: New value "XX" appeared (14 records)
        "XX" is not a valid ISO 3166-1 code
        Expectation: country_code IN (valid ISO codes)
        INVESTIGATE: Source system validation failure

  Temporal Patterns:

    FAIL: Hourly distribution anomaly
      Orders between 03:00-04:00 UTC: 2,340 (normal: ~500)
      4.7x spike — possible bot activity or bulk import
      INVESTIGATE: Check IP diversity, user-agent patterns
      If legitimate: Update baseline expectations

    PASS: Day-of-week pattern matches historical (Mon-Sun cycle)
    PASS: Month-over-month growth within expected range (2-5%)
```

### Step 7: Validate Uniqueness and Referential Integrity

The agent checks for duplicates and broken references:

```
Uniqueness Analysis:

  FAIL: Duplicate records detected
    Table: orders_daily
    Duplicate key: order_id
    Duplicates found: 47 records (23 unique order_ids appearing twice)
    RISK: Revenue double-counted, inventory miscalculated
    Root cause: Pipeline ran twice on April 28 without idempotency check
    FIX: Add deduplication step:
      ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ingestion_ts DESC) = 1
    PREVENT: Add unique constraint or upsert logic in pipeline

  WARN: Near-duplicates detected
    12 order pairs with same (customer_id, total_amount, order_date)
    but different order_ids
    May be legitimate (same customer, same day, same amount)
    OR: Duplicate submission due to double-click
    ACTION: Flag for business review

  Referential Integrity:

    FAIL: 234 orders reference non-existent product_ids
      product_id values not found in products table
      Likely: Products deleted after orders were placed
      FIX: Use soft delete for products, or archive with foreign key intact
      IMPACT: Product-level analytics incomplete for these orders

    PASS: All customer_ids in orders exist in customers table
    PASS: All category_ids in products exist in categories table

    WARN: 1,456 customers in customers table with zero orders
      Expected some (new signups), but 1,456 is 3x normal
      INVESTIGATE: Are these bot registrations or abandoned signups?
```

### Step 8: Generate Quality Expectations Code

The agent produces implementable quality checks:

```python
# Generated Data Quality Expectations
# Framework: Great Expectations / Pandera / SQL assertions

# === Completeness Expectations ===

def expect_completeness(df):
    """Validate column completeness meets thresholds."""
    expectations = {
        "order_id": {"max_null_pct": 0.0},
        "customer_id": {"max_null_pct": 0.0},
        "email": {"max_null_pct": 1.0},  # Allow up to 1% null
        "total_amount": {"max_null_pct": 0.0},
        "status": {"max_null_pct": 0.0},
        "shipping_cost": {"max_null_pct": 15.0},  # Digital products
    }
    results = []
    for col, rules in expectations.items():
        null_pct = df[col].isnull().sum() / len(df) * 100
        passed = null_pct <= rules["max_null_pct"]
        results.append({
            "check": f"completeness_{col}",
            "passed": passed,
            "actual": f"{null_pct:.2f}%",
            "threshold": f"{rules['max_null_pct']}%",
        })
    return results


# === Consistency Expectations ===

def expect_consistency(df):
    """Validate cross-field business rules."""
    checks = []
    # Completed orders must have positive amount
    mask = (df["status"] == "completed") & (df["total_amount"] <= 0)
    checks.append({
        "check": "completed_orders_positive_amount",
        "passed": mask.sum() == 0,
        "violations": int(mask.sum()),
    })
    # Shipping cost should not exceed order total
    mask = df["shipping_cost"] > df["total_amount"] * 0.5
    checks.append({
        "check": "shipping_cost_reasonable",
        "passed": mask.sum() == 0,
        "violations": int(mask.sum()),
    })
    return checks


# === Volume Expectations ===

def expect_volume(df, date):
    """Validate record count within expected range."""
    row_count = len(df)
    weekday = date.weekday()
    if weekday < 5:  # Weekday
        expected_min, expected_max = 10000, 16000
    else:  # Weekend
        expected_min, expected_max = 7000, 12000
    return {
        "check": "row_count_in_range",
        "passed": expected_min <= row_count <= expected_max,
        "actual": row_count,
        "expected_range": f"{expected_min}-{expected_max}",
    }


# === Distribution Expectations ===

def expect_distribution(df, baseline_stats):
    """Detect statistical anomalies vs. baseline."""
    checks = []
    for col in ["total_amount", "quantity", "shipping_cost"]:
        current_mean = df[col].mean()
        baseline_mean = baseline_stats[col]["mean"]
        baseline_std = baseline_stats[col]["std"]
        z_score = abs(current_mean - baseline_mean) / baseline_std
        checks.append({
            "check": f"distribution_{col}_mean",
            "passed": z_score < 3.0,  # 3-sigma threshold
            "z_score": round(z_score, 2),
            "current_mean": round(current_mean, 2),
            "baseline_mean": round(baseline_mean, 2),
        })
    return checks
```

### Step 9: Define Monitoring and Alerting Rules

The agent produces monitoring configuration:

```
Data Quality Monitoring Rules:

  Rule 1: Freshness Alert (CRITICAL)
    Check: Last update timestamp < SLA threshold
    Frequency: Every 15 minutes
    Alert if: orders_daily not updated by 07:30 UTC
    Channel: PagerDuty (on-call data engineer)
    Auto-escalate: After 30 minutes with no acknowledgment

  Rule 2: Volume Anomaly (HIGH)
    Check: Row count outside 3-sigma historical range
    Frequency: After each pipeline run
    Alert if: |current_count - mean| > 3 * stddev
    Channel: Slack #data-quality
    Include: Current count, expected range, last 7 days trend

  Rule 3: Null Rate Spike (MEDIUM)
    Check: Column null rate exceeds threshold
    Frequency: After each pipeline run
    Alert if: Any column null rate > 2x baseline
    Channel: Slack #data-quality
    Include: Column name, current rate, baseline rate

  Rule 4: Duplicate Detection (CRITICAL)
    Check: Primary key uniqueness
    Frequency: After each pipeline run
    Alert if: Any duplicate primary keys detected
    Channel: PagerDuty + Slack
    Include: Duplicate count, sample duplicate IDs

  Rule 5: Schema Drift (HIGH)
    Check: Column count, types, and names vs. baseline
    Frequency: After each pipeline run
    Alert if: Any schema change detected
    Channel: Slack #data-platform
    Include: Diff of schema changes, compatibility assessment

  Rule 6: Distribution Shift (MEDIUM)
    Check: Statistical distribution vs. 30-day baseline
    Frequency: Daily
    Alert if: Z-score > 3 on any numeric column mean
    Channel: Slack #data-quality
    Include: Column, z-score, current vs. baseline stats
```

### Step 10: Produce the Analysis Report

The agent generates a comprehensive report:

```
# Data Quality Report
# Pipeline: orders_daily | Date: April 30, 2026

## Overview
  Records analyzed: 12,847
  Columns: 18
  Quality checks run: 47
  Checks passed: 31/47 (66%)
  Checks warned: 8/47 (17%)
  Checks failed: 8/47 (17%)

## Overall Quality Score: 64/100

## Dimension Scores
  Completeness:    6/10  (email null rate spike, missing Japan data)
  Consistency:     5/10  (zero-amount completed orders, cross-source delta)
  Freshness:       7/10  (2 pipelines stale, 1 critically stale)
  Accuracy:        5/10  (quantity outlier, negative shipping, invalid country)
  Uniqueness:      6/10  (47 duplicate records from double-run)
  Schema Stability: 7/10  (new column undocumented, type change)
  Distribution:     6/10  (pending rate spike, mean AOV drop)

## Critical Issues
  1. 47 duplicate order records — revenue double-counted ($5,983)
  2. inventory_sync pipeline stale by 2 hours — overselling risk
  3. customer_360 pipeline failed for 2 days — stale segmentation
  4. 847 completed orders with $0 total — $107K revenue gap
  5. Quantity value 99,999 — test/bad data in production

## Data Quality Trend (Last 7 Days)
  Apr 24: 78/100
  Apr 25: 81/100
  Apr 26: 79/100
  Apr 27: 75/100
  Apr 28: 68/100  <-- duplicate ingestion incident
  Apr 29: 66/100  <-- customer_360 pipeline failure
  Apr 30: 64/100  <-- inventory_sync stale + ongoing issues
  TREND: Declining — 3 consecutive days below baseline (75)

## Recommendations Summary
  Estimated effort: 3-5 days for critical + high priority fixes
  Expected improvement: 64 -> 85 quality score
  Quick wins: Dedup pipeline (1 day), fix freshness alerts (0.5 day)
```

## Output

The agent produces:

- **Quality score**: 0-100 overall data quality rating across all dimensions
- **Dimension scores**: completeness, consistency, freshness, accuracy, uniqueness, schema stability
- **Critical issues**: problems that affect business decisions or downstream consumers
- **Data profiles**: statistical summaries of each column with anomaly flags
- **Expectation definitions**: implementable quality check code (Python/SQL)
- **Schema drift report**: changes between current and baseline schema
- **Freshness dashboard**: SLA compliance for each pipeline
- **Distribution analysis**: statistical anomalies with z-scores
- **Monitoring rules**: alerting configuration for continuous quality monitoring
- **Trend analysis**: quality score over time with incident correlation

## Scope Options

| Scope | What It Covers |
|-------|---------------|
| **Full** (default) | All dimensions across all data sources |
| **Single source** | Deep quality analysis of one dataset |
| **Freshness** | Timeliness audit across all pipelines |
| **Completeness** | Null analysis and missing data detection |
| **Anomaly** | Distribution profiling and outlier detection |
| **Schema** | Schema drift detection between runs |
| **Cross-source** | Consistency between multiple data sources |

## Framework Integration

The agent generates expectations compatible with popular frameworks:

| Framework | Output Format |
|-----------|--------------|
| Great Expectations | Expectation suite JSON |
| dbt (dbt-expectations) | schema.yml tests |
| Soda | SodaCL checks YAML |
| Pandera | Python schema definitions |
| Monte Carlo | Monitor definitions |
| Raw SQL | CHECK constraints and assertion queries |
| Custom Python | pytest-style validation functions |

## Tips for Best Results

- Provide access to both current data and historical baselines (30+ days)
- Include pipeline orchestration configs for freshness SLA verification
- Share data dictionaries so the agent knows business rules for consistency checks
- Point the agent at downstream consumer queries to understand impact of quality issues
- Run after pipeline changes to catch regressions before stakeholders notice
- For initial setup, run in profile-only mode to establish baselines before defining thresholds
- Combine with pipeline monitoring to correlate quality drops with infrastructure events
