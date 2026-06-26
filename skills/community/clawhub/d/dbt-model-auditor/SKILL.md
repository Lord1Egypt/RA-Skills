---
name: cm-dbt-model-auditor
description: Audit dbt (data build tool) projects for model quality, test coverage, documentation completeness, performance, and adherence to best practices. Checks naming conventions, ref/source usage, materialization strategy, DAG structure, and model contracts. Use when asked to audit a dbt project, review dbt models, check dbt test coverage, validate dbt documentation, assess dbt model performance, check dbt best practices, or review data model quality. Triggers on "dbt audit", "dbt review", "dbt model", "dbt quality", "dbt test coverage", "dbt documentation", "dbt best practices", "dbt lint", "data model audit", "dbt project review", "dbt health check".
metadata:
  tags: ["dbt", "data-engineering", "data-quality", "analytics", "sql", "data-modeling", "testing", "documentation", "data-warehouse"]
---

# dbt Model Auditor

Audit dbt projects for model quality, test coverage, documentation completeness, performance optimization, and adherence to community best practices. Acts as an experienced analytics engineer reviewing your dbt project structure, model design, and configuration.

## Usage

Invoke this skill when you need to assess the health of a dbt project or review specific models.

**Basic invocation:**
> Audit the dbt project in /path/to/dbt/project
> Review dbt model quality in this project
> Check dbt test coverage for our models

**Focused audits:**
> Audit only the staging models
> Check materialization strategy for the marts layer
> Review documentation completeness for customer-facing models
> Find models that violate naming conventions

The agent reads the dbt project files (models, schemas, configs) and produces a comprehensive audit report.

## How It Works

### Step 1: Discover the dbt Project Structure

The agent maps the project layout:

```bash
# Identify the dbt project
cat dbt_project.yml

# Map all model files
find models/ -name "*.sql" | head -50

# Map all schema/YAML files
find models/ -name "*.yml" -o -name "*.yaml" | head -50

# Check for packages
cat packages.yml 2>/dev/null || cat dependencies.yml 2>/dev/null

# Check profiles (for target config)
cat profiles.yml 2>/dev/null
```

The agent identifies:
- **Project name and version** from `dbt_project.yml`
- **Model layers**: staging, intermediate, marts (or custom layer names)
- **Sources**: defined source tables
- **Seeds and snapshots**: static data and SCD configurations
- **Macros**: custom Jinja macros
- **Packages**: installed dbt packages (dbt_utils, codegen, etc.)

### Step 2: Audit Naming Conventions

The agent checks model file names against community best practices:

**Expected naming patterns:**

| Layer | Convention | Example |
|-------|-----------|---------|
| **Staging** | `stg_<source>__<entity>` | `stg_stripe__payments.sql` |
| **Intermediate** | `int_<entity>_<verb>` | `int_payments_pivoted.sql` |
| **Marts** | `<entity>` or `fct_/dim_` | `fct_orders.sql`, `dim_customers.sql` |
| **Sources** | defined in YAML, not SQL | `src_stripe.yml` |

**Checks performed:**

```
PASS: models/staging/stripe/stg_stripe__payments.sql
  Follows stg_<source>__<entity> convention

FAIL: models/staging/payments.sql
  Missing source prefix. Should be: stg_<source>__payments.sql

FAIL: models/marts/core/customer_orders_joined_final_v2.sql
  Unclear naming. Suggest: fct_customer_orders.sql
  Issues: "joined" describes implementation, "final" and "v2" are anti-patterns

WARN: models/staging/stripe/stripe_charges.sql
  Source name repeated without stg_ prefix
```

**Additional naming checks:**
- No spaces or special characters in filenames
- Consistent casing (snake_case required)
- No `_final`, `_v2`, `_backup`, `_old` suffixes
- Source names match between YAML definitions and file paths
- Schema YAML filenames match their directory (`_stripe__models.yml` in `stripe/`)

### Step 3: Validate ref() and source() Usage

The agent ensures proper dependency management:

```bash
# Find models using hardcoded table references instead of ref()
grep -rn "FROM\s\+\`\?[a-z_]\+\.\|JOIN\s\+\`\?[a-z_]\+" models/ \
  --include="*.sql" | grep -v "ref\|source\|this"
```

**Checks performed:**

```
FAIL: models/marts/core/fct_orders.sql:12
  Hardcoded reference: FROM raw.stripe.payments
  Should be: FROM {{ source('stripe', 'payments') }}
  OR: FROM {{ ref('stg_stripe__payments') }}

FAIL: models/marts/core/fct_orders.sql:18
  Cross-layer skip: marts model directly references source
  fct_orders -> source('stripe', 'payments')
  Should go through staging: fct_orders -> ref('stg_stripe__payments')

PASS: models/staging/stripe/stg_stripe__payments.sql
  Correctly uses {{ source('stripe', 'payments') }}
```

**DAG structure validation:**
- Staging models should reference only `source()`
- Intermediate models should reference `ref()` to staging or other intermediate models
- Marts models should reference `ref()` to intermediate or staging models
- No circular dependencies
- No excessively deep chains (> 8 levels suggests over-engineering)
- No "orphan" models (models not referenced by any other model or exposure)

### Step 4: Assess Test Coverage

The agent evaluates testing completeness:

```bash
# Parse schema YAML files for test definitions
cat models/staging/stripe/_stripe__models.yml
```

**Test coverage analysis:**

```
Model: stg_stripe__payments
  Columns defined in YAML: 8
  Columns with tests: 3 (37.5%)
  Tests:
    - payment_id: unique, not_null [GOOD: primary key tested]
    - status: accepted_values [GOOD: enum validated]
    - amount: not_null [GOOD]
  Missing tests:
    - payment_id: no relationships test to orders [WARN]
    - created_at: no not_null, no recency test [WARN]
    - customer_id: no relationships test [FAIL — FK should be tested]
    - currency: no accepted_values test [WARN]
    - payment_method: no accepted_values test [WARN]

Test Coverage Summary:
  Total models: 47
  Models with any tests: 31 (66%)
  Models with primary key tests: 28 (60%)
  Models with relationship tests: 12 (26%) <-- LOW
  Models with zero tests: 16 (34%) <-- CRITICAL
```

**Required tests per model (recommended minimum):**

| Test Type | When Required | Priority |
|-----------|---------------|----------|
| `unique` + `not_null` on PK | Every model | Critical |
| `not_null` on important columns | Columns used in joins/filters | High |
| `relationships` (FK) | Every foreign key | High |
| `accepted_values` | Enum/status columns | Medium |
| Custom data quality tests | Business-critical models | Medium |
| Recency test | Source freshness | Medium |

**Source freshness checks:**

```
WARN: Source 'stripe.payments' has no freshness configuration
  Recommend adding:
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
```

### Step 5: Check Documentation Completeness

The agent verifies that models and columns are documented:

```
Documentation Coverage:
  Models with description: 29/47 (62%)
  Columns with description: 112/380 (29%) <-- LOW

Undocumented models (most critical first):
  1. fct_revenue — marts model, likely consumed by stakeholders
  2. dim_customers — marts model, core entity
  3. int_orders_enriched — intermediate, complex transformations
  ...

Undocumented columns in documented models:
  1. fct_orders.discount_amount — What discounts? Pre/post tax?
  2. dim_customers.segment — How is segment determined?
  3. fct_revenue.mrr — What's included in MRR calculation?
```

**Documentation quality checks:**
- Model-level descriptions present and meaningful (not just the model name restated)
- Column descriptions explain business meaning, not just data type
- Sources have descriptions
- Exposures defined for downstream consumers (dashboards, reverse ETL)
- Meta fields used consistently for ownership and classification

### Step 6: Evaluate Materialization Strategy

The agent reviews how each model is materialized:

```
Materialization Analysis:
  views: 28 models
  tables: 15 models
  incremental: 3 models
  ephemeral: 1 model

Recommendations:
  WARN: fct_orders (materialized as view, 2.4M rows)
    Query time as view: ~8s
    Recommend: table or incremental
    Reason: Large row count, queried frequently by BI tools

  WARN: stg_stripe__events (materialized as table, 200 rows)
    Recommend: view
    Reason: Small table, no performance benefit from materialization

  WARN: int_payments_pivoted (materialized as table, rebuilt daily)
    Recommend: incremental
    Reason: Source is append-only, full rebuild wastes compute
    Suggest: Add incremental config with unique_key and strategy

  OK: dim_customers (materialized as table, 50K rows)
    Appropriate materialization for a dimension table
```

**Incremental model review:**

For existing incremental models, the agent checks:
- `unique_key` is defined (prevents duplicates)
- `incremental_strategy` is appropriate (merge vs. delete+insert vs. append)
- `is_incremental()` block filters correctly
- Late-arriving data handling (lookback window)
- Full refresh fallback works (`--full-refresh`)

### Step 7: Analyze SQL Quality

The agent reads each model's SQL and checks for common issues:

**Anti-patterns detected:**

```
FAIL: models/marts/fct_orders.sql
  Line 15: SELECT * — always specify columns explicitly
  Line 23: UNION instead of UNION ALL — unnecessary dedup overhead
  Line 31: WHERE date_trunc('day', created_at) = '2026-01-01'
           Function on column prevents index use
           Rewrite: WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'

WARN: models/staging/stg_shopify__orders.sql
  Line 8: Casting in SELECT but no column alias
           CAST(order_date AS DATE) should be aliased: CAST(order_date AS DATE) AS order_date

WARN: models/intermediate/int_events_sessionized.sql
  Line 45: Complex window function without comments
           Add a comment explaining the sessionization logic

FAIL: models/marts/dim_products.sql
  Line 12: COALESCE(p.name, 'Unknown') — magic string
           Use a variable or macro for default values
```

**Complexity analysis:**
- Lines of SQL per model (flag models > 200 lines as candidates for splitting)
- Number of CTEs (> 6 may indicate a model doing too much)
- Number of JOINs (> 5 may need intermediate models)
- Subquery depth (> 2 levels should be refactored to CTEs)
- Window function complexity

### Step 8: Review Model Contracts and Governance

For dbt 1.5+ projects, the agent checks model contracts:

```yaml
# Expected for critical marts models:
models:
  - name: fct_orders
    config:
      contract:
        enforced: true
    columns:
      - name: order_id
        data_type: integer
        constraints:
          - type: not_null
          - type: primary_key
```

**Governance checks:**
- Model access levels (public vs. protected vs. private)
- Group assignments for ownership
- Version definitions for breaking change management
- Meta tags for PII classification
- Exposure definitions for downstream dependency tracking

### Step 9: Performance Analysis

The agent checks for performance-related configuration:

```
Performance Findings:
  1. No cluster keys defined for large incremental models on Snowflake
     Recommend: cluster_by for fct_events (partitioned by event_date)

  2. No pre/post hooks for table statistics on Redshift
     Recommend: post_hook = "ANALYZE {{ this }}"

  3. Parallel thread count in profiles.yml: 1
     Recommend: Increase threads to 4-8 for faster builds

  4. Model fct_revenue depends on 12 upstream models
     Critical path analysis: build time bottleneck is int_payments (45s)
     Recommend: Optimize int_payments or materialize as incremental
```

### Step 10: Produce the Audit Report

The agent generates a comprehensive report:

```
# dbt Project Audit Report
# Project: analytics | Date: April 30, 2026

## Overall Health Score: 62/100

## Summary
  Models: 47 | Sources: 8 | Tests: 94 | Macros: 12
  
  Category Scores:
    Naming Conventions:     7/10  (3 violations)
    ref/source Usage:       8/10  (2 hardcoded refs)
    Test Coverage:          5/10  (34% models untested)
    Documentation:          4/10  (29% columns documented)
    Materialization:        7/10  (3 suboptimal choices)
    SQL Quality:            6/10  (5 anti-patterns)
    Governance:             5/10  (no contracts, no access control)
    Performance:            6/10  (incremental opportunities missed)

## Critical Issues (Fix Immediately)
  1. 16 models have zero tests — data quality blind spots
  2. 2 models use hardcoded table references — broken lineage
  3. fct_revenue has no documentation — business-critical model

## High Priority (Fix This Sprint)
  4. 3 models should be incremental (saving ~$X/month compute)
  5. Primary key tests missing on 19 models
  6. Foreign key tests missing on 35 relationships
  7. 5 SQL anti-patterns (SELECT *, UNION without ALL)

## Medium Priority (Fix This Quarter)
  8. Add model contracts to marts layer
  9. Define exposures for BI dashboards
  10. Add source freshness checks for all 8 sources
  11. Document remaining 268 columns
  12. Split 3 models exceeding 200 lines

## Low Priority (Best Practices)
  13. Standardize macro naming
  14. Add meta tags for PII classification
  15. Configure model groups for team ownership
```

## Output

The agent produces:

- **Health score**: 0-100 overall project health rating
- **Category breakdown**: scores for naming, testing, docs, performance, governance, SQL quality, DAG structure, and materialization
- **Critical issues**: problems that could cause data quality failures or broken pipelines
- **Prioritized recommendations**: ordered by impact and effort
- **Per-model details**: specific findings for each model that has issues
- **Remediation examples**: exact YAML and SQL to fix each issue

## Audit Scope Options

| Scope | What It Covers |
|-------|---------------|
| **Full** (default) | All models, all checks |
| **Layer** | Single layer (staging, intermediate, marts) |
| **Model** | Single model deep-dive with all checks |
| **Category** | Single category across all models (e.g., only test coverage) |
| **Changed** | Only models changed in current branch (git diff) |

## Tips for Best Results

- Run from the dbt project root directory so the agent can find all files
- Ensure `dbt_project.yml` is present and valid
- For the most useful audit, include schema YAML files with column definitions
- The agent works with dbt Core, dbt Cloud, and all adapters (Snowflake, BigQuery, Redshift, Postgres, Databricks)
- Provide your `profiles.yml` target info if you want adapter-specific recommendations
- For incremental analysis over time, run audits regularly and compare scores
