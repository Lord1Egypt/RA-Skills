---
name: freqtrade-strategy-dev
description: "Develop, iterate, and improve Freqtrade cryptocurrency trading strategies. Use when writing a new strategy, improving an existing one, analyzing why a strategy is losing, or understanding which indicators to use. Covers strategy anatomy, key configuration parameters, proven entry/exit patterns, and the iteration workflow. Trigger phrases: write freqtrade strategy, improve strategy, why is my strategy losing, freqtrade indicators, strategy not profitable, freqtrade entry conditions."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["docker","docker-compose"]},"os":["linux","darwin","win32"]}}
---

# Freqtrade Strategy Development

Build profitable trading strategies with disciplined iteration, tight risk management, and data-driven entry/exit rules. Assumes Freqtrade is running via Docker (`docker-compose`).

## Strategy Anatomy

Every Freqtrade strategy requires three methods:

- **`populate_indicators(dataframe, metadata)`** — Add technical indicators (RSI, MACD, Bollinger Bands, etc.) to the dataframe
- **`populate_entry_trend(dataframe, metadata)`** — Define buy signal logic; set `enter_long = 1` when conditions met
- **`populate_exit_trend(dataframe, metadata)`** — Define sell signal logic; set `exit_long = 1` when conditions met (optional if using ROI/stop-loss)

## Key Config Parameters

```python
stoploss = -0.03  # 3% max loss per trade
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02

minimal_roi = {
    "0": 0.04,      # 4% profit target immediately
    "30": 0.02,     # 2% after 30 candles
    "60": 0.01,     # 1% after 60 candles
}

timeframe = "5m"  # or "15m", "1h", etc.
stake_currency = "USDT"
dry_run = True  # Always backtest/dry-run first
```

## Proven Entry Pattern

```python
stoploss = -0.03
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
minimal_roi = {"0": 0.04, "30": 0.02, "60": 0.01}

# In populate_indicators: calculate RSI, CCI, Bollinger Bands, EMA, Volume SMA

# In populate_entry_trend: only buy when ALL conditions met
conditions = [
    (dataframe['rsi'] < 30),  # Oversold
    (dataframe['cci'] < -100),  # Momentum confirmation
    (dataframe['close'] < dataframe['bb_lowerband']),  # Price near lower band
    (dataframe['volume'] > dataframe['volume_sma']),  # Volume confirms
    (dataframe['bullish_candle']),  # Pattern confirmation
]
dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
```

## Key Lessons Learned

1. **Tight stops save accounts** — 3% max loss beats 5%, 7%, or 8% every time
2. **Quality over quantity** — 25 selective trades outperform 308 mediocre ones
3. **Win rate alone is meaningless** — 63% win rate unprofitable if avg loss is 5x avg gain
4. **Selectivity is survival** — RSI(30) + CCI(-100) dual filters dramatically reduce noise
5. **Test in bear markets** — If strategy survives a crash, it works everywhere
6. **Volume confirms conviction** — Entries without above-average volume fail more often

## Useful Indicators

- **RSI (14)** — Momentum; < 30 = oversold, > 70 = overbought
- **CCI** — Commodity Channel Index; momentum confirmation; < -100 = deep oversold
- **MACD** — Trend following; watch for crossovers
- **Bollinger Bands** — Volatility; price near lower band = potential reversal
- **EMA** — Trend filter; price above EMA = uptrend
- **MFI** — Money Flow Index; volume-weighted momentum

## Iteration Workflow

1. Write baseline strategy with core entry/exit logic
2. Backtest on 90–120 days of historical data
3. Analyze exit reasons: are you exiting winners or losers too fast?
4. Tighten ONE parameter at a time (e.g., RSI threshold)
5. Backtest same period, compare vs. baseline
6. If better → keep; if worse → revert
7. Test different market conditions (Bull, bear, sideways)
8. Dry-run on live feeds before deploying to live trading

## Version Control

Keep all versions: name files `MyStrategy_v1.py`, `MyStrategy_v2.py`, etc. Add comments above each change explaining what improved and why. This preserves your iteration history and makes reverting safe.

## References

- **`references/indicators-guide.md`** — Technical indicator formulas and interpretation
- **`references/iteration-workflow.md`** — Step-by-step walkthrough of strategy optimization
