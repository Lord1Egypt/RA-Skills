---
name: baostock-skill
description: Query Chinese A-share market data using BaoStock. Use when user asks for stock quotes, historical K-line, fundamentals, or market analysis. Supports real-time quotation, daily/minute data, financial reports.
---

# BaoStock Finance Skill

This skill wraps BaoStock (http://baostock.com) to provide easy access to Chinese A-share market data. BaoStock is a stable domestic data source with no compilation requirements.

## What It Does

- **Real-time quotes**: Latest price, volume, change for A-shares
- **Historical data**: Daily, weekly, monthly, minute bars
- **K-line data**: OHLC with adjust factors (qfq, hfq)
- **Financial data**: Basic indicators, PE/PB, market cap
- **Index data**: SSE, SZSE, CSI indices
- **Stock basics**: List of A-shares, industry classification

## When to Use

User asks like:
- "查询贵州茅台最新股价"
- "获取宁德时代最近30天的日线数据"
- "列出所有银行股"
- "分析中国平安的市盈率"
- "获取上证指数历史数据"

## How to Invoke

```bash
# Single stock quote
baostock --symbol sh600519 --type quote

# Historical K-line (daily)
baostock --symbol sh600519 --type history --start-date 2024-01-01 --end-date 2024-12-31

# Minute data (5-minute intervals)
baostock --symbol sh600519 --type history --frequency 5 --start-date 2024-03-01

# Stock list (all A-shares)
baostock --type stock-list

# Index data
baostock --symbol sh000001 --type index-history --start-date 2024-01-01
```

## Dependencies

- Python 3.8+
- `baostock` package (pip install baostock)
- `pandas` (should be installed)

```bash
pip3 install baostock
```

## Data Source

BaoStock fetches data from BaoXin (宝新) data provider. It is:
- ✅ Domestic source, no external network issues
- ✅ Free for non-commercial use
- ✅ Supports minute-level data
- ⚠️ Some delay for real-time data (~15 min for minute bars)

## Output Format

Default: JSON

```json
{
  "symbol": "sh600519",
  "name": "贵州茅台",
  "price": 1680.50,
  "change": 1.23,
  "pct_change": 0.07,
  "volume": 1234567,
  "amount": 2000000000,
  "timestamp": "2025-03-18 15:00:00"
}
```

For historical data:
```json
[
  {
    "date": "2025-03-18",
    "open": 1670.00,
    "high": 1690.00,
    "low": 1668.50,
    "close": 1680.50,
    "volume": 1234567,
    "amount": 2000000000
  }
]
```

## Integration with OpenClaw

This skill can be assigned to `finance.yaml` role:

```yaml
plugins:
  allow:
    - baostock-skill
    - feishu-doc
    - feishu-bitable
```

## Limitations

- Real-time quotes are actually 15-min delayed (free tier)
- Some stocks may have missing data (new listings)
- No direct access to order book (Level 2)
- API rate limits: ~100 requests/minute

## Troubleshooting

| Issue | Check |
|-------|-------|
| Import error | `pip3 install baostock` |
| No data returned | Check symbol format (sh/sz prefix) and trading day |
| Network error | BaoStock uses domestic servers; should be fine |

## Examples

```bash
# Get all stock names and codes
baostock --type stock-list --output stocks.csv

# Get daily history for last 30 days
baostock --symbol sh600519 --type history --days 30

# Get 5-minute bars for today (if market open)
baostock --symbol sh600519 --type history --frequency 5
```