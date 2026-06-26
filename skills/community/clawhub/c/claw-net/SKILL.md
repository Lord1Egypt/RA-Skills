---
name: claw-net
description: Ask a question in plain English, get data from 13,000+ APIs in one call. Crypto prices, social data, market intelligence. Every response is cryptographically signed. Pay $0.001 per query. No account needed with x402 (USDC).
metadata:
  homepage: https://claw-net.org
  source: https://github.com/1xmint/claw-net
  soma: https://api.claw-net.org/.well-known/soma.json
  erc8004:
    chain: base
    agentId: 36119
    soma_agentId: 37696
  openclaw:
    requires:
      env:
        - CLAWNET_API_KEY
    primaryEnv: CLAWNET_API_KEY
  tags:
    - orchestration
    - x402
    - soma
    - identity
    - provenance
    - data-skills
    - mcp
---

# ClawNet

Ask a question in plain English. Get data from 13,000+ APIs in one call. ClawNet figures out which data sources to query, runs them in parallel, and gives you one clean answer.

## Quick Start

```bash
curl -X POST https://api.claw-net.org/v1/orchestrate \
  -H "X-API-Key: $CLAWNET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of SOL right now?"}'
```

```json
{
  "answer": "SOL is currently trading at $148.23, up 3.2% in 24h. Volume: $2.1B...",
  "costBreakdown": { "creditsUsed": 8, "costUsd": 0.008 },
  "metadata": { "stepsExecuted": 3, "totalDurationMs": 1240 }
}
```

That's it. One question in, one answer out.

## Setup (3 options)

**Option A: API Key** (most common)
1. Get a key at https://claw-net.org/dashboard
2. Set `CLAWNET_API_KEY` in your environment
3. Base URL: `https://api.claw-net.org`

**Option B: x402 / USDC** (no account needed)
Pay per call with USDC on Base. No API key, no signup. Your wallet-equipped agent just calls the endpoint and pays automatically.
```bash
POST https://api.claw-net.org/x402/orchestrate
POST https://api.claw-net.org/x402/skills/{id}
```

**Option C: MCP** (for AI coding tools)
Connect ClawNet as an MCP server in Claude Code, Cursor, VSCode, or Windsurf:
```json
{
  "mcpServers": {
    "clawnet": {
      "command": "npx",
      "args": ["tsx", "src/mcp/server.ts"],
      "env": { "CLAWNET_API_KEY": "your_key", "CLAWNET_BASE_URL": "https://api.claw-net.org" }
    }
  }
}
```

## Data Skills (4 built-in)

Pre-built skills that return structured JSON. No LLM involved — fast and cheap:

| Skill | Cost | What you get |
|---|---|---|
| `price-oracle-data` | 1 credit ($0.001) | Real-time price, 24h change, volume, market cap |
| `trending-tokens-data` | 2 credits ($0.002) | Top trending tokens by volume and social buzz |
| `whale-tracker-data` | 2 credits ($0.002) | Large holder movements, net flow, holder changes |
| `defi-yield-data` | 2 credits ($0.002) | DeFi yield opportunities, APY, TVL, risk tier |

```bash
curl "https://api.claw-net.org/v1/skills/price-oracle-data/query?token=SOL" \
  -H "X-API-Key: $CLAWNET_API_KEY"
```

## How to Use ClawNet

### Step 1: Browse (free, no auth)

See what's available without an API key:

```bash
# Browse the skill catalog
GET /v1/marketplace/skills

# Check a specific skill's input format and pricing
GET /v1/marketplace/skills/price-oracle-data
```

### Step 1b: Search & estimate (free, but needs API key)

```bash
# Semantic search for skills by topic
POST /v1/discover  {"query": "solana token prices"}

# Preview cost before running a query
GET /v1/estimate?query=What is SOL worth?
```

### Step 2: Ask (uses credits)

Send a natural language query. ClawNet's LLM picks the best endpoints, runs them in parallel, and synthesizes the answer:

```bash
POST /v1/orchestrate  {"query": "Compare SOL vs ETH performance this week"}
```

Every response includes cryptographic proof of where the data came from (see [Provenance](#provenance) below).

### Step 3: Call directly (after discovery)

Once you know which skill you need, skip the LLM routing and call it directly — faster and cheaper:

```bash
# With API key
POST /v1/skills/price-oracle-data/invoke  {"variables": {"token": "SOL"}}

# With USDC (no API key needed)
POST /x402/skills/price-oracle-data  {"variables": {"token": "SOL"}}
```

### Step 4: Come back when needs change

The registry updates every 4 hours with new endpoints from 7 discovery sources. New question? New data need? Use `/v1/orchestrate` again to discover the right endpoints.

## Verify Data (optional)

Cross-reference any answer against independent sources before acting on it:

```bash
curl -X POST https://api.claw-net.org/v1/manifest \
  -H "X-API-Key: $CLAWNET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tier": "standard", "verify": {"claims": [{"type": "price", "subject": "SOL", "value": 148.23}]}}'
```

Tiers: `quick` (0.5 credits), `standard` (2 credits), `deep` (5 credits).

## All Endpoints

### Free (no auth needed)

| Endpoint | What it does |
|---|---|
| `GET /v1/marketplace/skills` | Browse the skill catalog |
| `GET /v1/marketplace/skills/:id` | Skill details, input schema, pricing |
| `GET /v1/soma/:did/trust` | Check any agent's verification history |
| `GET /v1/soma/:did/verdicts` | Recent verification verdicts for an agent |
| `GET /.well-known/soma.json` | ClawNet's cryptographic identity |

### Requires API key (but no credit cost)

| Endpoint | What it does |
|---|---|
| `POST /v1/discover` | Semantic search for skills by topic |
| `GET /v1/estimate?query=...` | Preview cost before running a query |
| `GET /v1/balance` | Check your credit balance |

### Paid (API key or x402)

| Endpoint | Cost | What it does |
|---|---|---|
| `POST /v1/orchestrate` | 2+ credits | Natural language query across 13,000+ sources |
| `GET /v1/skills/:id/query` | 1-2 credits | Query a data skill (structured JSON) |
| `POST /v1/skills/:id/invoke` | varies | Invoke a skill directly with variables |
| `POST /v1/manifest` | 0.5-5 credits | Cross-reference data against independent sources |

## Pricing

**1 credit = $0.001.** Credits never expire. Buy at https://claw-net.org (Stripe or USDC).

A typical orchestration query costs 2-10 credits ($0.002-$0.01). Data skills cost 1-2 credits each.

## Endpoint Discovery

ClawNet doesn't just have a static list of APIs. It auto-discovers new endpoints every 4 hours from 7 sources:

| Source | Endpoints |
|---|---|
| Built-in registry | 274 curated |
| [ClawAPIs](https://clawapis.com) | Dynamic providers |
| [402index](https://402index.io) | 15,000+ community directory |
| [Coinbase Bazaar](https://cdp.coinbase.com) | Official x402 discovery |
| [Zauth](https://zauthx402.com) | Pre-verified (only WORKING status) |
| [Dexter](https://x402.dexter.cash) | Facilitator marketplace |
| [x402list](https://x402list.fun) | 17,000+ services |

When you ask a question, ClawNet searches across all of these to find the best data source.

## Provenance

Every response is cryptographically signed. You don't have to trust ClawNet — you can verify.

**What this means in practice:** Each response includes proof of what data was fetched, from where, and that it hasn't been tampered with. This happens automatically — no extra steps needed.

**Response headers** (on every orchestration and x402 response):
```
X-Soma-Protocol: soma/1.0
X-Soma-Data-Hash: <hash of the response data>
X-Soma-Signature: <cryptographic signature>
X-Soma-Model-Verified: true
X-Soma-Discovery: /.well-known/soma.json
```

**Want to go deeper?**
- `GET /.well-known/soma.json` — ClawNet's full cryptographic identity
- `GET /v1/soma/:did/trust` — verification history for any agent (free, public)
- Install [soma-sense](https://www.npmjs.com/package/soma-sense) to independently verify ClawNet's model usage via MCP
- Read the [Soma paper](https://doi.org/10.5281/zenodo.19260081) for the full protocol

**On-chain identity:** ClawNet ([36119](https://basescan.org/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/36119)) and Soma ([37696](https://basescan.org/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/37696)) are registered on Base Mainnet via [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004).

## Error Codes

| Code | Status | Meaning |
|---|---|---|
| `INSUFFICIENT_CREDITS` | 402 | Out of credits — buy more or use x402 |
| `INVALID_API_KEY` | 401 | Bad or missing API key |
| `RATE_LIMITED` | 429 | Too many requests — wait and retry |
| `SOURCE_ERROR` | 502 | Upstream data source failed — try again |
