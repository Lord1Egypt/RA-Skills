---
name: crypto-price-alerter
description: Monitor cryptocurrency prices and generate trading alerts/analyses. Use when the user wants to (1) check the current price of a crypto symbol (BTC, ETH, SOL, etc.), (2) see 24h price change, volume, and market cap, (3) get technical signals (SMA, RSI, support/resistance), (4) set price threshold alerts, or (5) generate a crypto portfolio price summary. Triggers: "crypto price", "check price", "BTC", "ETH", "solana", "alert", "trading", "price alert", "crypto analysis", "technical analysis", "RSI", "SMA", "support resistance".
---

# Crypto Price Alerter

Fetch live cryptocurrency prices and technical indicators via CoinGecko free API.

## Quick Usage

```bash
uv run python scripts/price_check.py --symbol BTC --currency USD
uv run python scripts/price_check.py --symbol ETH --currency USD --upper 4000 --lower 2000
uv run python scripts/price_check.py --symbol SOL --currency USD --output json
```

## Core Features

1. **Current Price** — Live price, 24h change %, 24h volume, market cap
2. **Technical Indicators** — SMA(7), SMA(21), RSI(14) from 30-day historical data
3. **Key Levels** — 30-day resistance and support
4. **Price Alerts** — Triggered when 24h change >5% or price crosses user thresholds
5. **JSON output** — For automation pipelines: `--output json`

## Scripts

- `scripts/price_check.py` — Main script. Run standalone with `uv run python scripts/price_check.py [args]`

### Arguments

| Arg | Description |
|-----|-------------|
| `--symbol` | Crypto symbol (e.g. BTC, ETH, SOL) — **required** |
| `--currency` | Fiat currency (default: USD) |
| `--upper` | Upper price threshold for alert |
| `--lower` | Lower price threshold for alert |
| `--days` | Historical days for SMA (default: 30) |
| `--output` | `text` (default) or `json` |

## Technical Signals

See `references/signals.md` for explanation of SMA, RSI, support/resistance, and trading signal interpretation.

## Alert Logic

- 24h change > +5% → Bullish alert
- 24h change < -5% → Bearish alert
- Price >= `--upper` threshold → Price ceiling alert
- Price <= `--lower` threshold → Price floor alert
