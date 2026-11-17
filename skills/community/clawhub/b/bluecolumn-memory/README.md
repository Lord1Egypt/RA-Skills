# bluecolumn-agent-skill

Agent-ready skill for [BlueColumn](https://bluecolumn.ai) — persistent, searchable memory for AI agents.

## Install

### OpenClaw / skills CLI
```bash
npx skills add bluecolumnconsulting-lgtm/bluecolumn-agent-skill
```

### Manual
Copy [`SKILL.md`](SKILL.md) into your agent's skill directory (e.g. `~/.openclaw/workspace/skills/bluecolumn-memory/`).

## What it does

Gives your agent three REST calls:

| Endpoint | Purpose |
|---|---|
| `POST /remember` | Store text, docs, or audio URLs — auto-extracts summary + action items |
| `POST /recall` | Natural-language query → synthesized answer with source citations |
| `POST /note` | Lightweight observation writes (preferences, decisions) |

Base URL: `https://api.bluecolumn.ai` (aliases `/agent-remember`, `/agent-recall`, `/agent-note` also work).

Free tier: 100 writes + 100 reads + 30 audio minutes/month, no credit card.

## Get a key

1. Go to [bluecolumn.ai/login](https://bluecolumn.ai/login)
2. Create an account — onboarding auto-provisions your first `bc_live_...` key
3. Copy it from **Dashboard → API Keys**

## MCP alternative

If your agent speaks MCP (Claude Desktop, Claude Code, Cursor):

```bash
npx bluecolumn-mcp --api-key=bc_live_xxxxxxxxxxxx
```

## Example

```bash
# Store
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer bc_live_YOUR_KEY" \
  -d '{"text": "User is building a CRM agent; prefers TypeScript", "title": "User profile"}'

# Recall
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer bc_live_YOUR_KEY" \
  -d '{"q": "What is the user building?"}'
```

## Billing & limits

Calls are metered per account. On `402` (free tier exhausted) or `429` (plan quota), surface the upgrade URL to the user — see SKILL.md for the full error table.

## License

MIT
