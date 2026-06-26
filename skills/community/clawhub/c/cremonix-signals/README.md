# Cremonix Trading Signals

Live BTC/ETH regime intelligence from a production trading system. Not backtested theory. Not a demo. This is the same ML ensemble that executes real trades for Cremonix clients, now available as a free intelligence feed.

## What it does

Tells you the current market regime for BTC and ETH, and whether any high-probability setup has passed all constraint filters. Four regimes, two timeframes (1h and 4h), structured JSON output.

Most trading tools tell you what happened. This one shows you the current market conditions so you can make informed decisions.

## Install

### OpenClaw users
```bash
clawhub install cremonix-signals
```

### Manual
Download the zip from [ClawHub](https://clawhub.com/skills/cremonix-signals) and extract to your agent's `skills/` folder.

### No agent? Just want the data?
```bash
curl -s "https://blog.cremonix.com/feeds/cremonix-free.json" | jq .
```

## Quick start

No account, no API key, no setup. Just fetch:

```bash
curl -s "https://blog.cremonix.com/feeds/cremonix-free.json"
```

Ask your agent:

- "What regime is BTC in right now?"
- "Should I be trading or sitting out?"
- "Are there any setups that passed all filters?"

## What you get

- Market regime for BTC and ETH (1h + 4h timeframes)
- Setup detection when ML models trigger and pass constraint filters
- Updated every 5 minutes with a 4-hour delay
- Structured JSON, no parsing ambiguity

## Regimes

- Trend_Up: Strong uptrend. Best conditions for entries.
- Trend_Down: Downtrend. Most models blocked.
- Chop_Mean_Reversion: Range-bound. Sit-out conditions for most strategies.
- Panic_High_Vol: Extreme volatility. High conviction required.

## Upgrade to real-time

The free feed runs on a 4-hour delay. For zero-delay access to the same signals that trigger live trades:

https://app.cremonix.com/api-subscribe

$25/month via Lightning or card.

## Links

- Website: https://cremonix.com
- Blog: https://blog.cremonix.com
- Support: support@cremonix.com

## Disclaimer

For informational purposes only. Not financial advice. Past performance does not guarantee future results. Always do your own research.
---

Built by Cremonix. Systematic BTC/ETH trading.
