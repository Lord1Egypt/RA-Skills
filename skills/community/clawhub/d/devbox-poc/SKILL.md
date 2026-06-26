---
name: devbox-poc
description: "Trading strategy sandbox — backtest and deploy strategies via natural language. POC demo with mock data."
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# Trading DevBox (POC)

Trading strategy sandbox. User describes trading intent in natural language, agent backtests and deploys.

## Setup

Install the OpenClaw plugin:

```bash
openclaw plugins install devbox-poc
```

Zero user interaction. Wallet auto-generated on first run.

## Tools

This plugin registers 3 tools:

- `trading_backtest` — Backtest a strategy from natural language description
- `trading_deploy` — Deploy a backtested strategy to live trading
- `trading_status` — Check status of deployed strategies

## Commands

- `/wallet` — Show wallet address and AIUSD balance
- `/status` — Show active trading strategies

## Usage

Just describe your trading idea:

```
BTC 跌破 MA20 做空，止损 2%，止盈 5%
```

Adjust:

```
加 RSI < 30 过滤
```

Deploy:

```
上线，100 USDC
```

## Response Format

Always respond in user's language. Keep messages concise.
