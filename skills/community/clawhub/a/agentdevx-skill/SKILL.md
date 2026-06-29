---
name: agentdevx-skill
description: "Give your AI hands. Register any API via OpenAPI spec — agents get Ed25519 identity, encrypted credential injection, rate limiting, and audit logging automatically. One bootstrap call, zero human setup."
version: 1.0.6
metadata:
  openclaw:
    requires: {}
    homepage: https://agentdevx.onrender.com
    primaryEnv: AGENTDEVX_API_KEY
    envVars:
      - name: AGENTDEVX_API_KEY
        required: false
        description: Auto-obtained on first tool call via self-bootstrap (POST /agents/v1/bootstrap). No human action needed.
      - name: AGENTDEVX_BASE_URL
        required: false
        description: "Default: https://agentdevx.onrender.com"
    tags:
      - mcp
      - api-gateway
      - agent-identity
      - developer-tools
      - ai-infrastructure
      - credential-vault
      - tool-registry
    category: data-and-apis
    homepage: https://agentdevx.onrender.com
---

# AgentDevX Gateway

The first infrastructure layer an AI agent can discover, install, and use entirely on its own — no human OAuth, no manual key exchange, no setup.

Every developer building an AI agent hits the same wall: auth spaghetti, credential sprawl, API integration hell, no stable agent identity, no persistent memory. AgentDevX solves all of this in one gateway.

## Transparency — What Happens On First Use

This skill connects to **AgentDevX**, a third-party hosted gateway. On first tool call, your agent automatically:

1. **Generates an Ed25519 keypair locally** — private key never leaves your machine
2. **Registers with AgentDevX** (`POST /agents/v1/bootstrap`) — outbound network call to `https://agentdevx.onrender.com`
3. **Receives a JWT + 75,000 free credits** — account created automatically
4. **Gains proxy access to any registered API** — pre-built examples include weather, GitHub, exchange rates, and more. Register your own via OpenAPI spec.

This is intentional self-provisioning, not a bug. If you do not want your agent registering with a third-party service, do not invoke this skill's tools.

To revoke access, visit your dashboard at https://agentdevx.onrender.com and delete your account.

## Install

```bash
openclaw skills install agentdevx-skill
```

## What Your Agent Can Do

After install, your agent has:

- **Cryptographic identity** — Ed25519, not OAuth. One identity across all tools.
- **Encrypted credential vault** — AES-256-GCM. Store API keys securely, auto-injected on every call.
- **Access to any registered API** — 7 pre-built examples included. Register any API via OpenAPI spec and agents can use it instantly.
- **Per-agent memory** — encrypted state that persists across sessions.
- **Policy engine** — OPA/Rego access control. Dry-run mode. Full audit log.

## Autonomous Bootstrap Flow

Your agent runs this automatically — no human action needed:

```bash
PUBLIC_KEY=$(openssl rand -hex 32)
BOOTSTRAP=$(curl -s -X POST https://agentdevx.onrender.com/agents/v1/bootstrap \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"openclaw-agent\",\"email\":\"agent@local\",\"public_key\":\"$PUBLIC_KEY\"}")
export AGENTDEVX_API_KEY=$(echo "$BOOTSTRAP" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
```

## MCP Config (Claude Desktop / Cursor / Windsurf / any MCP client)

```json
{
  "mcpServers": {
    "agentdevx": {
      "url": "https://agentdevx.onrender.com/mcp"
    }
  }
}
```

## Register Any API — Pre-built Examples Included

AgentDevX is not a fixed tool collection. Register any API via OpenAPI spec and it becomes instantly available to all agents with automatic credential injection, rate limiting, and audit logging.

Pre-registered examples:

| Tool | What It Does |
|------|-------------|
| open-weather | Live weather & forecasts |
| github-api | Repos, issues, PRs |
| exchange-rate | Live currency conversion |
| public-holidays | Holidays by country |
| acme-mailer | Send emails |
| jsonplaceholder | REST API testing |
| petstore-api | OpenAPI 3.0 demo |

These are examples. POST any OpenAPI spec to register your own API — every agent on the network can use it instantly.

## Why AgentDevX vs Composio / Nango / Auth0

| Feature | AgentDevX | Composio/Nango | Auth0 |
|---------|-----------|----------------|-------|
| AI self-bootstrap | ✅ Yes | ❌ No | ❌ No |
| Ed25519 identity | ✅ Yes | ❌ OAuth only | ❌ OAuth only |
| Encrypted vault | ✅ AES-256-GCM | ✅ OAuth-based | ✅ Enterprise |
| Per-agent memory | ✅ Yes | ❌ No | ❌ No |
| MCP native | ✅ Yes | ❌ No | ❌ No |
| Indie pricing | ✅ Free tier | ❌ Enterprise | ❌ Enterprise |

## Security & Revocation

> ⚠️ **Trust Boundary:** AgentDevX is a third-party hosted gateway. API calls, credentials, and memory contents route through AgentDevX servers. All credentials encrypted at rest with AES-256-GCM. All traffic encrypted via TLS. Full audit log of every action, viewable via the AgentDevX dashboard.

## Links

- 🌐 Gateway: https://agentdevx.onrender.com
- 📊 Smithery: https://smithery.ai/server/io.github.mirajmahmudul/agentdevx
- 🔧 SDK: https://github.com/mirajmahmudul/agentdevx-sdk
- 📦 npm: https://www.npmjs.com/package/@agentdevx/install
