---
name: amber-proactive
description: "Silently captures significant AI collaboration moments to amber memory storage"
metadata:
  openclaw:
    emoji: "🌙"
    events:
      - "agent:response"
      - "agent:bootstrap"
---

# Amber-Proactive Hook

## What It Does

1. **Fires on `agent:response`** — after every AI response
2. **Analyzes the exchange** for signals worth remembering
3. **Silently writes to amber** via amber-hunter localhost API — zero user interruption

## Significance Signals

| Signal | Examples | Type |
|--------|---------|------|
| User correction | "不对", "actually", "错了", "not quite" | `correction` |
| Error resolved | command failed → found working solution | `error_fix` |
| Key decision made | user confirmed architecture/approach | `decision` |
| User preference stated | "I prefer...", "I usually...", "never..." | `preference` |
| First success | first time achieving something | `discovery` |
| Better approach found | discovered better tool/method | `discovery` |

## No Disruption

- Writes happen silently, no messages to user
- If amber-hunter is down, silently skips
- If content is already captured, skips to avoid duplicates

## Configuration

Requires amber-hunter running on localhost:18998 with api_key configured.
