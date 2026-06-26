---
name: Financial Data Analyzer Lite
description: Free stock analysis skill — pull live data via yfinance, analyze any ticker with valuation metrics, financial health, and analyst consensus.
version: 1.0.0
author: Apex Stack
tags: finance, stock-analysis, yfinance, investing
---

# Financial Data Analyzer Lite

Analyze any stock ticker with live financial data. Pull real-time prices, valuation metrics, and financial health indicators using yfinance (no API key needed).

> **Want the full version?** [Financial Data Analyzer (Full)](https://apexstack.gumroad.com/l/financial-analyzer) includes: multi-stock comparison, custom scoring models, export to CSV/JSON, sector analysis, and dividend screening.

## How to Use

1. Tell me a stock ticker (e.g., AAPL, TSLA, MSFT)
2. I pull live data via yfinance
3. You get: current price, P/E ratio, market cap, dividend yield, 52-week range, analyst consensus

## What You Get

- **Price Summary**: Current price, day change, 52-week high/low
- **Valuation Metrics**: P/E, P/B, PEG ratio, EV/EBITDA
- **Financial Health**: Debt/Equity, Current Ratio, ROE
- **Analyst Consensus**: Buy/Hold/Sell ratings, price target

## Requirements

- Python 3.8+
- yfinance library (`pip install yfinance`)
- No API key needed — uses Yahoo Finance public data

## Limitations (Lite Version)

- Single ticker analysis only
- No comparison mode
- No custom scoring
- No export functionality
- Basic output format

---

*Built by [Apex Stack](https://apexstack.gumroad.com) — tools for developers who ship.*
