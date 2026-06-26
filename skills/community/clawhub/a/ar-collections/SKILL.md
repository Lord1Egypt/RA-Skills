---
name: ar-collections
description: >
  AR Collections & Aging Analysis pipeline for QBO clients. Produces a 7-tab Excel workbook
  with AR aging buckets (Current/1-30/31-60/61-90/90+), DSO, collection priority scoring,
  bad debt reserve, payment patterns, and CDC log. SOP-gated: auto-skips clients with no AR
  (e.g. POS-based businesses). Use for AR aging reports, collections analysis, DSO tracking,
  and bad debt reserve calculations. NOT for bank reconciliation, payroll, or tax preparation.
version: 1.0.0
tags:
  - finance
  - accounting
  - accounts-receivable
  - collections
  - DSO
  - aging
summary:
  - AR Collections & Aging Analysis pipeline for QBO clients
  - SOP-gated: auto-skips if client has no AR (e.g. SB Paulson/Willo — POS collection)
  - 7-tab Excel output: AR Summary | Aging Detail | Collection Priority | Payment Patterns | Bad Debt Reserve | DSO Analysis | CDC Log
  - All Decimal math; CDC tracks aging movement between runs
  - Trigger phrases: AR aging, collections report, accounts receivable, DSO, bad debt reserve
updated: 2026-03-18
---

# AR Collections & Aging Analysis Skill

## What This Does

Runs the AR Collections & Aging Analysis pipeline (`scripts/pipelines/ar-collections.py`) to produce a controller-level accounts receivable workbook from QBO data.

**Produces:**
1. AR aging bucketed into Current | 1-30 | 31-60 | 61-90 | 90+ days
2. Aging metrics: total AR, weighted average days outstanding, concentration risk
3. Collection priority scoring per customer (HIGH / MEDIUM / LOW / MONITOR)
4. Recommended collection actions per customer
5. Bad debt reserve (percentage-of-aging method)
6. Payment pattern analysis from GL history
7. DSO: current period and rolling 3-month
8. CDC: which customers improved or deteriorated since last run
9. Excel workbook (7 tabs)

## When to Use

**Use when:**
- Client asks for AR aging report, collections status, or DSO
- Monthly close includes AR review
- Need to know who owes money and what to do about it
- Bad debt reserve needs to be calculated for month-end
- Auditors or investors request AR aging schedule

**Do NOT use when:**
- Client SOP says AR is not applicable (pipeline exits gracefully — no report needed)
- Client collects at point of sale (e.g., SB Paulson / Willo Salons)
- Running for a non-QBO client (no data source)
- User wants a P&L or balance sheet (use pl-deep-analysis or client-dashboard)

## SOP Gate

The pipeline **automatically checks the client SOP** before pulling any data:
- `sb-paulson` → exits gracefully with explanation (POS collection, no AR)
- Unknown slugs → checks SOP markdown for AR-disabled signals, defaults to AR-applicable

To add a new client's AR status, update `CLIENT_AR_CONFIG` in the pipeline, OR add these markers to their `clients/{slug}/sop.md`:
```
**AR Aging:** ❌ Not applicable (POS collection)
```

## Usage

```bash
# Standard run — as of end of month
python3 scripts/pipelines/ar-collections.py --slug <client-slug> --as-of 2026-03-31

# With custom output directory
python3 scripts/pipelines/ar-collections.py --slug <client-slug> --as-of 2026-03-31 --out ~/Desktop/reports

# Skip GL pull (faster, no payment pattern analysis)
python3 scripts/pipelines/ar-collections.py --slug <client-slug> --as-of 2026-03-31 --skip-gl

# QBO sandbox
python3 scripts/pipelines/ar-collections.py --slug <client-slug> --as-of 2026-03-31 --sandbox

# Client with no AR — exits gracefully
python3 scripts/pipelines/ar-collections.py --slug sb-paulson --as-of 2026-03-31
```

## Output

**Default location:** `reports/ar-collections/ar-collections_{slug}_{as-of}.xlsx`

**Tabs:**

| Tab | Contents |
|-----|----------|
| AR Summary | Aging snapshot by bucket, key metrics, concentration risk |
| Aging Detail | Invoice-level list: customer, date, due date, balance, bucket |
| Collection Priority | Sorted action list: HIGH/MEDIUM/LOW/MONITOR with recommended actions |
| Payment Patterns | Avg days to pay per customer, vs. terms, reliability rating |
| Bad Debt Reserve | Percentage-of-aging reserve calc + suggested journal entry |
| DSO Analysis | Current and rolling 3-month DSO, monthly revenue detail |
| CDC Log | Changes since last run: improved / deteriorated / new / cleared |

## Collection Priority Logic

| Priority | Criteria | Recommended Action |
|----------|----------|--------------------|
| HIGH | 90+ days past due OR balance > $5K | Escalate / demand letter / write-off review |
| MEDIUM | 61-90 days OR balance > $2.5K | Follow-up call |
| LOW | 31-60 days | Send email reminder |
| MONITOR | Current or 1-30 days | Standard review next cycle |

## Bad Debt Reserve Rates (Percentage-of-Aging)

| Bucket | Rate |
|--------|------|
| Current | 1% |
| 1-30 | 3% |
| 31-60 | 10% |
| 61-90 | 25% |
| 90+ | 50% |

## DSO Formula

- **Current DSO** = (AR Balance ÷ Current Period Revenue) × Days in Period
- **Rolling DSO** = AR Balance ÷ (3-Month Revenue ÷ 90 days)

## CDC Cache

Cached at: `.cache/ar-collections/{slug}.json`

Each run saves customer balances and worst buckets. Next run computes:
- **Improved** — balance decreased or bucket moved earlier
- **Deteriorated** — balance increased or bucket moved later
- **New** — first appearance in AR
- **Cleared** — balance went to zero (collected)

## Requirements

```bash
pip install openpyxl
# Node.js QBO client must be auth'd
node bin/qbo info {slug}  # from your QBO integration directory
```

## Related Pipelines

- `pl-deep-analysis.py` — GL drill-down, P&L variance, accrual proposals
- `client-dashboard.py` — KPI dashboard (includes DSO as a KPI)
- `bank-reconciliation.py` — Bank rec (not AR-specific)
- `budget-vs-actual.py` — BvA (revenue-side context for AR)

## Clients

Configure AR applicability per client in `CLIENT_AR_CONFIG` or via `clients/{slug}/sop.md`.
