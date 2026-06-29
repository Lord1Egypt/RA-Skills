---
name: finance-daily-report
description: "AI财经日报生成助手。自动获取A股/港股/美股实时行情，分析大盘指数、行业板块、资金流向、外汇商品、财经要闻，生成交互式HTML可视化日报。触发词：财经日报、今日财经、股市日报、每日财经、金融日报、finance daily report、股市行情、大盘分析、今日股市。"
agent_created: true
---

# 财经日报 (Finance Daily Report)

## Overview

Generate a professional, interactive HTML financial daily report covering A-shares, Hong Kong stocks, and major global indices. The report follows Chinese stock market conventions (red for up, green for down) and uses AKShare for free real-time data.

## When to Use

Trigger this skill when the user asks for:
- 财经日报 / 今日财经 / 股市日报
- A daily financial market report
- Stock market overview or analysis
- 大盘分析 / 今日股市 / 金融日报
- Any request involving generating a daily financial summary

## Workflow

### Step 1: Prepare Environment

Before running the script, ensure dependencies are installed:

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple akshare pandas --trusted-host pypi.tuna.tsinghua.edu.cn
```

Use the managed Python runtime at `C:/Users/PC/.workbuddy/binaries/python/versions/3.13.12/python.exe` and create/use a venv if needed.

### Step 2: Run the Report Generator

Execute the main script to generate the report:

```bash
python scripts/generate_report.py [--output <path>] [--date YYYY-MM-DD]
```

Options:
- `--output`: Output HTML file path (default: current working directory `finance_daily_report_YYYY-MM-DD.html`)
- `--date`: Target date in YYYY-MM-DD format (default: today). Note: only historical dates work for complete data; today may have incomplete real-time data.

### Step 3: Present the Report

After generation, present the HTML file to the user using `present_files`. The report is a self-contained interactive HTML file that opens directly in the browser.

## Report Modules

The generated report includes 6 modules:

1. **大盘指数概览** — A-share main indices (SSE, SZSE, ChiNext, STAR 50), Hang Seng, Hang Seng Tech, with real-time price, change %, and change amount.
2. **行业板块热力** — Top 5 gaining and top 5 declining industry sectors with representative stocks.
3. **资金流向** — North-bound capital flow, total market turnover, main capital flow direction.
4. **外汇与商品** — USD/CNY exchange rate, gold price, crude oil price.
5. **财经要闻** — Key financial news headlines for the day.
6. **明日关注** — Financial calendar events and upcoming economic data releases.

## Visual Conventions

- **Red (红色 #e74c3c)**: Price increase (涨) — Chinese market convention
- **Green (绿色 #27ae60)**: Price decrease (跌) — Chinese market convention
- Interactive charts powered by Chart.js (loaded from CDN)
- Responsive design, mobile-friendly

## Data Sources

The script uses the following AKShare data sources (v1.18+ optimized for China network):

| Module | API | Source |
|--------|-----|--------|
| A-share indices | `ak.stock_zh_index_spot_sina()` | Sina (reliable in China) |
| HK indices | `ak.stock_hk_index_spot_sina()` | Sina |
| Industry sectors | `ak.stock_board_industry_summary_ths()` | TongHuaShun (THS) |
| North-bound flow | `ak.stock_hsgt_hist_em(symbol='沪股通')` | EastMoney |
| Turnover | Calculated from `stock_zh_index_spot_sina()` | Sina |
| Forex | `ak.fx_spot_quote()` | - |
| Commodities | `ak.futures_global_spot_em()` | EastMoney |
| News | `ak.stock_news_em()` | EastMoney |

See `references/akshare_apis.md` for detailed API mappings and column schemas.

## Important: Encoding

On Windows, always set `PYTHONIOENCODING=utf-8` when running the script to avoid GBK encoding errors:

```bash
PYTHONIOENCODING=utf-8 python scripts/generate_report.py --date 2026-06-16
```

## Error Handling

- Each API call includes automatic 2-retry with 1s delay for transient failures
- Failed modules gracefully degrade: show "暂无数据" placeholder in report
- Sina-based APIs (`stock_zh_index_spot_sina`, `stock_hk_index_spot_sina`) are preferred over EastMoney for reliability in China
- If AKShare is not installed, guide the user to install it first
