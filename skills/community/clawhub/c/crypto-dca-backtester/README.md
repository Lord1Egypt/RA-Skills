# Crypto DCA Backtester

Backtests dollar-cost averaging vs lump-sum investing on real historical crypto prices, using CoinGecko's free API.

## Why

DCA bots and trading skills on ClawHub focus on live execution; a plain "would DCA have beaten lump-sum here" backtester using real data was missing.

## Usage

```bash
python3 scripts/dca_backtest.py --coin bitcoin --days 365 --weekly-contribution 100
```

See `SKILL.md` for the full reference.

## How it works

1. Fetches daily USD prices for the given coin over the requested window from CoinGecko's `market_chart` endpoint.
2. Simulates weekly DCA: same USD contribution every ~7 days, buying units at that day's price.
3. Simulates a lump-sum: the same total capital invested entirely on day one.
4. Compares both strategies' end value (at the final day's price) and return %.

## Limitations

- Max 365-day lookback (CoinGecko free tier limit).
- Return-only comparison — doesn't account for risk-adjusted metrics like volatility or max drawdown during the holding period.
- No fees, slippage, or exchange spread are modeled.
