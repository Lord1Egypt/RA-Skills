# akshare API Quick Reference

akshare is a free, no-token-required Python library for Chinese financial data.

## Install
```bash
pip install akshare pandas
```

## Key Interfaces

### ETF Data

| Function | Parameters | Returns |
|----------|-----------|---------|
| `ak.fund_etf_hist_em(symbol)` | symbol="159915", period="daily", start_date, end_date | OHLCV DataFrame |
| `ak.fund_etf_hist_min_em(symbol)` | symbol="159915", period="1" (1/5/15/30/60 min) | Intraday OHLCV |
| `ak.fund_etf_spot_em()` | — | All ETF realtime quotes |
| `ak.fund_etf_category_sina(symbol)` | symbol="ETF基金" | ETF list by category |

### Stock Data

| Function | Parameters | Returns |
|----------|-----------|---------|
| `ak.stock_zh_a_hist(symbol)` | symbol="000001", period="daily", start_date, end_date | OHLCV DataFrame |
| `ak.stock_zh_a_spot_em()` | — | All A-share realtime quotes |
| `ak.stock_individual_info_em(symbol)` | symbol="000001" | Stock basic info |
| `ak.stock_board_concept_name_em()` | — | Concept sector list |
| `ak.stock_board_concept_cons_em(symbol)` | symbol="AI手机" | Sector constituents |

### Index Data

| Function | Parameters | Returns |
|----------|-----------|---------|
| `ak.index_zh_a_hist(symbol)` | symbol="000300", period="daily" | Index OHLCV |
| `ak.stock_index_pe_lg(symbol)` | symbol="上证50" | PE/PB valuation |
| `ak.index_stock_cons(symbol)` | symbol="000300" | Index constituents |

### Market Breadth

| Function | Returns |
|----------|---------|
| `ak.stock_market_activity_legu()` | Market activity metrics |
| `ak.stock_zt_pool_em(date)` | Limit-up stocks |
| `ak.stock_zt_pool_dtgc_em(date)` | Limit-up then opened stocks |
| `ak.stock_rank_lxsz_ths()` | Rising/falling stock count |

## Common Patterns

### Fetch ETF daily data
```python
import akshare as ak
df = ak.fund_etf_hist_em(
    symbol="159915",
    period="daily",
    start_date="20250101",
    end_date="20260324",
    adjust="qfq"  # 前复权
)
```

### Fetch intraday 1-minute
```python
df = ak.fund_etf_hist_min_em(
    symbol="159915",
    period="1",
    adjust="qfq"
)
```

### Standard column names (rename after fetch)
```python
df = df.rename(columns={
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "涨跌幅": "pct_chg",
})
```

### Check trading hours
```python
from datetime import datetime
now = datetime.now()
# A-share: 09:30-11:30, 13:00-15:00
# ETF: same, but some have extended hours
```

## Rate Limits
- akshare uses web scraping — respect rate limits
- Add `time.sleep(0.5)` between batch requests
- Cache results locally when possible

## Error Handling
```python
import akshare as ak
try:
    df = ak.fund_etf_hist_em(symbol="159915", period="daily")
    if df.empty:
        print("No data returned — check symbol or date range")
except Exception as e:
    print(f"Fetch failed: {e}")
    # Fallback: try again after delay, or use cached data
```
