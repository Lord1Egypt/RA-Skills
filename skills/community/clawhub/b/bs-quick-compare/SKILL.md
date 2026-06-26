---
name: BS Quick Compare
slug: bs-quick-compare
version: 1.0.0
description: >
  Period-over-period variance analysis on the Balance Sheet pulled from
  QuickBooks Online. Outputs a 4-tab Excel workbook: Summary, Detail, Flags,
  CDC Log. Covers Assets, Liabilities, and Equity sections with accounting
  equation validation and BS-specific analysis notes on flagged items.
tags:
  - finance
  - accounting
  - balance-sheet
  - qbo
  - excel
negative_boundaries:
  - P&L variance analysis → use pl-quick-compare skill
  - Cash flow analysis → use scf-quick-compare skill
  - AR aging deep-dive → use ar-collections skill
  - Financial projections or forecasting → use cash-flow-forecast skill
  - Full three-statement analysis → run all three compare pipelines separately
---

# BS Quick Compare — Skill

## What This Skill Does

Runs a period-over-period variance analysis on the **Balance Sheet (BS)** pulled directly from QuickBooks Online. Outputs a 4-tab Excel workbook: Summary | Detail | Flags | CDC Log.

Mirrors the `pl-quick-compare` and `scf-quick-compare` patterns but for the Balance Sheet — Assets / Liabilities / Equity sections, accounting equation validation, and BS-specific analysis notes on flagged items tying changes to SCF, AR/AP aging, capex, debt schedule, and equity activity.

## When to Use

**Use when:**
- A client needs month-end or YTD balance sheet comparison
- Reviewing BS as part of monthly close deliverables
- Investigating material shifts in assets, liabilities, or equity
- Client asks: "why did our AR/AP/cash/debt change?" or "what happened to our equity?"
- Pre-loan/investor analysis requiring clear BS trend visibility

**NOT for:**
- P&L variance analysis → use `pl-quick-compare.py`
- Cash flow analysis → use `scf-quick-compare.py`
- AR aging deep-dive → use `ar-collections`
- Financial projections or forecasting → use `cash-flow-forecast.py`
- Full three-statement analysis (run all three compare pipelines and cross-reference)

## Script Location

```
scripts/pipelines/bs-quick-compare.py
```

## Requirements

- `pip install openpyxl` (already installed in workspace)
- Node.js QBO client with valid auth token
- QBO credentials configured

## Usage

```bash
# Current month-end vs. prior month-end (auto-detects prior)
python3 scripts/pipelines/bs-quick-compare.py \
    --slug sb-paulson \
    --current-end 2026-03-31

# Explicit prior period
python3 scripts/pipelines/bs-quick-compare.py \
    --slug sb-paulson \
    --current-end 2026-02-28 --prior-end 2026-01-31

# YTD (as of end of last completed month vs. same date prior year)
python3 scripts/pipelines/bs-quick-compare.py \
    --slug sb-paulson --ytd --year 2026

# Full date control (for QBO BS reports needing explicit start dates)
python3 scripts/pipelines/bs-quick-compare.py \
    --slug sb-paulson \
    --current-start 2026-01-01 --current-end 2026-03-31 \
    --prior-start 2025-01-01 --prior-end 2025-03-31

# Custom output directory
python3 scripts/pipelines/bs-quick-compare.py \
    --slug glowlabs \
    --current-end 2026-03-31 \
    --out ~/Desktop/reports

# Sandbox mode (QBO sandbox environment)
python3 scripts/pipelines/bs-quick-compare.py \
    --slug glowlabs \
    --current-end 2026-03-31 \
    --sandbox
```

## Arguments

| Flag | Required | Description |
|------|----------|-------------|
| `--slug` | ✅ | Company slug (must be connected in qbo-client) |
| `--current-end` | ✅* | Current period "as of" date (YYYY-MM-DD) |
| `--current-start` | ❌ | Current period start (default: Jan 1 same year) |
| `--prior-end` | ❌ | Prior period "as of" date (default: 1 month back) |
| `--prior-start` | ❌ | Prior period start (default: Jan 1 same year as prior-end) |
| `--ytd` | ✅* | YTD mode (alternative to explicit dates) |
| `--year` | ❌ | Year for --ytd (default: current year) |
| `--out` | ❌ | Output directory (default: ~/Desktop) |
| `--sandbox` | ❌ | Use QBO sandbox environment |

*Either `--current-end` OR `--ytd` is required.

**Balance Sheet date note:** BS is a point-in-time statement. `--current-end` and `--prior-end` are the "as of" dates. The QBO CLI requires start/end dates even for BS — the script defaults `--current-start` to Jan 1 of the same year if omitted.

## Output

Excel file: `BS_QuickCompare_{slug}_{as-of-date}.xlsx` saved to Desktop (or `--out` directory).

### Tab 1: Summary
- Total Assets / Total Liabilities / Total Equity (current vs prior, $ change, % change, F/U)
- Total Liabilities + Equity (cross-check row)
- Accounting equation validation: `Total Assets = Total Liabilities + Total Equity` (both periods, ≤$1 tolerance)

### Tab 2: Detail
- Every BS line item with hierarchy preserved
- Prior period | Current period | $ Change | % Change | F/U label
- Color-coded by section (Assets = blue, Liabilities = gold, Equity = purple)

### Tab 3: ⚠ Flags
- Material changes: **≥10% change OR ≥$2,500 absolute**
- Analysis note for each flagged item — plain-English explanation tying the change to relevant follow-up actions
- BS-specific cross-references (see Analysis Notes section below)

### Tab 4: CDC Log
- Change Data Capture: compares current BS flat map against last cached run
- First run: full snapshot saved (no deltas)
- Subsequent runs: shows exactly what line items changed since last run
- Cache location: `.cache/bs-quick-compare/{slug}.json`

## BS Logic

### Section Classification
Each QBO BS row is classified into sections by keyword matching:
- **Assets**: cash, bank, accounts receivable, inventory, prepaid, property, equipment, fixed asset, accumulated depreciation, investment, due from, notes receivable
- **Liabilities**: liabilit, accounts payable, accrued, loan, note payable, line of credit, mortgage, deferred revenue, sales tax, payroll, credit card, due to
- **Equity**: equity, owner, capital, retained earnings, net income, distribution, contribution, member, shareholder, partner, opening balance equity, paid-in, common stock

Children inherit their parent section classification.

### Variance F/U Logic
| Section | Increase = | Decrease = |
|---------|-----------|-----------|
| Assets | ✓ Favorable | ✗ Unfavorable |
| Liabilities | ✗ Unfavorable | ✓ Favorable |
| Equity | ✓ Favorable | ✗ Unfavorable |

Strategic exceptions (new LOC for growth, timely AP buildup) are noted in the analysis notes column.

### Accounting Equation Validation
```
Total Assets = Total Liabilities + Total Equity   (≤$1 tolerance)
```
Runs on both periods and displayed in Summary tab with pass/fail icons.

### YTD Mode
`--ytd`: Current = as of end of last completed month. Prior = same date in prior year.
Example: run on March 17, 2026 → Current = as of Feb 28, 2026 | Prior = as of Feb 28, 2025.

## Analysis Notes (Flags Tab)

The Flags tab includes an **Analysis Note** column with BS-specific interpretation for each material change:

| Line Item | Analysis Note Focus |
|-----------|-------------------|
| Cash / Bank | Tie to SCF — identify source: operating CF, capex, debt, distribution |
| Accounts Receivable | Run AR aging — check DSO, past-due balances, collection trends |
| Inventory | Monitor turnover — buildup vs. drawdown relative to sales pace |
| Prepaid Expenses | Amortization vs. new prepaid spend |
| Fixed Assets / PP&E | Capex vs. disposal — verify depreciation schedule updated |
| Accumulated Depreciation | Confirm D&A add-back in SCF operating section |
| Related-party Receivables | Repayment terms and tax treatment of officer/shareholder loans |
| Accounts Payable | Run AP aging — confirm no overdue payables; payment terms intact |
| Credit Cards | Full payment schedule; confirm all charges categorized |
| Loans / Notes Payable | New borrowing vs. paydown — tie to SCF financing; verify debt schedule |
| Line of Credit | Draw vs. paydown — monitor utilization rate and available capacity |
| Mortgage | Normal amortization vs. lump-sum payment — confirm against schedule |
| Deferred Revenue | Cash received vs. revenue not yet earned — monitor recognition schedule |
| Payroll / Accrued | Settlement timing — verify no aged accruals outstanding |
| Sales Tax Payable | Confirm remittance current; no penalties |
| Retained Earnings | Tie to net income in P&L |
| Current Year Net Income | Deep-dive in P&L quick compare |
| Distributions / Draws | Verify cash availability; tie to SCF financing section |
| Equity Contributions | Tie to SCF financing; confirm cap table updated |
| Opening Balance Equity | Should zero out once books are fully set up |

## CDC Cache

```
.cache/bs-quick-compare/{slug}.json
```

Stores the flat map of all BS line names → balances for the most recent run. On re-run, diffs against the prior cache and shows exactly what changed. Useful for catching mid-month QBO adjustments, journal entries, or bank feed imports.

## Decimal Math

All calculations use Python `Decimal` with `ROUND_HALF_UP` — no floating-point rounding errors in financial outputs.

## Related Pipelines

Run all three compare pipelines for a complete monthly close package:

| Pipeline | Script | What it covers |
|----------|--------|---------------|
| P&L Quick Compare | `pl-quick-compare.py` | Revenue, COGS, expenses, net income |
| SCF Quick Compare | `scf-quick-compare.py` | Cash flows: operating, investing, financing |
| **BS Quick Compare** | `bs-quick-compare.py` | **Assets, liabilities, equity positions** |

Cross-reference flags across all three:
- Cash change on BS → tie to SCF net change
- AR/AP change on BS → tie to aging pipelines
- Net income on BS → tie to P&L net income
- Loan changes on BS → tie to SCF financing section
