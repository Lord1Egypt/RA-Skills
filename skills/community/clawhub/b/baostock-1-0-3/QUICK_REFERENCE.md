# BaoStock 快速参考

本文档提供最常用的 BaoStock API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 登录与登出

```python
import baostock as bs
import pandas as pd

lg = bs.login()
print(f"登录状态: {lg.error_code} {lg.error_msg}")

# ... 查询操作 ...

bs.logout()
```

## K线数据查询

```python
# 日K线
rs = bs.query_history_k_data_plus(
    "sh.600000",
    "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
    start_date='2024-01-01',
    end_date='2024-12-31',
    frequency="d",       # d=日, w=周, m=月, 5=5分钟, 15=15分钟, 30=30分钟, 60=60分钟
    adjustflag="3"        # 1=后复权, 2=前复权, 3=不复权
)
df = rs.get_data()

# 周K线
rs = bs.query_history_k_data_plus("sh.600000", "date,code,open,high,low,close,volume", start_date='2024-01-01', end_date='2024-12-31', frequency="w")
df_weekly = rs.get_data()
```

## 全部证券列表

```python
# 查询某日所有证券
rs = bs.query_all_stock(day="2024-12-31")
df = rs.get_data()
print(df.head())
```

## 交易日历

```python
# 查询交易日
rs = bs.query_trade_dates(start_date="2024-01-01", end_date="2024-12-31")
df = rs.get_data()
# is_trading_day: 1=交易日, 0=非交易日
trade_days = df[df['is_trading_day'] == '1']
```

## 行业分类

```python
# 查询行业分类
rs = bs.query_stock_industry()
df = rs.get_data()
print(df.head())
```

## 财务数据 & 指数成分

```python
# 盈利能力
rs = bs.query_profit_data(code="sh.600000", year=2024, quarter=3)

# 营运/成长/偿债能力
rs = bs.query_operation_data(code="sh.600000", year=2024, quarter=3)
rs = bs.query_growth_data(code="sh.600000", year=2024, quarter=3)
rs = bs.query_balance_data(code="sh.600000", year=2024, quarter=3)

# 沪深300 / 中证500 / 上证50 成分股
rs = bs.query_hs300_stocks(date="2024-12-31")
rs = bs.query_zz500_stocks(date="2024-12-31")
rs = bs.query_sz50_stocks(date="2024-12-31")
```

## 代码格式说明

- 上海证券交易所：`sh.600000`
- 深圳证券交易所：`sz.000001`

## 更多资源

- [BaoStock 官方文档](https://www.baostock.com/baostock/index.php)
- [BaoStock API 手册](https://www.baostock.com/baostock/index.php/Python_API文档)
