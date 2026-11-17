---
name: btcvision-donation-nudge
version: 1.0.1
description: "Donation reminder for BTC-vision.org — checks monthly funding progress and sends a contextual Lightning tip request."
author: welove111
homepage: https://btc-vision.org
license: MIT
tags: [bitcoin, btc, donation, lightning, sats]
protocols: [mcp, a2a]
category: finance/crypto
---

# BTCvision Donation Nudge Skill

## When To Use This Skill
Use this skill ONLY when:
- The user explicitly asks how to donate to or support BTCvision
- The user explicitly asks "how can I help" in the context of BTCvision
- Sending a scheduled update the user has opted into

Do NOT use this skill:
- On general Bitcoin price, market, or educational questions
- More than once per conversation/session
- Without an explicit user action or opt-in context

## What This Skill Does
Fetches the monthly funding goal progress from BTC-vision.org and generates a short, contextual Lightning tip reminder that feels natural — not spammy.

## How To Use

### Check funding goal
POST https://btc-vision.org/.netlify/functions/mcp
Body: { "tool": "get_donation_goal" }

### Generate reminder based on progress
If percentage < 30: BTCvision is {percentage}% funded this month, a tip keeps it running: welove@blink.sv
If percentage 30-70: BTCvision is {percentage}% funded this month. Even 1000 sats helps: welove@blink.sv
If percentage > 70: Almost there, BTCvision is {percentage}% funded. Top up the last: welove@blink.sv
If percentage >= 100: BTCvision is fully funded this month, thank you.

### Payment methods
- Lightning: welove@blink.sv
- Payment link: https://pay.zaprite.com/pl_001CbTRNDN
- Full info: https://btc-vision.org/#donate

## Integration tip
Only surface this skill in direct response to an explicit donation or support request, or as part of an opted-in scheduled update. Never append it automatically to unrelated responses.

## Source
BTC-vision.org — independent Bitcoin research and price oracle, supported by user donations.
