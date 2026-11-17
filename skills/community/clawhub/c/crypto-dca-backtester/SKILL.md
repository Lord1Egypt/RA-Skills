---
name: crypto-dca-backtester
description: Backtest dollar-cost averaging (DCA) against lump-sum investing on any coin's real historical price data, using the free CoinGecko market_chart API (no API key required, up to 365 days of daily history). Built for crypto traders and passive-income investors deciding between DCA and lump-sum entry strategies before committing capital. Simulates weekly contributions and compares final portfolio value, invested capital, and percent return against a lump-sum baseline of the same total capital deployed on day one. Complements trading, whale-tracking, and DeFi yield skills by covering the entry-strategy decision, which is distinct from picking what to buy or where to farm yield.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash
---

# Crypto DCA Backtester

Simulates weekly dollar-cost averaging vs a lump-sum investment of the same total capital, using real historical daily prices from CoinGecko's free market_chart API. No API key needed.

## When to use

- Deciding whether to DCA into a position or deploy capital all at once
- Backtesting how DCA would have performed on a specific coin over the last N days (up to 365)
- Comparing entry strategies across multiple coins before allocating
- Building intuition for how DCA smooths volatility vs a single entry point

## Commands

```bash
python3 scripts/dca_backtest.py --coin bitcoin --days 365 --weekly-contribution 100
python3 scripts/dca_backtest.py --coin ethereum --days 90 --weekly-contribution 250
python3 scripts/dca_backtest.py --coin solana --days 365 --weekly-contribution 100 --json
```

`--coin` takes a CoinGecko coin id (e.g. `bitcoin`, `ethereum`, `solana`, `matic-network`) — use CoinGecko's `/coins/list` if you need to look one up.

## Output

Total invested, end portfolio value, and return % for both DCA and lump-sum, using the same total capital for a fair comparison, plus a declared winner for that specific historical window.

## Notes

- Data source: CoinGecko free `market_chart` endpoint, daily granularity, max 365-day lookback on the free tier.
- This is a historical return comparison only — it does not model volatility-adjusted or risk-adjusted returns, and past performance over one specific window is not predictive of future results. Not financial advice.
- Requests use a curl-style User-Agent; some public API providers block the default Python User-Agent.
