# AKShare API 快速参考

本文档提供最常用的 AKShare API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 初始化

```python
import akshare as ak
# 无需配置 Token，直接调用
```

## A股实时行情

```python
# 全A股实时行情（东方财富）
df = ak.stock_zh_a_spot_em()
# 返回字段：代码、名称、最新价、涨跌幅、成交量、成交额等
```

## A股历史K线

```python
# 日K线（前复权）
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20240101", end_date="20241231", adjust="qfq")

# 周K线
df = ak.stock_zh_a_hist(symbol="000001", period="weekly", start_date="20240101", end_date="20241231", adjust="qfq")

# 不复权
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20240101", end_date="20241231", adjust="")
```

## 港股K线

```python
# 港股历史K线
df = ak.stock_hk_hist(symbol="00700", period="daily", start_date="20240101", end_date="20241231", adjust="qfq")
```

## 美股日线

```python
# 美股日线数据
df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
```

## ETF实时行情

```python
# ETF实时行情
df = ak.fund_etf_spot_em()
```

## 指数数据

```python
# A股指数历史行情
df = ak.index_zh_a_hist(symbol="000300", period="daily", start_date="20240101", end_date="20241231")
```

## 宏观经济数据

```python
# GDP年度数据
df = ak.macro_china_gdp_yearly()

# CPI月度数据
df = ak.macro_china_cpi_monthly()
```

## 个股新闻

```python
# 个股新闻（东方财富）
df = ak.stock_news_em(symbol="000001")
```

## 期货数据

```python
# 期货日线（新浪）
df = ak.futures_zh_daily_sina(symbol="RB0")
```

## 更多接口

完整接口列表请查看：
- [AKShare 官方文档](https://akshare.akfamily.xyz)
- [GitHub](https://github.com/akfamily/akshare)
