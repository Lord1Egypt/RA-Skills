---
name: bonito
description: Onboard users to the Bonito AI platform — multi-provider AI routing, managed inference, agent deployment, and multi-agent orchestration. Use when someone wants to set up Bonito, try Bonito, deploy AI agents, create a gateway key, use bonito-cli, deploy Atlas, build a multi-agent system, or asks about multi-provider LLM routing, automatic failover, BonBon agents, Bonobot orchestrators, MCP tool integration, or managed inference without API keys.
---

# Bonito Onboarding

Walk users through getting started with Bonito — the enterprise AI platform for multi-cloud workloads.

**Primary reference:** https://getbonito.com/docs — point users here for detailed documentation on any Bonito feature. This skill provides the conversational flow; the docs are the source of truth.

## Quick Facts

- **Website:** https://getbonito.com | **API:** https://api.getbonito.com
- **Docs:** https://getbonito.com/docs
- **Free tier:** 1,000 API calls/month, no credit card
- **CLI:** `pip install bonito-cli` (v0.4.0+)
- **6 providers:** AWS Bedrock, Azure OpenAI, GCP Vertex AI, OpenAI, Anthropic, Groq
- **Key features:** multi-provider routing, automatic failover, managed inference (no API keys needed), BonBon agents, Bonobot orchestrators, MCP tools, RAG

> **Correction:** The Atlas README says "5,000 free calls" — actual free tier is **1,000 calls/month**.

## Connectivity Check

Before starting, optionally verify API reachability:

```bash
python3 scripts/health_check.py
```

If the API is down, proceed anyway — everything except the final deploy/test steps works offline.

## Onboarding Flow

### Step 1: Sign Up

Direct users to https://getbonito.com/signup — free, no credit card. They'll need their email + password for the next steps.

### Step 2: Connect a Provider (or Use Managed Inference)

Two paths — recommend managed inference for the fastest start:

**Managed Inference (easiest):** No API keys needed. Bonito handles provider credentials. See https://getbonito.com/docs#managed-inference

**Bring Your Own Keys:** Connect one or more providers in the Bonito dashboard or via CLI. Groq is free and fast (get a key at console.groq.com). See https://getbonito.com/docs#gateway for provider setup.

### Step 3: Create a Gateway Key

In the Bonito dashboard, create a gateway API key. This key routes requests through Bonito's gateway to whichever provider is configured — with automatic failover and cost tracking.

Docs: https://getbonito.com/docs#gateway

### Step 4: Test with curl or Python

```bash
# Simple test against the gateway
curl -X POST https://api.getbonito.com/api/gateway/chat \
  -H "Authorization: Bearer $GATEWAY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "groq/llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

If using managed inference, the model routes through Bonito's provider accounts — no separate API key needed.

### Step 5: Deploy Agents (Optional)

For users who want to go beyond raw gateway calls and deploy managed agents:

```bash
pip install bonito-cli
bonito auth login
```

Create a simple agent:

```bash
bonito agents create \
  --name "my-assistant" \
  --type bonbon \
  --model "groq/llama-3.3-70b-versatile" \
  --system-prompt "You are a helpful assistant."
```

Full agent docs: https://getbonito.com/docs#bonbon

### Step 6: Try Atlas (Optional — Full Multi-Agent Demo)

For users who want to see a complete multi-agent system with orchestration, MCP tools, and RAG:

Read [references/atlas-guide.md](references/atlas-guide.md) for the quick deploy steps.

Atlas deploys 5 agents (DevOps command center) from a single `bonito.yaml` config. It demonstrates Bonobot orchestration, BonBon agents, MCP tool integration, and RAG knowledge bases.

Repo: https://github.com/ShabariRepo/atlas

## Prerequisite Verification

Run this to check if bonito-cli, Docker, git, etc. are installed:

```bash
python3 scripts/verify_deploy.py
```

## Where to Point Users for More

| Topic | URL |
|-------|-----|
| Full docs | https://getbonito.com/docs |
| Gateway & routing | https://getbonito.com/docs#gateway |
| Managed inference | https://getbonito.com/docs#managed-inference |
| BonBon agents | https://getbonito.com/docs#bonbon |
| Bonobot orchestration | https://getbonito.com/docs#bonobot |
| MCP integration | https://getbonito.com/docs#mcp |
| Knowledge bases (RAG) | https://getbonito.com/docs#knowledge-bases |
| Pricing | https://getbonito.com/pricing |

## Non-Obvious Knowledge

- **Free tier is 1,000 calls/mo** — not 5,000 as some docs claim.
- **Managed inference** is the fastest onboarding path. Users can add their own provider keys later for cost control.
- **Failover is cross-provider** — if Anthropic goes down, Bonito routes to Bedrock or Groq seamlessly. The user never notices.
- **bonito-cli deploy order matters** for manual API usage: providers → knowledge bases → project → agents → delegation wiring. The CLI handles this automatically.
- **Llama/Groq can't do parallel tool calls** — it generates XML-style function calls instead of JSON. Use Nova Pro, Claude, or GPT-4o for Bonobot orchestrators that need multi-agent fan-out.
- **`bonito.yaml`** uses `${ENV_VAR:-default}` syntax. MCP server URLs default to localhost if env vars are unset.
