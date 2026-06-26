# BestYou OpenClaw Skill

Connects OpenClaw agents to [BestYou](https://bestyou.ai)'s health intelligence platform via MCP. Query daily readiness, manage workouts, analyze meals, and coordinate your Action Plan through natural conversation.

## What's included

- `SKILL.md` — Full skill definition with setup, agent behavior rules, tool reference, and examples.
- `references/setup.md` — Self-contained setup guide.
- `references/security.md` — Data handling and privacy details.

## Install

```bash
clawhub install bestyou
```

## Prerequisites

1. BestYou iOS app installed with an active subscription.
2. API key generated in-app: **More → Connected Apps → OpenClaw → Generate Key**.
3. Set `BESTYOU_API_KEY` in your environment.
4. Add the MCP server via mcporter (see SKILL.md for config).

## Links

- [BestYou](https://bestyou.ai)
- [Setup Guide](https://bestyou.ai/openclaw-setup)
- [MCP Playground](https://mcp.bestyou.ai/openclaw)
- Free month with code `OPENCLAW1MO`
