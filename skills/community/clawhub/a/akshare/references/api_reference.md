# AKShare API Reference

Quick reference for commonly used AKShare functions.

## Stock Data

### Real-time Quotes

```python
# All A-shares real-time
ak.stock_zh_a_spot_em()
# Returns: DataFrame with columns [代码, 名称, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, ...]

# Individual stock info
ak.stock_individual_info_em(symbol="000001")
# Returns: DataFrame with stock basic information
```

### Historical K-line

```python
ak.stock_zh_a_hist(
    symbol="000001",           # Stock code (6 digits)
    period="daily",            # "daily", "weekly", "monthly"
    start_date="20200101",     # YYYYMMDD format
    end_date="20231231",       # YYYYMMDD format
    adjust="qfq"               # "qfq"=forward, "hfq"=backward, ""=none
)
# Returns: DataFrame with columns [日期, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅, 涨跌幅, 涨跌额, 换手率]
```

### Index Data

```python
# Shanghai Composite Index
ak.stock_zh_index_daily(symbol="sh000001")

# Shenzhen Component Index
ak.stock_zh_index_daily(symbol="sz399001")

# ChiNext Index
ak.stock_zh_index_daily(symbol="sz399006")

# Returns: DataFrame with columns [date, open, high, low, close, volume]
```

## Fund Data

### Fund Rankings

```python
ak.fund_open_fund_rank_em(symbol="全部")
# symbol options: "全部", "股票型", "混合型", "债券型", "指数型", "QDII", "FOF"
# Returns: DataFrame with fund rankings and performance
```

### Fund Net Value

```python
ak.fund_open_fund_info_em(fund="000001", indicator="单位净值走势")
# indicator options: "单位净值走势", "累计净值走势", "累计收益率走势", "同类排名走势", "同类排名百分比走势"
# Returns: DataFrame with historical net values
```

### ETF Data

```python
ak.fund_etf_spot_em()
# Returns: DataFrame with ETF real-time quotes
```

## Futures Data

### Futures Quotes

```python
ak.futures_zh_spot(symbol="主力合约")
# symbol options: "主力合约", "中金所", "上期所", "大商所", "郑商所"
# Returns: DataFrame with futures real-time quotes
```

### Futures Historical

```python
ak.futures_zh_daily_sina(symbol="CU0", start_date="20230101", end_date="20231231")
# symbol: Futures code (e.g., "CU0" for copper main contract)
# Returns: DataFrame with columns [date, open, high, low, close, volume, hold]
```

## Macroeconomic Data

### GDP

```python
ak.macro_china_gdp()
# Returns: DataFrame with quarterly GDP data
```

### CPI

```python
ak.macro_china_cpi()
# Returns: DataFrame with monthly CPI data
```

### PMI

```python
ak.macro_china_pmi()
# Returns: DataFrame with monthly manufacturing PMI
```

### Money Supply

```python
ak.macro_china_money_supply()
# Returns: DataFrame with M0, M1, M2 data
```

### Foreign Exchange Reserves

```python
ak.macro_china_fx_reserves()
# Returns: DataFrame with monthly FX reserves
```

### Interest Rates

```python
ak.macro_china_shibor()
# Returns: DataFrame with Shibor rates
```

## US Market Data

### US Stocks

```python
ak.stock_us_daily(symbol="AAPL", adjust="qfq")
# Returns: DataFrame with US stock historical data
```

### US GDP

```python
ak.macro_usa_gdp()
# Returns: DataFrame with US GDP data
```

## Common Data Columns

### Stock Historical Data (stock_zh_a_hist)
- 日期: Date
- 开盘: Open
- 收盘: Close
- 最高: High
- 最低: Low
- 成交量: Volume
- 成交额: Amount
- 振幅: Amplitude
- 涨跌幅: Change %
- 涨跌额: Change Amount
- 换手率: Turnover Rate

### Stock Real-time Data (stock_zh_a_spot_em)
- 代码: Code
- 名称: Name
- 最新价: Latest Price
- 涨跌幅: Change %
- 涨跌额: Change Amount
- 成交量: Volume
- 成交额: Amount
- 今开: Open
- 昨收: Previous Close
- 最高: High
- 最低: Low

## Tips

1. **Rate Limiting**: Add `time.sleep(1)` between requests
2. **Data Validation**: Always check for missing values
3. **Encoding**: Use `encoding='utf-8-sig'` when saving to CSV
4. **Stock Codes**: Use 6-digit format without exchange prefix
5. **Date Format**: Use YYYYMMDD string format (e.g., "20230101")
