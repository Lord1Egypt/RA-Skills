# CoolTrade Agent Skills for OpenClaw

This package provides native A-Share market integration (China Stock Market) for your AI Agents via OpenClaw.

## Prerequisites
1. Register an account at [CoolTrade](https://cooltrade.xyz)
2. Obtain an Agent API Key from the CoolTrade dashboard

## Usage
Simply replace `sk-XXXXX` in the url configs with your actual CoolTrade API Key in OpenClaw ecosystem.

## Available Skills

- **cooltrade_stock_quote**: Get deep market quote and financial fundamentals for any A-share stock (China Market).
- **cooltrade_stock_news**: Monitor the latest relevant news, market announcements, and abnormal movements for specified China A-share stocks.
- **cooltrade_financials**: Fetch core financial and valuation parameters (EPS, ROE, P/E, debt ratios, etc.) for China A-share companies to analyze deep fundamentals.
- **cooltrade_index**: Get daily quotes and trends for global/China market indexes (e.g. SSE, SZSE, NASDAQ) to evaluate macroeconomic environment.
- **cooltrade_us_stock**: Get market quotes and recent daily performance for US stocks (e.g. AAPL, TSLA).
- **cooltrade_futures**: Get market prices, open interest (OI), and trends for domestic China futures contracts (commodities, financial futures).
