---
name: ali-promotion-roi
description: "Analyze Alibaba International (alibaba.com) promotion ROI - evaluates total promotion spend vs. actual completed orders and revenue. Use when the user asks about Alibaba 国际站推广投入产出, 推广 ROI, 阿里广告效果分析, 标准推广/全站推广效果对比, 月度推广总结, or wants to know how much each completed order costs (CPO). Reads pre-loaded data from MySQL via sql-linker-cli (tables: alibaba_intl_orders + alibaba_intl_promotion_daily). Does NOT load data - that requires separate ingestion scripts."
---

# Ali Promotion ROI Analysis

## When This Skill Applies

Use this skill when the user wants to:
- Evaluate Alibaba International station (alibaba.com) promotion investment vs. returns
- Calculate ROI / CPO (Cost Per Order) for promotion campaigns
- Compare `standard_promotion` (标准推广) vs `sitewide_promotion` (全站推广)
- Generate monthly promotion reports: spend, completed orders, revenue
- Audit "the platform says 1 order but my records say 0" discrepancies

**Do NOT use this skill** for data ingestion. Loading Excel into MySQL is handled by `scripts/alibaba_intl/load_orders.py` and `load_promotion.py`. This skill **only reads** existing data.

---

## Prerequisites

1. **Tables must exist and be populated**:
   - `alibaba_intl_orders` (信保订单明细)
   - `alibaba_intl_promotion_daily` (标准+全站推广日度合并)
2. **sql-linker-cli** must be installed and configured (provides DB access via `db_bridge`)
3. **Both tables must be in `table_dictionary.json`** (already done if you ran `add_orders_promotion_to_dictionary.py`)

If tables are missing, tell the user to run the ingestion scripts first.

---

## Quick Start

```bash
cd skills/ali_promotion_roi
python scripts/cli.py                        # Full report (all months)
python scripts/cli.py --month 2026-01        # Single month
python scripts/cli.py --rate 7.25            # Custom USD/CNY rate
python scripts/cli.py --by-type              # Only promotion-type breakdown
python scripts/cli.py --by-date              # Only daily drilldown
python scripts/cli.py --json > report.json   # JSON for further processing
```

The CLI uses `DBBridge` with **explicit credential approval** (`explicit_credential_approval(approved=True)`) — this is required when the sql-linker-cli credential gate is enabled.

---

## Output Sections

The report contains 3 sections:

1. **Summary (月度总览)**: total spend, total completed orders, CPO, ROI
2. **By Type (按推广类型拆分)**: standard_promotion vs sitewide_promotion side-by-side
3. **By Date (按日对照)**: day-by-day spend vs actual completed orders (catches the "平台报1单但实际0单" discrepancies)

---

## Key Metrics (read `references/metrics.md` for full definitions)

- **CPO** = 推广花费(CNY) / 完成订单数
- **ROI** = (订单金额(USD) × 汇率) / 推广花费(CNY) × 100%
- **订单实付** = `order_amount + shipping_fee - discount_amount`
- **完成订单** = `order_status = '订单完成'` (closed/refunded excluded)

---

## Data Source

This skill **reads** from MySQL via sql-linker-cli's `DBBridge`:

| Table | Purpose |
|-------|---------|
| `alibaba_intl_orders` | Order facts (信保订单, row-level) |
| `alibaba_intl_promotion_daily` | Daily promotion metrics (standard + sitewide merged) |

For schema details, read `references/schema.md`. For metric definitions and common pitfalls, read `references/metrics.md`.

---

## Files

```
ali_promotion_roi/
├── SKILL.md                  # This file
├── scripts/
│   ├── cli.py                # CLI entry: argparse + report rendering
│   └── roi.py                # Pure compute: fetch / compute_summary / compute_by_type / compute_by_date
└── references/
    ├── schema.md             # Table column reference
    └── metrics.md            # Metric definitions + analysis patterns
```

The `scripts/roi.py` module exports reusable functions (`fetch_orders`, `fetch_promotion`, `compute_summary`, `compute_by_type`, `compute_by_date`, `connect_db`) — you can `import roi` from another script to embed ROI logic in larger workflows.

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `[WARN] 没有数据` | Tables empty or not loaded | Run ingestion scripts first |
| `TableAccessDenied` | Tables not in `table_dictionary.json` | Run `add_orders_promotion_to_dictionary.py` |
| `Silent credential access requires explicit approval` | Gate enabled but `approved=True` not passed | The CLI already handles this — re-run |
| ROI shows N/A | Cost = 0 (no promotion spend that month) | Expected, not an error |

---

## Extending This Skill

To add new analyses (e.g., per-buyer-country ROI, per-product ROI):

1. Add a compute function in `scripts/roi.py`
2. Add a render function in `scripts/cli.py`
3. Wire it into `main()` with a new CLI flag

Keep the compute layer pure (no SQL inside compute functions) — fetch all data upfront, then compute in-memory.