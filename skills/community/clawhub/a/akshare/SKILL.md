---
name: akshare
description: Fetch Chinese stock market data (A-shares, Hong Kong stocks, futures, funds, macroeconomic indicators) using AKShare library. Use when you need to get real-time or historical financial data from Chinese markets, including stock prices, trading volumes, financial statements, fund data, futures data, or macroeconomic statistics. Supports daily/weekly/monthly K-line data, stock fundamentals, market indices, and more. No API key required - completely free.
---

# AKShare - Chinese Financial Data

AKShare is a free, open-source Python library for accessing Chinese financial market data.

## Quick Start

```python
import akshare as ak

# Get A-share real-time quotes
stock_spot = ak.stock_zh_a_spot_em()

# Get historical K-line data (with forward adjustment)
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                        start_date="20200101", end_date="20231231", 
                        adjust="qfq")
```

## Core Functions

### Stock Data

**Real-time quotes:**
```python
# All A-shares
ak.stock_zh_a_spot_em()

# Individual stock info
ak.stock_individual_info_em(symbol="000001")
```

**Historical data:**
```python
# Daily K-line (symbol without exchange prefix)
ak.stock_zh_a_hist(
    symbol="000001",      # Stock code
    period="daily",       # daily/weekly/monthly
    start_date="20200101",
    end_date="20231231",
    adjust="qfq"         # qfq=forward, hfq=backward, ""=none
)
```

**Index data:**
```python
# Shanghai Composite
ak.stock_zh_index_daily(symbol="sh000001")

# Shenzhen Component
ak.stock_zh_index_daily(symbol="sz399001")
```

### Fund Data

```python
# Fund rankings
ak.fund_open_fund_rank_em(symbol="全部")

# Fund net value history
ak.fund_open_fund_info_em(fund="000001", indicator="单位净值走势")

# ETF real-time quotes
ak.fund_etf_spot_em()
```

### Futures Data

```python
# Futures real-time quotes
ak.futures_zh_spot(symbol="主力合约")

# Futures historical data
ak.futures_zh_daily_sina(symbol="CU0", start_date="20230101", end_date="20231231")
```

### Macroeconomic Data

```python
# GDP
ak.macro_china_gdp()

# CPI
ak.macro_china_cpi()

# PMI
ak.macro_china_pmi()

# Money supply
ak.macro_china_money_supply()
```

## Important Notes

### Rate Limiting
- AKShare scrapes public websites - add delays between requests
- Recommended: `time.sleep(1)` between calls
- Batch downloads may trigger rate limits

### Data Quality
- Free data may have occasional gaps or errors
- For production use, consider Tushare Pro (paid)
- Always validate critical data

### Stock Code Format
- Use 6-digit code without exchange prefix: `"000001"` not `"sz000001"`
- Index codes need prefix: `"sh000001"`, `"sz399001"`

## Common Patterns

**Get multiple stocks:**
```python
import time

stocks = ["000001", "600519", "000858"]
data = {}

for code in stocks:
    data[code] = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
    time.sleep(1)  # Avoid rate limiting
```

**Calculate returns:**
```python
df = ak.stock_zh_a_hist(symbol="000001", period="daily", adjust="qfq")
df['日收益率'] = df['收盘'].pct_change() * 100
total_return = ((df['收盘'].iloc[-1] / df['收盘'].iloc[0]) - 1) * 100
```

## Resources

- **Installation**: `pip install akshare --upgrade`
- **Official docs**: https://akshare.akfamily.xyz/
- **GitHub**: https://github.com/akfamily/akshare
- **Example scripts**: See `scripts/` directory
- **API reference**: See `references/api_reference.md`

## When to Use

Use AKShare when:
- Getting Chinese market data (A-shares, Hong Kong, futures)
- No budget for paid data services
- Prototyping or learning quantitative strategies
- Need macroeconomic indicators

Consider alternatives when:
- Need guaranteed data stability (use Tushare Pro)
- High-frequency trading (use professional data feeds)
- Need real-time tick data (use broker APIs)
