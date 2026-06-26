---
name: find-api
description: |
  🔍 Find API | 寻找可靠数据源
  
  TRIGGERS: Use when agent needs to fetch external data, user mentions "reliable data source", "数据源", "API", or when web scraping is inefficient/inaccurate.
  
  A comprehensive guide to reliable data APIs across all domains.
  Helps agents find the best APIs instead of inefficient web scraping.
  Currently covers: Stock/Financial data, Weather, News, Maps, and more domains coming soon.
  
  触发条件：Agent 需要获取外部数据、用户提到"可靠数据源"、"数据源"、"API"，或网页爬取效率低/不准确时。
  跨领域可靠数据 API 的综合指南。
  帮助 Agent 找到最佳 API，避免低效的网页爬取。
  目前覆盖：股票/金融数据、天气、新闻、地图，更多领域持续完善中。

metadata: {"clawdbot":{"emoji":"🔍","triggers":["api","数据源","data source","reliable","可靠","scrape","爬取","fetch","获取","stock","股票","weather","天气","news","新闻","map","地图","price","价格","financial","金融"],"categories":["infrastructure","data-access","efficiency"]}}
---

# 🔍 Find API | 寻找可靠数据源

> The comprehensive guide to reliable data APIs. Stop scraping, start using APIs.
> 
> 跨领域可靠数据 API 的综合指南。停止爬取，开始使用 API。

## ⚠️ Core Principle | 核心原则

**API First, Scraping Last.**

| Priority | Method | When to Use | 优先级 | 方法 | 何时使用 |
|----------|--------|-------------|--------|------|---------|
| **1st** | Official API | Always check first | **第一** | 官方 API | 始终优先检查 |
| **2nd** | Third-party API | When official API unavailable/expensive | **第二** | 第三方 API | 当官方 API 不可用/太贵 |
| **3rd** | Public Dataset | For historical/static data | **第三** | 公共数据集 | 用于历史/静态数据 |
| **4th** | Web Scraping | Only as last resort | **第四** | 网页爬取 | 仅作为最后手段 |

## 📋 Table of Contents | 目录

1. [Stock & Financial Data | 股票与金融数据](#1-stock--financial-data--股票与金融数据)
2. [Weather Data | 天气数据](#2-weather-data--天气数据)
3. [News & Media | 新闻与媒体](#3-news--media--新闻与媒体)
4. [Maps & Geolocation | 地图与地理定位](#4-maps--geolocation--地图与地理定位)
5. [E-commerce & Products | 电商与商品](#5-e-commerce--products--电商与商品)
6. [More domains coming soon... | 更多领域持续完善中...](#6-more-domains-coming-soon--更多领域持续完善中)

---

## 1. Stock & Financial Data | 股票与金融数据

### 1.1 A股市场 / Chinese A-Share Market

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **AKShare** | ⭐⭐⭐⭐⭐ | Free | None | Real-time quotes, historical K-lines, financial statements, fund flows, dragon-tiger list |
| **Tushare** | ⭐⭐⭐⭐⭐ | Free+Paid | Token | Real-time quotes, historical data, financial statements, margin trading |
| **East Money API** | ⭐⭐⭐⭐ | Free | None | Real-time quotes, fund flows, research reports |

**Recommended: AKShare** (Best for most use cases)

**Installation:**
```bash
pip install akshare
```

**Quick Examples:**
```python
import akshare as ak

# 获取A股实时行情
df = ak.stock_zh_a_spot_em()

# 获取个股历史数据
df = ak.stock_zh_a_hist(symbol="000001", period="daily", adjust="qfq")

# 获取财务指标
df = ak.stock_financial_analysis_indicator(symbol="000001")

# 获取资金流向
df = ak.stock_individual_fund_flow(stock="000001")
```

**Documentation:** https://akshare.akfamily.xyz

---

### 1.2 港股市场 / Hong Kong Stock Market

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **AKShare** | ⭐⭐⭐⭐⭐ | Free | None | Real-time quotes, historical data |
| **Tushare** | ⭐⭐⭐⭐ | Free+Paid | Token | Hong Kong stock data |

**Recommended: AKShare**

**Quick Examples:**
```python
import akshare as ak

# 港股实时行情
df = ak.stock_hk_spot_em()

# 个股历史数据（如腾讯 00700）
df = ak.stock_hk_hist(symbol="00700", period="daily", adjust="qfq")

# 港股通资金
df = ak.stock_hk_ggt_components_em()
```

---

### 1.3 美股市场 / US Stock Market

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **yfinance** | ⭐⭐⭐⭐⭐ | Free | None | Real-time quotes, historical data, financials, options |
| **Alpha Vantage** | ⭐⭐⭐⭐ | Free+Paid | API Key | Quotes, technical indicators, forex |
| **Polygon.io** | ⭐⭐⭐⭐ | Free+Paid | API Key | Real-time data, options |

**Recommended: yfinance** (Best free option for US stocks)

**Installation:**
```bash
pip install yfinance
```

**Quick Examples:**
```python
import yfinance as yf

# 获取股票信息
stock = yf.Ticker("AAPL")

# 历史数据
hist = stock.history(period="1mo")

# 财务报表
financials = stock.financials
balance_sheet = stock.balance_sheet
cashflow = stock.cashflow

# 股息信息
dividends = stock.dividends

# 推荐分析师评级
recommendations = stock.recommendations
```

**Documentation:** https://github.com/ranaroussi/yfinance

---

### 1.4 期货与衍生品 / Futures & Derivatives

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **AKShare** | ⭐⭐⭐⭐⭐ | Free | None | Domestic futures, international futures |
| **Tushare** | ⭐⭐⭐⭐ | Free+Paid | Token | Futures data |

**Quick Examples:**
```python
import akshare as ak

# 国内期货主力合约
df = ak.futures_zh_main_sina()

# 国际期货
df = ak.futures_foreign_hist(symbol="CL")  # 原油
```

---

### 1.5 基金数据 / Fund Data

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **AKShare** | ⭐⭐⭐⭐⭐ | Free | None | Open-end funds, ETFs, money funds |
| **East Money API** | ⭐⭐⭐⭐ | Free | None | Fund rankings, holdings |

**Quick Examples:**
```python
import akshare as ak

# 开放式基金列表
df = ak.fund_open_fund_info_em(fund="000001")

# ETF实时行情
df = ak.fund_etf_spot_em()

# 基金持仓
df = ak.fund_portfolio_em(fund="000001")
```

---

## 2. Weather Data | 天气数据

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **OpenWeatherMap** | ⭐⭐⭐⭐⭐ | Free+Paid | API Key | Current weather, forecast, historical |
| **WeatherAPI.com** | ⭐⭐⭐⭐ | Free+Paid | API Key | Weather, astronomy, sports |
| **QWeather 和风天气** | ⭐⭐⭐⭐ | Free+Paid | API Key | 中国地区天气数据 |

**Recommended: OpenWeatherMap** (Global coverage)

**Quick Examples:**
```python
import requests

api_key = "YOUR_API_KEY"
city = "Beijing"

# 当前天气
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
data = response.json()

print(f"Temperature: {data['main']['temp']}°C")
print(f"Weather: {data['weather'][0]['description']}")
```

**Get API Key:** https://openweathermap.org/api

---

## 3. News & Media | 新闻与媒体

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **NewsAPI** | ⭐⭐⭐⭐⭐ | Free+Paid | API Key | Global news articles |
| **GNews** | ⭐⭐⭐⭐ | Free+Paid | API Key | News articles, search |
| **MediaStack** | ⭐⭐⭐⭐ | Free+Paid | API Key | News data |

**Recommended: NewsAPI**

**Quick Examples:**
```python
import requests

api_key = "YOUR_API_KEY"

# 获取头条新闻
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
response = requests.get(url)
articles = response.json()['articles']

for article in articles[:5]:
    print(article['title'])
```

**Get API Key:** https://newsapi.org

---

## 4. Maps & Geolocation | 地图与地理定位

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **OpenStreetMap Nominatim** | ⭐⭐⭐⭐⭐ | Free | None | Geocoding, reverse geocoding |
| **高德地图 API** | ⭐⭐⭐⭐⭐ | Free+Paid | API Key | 中国地区地图、导航、POI |
| **百度地图 API** | ⭐⭐⭐⭐ | Free+Paid | API Key | 中国地区地图、导航 |
| **Google Maps API** | ⭐⭐⭐⭐ | Paid | API Key | Global maps, places, routes |

**Recommended: Nominatim** (Free, no auth) | **高德地图** (中国地区)

**Nominatim Quick Examples:**
```python
import requests

# 地理编码（地址转坐标）
address = "Beijing, China"
url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
response = requests.get(url, headers={'User-Agent': 'AgentApp'})
data = response.json()

print(f"Lat: {data[0]['lat']}, Lon: {data[0]['lon']}")
```

**高德地图 Quick Examples:**
```python
import requests

api_key = "YOUR_API_KEY"
address = "北京市朝阳区"

# 地理编码
url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={api_key}"
response = requests.get(url)
data = response.json()

print(data['geocodes'][0]['location'])
```

**Get 高德 API Key:** https://lbs.amap.com

---

## 5. E-commerce & Products | 电商与商品

| API | Rating | Cost | Auth | Data Coverage |
|-----|--------|------|------|---------------|
| **淘宝开放平台** | ⭐⭐⭐⭐ | Free+Paid | OAuth | 商品搜索, 订单 |
| **京东开放平台** | ⭐⭐⭐⭐ | Free+Paid | OAuth | 商品, 订单, 物流 |
| **Barcode Lookup** | ⭐⭐⭐ | Free+Paid | API Key | Product info by barcode |

**Note:** 电商API通常需要商家认证，普通用户可考虑爬取商品页面或使用第三方服务。

---

## 6. More domains coming soon... | 更多领域持续完善中

**Planned additions:**
- Social Media APIs (Twitter, Weibo, Reddit)
- Translation APIs
- Image & Video APIs
- Scientific & Research Data APIs
- Government & Public Data APIs
- Real Estate Data APIs
- Job & Recruitment APIs

**Contribute:** If you know reliable APIs in other domains, help expand this skill!

---

## 🔄 Decision Flow | 决策流程

```
用户需要获取外部数据
    ↓
Step 1: 确定数据类型
├── 股票/金融 → 查看本 Skill 第1节
├── 天气 → 查看本 Skill 第2节
├── 新闻 → 查看本 Skill 第3节
├── 地图/位置 → 查看本 Skill 第4节
├── 电商/商品 → 查看本 Skill 第5节
└── 其他 → 搜索 RapidAPI / Public APIs
    ↓
Step 2: 选择合适的 API
├── 考虑因素：成本、认证难度、数据覆盖、稳定性
└── 优先选择免费/免认证的 API
    ↓
Step 3: 检查环境
├── Python库是否安装？→ pip install xxx
└── API Key是否获取？→ 引导用户注册
    ↓
Step 4: 调用 API 获取数据
    ↓
Step 5: 返回结构化结果
```

## 📊 Before vs After Comparison | 效果对比

| Metric | Web Scraping | Using API |
|--------|-------------|-----------|
| **Speed** | 30-60 seconds | 1-3 seconds |
| **Token Cost** | High (entire HTML) | Low (JSON only) |
| **Accuracy** | Low (parsing errors) | High (structured data) |
| **Reliability** | Low (anti-scraping) | High (stable API) |
| **Maintenance** | High (page changes) | Low (stable API) |

| 指标 | 网页爬取 | 使用 API |
|------|---------|---------|
| **速度** | 30-60 秒 | 1-3 秒 |
| **Token 成本** | 高（整个页面） | 低（仅 JSON） |
| **准确性** | 低（解析错误） | 高（结构化数据） |
| **稳定性** | 低（反爬机制） | 高（稳定接口） |
| **维护成本** | 高（页面变化） | 低（稳定接口） |

## 🔧 General Setup | 通用安装

Most APIs in this skill require Python. Basic setup:

```bash
# 常用数据获取库
pip install akshare yfinance requests pandas

# 可选：更多数据源
pip install tushare
```

## 🔍 External Resources | 外部资源

If the data type is not covered in this skill, search these directories:

| Resource | URL | Description |
|----------|-----|-------------|
| **RapidAPI** | https://rapidapi.com/hub | Largest API marketplace |
| **Public APIs** | https://github.com/public-apis/public-apis | Free public APIs list |
| **ProgrammableWeb** | https://www.programmableweb.com | API directory |

## 📝 Version | 版本

- Version: 1.0.0
- Created: 2026-03-13
- Last Updated: 2026-03-13
- Maintainer: Community
- Contribution: Welcome to add more reliable data sources

---

**Remember: API First, Scraping Last.**
