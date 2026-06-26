---
name: freqtrade-backtester
description: "Run Freqtrade backtests for cryptocurrency trading strategies, interpret results, and iterate. Use when downloading historical data, running a backtest, reading backtest output, comparing strategies, or deciding whether a strategy is ready for live trading. Trigger phrases: backtest freqtrade, run backtest, download freqtrade data, compare strategies, is my strategy good, freqtrade results."
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["docker","docker-compose"]},"os":["linux","darwin","win32"]}}
---

# Freqtrade Backtester

Run backtests on your trading strategies, interpret results, and iterate safely before going live.

## What Backtesting Does

Backtesting runs your strategy against historical market data to see how it would have performed. It shows you win rates, losses, drawdowns, and exit reasons — everything you need to decide if a strategy is worth trading with real money.

## Download Data

Historical data is cached, so download once and reuse it for many backtests.

⚠️ **Download one pair at a time** — passing multiple pairs to `--pairs` can cause errors. Run the command separately for each pair:

```bash
docker-compose run --rm freqtrade download-data \
  --exchange kraken \
  --pairs BTC/USDT \
  --timeframe 5m \
  --timerange 20240101-
```

Replace the pair, timeframe, and timerange as needed. The `--timerange` format is `YYYYMMDD-YYYYMMDD`; omit the end date to download through today.

## Run a Backtest

```bash
docker-compose run --rm freqtrade backtesting \
  --strategy YourStrategy \
  --timerange 20240101-20260101 \
  --export trades \
  --export-filename user_data/backtest_results/my_backtest.json
```

Replace `YourStrategy` with your actual strategy class name. The `--export trades` flag creates a JSON file with detailed trade logs.

## Key Metrics

- **Win rate** — Percentage of winning trades. >55% is decent; >60% is strong.
- **Max drawdown** — Largest peak-to-trough decline. Keep it <20%; above 25% indicates excessive risk.
- **Sharpe ratio** — Risk-adjusted return. >1.0 is acceptable; >2.0 is excellent.
- **Avg profit per trade** — Average win/loss size. Wins should be larger than losses.
- **Exit reasons** — Breakdown of why trades closed (ROI, stop-loss, trailing stop, etc.).

## The Key Insight

**High win rate ≠ profitability.** A 70% win rate with 5% average loss per trade loses money. A 40% win rate with 2% average wins and 1% average loss is profitable. Control your losses; the wins take care of themselves.

Example: A strategy with tight stops (-3%) outperforms one with loose stops (-7% or -8%), even if the loose version has more winners.

## Iteration Pattern

1. Run a backtest on a fixed time period (e.g., 6 months of data).
2. Change **one parameter** (e.g., RSI threshold, stop-loss percentage).
3. Backtest the **same period** again.
4. Compare results — did it improve?
5. If yes, keep it; if no, revert.
6. Repeat until satisfied.

Always test across multiple market conditions (bull runs, bear markets, sideways consolidation) before going live. A strategy that works in one environment often fails in another.

## Environment Variables

Freqtrade reads secrets from environment variables at runtime. Use the double-underscore format:

```bash
export FREQTRADE__EXCHANGE__KEY=your-api-key
export FREQTRADE__EXCHANGE__SECRET=your-api-secret
```

In your `config.json`, set these fields to empty strings:

```json
{
  "exchange": {
    "key": "",
    "secret": ""
  }
}
```

Freqtrade will populate them from the environment at startup.

## References

- **Reading Results** — `references/reading-results.md`
- **Iteration Guide** — `references/iteration-guide.md`
