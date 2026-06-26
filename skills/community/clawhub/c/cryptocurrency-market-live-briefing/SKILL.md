---
name: desk3-crypto-briefing
description: Desk3 Crypto Market Real-time Briefing - Provides BTC/ETH/SOL core prices, Fear & Greed Index, Puell/Pi Cycle/Bitcoin Dominance technical indicators, geopolitical and blockchain industry news, and trending coins real-time prices. Based on Desk3 API, direct API calls without MCP installation. Credit: Desk3
homepage: https://www.desk3.io
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["node"]},"primaryEnv":""}}
---

# Desk3 Crypto Briefing

Real-time cryptocurrency market briefing tool based on Desk3 API. API sources: `mcp.desk3.io` and `api1.desk3.io`

## Get Full Briefing

```bash
node {baseDir}/scripts/briefing.mjs
```

Briefing includes:
1. **Core Prices** - BTC/ETH/SOL prices and percentage changes
2. **Sentiment Indicators** - Fear & Greed Index + explanation
3. **Technical Indicators** - Puell, Pi Cycle, Dominance + explanations
4. **Policy & Macro News** - Top 10
5. **Blockchain Industry News** - Top 10
6. **Trending** - Top 10 coins real-time prices

## Get Individual Data

### Core Prices

```bash
# 24h prices
node {baseDir}/scripts/prices.mjs
```

### Sentiment Indicators

```bash
# Fear & Greed Index
node {baseDir}/scripts/fear-greed.mjs

# Altcoin Season Index
node {baseDir}/scripts/altcoin-season.mjs
```

### Technical Indicators

```bash
# Puell Multiple
node {baseDir}/scripts/puell.mjs

# Pi Cycle Top
node {baseDir}/scripts/pi-cycle.mjs

# Bitcoin Dominance
node {baseDir}/scripts/dominance.mjs

# Cycle Composite Analysis (Puell + Pi Cycle + Probabilities)
node {baseDir}/scripts/cycles.mjs

# Cycle Indicators Detail (30+ indicators)
node {baseDir}/scripts/cycle-indicators.mjs
```

### Trend Data

```bash
# BTC Trend
node {baseDir}/scripts/btc-trend.mjs

# ETH Trend
node {baseDir}/scripts/eth-trend.mjs

# Trending (Top 10 coins)
node {baseDir}/scripts/trending.mjs
```

### News

```bash
# Blockchain Industry News (catid=1)
node {baseDir}/scripts/news.mjs crypto

# Policy/Macro News (catid=3)
node {baseDir}/scripts/news.mjs policy
```

### Other

```bash
# Exchange Rate Info
node {baseDir}/scripts/exchange-rate.mjs

# Market Calendar
node {baseDir}/scripts/calendar.mjs
```

## API Documentation

All endpoints use the following base URLs, add `language: en` header when making requests:

- `https://api1.desk3.io/v1/` - Main market data
- `https://mcp.desk3.io/v1/` - MCP service API

### Complete API List

| Feature | Endpoint |
|---------|----------|
| Price Ticker | `/v1/market/mini/24hr` |
| Fear & Greed | `/v1/market/fear-greed` |
| Puell Multiple | `/v1/market/puell-multiple` |
| Pi Cycle Top | `/v1/market/pi-cycle-top` |
| Dominance | `/v1/market/bitcoin/dominance` |
| Cycle Composite | `/v1/market/cycles` |
| Cycle Indicators Detail | `/v1/market/cycleIndicators` |
| Altcoin Season | `/v1/market/altcoin/season` |
| BTC Trend | `/v1/market/btc/trend` |
| ETH Trend | `/v1/market/eth/trend` |
| Exchange Rate | `/v1/market/exchangeRate` |
| Calendar | `/v1/market/calendar` |
| News | `/v1/news/list` |

Notes:
- Data source: Desk3 API (free, no API key required)
- All endpoints use direct HTTP calls, no MCP server installation needed
- Supports Chinese and English responses (language: zh/en)
- Credit: Desk3
