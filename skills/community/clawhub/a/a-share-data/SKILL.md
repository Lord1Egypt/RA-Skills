---
name: "a-share-data"
description: "A股数据层：行情/财务/板块/资金流向/K线，多数据源自动切换（AkShare/东方财富/新浪/腾讯），纯数据接口"
user-invocable: true
metadata:
  openclaw:
    emoji: "📡"
    tags: ["a-share", "data", "akshare", "eastmoney", "finance"]
---

# A-Share Data v2.0 — A股全能数据接口

## 定位

A 股数据的**唯一数据层 skill**。分析/交易 skill 通过本 skill 获取数据。纯数据，不做判断。

## 数据源层次

| 层 | 源 | 覆盖 | 特点 |
|----|----|------|------|
| 1 主力 | 东方财富（AkShare） | A股全量 | 最全最快，免费 |
| 2 备用 | 腾讯财经 | 行情 | 稳定快速 |
| 3 备用 | 新浪财经 | 行情+指数 | 老牌可靠 |
| 4 备用 | 雪球 | 行情+市值 | 有市盈率 |
| 5 扩展 | Tushare | 全量 | 需积分 |
| 6 跨市场 | yfinance | 港股/美股/ETF | 免费有限流 |
| 7 兜底 | Baostock | 基础行情 | 无需网络配置 |

### 容错策略
每个源内尝试 ≥3 种不同方法，全部失败才切换。首次失败不判定为不可用。

---

## 1. 实时行情

```python
import akshare as ak
df = ak.stock_zh_a_spot_em()                          # 全A股实时
df[df['代码'] == '600519']                             # 单只筛选
```

回退：`https://hq.sinajs.cn/list=sh600519` / `https://qt.gtimg.cn/q=sh600519`

---

## 2. 历史K线

```python
df = ak.stock_zh_a_hist(symbol="000001", period="daily",
    start_date="20240101", end_date="20241231", adjust="qfq")
# period: daily/weekly/monthly  adjust: qfq/hfq/不复权
```

---

## 3. 财务数据

```python
df = ak.stock_financial_analysis_indicator(symbol="000001")  # 核心指标
df = ak.stock_financial_abstract_ths(symbol="000001", indicator="按报告期")
```

---

## 4. 板块/行业

```python
ak.stock_board_industry_name_em()              # 行业板块行情
ak.stock_board_concept_name_em()               # 概念板块行情
ak.stock_board_industry_cons_em(symbol="半导体") # 板块成分股
```

---

## 5. 资金流向

```python
ak.stock_individual_fund_flow(stock="000001", market="sh")
```

---

## 6. 龙虎榜

```python
ak.stock_lhb_detail_em(date="20240930")        # 每日龙虎榜
ak.stock_zlzj_em()                              # 机构调研
```

---

## 7. 新股/IPO

```python
ak.stock_new_ipo_em()
```

---

## 8. 融资融券

```python
ak.stock_margin_sse(symbol="600000")
ak.stock_rzrq_detail_em(symbol="600000", date="20240930")
```

---

## 9. 筹码分布

```python
ak.stock_cyq_em(symbol="000001")
```

---

## 10. 指数

```python
ak.stock_zh_index_daily_em(symbol="sh000001")  # 上证
# 新浪: sh000001(上证) sh000300(沪深300) sz399006(创业板) sh000688(科创50) sh000016(上证50)
```

---

## 11. 跨市场（yfinance）

```python
import yfinance as yf
ticker = yf.Ticker("0700.HK")      # 港股
ticker = yf.Ticker("AAPL")         # 美股
ticker = yf.Ticker("510050.SS")    # A股ETF
info = ticker.info                 # 基本信息
hist = ticker.history(period="1mo") # 近月K线
```

---

## 12. 外汇

```python
usd_cny = yf.Ticker("CNY=X")
rate = usd_cny.fast_info.get("lastPrice")
```

---

## 安装

```bash
pip install akshare baostock yfinance
```

---

## 使用原则

1. 纯数据层，只取数、不分析、不给投资建议
2. 标注数据来源和更新时间
3. 失败时在同源换方法 ≥3 次再切换
4. 数据仅供学习研究
