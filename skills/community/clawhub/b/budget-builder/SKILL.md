---
name: budget-builder
description: >
  Dual-mode budget pipeline for FP&A-quality budget management. Mode A (--build) generates an
  annual budget from 12 months of QBO history with auto-detected seasonal patterns, configurable
  growth assumptions, and manual overrides. Mode B (--compare, default) pulls YTD actuals from
  QBO, compares against the saved budget, flags material variances, generates management commentary
  stubs, builds a rolling forecast, and tracks budget accuracy over time via CDC.
  Outputs professional Excel workbooks with 4 tabs (Build) or 6 tabs (Compare).
  Use when: building the annual operating plan, running monthly BvA close, generating board-ready
  variance reports, or tracking which categories consistently miss budget.
  NOT for: multi-entity consolidations, tax preparation, real-time bookkeeping, or ad-hoc P&L
  analysis without a budget baseline (use pl-deep-analysis instead).
version: 1.0.0
tags:
  - finance
  - accounting
  - budgeting
  - FP&A
  - variance
  - management-reporting
  - forecasting
---

# Budget Builder + Budget vs Actual

## Overview

This pipeline handles the full FP&A budget cycle for QBO-connected clients:
1. **Build** an annual budget from QBO history with seasonal patterns + growth assumptions
2. **Compare** YTD actuals vs. budget with material flags, commentary, and rolling forecast

Both modes output Excel workbooks in a standard suite format (Calibri, dark header, F/U coloring, CDC log).

---

## Script Location

```
scripts/pipelines/budget-builder.py
```

## Cache Locations (auto-created)

```
.cache/budget-builder/{slug}_budget_{year}.json   # Budget file for Mode B
.cache/budget-builder/{slug}_cdc.json             # CDC accuracy tracker
```

---

## Mode A: Budget Builder (--build)

### What It Does

1. Pulls 12 months of monthly P&L from QBO (trailing from today's last completed month)
2. Discovers all accounts and their section types (income / cogs / expense)
3. Loads growth assumptions (global + per-account overrides from JSON)
4. Auto-detects seasonal patterns for each account (strength ≥ 1.30 = seasonal)
5. Generates monthly budget: `base_monthly_avg × seasonal_index × growth_factor`
6. Applies manual dollar overrides from CSV (full precedence over calculated amounts)
7. Saves budget to JSON cache + produces Excel workbook

### Excel Output (4 tabs)

| Tab | Contents |
|---|---|
| Budget Summary | Annual KPI totals + monthly Revenue/EBITDA grid |
| Monthly Detail | All line items × 12 months + Annual total |
| Assumptions | Growth method, rate, base avg, annual budget per account |
| Seasonal Patterns | Monthly indices, strength, peak/trough months per account |

### Usage

```bash
# Basic — use default growth rates (revenue +5%, COGS +3%, expenses +3%)
python3 budget-builder.py --slug <client-slug> --build --year 2026

# Custom growth assumptions
python3 budget-builder.py --slug <client-slug> --build --year 2026 --assumptions growth.json

# With manual overrides for specific accounts
python3 budget-builder.py --slug <client-slug> --build --year 2026 --overrides overrides.csv

# Custom output directory
python3 budget-builder.py --slug <client-slug> --build --year 2026 --out ~/Desktop/reports
```

### Assumptions JSON Format

```json
{
  "global": {
    "income":  0.08,
    "cogs":    0.04,
    "expense": 0.03
  },
  "overrides": {
    "Rent": {"method": "flat"},
    "Software Subscriptions": {"method": "pct_growth", "rate": 0.12},
    "Total Income": {"method": "pct_growth", "rate": 0.08}
  }
}
```

**Methods:**
- `pct_growth` (default) — apply percentage growth rate to trailing average
- `flat` — no growth from trailing average (rate = 0)

### Overrides CSV Format (--overrides)

For hard-coded monthly amounts that override the calculated budget:

```csv
account,section_type,2026-01,2026-02,2026-03,...,2026-12
Rent,expense,3500,3500,3500,...,3500
Owner's Draw,expense,8000,8000,8000,...,8000
```

Columns: `account` + `section_type` + one column per YYYY-MM (or Jan/Feb/Mar shorthand).

---

## Mode B: Budget vs Actual (--compare, default)

### What It Does

1. Loads saved budget (JSON cache or supplied file)
2. Pulls YTD actuals from QBO P&L (Jan 1 → end of last completed month)
3. Also pulls each month individually for per-month variance detail
4. Computes: $ delta, % delta, Favorable/Unfavorable per line item
5. Flags material variances: revenue ≥5% or ≥$2,500 | expenses ≥10% or ≥$2,500
6. Generates WHAT/WHY/ACTION/OUTLOOK commentary stubs for flagged variances
7. Builds rolling forecast: actuals locked for closed months + budget × blend for open months
8. Updates CDC accuracy log and surfaces systematic bias patterns

### Excel Output (6 tabs)

| Tab | Contents |
|---|---|
| Variance Summary | Headline KPIs + all material variances |
| Monthly Detail | All line items × closed months (Budget \| Actual \| Var per month) |
| Material Flags | Sorted by $ variance + monthly trend + action prompts |
| Rolling Forecast | Full-year forecast by account (gray=closed, blue=forecasted) |
| Management Commentary | WHAT/WHY/ACTION/OUTLOOK per material variance (draft) |
| CDC Log | Budget accuracy tracker + systematic bias analysis |

### Usage

```bash
# Default: compare through last completed month, use cached budget
python3 budget-builder.py --slug <client-slug> --compare

# Specify through month
python3 budget-builder.py --slug <client-slug> --compare --through 2026-02

# Use explicit budget file
python3 budget-builder.py --slug <client-slug> --compare --budget-file ~/Desktop/Budget_client_2026.json

# Use manually-prepared budget CSV
python3 budget-builder.py --slug <client-slug> --compare --budget-file my_budget.csv

# Custom output
python3 budget-builder.py --slug <client-slug> --compare --through 2026-03 --out ~/Desktop/reports
```

### Budget CSV Format (for --budget-file)

If the budget was prepared outside this tool (e.g., in Excel), export as:

```csv
account,section_type,2026-01,2026-02,...,2026-12
Total Income,income,50000,52000,...,85000
Cost of Goods Sold,cogs,15000,15600,...,25500
Rent,expense,3500,3500,...,3500
```

---

## Material Variance Thresholds

| Category | $ Threshold | % Threshold |
|---|---|---|
| Revenue | ≥ $2,500 | ≥ 5% |
| Expenses | ≥ $2,500 | ≥ 10% |

Both conditions use OR logic — either trigger alone is enough to flag.

---

## Seasonal Pattern Detection

- **Seasonal strength** = max_monthly_index / min_monthly_index
- Accounts with strength ≥ 1.30 are marked `IS SEASONAL = YES`
- Monthly index = month_amount / annual_average_monthly
- Index > 1.0 = above average month; index < 1.0 = below average
- Peak/trough months are identified and highlighted in the Seasonal Patterns tab

**Example:** Q4 revenue spike → indices for Oct/Nov/Dec will be > 1.0, Q1-Q2 will be < 1.0. Budget will correctly allocate more to Q4.

---

## Rolling Forecast Logic

```
Closed months:  Actual values locked in (not adjusted)
Open months:    Budget × blend_factor

blend_factor = (0.70 × ytd_factor) + (0.30 × 1.0)
ytd_factor   = actual_YTD / budget_YTD
```

- If actuals are running 15% above budget → open months forecasted at +10.5% above budget
- If actuals are running 10% below budget → open months forecasted at -7% below budget
- Blend weight (0.70) is configurable in script `FORECAST_TREND_WEIGHT`

---

## CDC — Budget Accuracy Tracker

Tracks per-account variance data across all BvA runs. After 2+ periods, identifies:
- **Consistently over-budget** accounts (actual > budget 75%+ of the time)
- **Consistently under-budget** accounts (actual < budget 75%+ of the time)
- **Average variance** magnitude per account

**Use case:** If Marketing always runs 20% over budget, the CDC will surface this after 2-3 months. Use for next year's budget calibration.

CDC is appended, not overwritten — it accumulates across fiscal years.

---

## Workflow Integration

```
1. [Month 1 of new FY] Run --build to generate annual budget
   → Saves: .cache/budget-builder/{slug}_budget_{year}.json
   → Share Excel with the reviewer for approval before using in BvA

2. [Each month after close] Run --compare
   → Pulls actuals from QBO automatically
   → Flags variances, generates commentary stubs
   → Updates CDC accuracy log

3. [Mid-year review] Re-run --build with updated assumptions + YTD overrides
   → Export updated budget JSON, pass to --budget-file in --compare
```

---

## Error Handling

| Scenario | Behavior |
|---|---|
| QBO connection error | Raises RuntimeError with stdout/stderr for diagnosis |
| Missing month in history | Fills with $0; warns in console |
| Budget file not found | Raises FileNotFoundError with clear message + instructions |
| Division by zero (budget = $0 for actuals) | Returns ZERO variance; flags if actual > $2,500 |
| Invalid CSV column format | Skips unrecognized columns; warns |

---

## Dependencies

```bash
pip install openpyxl
# Node.js QBO client must be configured with valid auth tokens
```

---

## Output File Naming

```
Mode A: Budget_{slug}_{year}.xlsx              (e.g., Budget_acme_2026.xlsx)
Mode B: BvA_{slug}_{month_label}.xlsx         (e.g., BvA_acme_Feb_26.xlsx)
Cache:  .cache/budget-builder/{slug}_budget_{year}.json
CDC:    .cache/budget-builder/{slug}_cdc.json
```

---

## Example: Full FY2026 Cycle

```bash
# January 2026: Build the budget
python3 budget-builder.py --slug <client-slug> --build --year 2026 \
  --assumptions clients/<client-slug>/budget-assumptions-2026.json

# February 28 (after Jan close):
python3 budget-builder.py --slug <client-slug> --compare --through 2026-01

# March 31 (after Feb close):
python3 budget-builder.py --slug <client-slug> --compare --through 2026-02

# Q2 reforecast (after March close):
python3 budget-builder.py --slug <client-slug> --compare --through 2026-03
# Review CDC log — which categories need budget adjustment?
# Build revised budget with Q1 actuals as overrides:
python3 budget-builder.py --slug <client-slug> --build --year 2026 \
  --overrides clients/<client-slug>/q1-actuals-overrides.csv
```
