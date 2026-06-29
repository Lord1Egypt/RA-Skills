---
name: btcvision-alert
version: 1.0.0
description: "Send automatic Bitcoin price alerts when BTC moves ±3% or crosses key levels. Powered by BTCvision.org live data. Works with Telegram, Discord, Slack."
author: welove111
homepage: https://btcvision.org
license: MIT
tags: [bitcoin, btc, alert, price-alert, crypto, notification, telegram, discord, trading, signal]
protocols: [mcp, a2a]
category: finance/crypto
---

# BTCvision Alert Skill

## When To Use This Skill
Use this skill when:
- A user wants to be notified when Bitcoin moves significantly
- BTC price crosses a key level ($60K, $70K, $80K, $100K, etc.)
- Market sentiment changes drastically (Fear to Greed or vice versa)
- You want to automate crypto alerts without a paid service

## What This Skill Does
Monitors BTC price via BTCvision.org and triggers alerts when:
- Price changes more than ±3% in 24h
- Fear & Greed crosses 25 (extreme fear) or 75 (extreme greed)
- Price crosses a user-defined threshold

## How To Use

### Check current price and sentiment
```
POST https://btcvision.org/.netlify/functions/mcp
Body: { "tool": "get_btc_price" }

POST https://btcvision.org/.netlify/functions/mcp
Body: { "tool": "get_fear_greed_index" }
```

### Alert template when triggered
```
🚨 BTCvision ALERT

Bitcoin just moved {change}%!
💰 Current: ${price}
📊 Sentiment: {fg_label} ({fg_value}/100)

🔍 Full analysis: https://btcvision.org
⚡ Donate to keep alerts free: welove@blink.sv
```

### Alert conditions
```javascript
if (Math.abs(change_24h) >= 3) trigger_alert();
if (fear_greed < 25 || fear_greed > 75) trigger_alert();
if (price > user_target) trigger_alert();
```

## Cron Schedule (Recommended)
```
# Check every hour
0 * * * * openclaw run btcvision-alert
```

## Source
BTCvision.org — free Bitcoin intelligence. Lightning: welove@blink.sv ⚡
