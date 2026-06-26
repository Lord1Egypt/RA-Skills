# Atlas — Optional Multi-Agent Demo

Atlas is a reference project that deploys 5 AI agents (DevOps command center) to Bonito. It's a good way to see multi-agent orchestration, MCP tool integration, and RAG in action — but it's **not required** to use Bonito.

## Prerequisites

- Bonito account + gateway key (complete the main onboarding first)
- Docker (for mock MCP servers)
- bonito-cli: `pip install bonito-cli`

## Quick Deploy

```bash
git clone https://github.com/ShabariRepo/atlas.git
cd atlas
cp .env.example .env
# Edit .env with your Bonito credentials + at least one provider key
# (or use managed inference — just set BONITO_EMAIL/PASSWORD/API_URL)

# Start 4 mock MCP servers (GitHub, PagerDuty, Slack, Jira on ports 3100-3103)
docker compose -f docker-compose.mcp.yml up -d

# Authenticate and deploy
bonito auth login
bonito deploy -f bonito.yaml          # --dry-run to validate first
```

## What Gets Deployed

| Agent | Type | Role |
|-------|------|------|
| Command Center | Bonobot (orchestrator) | Routes requests to specialists |
| Incident Responder | BonBon | Triage alerts via PagerDuty/Jira/Slack MCP |
| Code Reviewer | BonBon | Review PRs via GitHub MCP |
| Docs Assistant | BonBon | Answer questions via RAG knowledge base |
| Deploy Monitor | BonBon | Track deploys via GitHub/Slack MCP |

The entire stack is defined in a single `bonito.yaml`. See comments in that file for what's working vs roadmap.

## Test

```bash
./scripts/test-agents.sh
```

## Model Note

Use a strong model (Nova Pro, Claude, GPT-4o) for the Command Center orchestrator. Llama/Groq works for sub-agents but fails on parallel multi-agent fan-out.

## More Info

- Full README in the repo: https://github.com/ShabariRepo/atlas
- Bonito docs: https://getbonito.com/docs
