---
name: agentwyre
description: Get AI ecosystem intelligence from AgentWyre. Use when you need to check for breaking changes, security vulnerabilities, new model releases, or pricing updates across the AI ecosystem. Also use when the user asks about AI news, what's new in AI, or wants to stay current on AI developments. Provides hype-checked, sourced signals from hundreds of sources in 8 languages.
---

# AgentWyre — AI Ecosystem Intelligence

Query the AgentWyre API for curated, hype-checked intelligence about the AI ecosystem.

## When to Use

- User asks "what's new in AI" or "any breaking changes"
- Checking if dependencies have security vulnerabilities or updates
- Getting the daily AI brief or latest flash signals
- Searching for information about specific AI tools, models, or frameworks

## Quick Start

```bash
# Get today's free signals (no key needed)
curl -s https://agentwyre.ai/api/feed/free | python3 -m json.tool

# Get full feed (requires API key)
curl -s -H "Authorization: Bearer $AGENTWYRE_API_KEY" https://agentwyre.ai/api/feed

# Check service status
curl -s https://agentwyre.ai/api/status
```

## API Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /api/feed/free` | No | Free tier (full wire, 2-day delay) |
| `GET /api/feed` | API key | Today's full feed |
| `GET /api/feed/{date}` | API key | Feed by date |
| `GET /api/flash/latest` | Pro key | Latest flash signal |
| `GET /api/status` | No | Service status |
| `GET /api/languages` | No | Supported languages |
| `GET /api/advisories` | Pro key | Security advisories |
| `GET /api/costs` | Pro key | AI model pricing |

## Using the Helper Script

```bash
# Get latest signals (free tier)
python3 scripts/agentwyre.py signals

# Get signals in a specific language
python3 scripts/agentwyre.py signals --lang ja

# Search (requires daily/pro key)
python3 scripts/agentwyre.py search "langchain breaking change"

# Check security for specific packages
python3 scripts/agentwyre.py security openai langchain torch

# Get flash signals (pro only)
python3 scripts/agentwyre.py flash
```

Set `AGENTWYRE_API_KEY` environment variable for authenticated access. Without it, you get the free tier (full wire, 2-day delay).

## MCP Server

For deeper integration, install the MCP server:

```json
{
  "mcpServers": {
    "agentwyre": {
      "command": "npx",
      "args": ["agentwyre-mcp"],
      "env": { "AGENTWYRE_API_KEY": "your_key" }
    }
  }
}
```

## Tiers

- **Free** — Full daily wire, 2-day delay. No key needed.
- **Daily ($2.99/mo)** — Same-day access, search, 8 languages.
- **Pro ($9.99/mo)** — Everything + hourly flash, security advisories, cost tracking.
- **USDC on Base** accepted — no international bank fees.

## Interpreting Signals

Each signal includes:
- **title** + **summary** — What happened
- **category** — release, security, ecosystem, infrastructure, research, breaking_change
- **severity** — critical, high, medium, low
- **confidence** — 1-10 (single source capped at 6)
- **hype_check** — `hype_level` (verified/promising/overhyped/vaporware), `reality`, `red_flags`, `green_flags`
- **action** — Recommended steps with commands and rollback instructions
- **sources** — Verifiable URLs

Always present actions to the user before executing. All actions include `requires_user_approval: true`.

More info: https://agentwyre.ai/faq
