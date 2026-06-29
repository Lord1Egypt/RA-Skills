# AKShare API Reference for Finance Daily Report v2.0

## Installation

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple akshare pandas --trusted-host pypi.tuna.tsinghua.edu.cn
```

## Core APIs Used (v1.18+)

### 1. A-Share Index Spot Data
```python
ak.stock_zh_index_spot_em()
# Columns: 代码, 名称, 最新价, 涨跌幅, 涨跌额, 成交量, 成交额, 今开, 昨收, 最高, 最低
# Note: May have connection issues. Script includes 3-retry fallback.
```

### 2. HK Index Spot (Sina source - more reliable)
```python
ak.stock_hk_index_spot_sina()
# Columns: name, value, 涨跌幅, 涨跌额
# Target: '恒生指数', '恒生科技指数'
```

### 3. Industry Sector Rankings
```python
ak.stock_board_industry_spot_em()
# Columns: 板块名称, 最新价, 涨跌幅, 涨跌额, 总市值, 换手率, 上涨家数, 下跌家数, 领涨股票, 领涨股票-涨跌幅
```

### 4. North-Bound Capital Flow
```python
ak.stock_hsgt_hist_em(symbol='沪股通')
# Columns: 日期, 当日成交净买额, 买入成交额, 卖出成交额, 历史累计净买额, 当日资金流入, 当日余额, 持股市值, 领涨股, 领涨股-涨跌幅, 上证指数, 上证指数-涨跌幅, 领涨股-代码
# Note: '当日成交净买额' is the net buy amount we care about
```

### 5. Market Turnover
```python
ak.stock_zh_a_spot_em()
# Columns include: 成交额
# Sum all 成交额 values and convert to 亿元
```

### 6. Foreign Exchange
```python
ak.fx_spot_quote()
# Columns: 货币对, 买报价, 卖报价
# Filter: 'USD/CNY', 'EUR/CNY'
# Note: No 涨跌幅 column; change_pct set to 0.0
```

### 7. Global Commodities
```python
ak.futures_global_spot_em()
# Columns: 序号, 代码, 名称, 最新价, 涨跌额, 涨跌幅, 今开, 最高, 最低, 昨结, 成交量, 买盘, 卖盘, 持仓量
# Filter for: 黄金 (XAU), 原油 (CL/WTI/Brent)
```

### 8. Financial News
```python
ak.stock_news_em()
# Columns: 关键词, 新闻标题, 新闻内容, 发布时间, 文章来源, 新闻链接
# Use top 10 headlines
```

## Network Issues

East Money APIs (stock_zh_index_spot_em, stock_board_industry_spot_em, stock_zh_a_spot_em) may have connection issues in China. The script includes:
- Automatic 3-retry with 1.5s delay
- Graceful degradation (failed modules show "暂无数据" in report)
- Sina-based fallback for HK indices (stock_hk_index_spot_sina)

## Version Compatibility

- Tested with: akshare 1.18.64, pandas 3.0.3, Python 3.13
- Known issue: `futures_zh_spot()` broken in 1.18.64 due to pandas 3.x column assignment bug
- Known issue: `stock_financial_calendar()` not available; calendar uses static fallback text
