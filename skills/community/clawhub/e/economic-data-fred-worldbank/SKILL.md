---
name: economic-data-fred-worldbank
description: Economic data for AI agents — search 800k+ Federal Reserve (FRED) economic series, pull any FRED series by id, World Bank country indicators, and derived US market stats (housing affordability, market vitality, industry saturation). Use for macroeconomic research, market analysis, and economic indicators. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [economic-data, fred, federal-reserve, world-bank, macroeconomics, market-data, indicators, gdp, inflation, housing, census, research]
author: gocreative
version: 1.0.0
license: MIT
---

# Economic Data — FRED, World Bank & Market Stats

> 800k+ Federal Reserve series, World Bank indicators, and US market stats. One install, pay-per-call, no API key.

## When to use this
- Pull a **macroeconomic indicator** (rates, inflation, GDP, employment) from FRED.
- Get **World Bank country data** or **US market/housing stats**.
- Feed an economic-research, investment, or market-analysis agent.

## How it's paid (x402)
Plain HTTPS GET. First call returns HTTP 402; your wallet auto-pays the USDC fee and retries → JSON.

## Tools
| Call | What you get | Price |
|---|---|---|
| `GET .../v1/fred/search/{keyword}` | Search 800k+ Federal Reserve economic series | ~$0.02 |
| `GET .../v1/fred/series/{fred_id}` | Any FRED series by id (e.g. `GDP`, `UNRATE`) | ~$0.02 |
| `GET .../v1/data/worldbank/{country}` | World Bank economic indicator by country | ~$0.004 |
| `GET .../v1/market/profile/{state-or-fips}` | DERIVED US market-vitality profile | ~$0.05 |
| `GET .../v1/market/affordability/{state-or-zip}` | DERIVED housing-affordability signal | ~$0.05 |
| `GET .../v1/market/saturation/{NAICS-GEO}` | DERIVED market-saturation for an industry in a place | ~$0.06 |

(Base URL: `https://api.gocreativeai.com`)

## Why GoCreative
Live FRED + World Bank + derived US market data, pay-per-call, no signup — the **only native economic-data feed for agents** (no competition in this category).

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
