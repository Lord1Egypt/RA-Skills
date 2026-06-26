---
name: akshare-cn-market
description: 中国A股行情与宏观经济数据工具，基于 AKShare 库。支持个股K线、大盘指数、财务摘要、GDP/CPI/PMI/M2货币供应、中美国债收益率等。
runtime: python3
---

# AKShare 中国市场数据

## 安装依赖

```bash
pip install akshare pandas
# 验证
python3 -c "import akshare; print(akshare.__version__)"
```

## 脚本用法

### 股票行情（scripts/stock.py）

```bash
# 个股历史K线（默认最近10条日线，前复权）
python3 scripts/stock.py hist 000001
python3 scripts/stock.py hist 600519 --n 20 --start 20240101

# 大盘指数K线（新浪源）
python3 scripts/stock.py index sh000001      # 上证综指
python3 scripts/stock.py index sh000300      # 沪深300
python3 scripts/stock.py index sz399001      # 深证成指
python3 scripts/stock.py index sh000016 --n 5   # 上证50，最近5条

# 个股财务摘要（近5年）
python3 scripts/stock.py financial 000001
python3 scripts/stock.py financial 600519
```

### 宏观数据（scripts/macro.py）

```bash
# GDP 季度数据（默认最近8季度）
python3 scripts/macro.py gdp
python3 scripts/macro.py gdp --n 4

# CPI 月度数据（默认最近12个月）
python3 scripts/macro.py cpi

# PMI（制造业 + 非制造业，默认最近12个月）
python3 scripts/macro.py pmi

# 货币供应量 M0/M1/M2（默认最近12个月）
python3 scripts/macro.py money

# 中美国债收益率（默认最近10个交易日）
python3 scripts/macro.py bond --n 5
```

### 交易日历（scripts/trade_cal.py）

```bash
# 判断今天是否为交易日
python3 scripts/trade_cal.py check today

# 判断指定日期
python3 scripts/trade_cal.py check 2026-03-01

# 当天或之后最近的交易日
python3 scripts/trade_cal.py next today
python3 scripts/trade_cal.py next 2026-02-01

# 当天或之前最近的交易日（获取最近一个收盘日）
python3 scripts/trade_cal.py prev today

# 列出区间内所有交易日
python3 scripts/trade_cal.py range 2026-03-02 2026-03-06
```

数据来源：新浪财经，覆盖 1990-12-19 至 2026-12-31。

## 在 Agent 中直接调用

```python
import akshare as ak

# A股个股K线
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20240101", adjust="qfq")

# 大盘指数（新浪源，不受东方财富代理限制）
df = ak.stock_zh_index_daily(symbol="sh000001")

# 宏观：GDP / CPI / PMI / 货币供应
df = ak.macro_china_gdp()
df = ak.macro_china_cpi()
df = ak.macro_china_pmi()
df = ak.macro_china_money_supply()

# 中美国债收益率
df = ak.bond_zh_us_rate()

# 交易日判断（覆盖至2026年底）
from scripts.trade_cal import is_trade_day, next_trade_day, prev_trade_day
if not is_trade_day("2026-03-02"):
    print("非交易日，跳过")
last_close = prev_trade_day("2026-03-02")  # 最近一个收盘日

# 个股财务摘要（同花顺）
df = ak.stock_financial_abstract_ths(symbol="000001", indicator="按年度")
```

## 返回格式

所有脚本输出均为 JSON 数组（每条记录一个对象）。

## 常用指数代码

| 代码 | 指数 |
|------|------|
| sh000001 | 上证综指 |
| sz399001 | 深证成指 |
| sh000300 | 沪深300 |
| sh000016 | 上证50 |
| sh000905 | 中证500 |

## 超短复盘专用接口（已验证可用）

### 情绪数据

```python
# 涨停板池（含连板数、封板时间、炸板次数）
df = ak.stock_zt_pool_em(date="20260302")      # 格式 YYYYMMDD
# 字段: 代码, 名称, 涨跌幅, 换手率, 封板资金, 首次封板时间, 炸板次数, 连板数, 所属行业

# 强势股池（60日新高 + 涨停候选）
df = ak.stock_zt_pool_strong_em(date="20260302")

# 跌停板池
df = ak.stock_zt_pool_dtgc_em(date="20260302")

# 昨日涨停（用于次日跟踪）
df = ak.stock_zt_pool_previous_em(date="20260302")
```

### 龙虎榜

```python
# 龙虎榜明细（含游资席位、净买额）
df = ak.stock_lhb_detail_em(start_date="20260302", end_date="20260302")
# 字段: 代码, 名称, 涨跌幅, 龙虎榜净买额, 上榜原因, 上榜后1/2/5/10日

# 游资席位统计
df = ak.stock_lhb_traderstatistic_em(period="近一月")
```

### 资金流向

```python
# 全市场主力资金流向（历史，按日）
df = ak.stock_market_fund_flow()
# 字段: 日期, 主力净流入-净额, 超大单净流入-净额, 大单净流入-净额

# 板块资金流向排名
df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="概念资金流向")
df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流向")  # 可能代理受限
```

### 北向资金

```python
# 北向资金历史（沪深300同步）
df = ak.stock_hsgt_hist_em(symbol="北向资金")
# 字段: 日期, 当日成交净买额, 持股市值, 领涨股, 沪深300-涨跌幅
# ⚠️ 当日成交净买额近期可能为 nan（数据源问题），用持股市值环比估算
```

### ⚠️ 网络限制说明

| 接口类型 | 可用性 | 说明 |
|----------|--------|------|
| 新浪源指数K线 | ✅ 稳定 | `stock_zh_index_daily` |
| 涨停板池/龙虎榜 | ✅ 稳定 | 东方财富历史数据接口 |
| 主力资金流向历史 | ✅ 稳定 | `stock_market_fund_flow` |
| 北向资金历史 | ✅ 可用（部分字段nan） | `stock_hsgt_hist_em` |
| 板块实时排行 | ❌ 代理受限 | 东方财富push接口被SSRF策略拦截 |

## 注意事项

- **数据来源**：公开财经网站，仅供研究参考
- **网络要求**：新浪源指数 + 历史数据接口稳定；东方财富 push 实时接口在 sandbox 被代理拦截
- **数据延迟**：日线数据次日可用；实时行情不可用
- **投资风险**：数据仅供参考，投资决策请自行判断
