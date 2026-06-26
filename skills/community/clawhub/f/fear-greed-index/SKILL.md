---
name: fear-greed-index
description: Crypto Fear & Greed Index reporter. Fetches current market sentiment index and provides simple analysis combined with BTC price movement. Use when users want to check market sentiment, view current fear/greed level, or get daily market emotion update.
---

# Crypto Fear & Greed Index

## Overview

Get the current Crypto Fear & Greed Index from Alternative.me, combined with Bitcoin's latest price change, and provides simple market sentiment analysis for traders.

Data source: [Alternative.me Crypto Fear & Greed Index API](https://alternative.me/crypto/fear-and-greed-index/)

## Commands

| Command | Description |
|:---|:---|
| `index.py` | Get latest fear & greed index with market analysis |
| `history.py` | Get 30-day historical data |

## Usage

```bash
# Get latest index and analysis
python scripts/index.py --user-id <user-id>
```

**Pricing:** 0.001 USDT per call, billed via SkillPay.me.

## Output

- Current fear & greed index value (0-100)
- Sentiment classification (Extreme Fear / Fear / Neutral / Greed / Extreme Greed)
- Trend compared to yesterday
- BTC latest price and 24h change
- Simple market sentiment analysis

## Index Classification

| Value | Sentiment |
|:---|:---|
| 0-24 | Extreme Fear |
| 25-44 | Fear |
| 45-55 | Neutral |
| 56-75 | Greed |
| 76-100 | Extreme Greed |
