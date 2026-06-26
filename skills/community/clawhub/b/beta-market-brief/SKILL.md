---
name: tiger-market-brief
description: Generate a concise Chinese market brief for the trader agent using Tiger API first and Yahoo Finance as supplement. Use for hourly market snapshots, trader brief requests, or scheduled market updates. Always run the local script instead of freehand summarizing.
---

# Tiger Market Brief

Use this skill when the user asks for:

- `market brief`
- 每小时市场简报
- trader 简报
- 用 Tiger API 拉市场快照

## Required Command

Always run:

```bash
/Users/zhouwen/.openclaw/workspace-papertrader/venv/bin/python \
  /Users/zhouwen/.openclaw/workspace-papertrader/scripts/tiger_market_brief.py \
  --mode hourly
```

## Rules

- Use Tiger API for market data first
- If US real-time quote permission is unavailable, use Tiger delayed briefs and state that clearly
- Use Yahoo Finance only for supplementary items such as VIX, US10Y, BTC, and headline links
- Return the script output directly with minimal extra commentary
