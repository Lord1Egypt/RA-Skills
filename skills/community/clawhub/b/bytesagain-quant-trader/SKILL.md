---
name: "bytesagain-quant-trader"
description: "Build and analyze quantitative trading strategies. Input: asset, timeframe, parameters. Output: strategy logic, backtest signals, risk metrics, position sizing recommendations."
version: "1.0.0"
author: "BytesAgain"
tags: ["trading", "quantitative", "finance", "crypto", "stocks", "backtest", "strategy"]
---

# Quant Trader

Build, analyze, and optimize quantitative trading strategies. Covers signal generation, risk metrics, position sizing, and backtesting logic for crypto and equity markets.

## Commands

### strategy
Generate a quantitative trading strategy for a given asset and timeframe.
```bash
bash scripts/script.sh strategy --asset BTC --timeframe 4h --style momentum
```
Styles: `momentum`, `mean-reversion`, `breakout`, `trend-following`, `pairs`

### signal
Analyze price action and generate entry/exit signals.
```bash
bash scripts/script.sh signal --asset ETH --price 3200 --ma20 3050 --ma50 2900 --rsi 62 --volume "above-avg"
```

### backtest
Estimate strategy performance metrics from parameters.
```bash
bash scripts/script.sh backtest --strategy momentum --asset BTC --period "2023-2024" --entry-rsi 30 --exit-rsi 70
```

### risk
Calculate position size and risk metrics.
```bash
bash scripts/script.sh risk --capital 10000 --risk-pct 1 --entry 3200 --stop 3050
```

### portfolio
Analyze portfolio allocation and correlation.
```bash
bash scripts/script.sh portfolio --assets "BTC,ETH,SOL,BNB" --weights "40,30,20,10"
```

### screener
Screen assets by technical criteria.
```bash
bash scripts/script.sh screener --market crypto --filter "rsi<35,above-ma200,volume-spike"
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Key Metrics Output
- Sharpe ratio, max drawdown, win rate, profit factor
- Position sizing: Kelly criterion and fixed fractional
- Risk/reward ratio per trade

## Disclaimer
For educational and research purposes only. Not financial advice. Always verify with real market data before trading.

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
