# Crypto Trading Bot

> Automated crypto scalping bot for Binance Futures USDT-M

## Description

A complete crypto trading bot with multiple strategies:
- **Scalper**: RSI + EMA + Volume based trading
- **Bollinger Bands**: Mean reversion strategy
- **QA System**: Auto health checks

## Features

- 6 trading pairs: BTC, ETH, SOL, BNB, XAU, XAG
- Auto SL/TP management
- Telegram notifications
- System health monitoring
- Backtest ready

## Usage

```bash
# Setup credentials
nano binance.env
nano telegram.env

# Verify setup
bash setup.sh

# Run strategies
bash run_cycle.sh              # Scalper
bash run_mean_reversion.sh     # Bollinger
bash run_qa.sh                # QA check
```

## Requirements

- Python 3.8+
- Binance Futures account
- VPS (recommended)

## Docs

See README.md for full installation guide.
