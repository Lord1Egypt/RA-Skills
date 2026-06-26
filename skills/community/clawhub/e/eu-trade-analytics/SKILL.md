---
name: eu-trade-analytics
description: Query 28M+ Eurostat COMEXT trade records — 27 EU countries, bilateral flows, HS2-CN8 codes, 1988-2025
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["trade","eurostat","analytics","eu","data"]}
---

# EU Trade Analytics

28M+ Eurostat COMEXT bilateral trade records. 27 EU countries, HS2 to CN8 product codes, 1988-2025. Monthly data, import/export flows, price-per-tonne, seasonality, concentration (HHI).

## Base URL

`https://sputnikx.xyz/api/v1/agent`

## Key Endpoints

### Trade Overview (free tier: 1000/day)
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/overview?reporter=LV&year=2025"
```

### Trade Timeline
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/timeline?reporter=LV&partner=DE&hs2=44&years=2020-2025"
```

### Top Partners
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/top-partners?reporter=LV&hs2=44&year=2025&flow=export"
```

### Price Per Tonne ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/price-per-tonne?reporter=LV&hs2=44"
```

### Seasonality ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/seasonality?reporter=LV&hs2=27"
```

### Concentration/HHI ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/concentration?hs2=44&year=2025&flow=export"
```

## MCP Server
```
Endpoint: https://mcp.sputnikx.xyz/mcp
Tool: query_trade
```

## Data Coverage
- 28M+ records (63M with customs)
- 27 EU member states
- HS2 to CN8 product classification
- Monthly granularity, 1988-2025
- Import + export flows with EUR values and KG quantities

## When to use this skill
- Analyze bilateral trade flows between EU countries
- Find top trading partners for specific product codes
- Track price trends and seasonal patterns
- Calculate market concentration (Herfindahl-Hirschman Index)
- Research supply chain corridors
