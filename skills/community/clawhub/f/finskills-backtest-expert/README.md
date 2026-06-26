# backtest-expert

> Design, simulate, and rigorously evaluate quantitative trading strategies using historical OHLCV data and Fama-French factor attribution — powered by [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro%20%2B%20Free-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-quantitative-red.svg)]()

---

## What This Skill Does

1. Translates a natural-language strategy hypothesis into formal entry/exit rules
2. Fetches historical OHLCV data for all strategy symbols and the benchmark
3. Computes signals from price data (SMA crossover, RSI, momentum, etc.)
4. Calculates a full performance scorecard: CAGR, Sharpe, Sortino, Max Drawdown, Calmar, Win Rate
5. Runs Fama-French 3-factor attribution to isolate true alpha
6. Performs walk-forward validation to detect overfitting (In-Sample vs. Out-of-Sample)
7. Stress-tests performance during COVID crash, 2022 bear market, and 2008 crisis

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/finskills-backtest-expert):

1. Visit **[https://clawhub.ai/finskills/finskills-backtest-expert](https://clawhub.ai/finskills/finskills-backtest-expert)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: Backtest a 20/50 day SMA crossover on AAPL for the last 5 years vs SPY
Claude: [Fetches 5Y daily AAPL + SPY history, generates signals, computes full scorecard, runs F-F attribution]
```

## Example Triggers

- `"Backtest a momentum strategy on the S&P 500 for 3 years"`
- `"How would a buy-when-RSI<30 strategy perform on QQQ?"`
- `"Test a mean-reversion strategy on SPY using Bollinger Bands"`
- `"Compare a 50/200 SMA crossover vs buy-and-hold on NVDA"`
- `"Build a walk-forward test for my golden cross strategy"`

## Performance Metrics Generated

| Metric | Description |
|--------|-------------|
| CAGR | Compound annual growth rate |
| Sharpe Ratio | Risk-adjusted return (excess return / vol) |
| Sortino Ratio | Downside-risk adjusted return |
| Max Drawdown | Largest peak-to-trough decline |
| Calmar Ratio | CAGR / Max Drawdown |
| Win Rate | % of trading days profitable |
| Factor Alpha | Return unexplained by market/size/value |
| WF Efficiency | Out-of-sample Sharpe / In-sample Sharpe |

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/stocks/history/{symbol}?period=5y&interval=1d` | Pro | OHLCV history |
| `GET /v1/free/market/fama-french` | Free | 3-factor attribution |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **Pro plan required** for historical price data
- Free plan is used for Fama-French factor data
- **Claude** with skill support

## Strategy Examples

| Strategy | Signal | Typical Use |
|----------|--------|-------------|
| SMA Crossover | Fast MA > Slow MA | Trend following |
| RSI Reversion | RSI < 30 buy / > 70 sell | Mean reversion |
| Momentum | 12-month return > 0 | Factor momentum |
| Bollinger Band | Price < lower band | Volatility breakout |

## License

MIT — see [LICENSE](../LICENSE)
