---
name: agent-launchpad
description: Generate complete, deployable AI agent skill packages from natural language descriptions. Includes 6 templates (monitor, scraper, analyst, trader, assistant, webhook) with optional SkillPay monetization. Use when a user wants to create a new agent, build a skill from scratch, scaffold an agent project, or generate a deployable skill package.
---

# Agent Launchpad

Describe what you want → get a complete agent skill package → publish to ClawHub.

## Generate an Agent

```bash
curl -X POST https://launchpad.gpupulse.dev/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "Monitor ETH price and alert below $2000", "price_credits": 5}'
```

Returns complete SKILL.md + scripts with SkillPay wired in.

## Templates

- **monitor** — watch data, alert on conditions
- **scraper** — extract web data
- **analyst** — reports + insights
- **trader** — paper trading strategies
- **assistant** — domain Q&A
- **webhook** — event listener

## Pipeline

1. POST `/generate` with description
2. Review generated files
3. `clawhub publish` → Live on ClawHub

## Add Payments Later

```bash
curl -X POST /api/v1/monetize -H "Content-Type: application/json" \
  -d '{"agent_id": "ag_...", "price_credits": 10}'
```
