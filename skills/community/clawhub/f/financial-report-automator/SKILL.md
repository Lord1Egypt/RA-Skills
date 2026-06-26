---
name: financial-report-automator
description: Automated quarterly financial report generation with dividend-adjusted total return calculations. Use when generating stock performance reports, quarterly earnings summaries, or return analytics for any ticker with CSV price data.
version: 1.2.1
tags: ['finance', 'reporting', 'quarterly', 'returns', 'dividends']
---

# Financial Report Automator

Generates quarterly stock performance reports with **dividend-adjusted total return**.

## What It Does

- Parses CSV price data (Yahoo Finance export format)
- Computes **price return** (raw close) and **total return** (adjusted close with dividends)
- Produces structured quarterly reports: start/end price, returns, high/low, avg volume, dividends paid

## Key Fix (v1.0.1)

Previous versions used raw close for return calculations, which **understated returns for dividend-paying stocks** like AAPL. v1.0.1 introduces:

1. **Column name normalization** — handles mixed-case CSV headers (`Date` → `date`)
2. **Adjusted close computation** — backward-adjusts prices for dividends so total return reflects reinvested dividends
3. **Separate price_return vs total_return** — both are reported for transparency
4. **Dividend tracking** — `dividend` column is optional; defaults to 0 if absent

## Usage

### As a Python module

```python
from scripts.stock_analyzer import StockAnalyzer

analyzer = StockAnalyzer(data_path="finance/AAPL.csv")

# 30-day total return (dividend-adjusted)
print(analyzer.calculate_returns(30))

# 30-day price return only (no dividends)
print(analyzer.calculate_returns(30, use_adj=False))

# Full quarterly report
report = analyzer.generate_quarterly_report(quarter=2, year=2026)
print(report)
```

### CLI

```bash
python3 scripts/stock_analyzer.py
```

## CSV Format Expected

```
Date,Close,Volume,Open,High,Low
01/02/2026,$269.77,21755774,$272.05,$277.82,$269.11
```

Optional columns:
- `dividend` — per-share dividend on ex-div date
- `adj_close` — pre-computed adjusted close (overrides internal calculation)

## Report Output

```json
{
  "quarter": "Q2 2026",
  "start_date": "2026-04-01",
  "end_date": "2026-06-30",
  "start_price": 223.0,
  "end_price": 235.5,
  "price_return_pct": 5.61,
  "total_return_pct": 6.12,
  "dividends_per_share": 0.25,
  "highest_price": 240.0,
  "lowest_price": 218.5,
  "average_volume": 35000000
}
```

## Requirements

- Python 3.10+
- pandas
