---
name: akshare
description: "Get Chinese financial data via AKShare. Trigger: stock data, A-share, fund, bond, futures, financial data, 股票数据, 基金, 债券, 期货, 财经数据, akshare."
---

# AKShare — 中国财经数据接口库

获取 A 股、港股、美股、期货、期权、基金、外汇、债券、指数、加密货币等金融产品的基本面数据、实时和历史行情数据。数据来源于公开财经网站（东方财富、新浪财经、上交所、深交所等），仅用于学术研究。

## 安装

```bash
pip install akshare pandas
```

验证安装：

```bash
python -c "import akshare; print(akshare.__version__)"
```

建议使用 Python 3.12+。接口经常更新，保持最新版本。

## 名称标注

- 东方财富: 简称东财

## 常用接口

### 股票行情

```python
import akshare as ak

# A 股实时行情（东财）
ak.stock_zh_a_spot_em()

# 港股实时行情
ak.stock_hk_spot_em()

# 美股实时行情
ak.stock_us_spot()

# A 股 K 线数据（日/周/月）
ak.stock_zh_a_hist(symbol="000001", period="daily",
    start_date="20250101", end_date="20251231", adjust="qfq")
```

### 期货数据

```python
# 中金所每日交易数据
ak.get_cffex_daily()
# 郑商所每日交易数据
ak.get_czce_daily()
# 大商所每日交易数据
ak.get_dce_daily()
# 广期所每日交易数据
ak.get_gfex_daily()
# 上海国际能源交易中心每日交易数据
ak.get_ine_daily()
# 四大交易所前 5/10/15/20 会员持仓排名
ak.get_rank_sum()
```

### 基金数据

```python
# 开放式基金实时行情（东财）
ak.fund_open_fund_daily_em()
# ETF 基金实时行情
ak.fund_etf_spot_em()
# 基金历史净值
ak.fund_etf_hist_em(symbol="510300", period="daily",
    start_date="20250101", end_date="20251231", adjust="qfq")
```

### 债券数据

```python
# 中国国债收益率（新浪）
ak.bond_gb_zh_sina()
# 美国国债收益率（新浪）
ak.bond_gb_us_sina()
```

### 外汇数据

```python
# 外汇实时行情
ak.fx_spot_quote()
# 外汇历史数据
ak.fx_hist_data(symbol="USDCNY")
```

### 指数数据

```python
# 中国股票指数
ak.index_zh_a_hist(symbol="000001", period="daily",
    start_date="20250101", end_date="20251231")
# 全球指数
ak.index_global_hist(symbol="NDX")
```

### 宏观经济

```python
# 中国宏观经济数据
ak.macro_china_gdp()
# 中国 CPI
ak.macro_china_cpi()
# 中国 PMI
ak.macro_china_pmi()
```

## 完整接口列表

AKShare 有数百个接口，涵盖：

- 股票（A 股/港股/美股/台股）
- 期货（中金所/郑商所/大商所/广期所/新交所）
- 期权（50ETF/300ETF/商品期权）
- 基金（开放/封闭/ETF/LOF/货基）
- 债券（国债/企业债/可转债/美债）
- 外汇（人民币/主要货币对）
- 指数（国内/全球）
- 加密货币
- 宏观经济（GDP/CPI/PMI/社融等）

完整接口列表参见 [references/api-list.md](references/api-list.md) 或 [AKShare 数据接口一览表](https://akshare.akfamily.xyz/tutorial.html)。

## 注意事项

1. **数据来源**: 数据来源于公开财经网站，仅用于学术研究
2. **商业风险**: 投资有风险，决策需谨慎
3. **更新频率**: 实时数据可能有延迟
4. **数据验证**: 应多数据源交叉验证，单一数据源的数据不可信
5. **时效性**: 仔细校验时间，错误的数据导致错误的决策

## 问题定位

- 接口报错或未找到 → 查看 [接口更新一览表](https://akshare.akfamily.xyz/changelog.html)，接口可能已更名
- 数据为空 → 检查日期参数格式（YYYYMMDD）
- 网络超时 → 重试或检查网络代理

## 参考文档

- [AKShare 文档](https://akshare.akfamily.xyz/)
- [AKShare GitHub](https://github.com/akfamily/akshare)
- [安装指导](https://akshare.akfamily.xyz/installation.html)
- [接口更新一览表](https://akshare.akfamily.xyz/changelog.html)
- [数据接口一览表](https://akshare.akfamily.xyz/tutorial.html)
