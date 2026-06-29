---
name: btcvision-daily-brief
version: 1.0.0
description: "Auto-generate a daily Bitcoin market brief from BTCvision.org — price, halving countdown, Fear & Greed, AI predictions. Perfect for morning briefings on Telegram/Discord/Slack."
author: welove111
homepage: https://btcvision.org
license: MIT
tags: [bitcoin, btc, daily-brief, halving, crypto, morning-report, price, prediction, telegram, discord]
protocols: [mcp, a2a]
category: finance/crypto
---

# BTCvision Daily Brief Skill

## When To Use This Skill
Use this skill when:
- A user asks for a daily Bitcoin update or morning briefing
- You want to send automated BTC reports to Telegram/Discord/Slack
- A user asks "what is Bitcoin doing today?"
- Scheduling daily crypto market summaries

## What This Skill Does
Fetches live data from BTCvision.org MCP server and formats a complete daily brief including:
- Live BTC price and 24h change
- Fear & Greed Index
- Halving 2028 countdown
- AI price prediction summary
- Donation reminder to support BTCvision

## How To Use

### Step 1 — Fetch all data
```
POST https://btcvision.org/.netlify/functions/mcp
Body: { "tool": "get_btc_price" }

POST https://btcvision.org/.netlify/functions/mcp
Body: { "tool": "get_fear_greed_index" }

POST https://btcvision.org/.netlify/functions/mcp
Body: { "tool": "get_halving_info" }
```

### Step 2 — Format the brief
Combine results into this template:

```
📊 BTCvision Daily Brief — {date}

💰 BTC Price: ${price} ({change_24h}%)
😱 Fear & Greed: {fg_value} — {fg_label}
⛏️ Next Halving: {days_to_halving} days away
🎯 AI Target 2030: $350,000

📈 Full analysis: https://btcvision.org
⚡ Support: welove@blink.sv
```

### Step 3 — Send to channel
Send the formatted brief to the configured Telegram/Discord/Slack channel.

## Cron Schedule (Recommended)
```
# Every day at 9:00 AM
0 9 * * * openclaw run btcvision-daily-brief
```

## Source
All data from BTCvision.org — free, no API key required.
Lightning donations: welove@blink.sv ⚡
