# Indicator Mapping Reference

## Overview

This document provides the complete mapping of financial indicators to data sources and symbols.

## Data Sources

### Yahoo Finance
- Free, no API key required
- Covers: commodities futures, stock indices, ETFs, forex
- Data availability: Typically 10-30 years for major assets
- Update frequency: Daily

### FRED (Federal Reserve Economic Data)
- Requires API key (set `FRED_API_KEY` environment variable)
- Covers: US macroeconomic data
- Data availability: Decades of historical data
- Update frequency: Monthly/Quarterly

### Tushare
- Requires API token (set `TUSHARE_TOKEN` environment variable)
- Covers: A-share indices, Chinese market data
- Registration: https://tushare.pro/register
- Data availability: Since 1990 for indices

---

## Complete Indicator List

### Commodities (Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `brent_crude` | BZ=F | Brent Crude Oil | Global oil benchmark |
| `wti_crude` | CL=F | WTI Crude Oil | US oil benchmark |
| `gold` | GC=F | Gold Futures | Precious metal |
| `silver` | SI=F | Silver Futures | Precious metal |
| `copper` | HG=F | Copper Futures | Industrial metal |
| `aluminum` | ALI=F | Aluminum Futures | Industrial metal |
| `natural_gas` | NG=F | Natural Gas | Energy commodity |

### US Market Indices (Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `sp500` | ^GSPC | S&P 500 | Large-cap US stocks |
| `nasdaq` | ^IXIC | NASDAQ Composite | Tech-heavy index |
| `dow_jones` | ^DJI | Dow Jones Industrial | 30 large stocks |
| `russell2000` | ^RUT | Russell 2000 | Small-cap index |
| `vix` | ^VIX | VIX Index | Volatility index |

### US Sector ETFs (Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `xlk` | XLK | Technology ETF | Tech sector |
| `xle` | XLE | Energy ETF | Energy sector |
| `xlf` | XLF | Financial ETF | Banks, insurers |
| `xlv` | XLV | Healthcare ETF | Healthcare sector |
| `xli` | XLI | Industrial ETF | Industrials |
| `jets` | JETS | Airlines ETF | Aviation sector |
| `iyr` | IYR | Real Estate ETF | REITs |

### Foreign Exchange (Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `usd_cny` | CNY=X | USD/CNY | US dollar to Chinese yuan |
| `usd_index` | DX-Y.NYB | US Dollar Index | Dollar strength vs basket |
| `eur_usd` | EURUSD=X | EUR/USD | Euro to US dollar |

### US Treasury Yields (Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `us_10y_treasury` | ^TNX | 10-Year Treasury | Long-term rates |
| `us_2y_treasury` | ^FVX | 2-Year Treasury | Short-term rates |

### FRED Macro Data

| Indicator ID | FRED Code | Name | Description |
|-------------|-----------|------|-------------|
| `fed_funds_rate` | FEDFUNDS | Federal Funds Rate | Fed policy rate |
| `cpi_us` | CPIAUCSL | US CPI | Consumer inflation |
| `gdp_us` | GDP | US GDP | Economic output |
| `unemployment_us` | UNRATE | Unemployment Rate | Labor market |
| `oil_production_us` | IPG2111111SQ | Oil Production | US oil output |

### A-Share Indices (Tushare)

| Indicator ID | Tushare Code | Name | Description |
|-------------|--------------|------|-------------|
| `csi300` | 000300.SH | CSI 300 Index | Large-cap A-shares |
| `sse_composite` | 000001.SH | Shanghai Composite | SSE benchmark |
| `chinext` | 399006.SZ | ChiNext Index | Growth stocks |
| `sse50` | 000016.SH | SSE 50 Index | Top 50 SSE stocks |

---

## 🌍 多经济体指标扩展 (Multi-Economy Indicators)

### 中国市场 (China - Tushare)

| Indicator ID | Tushare Code | Name | Description |
|-------------|--------------|------|-------------|
| `csi300` | 000300.SH | 沪深300 | A股核心资产 |
| `sse_composite` | 000001.SH | 上证指数 | A股主板基准 |
| `chinext` | 399006.SZ | 创业板指 | 成长股代表 |
| `sse50` | 000016.SH | 上证50 | 超大盘蓝筹 |
| `csi500` | 000905.SH | 中证500 | 中小盘代表 |
| `csi1000` | 000852.SH | 中证1000 | 小盘股 |
| `shanghai_tech` | 000688.SH | 科创50 | 科技创新板 |
| **中国宏观 (Tushare)** ||||
| `cpi_china` | CPI月度数据 | 中国CPI | 居民消费价格指数 |
| `ppi_china` | PPI月度数据 | 中国PPI | 工业生产者价格指数 |
| `gdp_china` | GDP季度数据 | 中国GDP | 国内生产总值 |
| `m2_china` | M2月度数据 | 中国M2 | 广义货币供应量 |
| `m1_china` | M1月度数据 | 中国M1 | 狭义货币供应量 |
| `social_financing` | 社融月度数据 | 社会融资规模 | 信用扩张指标 |
| `pmi_china` | PMI月度数据 | 中国PMI | 制造业采购经理指数 |
| `loan_rate_china` | LPR数据 | 中国LPR | 贷款市场报价利率 |
| `bond_10y_china` | 10年期国债收益率 | 中国10Y国债 | 长期无风险利率 |

### 日本市场 (Japan - Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `nikkei225` | ^N225 | 日经225 | 日本核心股指 |
| `topix` | ^TPX | TOPIX | 东证指数 |
| `japan_10y_bond` | ^JP10Y | 日本10Y国债 | 长期利率 |
| `usd_jpy` | JPY=X | USD/JPY | 美元兑日元 |
| **日本宏观 (FRED)** ||||
| `gdp_japan` | JPNNGDP | 日本GDP | 经济产出 |
| `cpi_japan` | JPNCPIALLMINMEI | 日本CPI | 消费通胀 |
| `m2_japan` | MYAGM2JPJPM189N | 日本M2 | 货币供应量 |

### 韩国市场 (Korea - Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `kospi` | ^KS11 | 韩国综合指数 | KOSPI主板 |
| `kosdaq` | ^KQ11 | 韩国创业板 | KOSDAQ成长 |
| `usd_krw` | KRW=X | USD/KRW | 美元兑韩元 |
| **韩国宏观 (FRED)** ||||
| `gdp_korea` | KORNGDP | 韩国GDP | 经济产出 |
| `cpi_korea` | KORCPIALLMINMEI | 韩国CPI | 消费通胀 |

### 欧洲市场 (Europe - Yahoo Finance)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `eu_stoxx50` | ^STOXX50E | 欧洲斯托克50 | 欧元区蓝筹 |
| `dax` | ^GDAXI | 德国DAX | 德国核心股指 |
| `cac40` | ^FCHI | 法国CAC40 | 法国核心股指 |
| `ftse100` | ^FTSE | 英国富时100 | 英国核心股指 |
| `ftse_mib` | ^FTSEMIB | 意大利MIB | 意大利股指 |
| `ibex35` | ^IBEX | 西班牙IBEX35 | 西班牙股指 |
| `eur_usd` | EURUSD=X | EUR/USD | 欧元兑美元 |
| `gbp_usd` | GBPUSD=X | GBP/USD | 英镑兑美元 |
| `euro_10y_bond` | ^DE10Y | 德国10Y国债 | 欧元区基准利率 |
| **欧洲宏观 (FRED)** ||||
| `gdp_eurozone` | EURNGDP | 欧元区GDP | 经济产出 |
| `cpi_eurozone` | CPALTT01EZQ657N | 欧元区CPI | 消费通胀 |
| `m2_eurozone` | MYAGM2EZM196N | 欧元区M2 | 货币供应量 |

### 亚太新兴市场 (Asia-Pacific Emerging)

| Indicator ID | Symbol | Name | Description |
|-------------|--------|------|-------------|
| `hsi` | ^HSI | 恒生指数 | 港股基准 |
| `hsi_tech` | ^HSTECH | 恒生科技 | 港股科技股 |
| `hang_seng_china` | ^HSCEI | 恒生中国企业 | H股指数 |
| `sgx_nifty` | ^NSEI | 印度Nifty50 | 印度股指 |
| `sensex` | ^BSESN | 印度BSE Sensex | 孟买指数 |
| `jakarta` | ^JKSE | 雅加达指数 | 印尼股指 |
| `bangkok` | ^BKSETI | 泰国SET指数 | 泰国股指 |
| `usd_hkd` | HKD=X | USD/HKD | 美元兑港币 |

---

## 🌐 多经济体因果分析映射表

### 油价暴涨影响 → 多经济体传导

| 经济体 | 受益指标 | 受损指标 | 传导机制 |
|-------|---------|---------|---------|
| **中国** | 能源ETF (159930)、石油石化股 | 航空股、化工股、运输股 | 进口依赖→成本上升 |
| **日本** | 能源股、日元贬值(出口利好) | 航空股、制造业股 | 能源进口依赖 |
| **韩国** | 能源股、韩元贬值(出口利好) | 化工股、航空股 | 能源进口依赖 |
| **欧洲** | 能源股(壳牌、BP) | 航空股、汽车股、化工股 | 能源进口依赖 |
| **印度** | 能源股(Reliance) | 航空股、化肥股 | 高进口依赖 |

### 美元走强 → 多经济体传导

| 经济体 | 受益指标 | 受损指标 | 传导机制 |
|-------|---------|---------|---------|
| **中国** | 出口股(家电、纺织) | A股整体、USD/CNY贬值压力 | 资本流出压力 |
| **日本** | 出口股(汽车、电子) | 日股整体、USD/JPY贬值压力 | 资本流出压力 |
| **韩国** | 出口股(半导体、电子) | 韩股整体、USD/KRW贬值压力 | 资本流出压力 |
| **欧洲** | 出口股(奢侈品、汽车) | 欧股整体、EUR/USD贬值压力 | 资本流出压力 |
| **新兴市场** | - | 本币贬值、资本流出 | 美元债务压力 |

### 利率上升 → 多经济体传导

| 经济体 | 受益指标 | 受损指标 | 传导机制 |
|-------|---------|---------|---------|
| **中国** | 银行股、保险股 | 成长股、地产股、高杠杆股 | LPR上行压力 |
| **日本** | 银行股、保险股 | 成长股、高杠杆股 | 虽负利率，但利率上行趋势影响估值 |
| **韩国** | 银行股、保险股 | 成长股、地产股 | 利率联动 |
| **欧洲** | 银行股、保险股 | 成长股、地产股、高杠杆股 | 欧央行政策联动 |

### 通胀上升 → 多经济体传导

| 经济体 | 受益指标 | 受损指标 | 传导机制 |
|-------|---------|---------|---------|
| **中国** | 抗通胀资产(黄金、白酒) | 高估值成长股、消费股 | CPI传导→政策收紧压力 |
| **日本** | 抗通胀资产(黄金) | 消费股、高估值股 | 通胀摆脱通缩→政策调整 |
| **韩国** | 抗通胀资产(黄金) | 消费股、高估值股 | 利率上行压力 |
| **欧洲** | 抗通胀资产(黄金) | 消费股、高估值股 | 欧央行加息压力 |

### VIX飙升 → 多经济体传导

| 经济体 | 受益指标 | 受损指标 | 传导机制 |
|-------|---------|---------|---------|
| **中国** | 防守板块(银行、医药) | A股成长股、创业板 | 风险厌恶传导 |
| **日本** | 防守板块 | 日股成长股 | 风险厌恶传导 |
| **韩国** | 防守板块 | 韩股成长股 | 风险厌恶传导 |
| **欧洲** | 防守板块 | 欧股成长股 | 风险厌恶传导 |

---

## 📊 多经济体指标获取方法

### Yahoo Finance 获取方式

```bash
# 日经225
python scripts/fetch_indicator_data.py nikkei225 --years 30 --output data/nikkei225.json

# 德国DAX
python scripts/fetch_indicator_data.py dax --years 30 --output data/dax.json

# 恒生指数
python scripts/fetch_indicator_data.py hsi --years 30 --output data/hsi.json
```

### Tushare 获取中国宏观

```python
import tushare as ts
pro = ts.pro_api()

# CPI
pro.cn_cpi(start_date='20100101', end_date='20260331')

# PPI
pro.cn_ppi(start_date='20100101', end_date='20260331')

# GDP
pro.cn_gdp(start_date='20100101', end_date='20260331')

# M2
pro.cn_m(start_date='20100101', end_date='20260331')
```

### FRED 获取国际宏观

```bash
# 日本GDP
python scripts/fetch_indicator_data.py gdp_japan --years 30 --output data/gdp_japan.json

# 欧元区CPI
python scripts/fetch_indicator_data.py cpi_eurozone --years 30 --output data/cpi_eurozone.json
```

---

## Event Type to Indicator Mapping

### Oil Price Events
- Primary indicators: `brent_crude`, `wti_crude`
- Related indicators: `xle`, `jets`, `xli`, `gold`, `natural_gas`, `csi300`

### Gold Price Events
- Primary indicators: `gold`
- Related indicators: `silver`, `gdx`, `sp500`, `xlf`

### Interest Rate Events
- Primary indicators: `us_10y_treasury`, `fed_funds_rate`
- Related indicators: `xlf`, `tlt`, `iyr`, `nasdaq`, `usd_index`

### VIX/Volatility Events
- Primary indicators: `vix`
- Related indicators: `sp500`, `nasdaq`, `gold`, `xlp`, `xlv`

### Dollar Events
- Primary indicators: `usd_index`
- Related indicators: `gold`, `brent_crude`, `csi300`, `sp500`, `xli`

### Inflation Events
- Primary indicators: `cpi_us`
- Related indicators: `gold`, `silver`, `xle`, `tlt`, `iyr`

---

## Usage Notes

1. **Yahoo Finance**: Works without API key, but may have rate limits
2. **FRED**: Register at https://fred.stlouisfed.org/docs/api/api_key.html
3. **Tushare**: Register at https://tushare.pro, get token from profile page

### Environment Variables
```bash
export TUSHARE_TOKEN="your_token_here"
export FRED_API_KEY="your_api_key_here"
```