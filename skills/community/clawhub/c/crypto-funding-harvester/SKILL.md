---
name: crypto-funding-harvester
description: Scans perpetual futures funding rates across Hyperliquid, Binance, and Bybit to identify delta-neutral carry trade opportunities. A delta-neutral carry trade involves going long spot and short the perpetual future on the same asset, collecting the funding rate as profit without directional price exposure. The skill normalizes all funding rates to annualized percentages, filters for high-yield opportunities above 20% APY, ranks them by profitability, detects cross-exchange arbitrage spreads, and saves results to /tmp/funding_opportunities.json. Runs every 15 minutes to keep opportunity data fresh. No API keys required — all data is sourced from free public endpoints.
metadata:
  author: Mibayy
  version: 1.0.0
  displayName: Crypto Funding Rate Harvester
  difficulty: intermediate
  type: automaton
---

# Crypto Funding Rate Harvester

Scans perpetual futures funding rates across Hyperliquid, Binance, and Bybit to surface delta-neutral carry trade opportunities in real time.

## What it does

A delta-neutral carry trade works like this:
- Buy spot (e.g. BTC on any exchange)
- Short the perpetual future on the same asset
- Net directional exposure = zero
- Collect the funding rate paid by longs to shorts
- Pure yield, no price risk (ignoring basis risk)

This skill identifies assets where funding rates are high enough (>20% annualized) to make this trade worthwhile after accounting for fees and capital costs.

## Output

Results are saved to `/tmp/funding_opportunities.json` with the following structure:

```json
{
  "generated_at": "2025-01-01T00:00:00.000000",
  "opportunities": [
    {
      "asset": "BTC",
      "exchange": "binance",
      "funding_rate_8h": 0.0003,
      "annualized_pct": 32.85,
      "current_price": 65000.0
    }
  ],
  "cross_exchange_spreads": [
    {
      "asset": "BTC",
      "binance_annualized_pct": 32.85,
      "bybit_annualized_pct": 10.95,
      "spread_pct": 21.9,
      "note": "Binance funding significantly higher than Bybit — potential cross-exchange arb"
    }
  ],
  "summary": {
    "total_opportunities": 5,
    "exchanges_scanned": ["hyperliquid", "binance", "bybit"],
    "min_annualized_threshold_pct": 20
  }
}
```

## Environment Variables

No environment variables are required. All APIs used are free and public.

The following optional environment variables can be used to tune behavior:

| Variable | Default | Description |
|---|---|---|
| `MIN_ANNUALIZED_PCT` | `20` | Minimum annualized funding rate (%) to include in results |
| `CROSS_EXCHANGE_SPREAD_THRESHOLD` | `10` | Minimum spread (%) between Binance and Bybit to flag as a cross-exchange opportunity |
| `REQUEST_TIMEOUT` | `10` | HTTP request timeout in seconds |

## Exchanges

| Exchange | Endpoint | Notes |
|---|---|---|
| Hyperliquid | `https://api.hyperliquid.xyz/info` | POST, type=metaAndAssetCtxs |
| Binance | `https://fapi.binance.com/fapi/v1/premiumIndex` | GET, all USDT perps |
| Bybit | `https://api.bybit.com/v5/market/tickers` | GET, category=linear |

## Funding Rate Normalization

All exchanges use 8-hour funding intervals. Annualized rate is calculated as:

  annualized_pct = funding_rate_8h * 3 * 365 * 100

Where `* 3` converts 8h to daily (3 periods per day) and `* 365` converts daily to annual.

## Cron Schedule

Runs every 15 minutes: `*/15 * * * *`
