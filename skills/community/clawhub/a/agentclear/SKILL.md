---
name: agentclear
description: "Discover, call, and pay for APIs through AgentClear — the commerce layer for AI agents. Use when you need to: (1) find an API or tool by describing what you need in natural language, (2) call a paid API service through the AgentClear proxy with automatic micro-billing, (3) list available services on the marketplace, (4) check your AgentClear balance or account status. Requires an AgentClear API key (starts with axk_). Get one free at https://agentclear.dev with $5 in credits."
metadata:
  openclaw:
    requires:
      env:
        - AGENTCLEAR_API_KEY
---

# AgentClear — Agent Commerce Layer

Discover and call paid APIs with natural language. One API key, per-call billing, zero friction.

## Setup

Requires `AGENTCLEAR_API_KEY` environment variable (starts with `axk_`).

```bash
export AGENTCLEAR_API_KEY="axk_your_key_here"
```

Get a free key with $5 credits: https://agentclear.dev/login

## Data & Privacy

- **Discovery queries** are used for semantic matching and logged to power the Bounty Board (demand signals for missing services). No PII is collected.
- **Proxy calls** forward your payload to the upstream service provider you selected. AgentClear does not store request/response payloads — only billing metadata (service ID, timestamp, cost).
- **API keys** authenticate and meter usage. Keys are scoped to your account and can be revoked at any time.
- All traffic is over HTTPS. See https://agentclear.dev/security for full details.

## Endpoints

Base URL: `https://agentclear.dev`

### Discover Services
Find APIs by describing what you need:
```bash
curl -X POST https://agentclear.dev/api/discover \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "parse invoices from PDF", "limit": 5}'
```

Response returns ranked services with `id`, `name`, `description`, `price_per_call`, and `trust_score`.

### Call a Service
Proxy a request through AgentClear (auto-billed per call):
```bash
curl -X POST https://agentclear.dev/api/proxy/{service_id} \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"your": "payload"}'
```

The payload is forwarded to the upstream service. Response includes the service result plus billing metadata.

### List Services
Browse available services:
```bash
curl https://agentclear.dev/api/services \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY"
```

## Workflow

1. **Discover** — Describe what you need → get ranked service matches
2. **Evaluate** — Check price, trust score, and description
3. **Call** — Proxy the request → get result + pay per call
4. If no service exists, check the **Bounty Board** at https://agentclear.dev/bounties

## Pricing

- Services range from $0.001 to $1+ per call (provider-set)
- Platform fee: 2.5%
- New accounts get **$5 free credits**
- Balance auto-deducts per call

## Tips

- Use specific, descriptive queries for better discovery results ("parse QuickBooks QBO files to JSON" beats "parse files")
- Chain services: discover → call → use result as input to another service
- If a discover query returns no results, the query is logged as demand on the Bounty Board — providers will build it
