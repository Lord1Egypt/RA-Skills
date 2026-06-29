---
name: crypto-one-way-market
description: Fetch cryptocurrency OHLCV candle data and judge whether the market is in a one-way bullish or bearish trend. Use when the user asks to pull crypto market data, analyze BTC/ETH/altcoin candles, detect 单边行情, classify trend versus chop/range, or produce an evidence-based crypto trend summary from public exchange data.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📈"
---

# Crypto One-Way Market

## Overview

Use this skill to fetch public crypto candle data, compute directional trend metrics, and decide whether price action is a one-way market (`单边上涨` / `单边下跌`) or a range/choppy market.

Default to the bundled script for repeatable calculations:

```bash
python3 scripts/fetch_and_classify.py --symbol BTCUSDT --interval 15m --limit 200
```

## Workflow

1. Clarify the symbol, timeframe, and lookback if missing. Default to `BTCUSDT`, `15m`, and `200` candles for intraday checks.
2. Run `scripts/fetch_and_classify.py` to fetch candles and compute the classification.
3. Read `references/methodology.md` when explaining thresholds, edge cases, or if the result is borderline.
4. Summarize direction, confidence, key evidence, and invalidation conditions. Avoid financial advice wording; present the result as market-structure analysis, not a trade instruction.

## Data Fetching

The script uses Binance public REST klines by default and needs no API key:

```bash
python3 scripts/fetch_and_classify.py \
  --symbol ETHUSDT \
  --interval 1h \
  --limit 240
```

Useful options:

```bash
--market spot
--market futures
--base-url https://api.binance.us
--json
--output candles.csv
```

If Binance is blocked or unstable, ask the user for an accessible exchange/API endpoint or use `--base-url` when they have a working Binance-compatible mirror.

## Interpretation Rules

Treat a one-way market as a move with persistent direction, high trend efficiency, limited counter-trend retracement, and enough volatility-adjusted distance from the start.

Report one of:

- `bullish_one_way`: likely 单边上涨.
- `bearish_one_way`: likely 单边下跌.
- `weak_trend`: directional but not clean enough to call one-way.
- `range_or_chop`: no strong one-way evidence.

In the final answer, include:

- Symbol, exchange source, interval, candle count, and time span.
- Classification and confidence.
- Directional return, trend efficiency, ADX, ATR-normalized move, max pullback, moving-average slope agreement.
- A concise explanation in Chinese when the user asks in Chinese.

## Risk Notes

Crypto data can have exchange outages, API regional restrictions, and sudden regime shifts. Never claim certainty. For live trading contexts, mention that low-liquidity symbols, news events, and funding/contract basis can invalidate candle-only signals.
