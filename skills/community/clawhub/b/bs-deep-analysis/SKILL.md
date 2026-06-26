---
name: BS Deep Analysis
slug: bs-deep-analysis
version: 1.0.0
description: >
  Controller-level Balance Sheet deep analysis from QuickBooks Online. Pulls
  current and prior period BS, runs 3-month rolling averages, GL drill-down
  for material changes, and generates a 7-tab Excel workbook with actionable
  findings. Covers working capital health, current ratio flags, equity
  rollforward, and common-size vertical analysis.
tags:
  - finance
  - accounting
  - balance-sheet
  - qbo
  - excel
negative_boundaries:
  - Cash flow statement analysis → use scf-deep-analysis or scf-quick-compare
  - P&L variance analysis → use pl-deep-analysis skill
  - Multi-entity consolidations → not supported (single-entity only)
  - Real-time balance changes → snapshot-based, not bank-feed
---

# BS Deep Analysis

## What This Skill Does

Controller-level Balance Sheet deep analysis from QuickBooks Online. Mirrors the P&L Deep Analysis pattern but for the balance sheet — pulls current + prior period BS, runs 3-month rolling averages, GL drill-down for material changes, and generates a 7-tab Excel workbook with actionable findings.

**Use when:**
- Monthly close deliverable needs a BS review (not just a P&L comparison)
- Client needs working capital health check or current ratio flag
- Equity rollforward reconciliation is needed for a close
- Material balance changes on cash, AR, inventory, or debt need narrative explanation
- Common-size (vertical) analysis is required for a lender or board report

**NOT for:**
- Cash flow statement analysis — use a dedicated CF pipeline
- P&L variance analysis — use `pl-deep-analysis.py`
- Multi-entity consolidations — this is a single-entity BS pipeline
- Real-time balance changes (it's snapshot-based, not bank-feed)

---

## Pipeline Location

```
scripts/pipelines/bs-deep-analysis.py
```

Cache directory: `.cache/bs-deep-analysis/{slug}.json`

---

## Usage

```bash
# Current month-end vs. auto prior month-end
python3 scripts/pipelines/bs-deep-analysis.py \
  --slug sb-paulson --current-end 2026-03-31

# Explicit prior period
python3 scripts/pipelines/bs-deep-analysis.py \
  --slug sb-paulson \
  --current-end 2026-03-31 --prior-end 2026-02-28

# Skip GL drill-down (faster, no vendor-level detail)
python3 scripts/pipelines/bs-deep-analysis.py \
  --slug sb-paulson --current-end 2026-03-31 --skip-gl

# Custom output directory
python3 scripts/pipelines/bs-deep-analysis.py \
  --slug glowlabs --current-end 2026-03-31 --out ~/Desktop/reports

# QBO sandbox
python3 scripts/pipelines/bs-deep-analysis.py \
  --slug sb-paulson --current-end 2026-03-31 --sandbox
```

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--slug` | ✅ | QBO company slug (must be connected in qbo-client) |
| `--current-end` | ✅ | As-of date for current BS (YYYY-MM-DD) |
| `--prior-end` | ❌ | Prior period as-of date (auto = prior month-end) |
| `--skip-gl` | ❌ | Skip GL drill-down (faster) |
| `--out` | ❌ | Output directory (default: ~/Desktop) |
| `--sandbox` | ❌ | Use QBO sandbox environment |

---

## What It Pulls from QBO

1. **Balance Sheet** (as-of) — current period
2. **Balance Sheet** (as-of) — prior period
3. **Balance Sheet** (as-of) — 3 prior month-ends for rolling averages
4. **General Ledger** — current period GL for flagged accounts (unless `--skip-gl`)
5. **P&L** — current period net income for equity rollforward

---

## Analysis Modules

### 1. Horizontal Analysis (Period-over-Period)
- Every BS line: prior → current → $ change → % change
- Material threshold: ≥$2,500 absolute OR ≥10% change rate
- Flagged accounts sorted by absolute dollar change

### 2. Vertical Analysis (Common-Size)
- Every BS line as % of total assets
- Prior period % vs. current period %
- % point change highlights structural shifts

### 3. 3-Month Rolling Averages
- Pulls 3 prior month-end BS snapshots
- Per-account rolling average as trend baseline
- Rolling delta and rolling % vs. current balance

### 4. GL Drill-Down
- Transaction-level detail for all flagged accounts
- Vendor/payee aggregation: top contributors by dollar
- Max 50 transactions per account (configurable via `GL_MAX_ROWS_PER_ACCOUNT`)

### 5. Working Capital Deep Dive
- Current assets vs. current liabilities decomposition
- Current ratio, quick ratio, cash ratio
- WC delta decomposed: cash change, AR change, inventory change, AP change
- Health classification: HEALTHY / WATCH / CRITICAL

### 6. Debt Schedule Analysis
- Short-term vs. long-term debt split
- D/E ratio and D/A ratio
- ST concentration warning: flags if ST > 60% of total debt
- Leverage risk classification: LOW / LOW-MEDIUM / MEDIUM / HIGH

### 7. Equity Rollforward
```
Beginning Equity
+ Net Income
− Distributions / Owner Draws
+ New Contributions / Paid-in Capital
= Computed Ending Equity
vs. Ending Equity per BS (reconciling difference flagged if ≥ $500)
```
- Retained earnings bridge separately
- Reconciling difference investigation prompt

### 8. Controller Findings
- Narrative: "Cash decreased $45K because AP payments of $60K exceeded collections of $15K"
- Urgency-tagged: HIGH / MEDIUM / LOW
- GL vendor attribution embedded in findings

### 9. Action Proposals
- Specific recommended actions per finding
- Urgency-ranked: HIGH → MEDIUM → LOW
- Categories: LIQUIDITY, CASH MANAGEMENT, COLLECTIONS, INVENTORY, DEBT MANAGEMENT, LEVERAGE, EQUITY INTEGRITY, BALANCE SHEET

### 10. CDC (Change Data Capture)
- Compares current BS flat map vs. prior run cache
- Tracks: new accounts, removed accounts, balance changes
- Cache saved to `.cache/bs-deep-analysis/{slug}.json`

---

## Excel Output — 7 Tabs

| Tab | Contents |
|---|---|
| **Summary** | KPI table, key ratios, controller findings, action proposals |
| **Detail** | Full BS with prior/current/delta/rolling avg per account |
| **⚠ Flags** | Material change accounts + findings summary |
| **GL Drill-Down** | Transaction-level detail for flagged accounts |
| **Common-Size Analysis** | Vertical analysis: each line as % of total assets |
| **Equity Rollforward** | Period reconciliation + retained earnings bridge |
| **CDC Log** | Balance changes vs. last pipeline run |

---

## Materiality Thresholds

| Metric | Threshold |
|---|---|
| Absolute change | ≥ $2,500 |
| Percentage change | ≥ 10% |
| Equity change (tighter) | ≥ 5% |
| Working capital watch | Current ratio < 1.5x |
| Working capital critical | Current ratio < 1.0x |
| ST debt concentration warning | ST debt > 60% of total |
| Equity rollforward diff flag | ≥ $500 |

---

## Dependencies

```
pip install openpyxl
Node.js QBO client with valid auth token
```

QBO auth token must be set (same as all other pipelines).

---

## Related Pipelines

| Pipeline | File | When to Use |
|---|---|---|
| P&L Deep Analysis | `pl-deep-analysis.py` | Income statement controller review |
| Financial Ratios | `financial-ratios.py` | Full ratio suite (uses BS data) |
| BS Deep Analysis | `bs-deep-analysis.py` | **This pipeline** — balance sheet focus |

---

## Notes

- All math uses Python `Decimal` — no float rounding errors
- GL account names must match BS account names for drill-down attribution (QBO may use slightly different names between reports)
- Prior month-end is auto-calculated if `--prior-end` is omitted (always safe for monthly close)
- `--skip-gl` reduces runtime significantly; use for quick runs when vendor detail is not needed
- CDC cache is per-slug; running for a new slug always starts fresh (first run snapshot only)
