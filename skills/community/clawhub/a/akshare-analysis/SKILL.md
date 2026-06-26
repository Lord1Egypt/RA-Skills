---
name: akshare-analysis
description: Stock analysis for Chinese companies: HK stocks (港股) and A-shares (A股). Use when user wants to analyze Chinese stocks by company name (腾讯, 阿里巴巴, 茅台, 比亚迪, 美团, 小米, 宁德时代, 京东, 拼多多, 网易, 百度, 快手) or ticker code (00700, 600519, etc.). Trigger for any request involving 港股, A股, 中概股, or investment/trading analysis of Chinese companies.
version: 1.0.0
commands:
  - /akshare - Analyze a HK or A-share stock (e.g., /akshare 00700)
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["uv"],"env":[]},"install":[]}}
---

# AKShare Stock Analysis

Analyze Hong Kong and A-share stocks with 6-dimension scoring using akshare as the data source. Works reliably on servers where Yahoo Finance is rate-limited.

## Ticker Format

| Market | Format | Example |
|--------|--------|---------|
| Hong Kong | 5-digit | `00700` (Tencent), `09988` (Alibaba) |
| A-Share | 6-digit | `600519` (Moutai), `000858` (Wuliangye) |

## Quick Commands

```bash
# Single stock analysis
uv run {baseDir}/scripts/analyze.py 00700

# Multiple stocks
uv run {baseDir}/scripts/analyze.py 00700 09988 600519

# JSON output
uv run {baseDir}/scripts/analyze.py 00700 --output json

# Verbose (show per-dimension scores)
uv run {baseDir}/scripts/analyze.py 00700 --verbose

# Generate HTML report
uv run {baseDir}/scripts/analyze.py 00700 --report
uv run {baseDir}/scripts/render_report.py /data/stock-reports/00700/20260329_030822

# Search stock news (supports multiple keywords)
uv run {baseDir}/scripts/news.py 00700 腾讯 港股
uv run {baseDir}/scripts/news.py 600519 茅台 A股 --json
```

## HTML Report Generation

Four-step workflow for generating comprehensive reports:

**Step 1: Analyze and generate report directory**
```bash
uv run {baseDir}/scripts/analyze.py 00700 --report
# Creates: /data/stock-reports/00700/20260329_030822/
#   ├── chart_data.json  (K线+MA+布林带+RSI+MACD+成交量)
#   └── data.json        (structured analysis data)
```

**Step 2: Search news**
```bash
# Search by ticker, name, and market keywords
uv run {baseDir}/scripts/news.py 00700 腾讯 港股
uv run {baseDir}/scripts/news.py 600519 茅台 A股

# For HK stocks, use: ticker + name + "港股"
# For A-shares, use: ticker + name + "A股"
```

**Step 3: Generate AI analysis (manual)**
Based on the news from Step 2 and technical data from Step 1, create `ai_analysis.md` in the report directory:

```markdown
---
generated_at: 2026-03-29T20:30:00
---

## 市场情绪
... (summarize key news sentiment)

## 技术面解读
... (combine news + technical indicators from data.json)

## 关键事件影响
... (major news events and their impact)

## 综合展望
... (overall outlook combining fundamentals + technicals + news)

## 风险提示
... (key risks identified from news and technicals)
```

**Step 4: Render HTML report**
```bash
uv run {baseDir}/scripts/render_report.py /data/stock-reports/00700/20260329_030822
# Generates: index.html (self-contained with embedded charts + AI analysis)
```

The HTML report includes: signal badge, dimension scores with visual bars, financial metrics, analyst forecasts (HK only), technical charts, and optional AI analysis section.

## Analysis Dimensions

| Dimension | Weight | HK | A-Share | Data Source |
|-----------|--------|:--:|:-------:|-------------|
| Fundamentals | 25% | ✅ | ✅ | ROE, net margin, profit growth |
| Analyst | 20% | ✅ | ❌ | Target prices, ratings |
| Momentum | 20% | ✅ | ✅ | RSI(14), 52-week position |
| Valuation | 15% | ✅ | ⚠️ | P/E, P/B |
| Trend | 10% | ✅ | ✅ | MA5/MA20 crossover, 20d change |
| Volume | 10% | ✅ | ✅ | 5d vs 60d average volume |

## Signal Logic

- **BUY**: weighted score > 0.33
- **SELL**: weighted score < -0.33
- **HOLD**: otherwise
- Confidence = abs(score) × 100%

## Limitations

- A-shares: no analyst forecast data (akshare doesn't provide per-stock analyst ratings for A-shares)
- A-shares: P/E and P/B may be unavailable depending on market hours
- Data is delayed (not real-time intraday)

## Disclaimer

⚠️ NOT FINANCIAL ADVICE. For informational purposes only.
