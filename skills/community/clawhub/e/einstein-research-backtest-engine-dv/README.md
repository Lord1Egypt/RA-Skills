# Backtest Engine

Programmatic backtesting framework for running trading strategies against historical data with comprehensive performance reporting.

## Description

The Backtest Engine is the execution counterpart to the Backtest Expert methodology skill. While Backtest Expert provides guidance on how to properly test strategies, this skill provides the actual Python framework to run backtests, calculate metrics, and generate reports. It supports momentum, mean-reversion, and custom signal-based strategies with walk-forward optimization and regime-aware analysis.

## Key Features

- **Multiple strategy types** - Built-in momentum, mean-reversion, and dual-momentum templates
- **Flexible data sources** - Yahoo Finance (free) or custom CSV files
- **Transaction cost modeling** - Configurable commission and slippage
- **Walk-forward optimization** - Train on historical data, test on out-of-sample periods
- **Regime-aware testing** - Split results by market conditions (bull/bear, high/low volatility)
- **Comprehensive metrics** - Sharpe, Sortino, Calmar, max drawdown, CAGR, win rate, profit factor
- **Export formats** - JSON for programmatic use, Markdown for human review

## Quick Start

```bash
# Install dependencies
pip install yfinance pandas numpy scipy

# Run a momentum strategy backtest
python3 scripts/backtest_engine.py \
  --tickers AAPL MSFT GOOG \
  --start 2015-01-01 \
  --end 2024-12-31 \
  --strategy momentum \
  --commission 0.001 \
  --slippage 0.0005 \
  --initial-capital 100000 \
  --output-dir reports/

# Walk-forward optimization
python3 scripts/backtest_engine.py \
  --tickers SPY QQQ IWM \
  --start 2010-01-01 \
  --end 2024-12-31 \
  --strategy dual_momentum \
  --walk-forward \
  --train-months 24 \
  --test-months 6 \
  --output-dir reports/
```

Results are saved as JSON and Markdown in the specified output directory.

## What It Does NOT Do

- Does NOT provide trade recommendations or signals for live trading
- Does NOT connect to brokers or execute real trades
- Does NOT guarantee profitable results (it's a testing tool)
- Does NOT include machine learning or complex factor models (designed for simple systematic strategies)
- Does NOT account for portfolio-level risk management across multiple strategies

## Requirements

- Python 3.8+
- yfinance (free Yahoo Finance data)
- pandas, numpy, scipy
- No API keys required
- Internet connection for downloading price data

## License

MIT
