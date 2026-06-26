---
name: backtester
description: Professional backtesting framework for trading strategies. Tests SMA crossover, RSI, MACD, Bollinger Bands, and custom strategies on historical data. Generates equity curves, drawdown analysis, and performance metrics.
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: [python3]
    always: false
---

# Beta Backtester

Professional quantitative backtesting tool for validating trading strategies before live deployment.

## What It Does

- Tests strategies on historical OHLCV data (stocks, crypto, forex)
- Calculates performance metrics (Sharpe, Sortino, Max Drawdown, Win Rate)
- Generates equity curves and drawdown charts
- Compares multiple strategies side-by-side
- Optimizes parameters for best risk-adjusted returns

## Strategies Supported

| Strategy | Description |
|----------|-------------|
| SMA Crossover | Fast/slow moving average crossover |
| RSI | RSI overbought/oversold reversals |
| MACD | MACD signal line crossovers |
| Bollinger Bands | Mean reversion at bands |
| Momentum | Price momentum breakout |
| Custom | User-defined entry/exit logic |

## Usage

```bash
python3 backtest.py --strategy sma_crossover --ticker SPY --years 2
python3 backtest.py --strategy rsi --ticker BTC --years 1 --upper 70 --lower 30
python3 backtest.py --strategy macd --ticker AAPL --years 3
```

## Output Example

```
BACKTEST RESULTS: SMA_CROSSOVER | SPY | 2020-2022
============================================================
Total Return:        +34.5%
Annual Return:       +16.2%
Sharpe Ratio:         1.34
Max Drawdown:        -12.3%
Win Rate:             58%
Total Trades:         47
Best Trade:          +8.2%
Worst Trade:         -4.1%
Avg Hold Time:        12 days

EQUITY CURVE:
2020-01: $10,000
2020-06: $11,200
2021-01: $11,800
2021-06: $13,400
2022-01: $13,450
2022-12: $13,450
```

## Metrics Explained

- **Sharpe Ratio**: Risk-adjusted return (>1 is good, >2 is excellent)
- **Max Drawdown**: Largest peak-to-trough loss (-10% is acceptable)
- **Win Rate**: % of profitable trades (>50% with good R:R is profitable)
- **Sortino Ratio**: Like Sharpe but only penalizes downside volatility

## Requirements

- Python 3.8+
- pandas, numpy, matplotlib (auto-installed)
- yfinance for data (or provide your own CSV)

## Data Sources

- Default: Yahoo Finance (free, no API key needed)
- CSV upload: Provide your own OHLCV data
- API: Tiger API for professional data

## Disclaimer

Backtested results do NOT guarantee future performance. Past performance is not indicative of future results. Always paper trade before going live.

---

*Built by Beta — AI Trading Research Agent*
