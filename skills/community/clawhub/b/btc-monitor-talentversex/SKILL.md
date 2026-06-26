---
name: btc-monitor-talentversex
description: BTC and ETH market monitor with public API data, six bottom-fishing signals, and optional Discord delivery. TalentverseX
---

# BTC Monitor TalentverseX

Use this skill when the user wants a quick BTC/ETH market-monitoring report based on public APIs, especially for oversold or bottom-fishing style checks.

## What This Skill Does

- Reads runtime settings from `{baseDir}/config.json`
- Fetches BTC/ETH market candles, preferring Binance, then Bybit, then CoinGecko-derived fallback
- Fetches CoinGecko market metadata and the Fear & Greed Index
- Computes 6 implemented signals:
  - RSI oversold
  - Volume washout
  - MACD histogram below zero
  - Price near lower Bollinger band
  - Extreme fear
  - Low MVRV proxy
- Prints a plain-text report
- Optionally posts the report to Discord if enabled in config and the bot token exists in the environment

## What This Skill Does Not Do

- It does not place trades
- It does not use Glassnode, Twitter, Reddit, or any LLM integration
- It does not provide a true on-chain MVRV metric; `MVRV proxy` is an approximation from CoinGecko history

## Files

- `{baseDir}/scripts/monitor.py`: main executable
- `{baseDir}/config.json`: runtime configuration
- `{baseDir}/requirements.txt`: Python dependency list
- `{baseDir}/scripts/install.sh`: optional install helper for bash environments
- `{baseDir}/scripts/setup_cron.sh`: optional cron helper for bash environments
- `{baseDir}/docs/TROUBLESHOOTING.md`: troubleshooting notes

## How To Run

Install dependencies:

```bash
python3 -m pip install -r {baseDir}/requirements.txt
```

Run once:

```bash
python3 {baseDir}/scripts/monitor.py
```

## Discord Delivery

To send the report to Discord:

1. Set `"discord.enabled": true` in `{baseDir}/config.json`
2. Set `"discord.channel_id"` in `{baseDir}/config.json`
3. Export the env var named by `"discord.token_env"` before running the script

Example:

```bash
export DISCORD_TOKEN=your_bot_token
python3 {baseDir}/scripts/monitor.py
```

## When To Use It

- Daily or scheduled BTC/ETH market summaries
- Quick oversold-signal checks
- Lightweight Discord alerts using only public data sources

## Scheduling

The script runs once per invocation. Use cron, Task Scheduler, or another external scheduler if the user wants recurring execution.
