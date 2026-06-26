---
name: client-dashboard
description: >
  Generates a client-facing executive KPI dashboard from QuickBooks Online data. Produces an
  Excel workbook with traffic-light scoring, 6-month trend sparklines, client-specific watch
  items, and a CDC log tracking KPI changes month-over-month. Use after monthly close to
  deliver the final executive summary deliverable to clients. NOT a substitute for P&L variance
  analysis, not for mid-month snapshots, and not for clients without QBO integration.
version: 1.0.0
tags:
  - finance
  - accounting
  - dashboard
  - KPI
  - client-reporting
  - QBO
updated: 2026-03-18
---

# Client Dashboard / KPI Report — SKILL.md

## What This Skill Does

Generates a client-facing executive KPI dashboard from QuickBooks Online data. Produces an Excel workbook with traffic-light scoring, 6-month trend sparklines, client-specific watch items, and a CDC log tracking KPI changes month-over-month.

## When To Use

- Monthly close is complete and it's time to generate the client dashboard
- User asks for KPI report, dashboard, or executive summary for any client
- After running P&L Quick Compare and bank rec — this is the final deliverable step

## When NOT To Use

- NOT a substitute for P&L Quick Compare (different purpose — this is executive summary, not variance analysis)
- NOT for mid-month snapshots — designed for complete monthly periods
- NOT for YTD / annual reports — use P&L Deep Analysis for those
- NOT for clients without QBO integration (no data source)

---

## Pipeline: `scripts/pipelines/client-dashboard.py`

### Prerequisites
```bash
pip install openpyxl
# Node.js qbo-client must be authenticated for the target slug
```

### Usage

```bash
# Example — March 2026
python3 scripts/pipelines/client-dashboard.py --slug <client-slug> --month 2026-03

# Custom output directory
python3 scripts/pipelines/client-dashboard.py --slug <client-slug> --month 2026-03 --out ~/Desktop/reports

# QBO sandbox
python3 scripts/pipelines/client-dashboard.py --slug <client-slug> --month 2026-03 --sandbox
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--slug` | ✅ | Company slug (must match qbo-client connection) |
| `--month` | ✅ | Report month: `YYYY-MM` format |
| `--out` | ❌ | Output directory (default: `~/Desktop`) |
| `--sandbox` | ❌ | Use QBO sandbox environment |

---

## Output: Excel Workbook

**Filename:** `KPI_Dashboard_{slug}_{YYYY_MM}.xlsx`

| Tab | Contents |
|-----|----------|
| **Executive Summary** | Headline numbers + traffic-light KPI table with benchmarks |
| **KPI Scorecard** | Full KPI detail with definitions, thresholds, and score |
| **Trends** | 6-month KPI trend with sparklines (↑↗→↘↓ + block chars) |
| **Cash Position** | Balance sheet cash, CF summary, liquidity ratios, runway |
| **Watch Items** | SOP-driven priority items surfaced prominently |
| **CDC Log** | Month-over-month KPI delta (what changed since last run) |

---

## KPIs Computed

| KPI | Formula | Unit |
|-----|---------|------|
| Revenue MoM Growth | `(curr_rev - prior_rev) / prior_rev × 100` | % |
| Revenue YoY Growth | `(curr_rev - yoy_rev) / yoy_rev × 100` | % |
| Gross Margin % | `gross_profit / revenue × 100` | % |
| Gross Margin (3-Mo Avg) | Rolling 3-month GP/Revenue | % |
| Net Margin % | `net_income / revenue × 100` | % |
| OpEx Ratio | `total_opex / revenue × 100` | % |
| Interest Expense Ratio | `interest_expense / revenue × 100` | % |
| Current Ratio | `current_assets / current_liabilities` | x |
| Quick Ratio | `(current_assets - inventory) / current_liabilities` | x |
| Debt-to-Equity | `total_liabilities / total_equity` | x |
| DSO | `ar / (revenue / days)` | days |
| DPO | `ap / (cogs / days)` | days |
| Cash Runway | `cash / monthly_burn` | months |
| Retail % of Revenue | `retail_revenue / total_revenue × 100` | % |

**All math uses Python `Decimal` for precision.**

---

## Traffic Light Scoring

Each KPI is scored GREEN / YELLOW / RED based on configurable thresholds per client SOP.

```
🟢 GREEN  = On target (within green band)
🟡 WATCH  = Approaching threshold (yellow band)
🔴 ACTION = Below/above acceptable range (outside yellow band)
⬜ N/A    = KPI not applicable or not configured
```

Thresholds are defined in `CLIENT_CONFIGS` in the script — one config block per client slug.

---

## Client SOP Integration

### Adding a New Client
Add a block to `CLIENT_CONFIGS` in the script:
```python
"new-slug": {
    "company_name": "Company Name",
    "industry": "Industry",
    "has_ar": True,
    "has_headcount": False,
    "kpis_enabled": ["revenue_mom", "gross_margin", ...],
    "thresholds": {
        "gross_margin": {"green": (Decimal("45"), None), "yellow": (Decimal("35"), Decimal("45"))},
        ...
    },
    "watch_items": [...],
    "benchmarks": {...},
    "benchmark_source": "Source description",
}
```

---

## CDC (Change Data Capture)

Cache stored at: `.cache/client-dashboard/{slug}.json`

- First run: saves full KPI snapshot, CDC tab shows "First run" message
- Subsequent runs: diffs current KPIs vs. prior run
- CDC log shows: KPI label | Prior | Current | Delta | % Change | Improved/Declined

---

## Trend Sparklines

6-month trend for each KPI uses two formats:
1. **Direction arrows:** `↑↑ ↑ ↗ → ↘ ↓ ↓↓` (based on % change over period)
2. **Block bars:** `█▇▅▃▁_` (relative to max value — in Trends tab mini-chart section)

---

## Peer Benchmarks

Manual config only. Benchmark values live in `CLIENT_CONFIGS[slug]["benchmarks"]`.
Source attribution displayed in every tab footer.
To update: edit `benchmarks` dict and `benchmark_source` string per client.

---

## Integration with Pipeline Suite

This pipeline is designed to run **after** monthly close is complete:

```
1. Bank Reconciliation      (bank-reconciliation.py)
2. P&L Quick Compare        (pl-quick-compare.py)
3. P&L Deep Analysis        (pl-deep-analysis.py)      ← optional for controller level
4. Client Dashboard         (client-dashboard.py)      ← this script
5. Cash Flow Forecast       (cash-flow-forecast.py)    ← quarterly advisory
```

---

## File Locations

| File | Path |
|------|------|
| Pipeline script | `scripts/pipelines/client-dashboard.py` |
| Skill file | `skills/client-dashboard/SKILL.md` |
| CDC cache | `.cache/client-dashboard/{slug}.json` |
| Output (default) | `~/Desktop/KPI_Dashboard_{slug}_{YYYY_MM}.xlsx` |

---

## Troubleshooting

**QBO CLI error:** Ensure your QBO integration is authenticated for the slug.

**Missing KPIs:** If Balance Sheet accounts don't match expected labels, values default to 0. Check `extract_bs_metrics()` candidates list for account name variants.

**New client config:** Add slug to `CLIENT_CONFIGS` before first run. Default config uses generic thresholds (not client-specific).

**Decimal errors:** All financial math uses Python `Decimal`. Do not mix `float` — use `to_d()` helper for any external values.
