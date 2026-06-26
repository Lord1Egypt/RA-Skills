---
name: cash-flow-forecast
description: "Build a 13-week rolling cash flow forecast from QBO data with 3-scenario modeling (base, upside, downside). Pulls Balance Sheet and CF Statement for starting cash and trend baseline. Use when a client needs cash runway projection, burn rate analysis, or scenario-based liquidity planning. NOT for annual budgets, P&L variance analysis, or bank reconciliation."
license: MIT
summary:
  - Builds a 13-week rolling cash flow forecast from QBO data with 3-scenario modeling
  - Pulls live Balance Sheet (starting cash) + CF Statement (trend baseline) from QBO
  - Outputs Excel: Summary | Weekly Detail | Scenarios | Burn Rate | Assumptions | CDC Log
  - GlowLabs-type clients: runway/burn emphasis; SB Paulson-type: interest expense emphasis
  - CDC tracks forecast accuracy vs. prior runs (predicted vs. actual starting cash)
updated: 2026-03-17
metadata:
  openclaw:
    emoji: "💸"
---

# Cash Flow Forecast Skill

## When to Use
- Client asks for a 13-week (or rolling n-week) cash flow forecast
- Need to project runway for a high-burn client (GlowLabs-type)
- Monthly or quarterly cash flow advisory deliverable
- Any time cash position monitoring or scenario modeling is needed
- SOP for the client marks "Cash Flow Forecast: ✅"

## NOT for
- Historical cash flow analysis (use P&L Deep Analysis pipeline)
- Bank reconciliation (use bank-reconciliation.py)
- Full audit of cash flows (use QBO CF report directly)
- Balance sheet projections / full financial models

## Script Location
`scripts/pipelines/cash-flow-forecast.py`

## Quick Start
```bash
cd /Users/samshouse/.openclaw/workspace

# Standard 13-week forecast
python3 scripts/pipelines/cash-flow-forecast.py --slug glowlabs

# 6-month history for better seasonality
python3 scripts/pipelines/cash-flow-forecast.py --slug sb-paulson --months 6

# Custom low-cash threshold (GlowLabs: high burn)
python3 scripts/pipelines/cash-flow-forecast.py --slug glowlabs \
    --low-cash-threshold 50000 \
    --critical-threshold 25000 \
    --out ~/Desktop/reports

# Sandbox testing
python3 scripts/pipelines/cash-flow-forecast.py --slug glowlabs --sandbox
```

## All CLI Options
| Flag | Default | Description |
|------|---------|-------------|
| `--slug` | required | QBO company slug |
| `--weeks` | 13 | Forecast horizon (weeks) |
| `--months` | 3 | Months of CF history to pull (1–6) |
| `--low-cash-threshold` | 25000 | Warn when balance < X |
| `--critical-threshold` | 10000 | Critical alert when balance < X |
| `--account` | auto | Specific bank account name filter |
| `--out` | ~/Desktop | Output directory |
| `--sandbox` | false | Use QBO sandbox |

## Output Excel Tabs

### Tab 1: Cash Flow Summary
- Current cash position (all bank/cash accounts from Balance Sheet)
- 13-week KPI summary: total inflows, outflows, net flow, end balance
- Burn rate and runway in callout box
- Full weekly trajectory table with alert coloring
- SOP notes printed at top (client-specific warnings)

### Tab 2: Weekly Detail
- Matrix: each row = a CF subcategory, each column = a week
- Inflows section (green) → Outflows section (red)
- Subtotals, Net Flow row, Running Balance row
- Alert coloring: yellow = warn, orange/red = critical

### Tab 3: Scenarios
- Side-by-side: Base | Optimistic | Pessimistic
- 12 KPI rows: inflows, outflows, net, end balance, burn, runway, alert weeks
- Weekly balance comparison table across all 3 scenarios
- Best/Worst delta and % spread columns

### Tab 4: Burn Rate
- Detailed burn metrics (base case)
- Runway comparison table (all 3 scenarios)
- Week-by-week burn trend
- 🔴 High burn emphasis for GlowLabs-type clients

### Tab 5: Assumptions
- All parameters used (thresholds, adjustments, seasonality weights)
- Monthly averages per category (the baseline used)
- Client SOP config summary
- Methodology notes

### Tab 6: CDC Log
- Run-over-run changes: starting cash, burn rate, runway
- Forecast accuracy: compares prior-run predicted starting cash vs. actual
- First run: saves baseline; second+ run shows deltas

## Scenario Definitions
| Scenario | Collections | Expenses |
|----------|-------------|----------|
| Base | Historical avg | Historical avg |
| Optimistic | +10% | Unchanged |
| Pessimistic | -15% | +5% |

## Cash Flow Categories
Automatically classified from QBO CF rows:

**Operating — Inflows**
- `collections`: Revenue, AR, Net Income, payment processor receipts
- `interest`: Interest income

**Operating — Outflows**
- `payroll`: Wages, salaries, officer comp, Deel (GlowLabs)
- `rent`: Rent, lease, occupancy
- `vendors`: AP, COGS, professional fees, software, subscriptions
- `interest`: Interest expense (SB Paulson: material line)
- `taxes`, `insurance`

**Investing**
- `capex`: Equipment, property, asset purchases

**Financing**
- `debt`: Loans, line of credit, notes payable
- `equity`: Owner distributions/contributions
- `safe`: SAFE notes (GlowLabs)

## Client SOP Integration
The script reads `clients/{slug}/sop.md` automatically and adjusts:

| SOP Signal | Effect |
|------------|--------|
| "burn rate", "runway", "high cash burn" | Burn Rate tab emphasized, 🔴 alert |
| "interest expense" | Interest tracked separately |
| "POS collection", "collected at POS" | No AR lag — flat weekly inflow distribution |
| "accounts receivable" | AR-based: note 30-45 day receipt lag |
| "SAFE" | SAFE financing category added |
| "crypto", "wallet", "ETH" | Crypto wallet note added |
| "Deel" | Deel inbound classified as expense reduction |

## Seasonality Weights
Default week-of-month distribution (configurable in script CONFIG section):

| Week | Inflows | Outflows | Rationale |
|------|---------|----------|-----------|
| Week 1 (days 1–7) | 30% | 35% | Collections/payroll land early |
| Week 2 (days 8–14) | 20% | 20% | Mid-month quiet |
| Week 3 (days 15–21) | 20% | 25% | Mid-month payroll + rent |
| Week 4 (days 22–28) | 30% | 20% | End-month collections |
| Week 5 (overflow) | 0% | 0% | Rarely used |

POS clients (e.g. SB Paulson): inflows flattened to equal weekly distribution.

## CDC Accuracy Loop
1. **First run**: saves `starting_cash`, `first_week_balance`, `avg_monthly_burn`, `months_of_runway`
2. **Second run**: compares new `starting_cash` against prior `first_week_balance`
3. Accuracy % = how close the forecast was to reality
4. Burn rate and runway deltas tracked run-over-run
5. Cache stored in `.cache/cash-flow-forecast/{slug}.json`

## Low-Cash Alert Colors
| Color | Excel Fill | Condition |
|-------|-----------|-----------|
| ✅ OK | White | Balance ≥ low threshold |
| ⚠ Warn | Yellow | Balance < $25K (configurable) |
| 🔴 Critical | Orange/Red | Balance < $10K (configurable) |

## Client-Specific Notes

### GlowLabs (High Burn)
- `--low-cash-threshold 50000 --critical-threshold 25000` recommended
- SOP auto-detected: burn rate tab emphasized with red header
- SAFE financing and Deel categories auto-classified
- Runway is the #1 KPI — shown prominently in Summary tab

### SB Paulson / Willo Salons
- `--months 6` for better seasonality (salon business is seasonal)
- POS collection = no AR lag; inflows distributed flat across weeks
- Interest expense tracked as separate operating outflow category
- Cash Flow Forecast frequency: quarterly advisory (per SOP)

## Dependencies
```
pip install openpyxl
```
Node.js QBO client must be authenticated with a valid token.

## Output Naming
`CashFlowForecast_{slug}_{YYYY-MM-DD}.xlsx`
Default output: `~/Desktop/`

## Related Pipelines
- `pl-quick-compare.py` — P&L variance analysis
- `pl-deep-analysis.py` — Controller-level with GL drill-down
- `bank-reconciliation.py` — Bank statement reconciliation
