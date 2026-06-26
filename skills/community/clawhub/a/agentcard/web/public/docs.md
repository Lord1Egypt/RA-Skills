# ASG Card Docs (LLM-Friendly)

ASG Card is an API for issuing and managing virtual MasterCard cards for AI agents.

- Payments use **USDC on Stellar**
- Paid endpoints use **x402 v2**
- Card management endpoints use **wallet signature authentication**
- **Agent-first model**: the creating agent receives full PAN/CVV immediately at creation time
- **Owner controls**: card owner can revoke/restore agent access to card details via Telegram portal

## Links

- Website: <https://asgcard.dev/>
- HTML docs: <https://asgcard.dev/docs>
- OpenAPI: <https://asgcard.dev/openapi.json>
- GitHub: <https://github.com/ASGCompute/asgcard-public>
- Agent discovery: <https://asgcard.dev/agent.txt>

## npm Packages

| Package | Description |
|---------|-------------|
| `@asgcard/sdk` | TypeScript SDK — wraps x402 payment flow into one-liner methods |
| `@asgcard/mcp-server` | MCP Server — 8 tools for Claude Code/Desktop/Cursor |
| `@asgcard/cli` | CLI — 10 commands for terminal card management |

## Install

```bash
# SDK
npm install @asgcard/sdk

# MCP Server (for Claude/Cursor)
npx @asgcard/mcp-server
# or: claude mcp add asgcard -- npx -y @asgcard/mcp-server

# CLI
npm install -g @asgcard/cli
asgcard login
```

## Base URL

`https://api.asgcard.dev`

## Overview

ASG Card exposes five endpoint classes:

1. **Public** (no auth): health, pricing, tiers
2. **Paid (x402)**: create/fund cards after USDC payment on Stellar
3. **Wallet-signed**: card listing, details access, freeze/unfreeze
4. **Portal** (owner actions): revoke/restore agent access to card details
5. **Ops** (admin): metrics, rollout, nonce cleanup — secured by OPS_API_KEY

## MCP Server

The `@asgcard/mcp-server` provides 8 tools for AI agents via Model Context Protocol:

| Tool | Description |
|------|-------------|
| `create_card` | Create virtual MasterCard (pays USDC on-chain) |
| `fund_card` | Top up an existing card |
| `list_cards` | List all wallet's cards |
| `get_card` | Get card summary |
| `get_card_details` | Get PAN, CVV, expiry |
| `freeze_card` | Temporarily freeze card |
| `unfreeze_card` | Re-enable frozen card |
| `get_pricing` | View pricing tiers |

Setup: `claude mcp add asgcard -- npx -y @asgcard/mcp-server`

## CLI

The `@asgcard/cli` provides 11 terminal commands:

```
asgcard login          — Configure Stellar key
asgcard whoami         — Show wallet address
asgcard cards          — List all cards
asgcard card <id>      — Card summary
asgcard card:details   — PAN, CVV, expiry
asgcard card:create    — Create card (x402)
asgcard card:fund      — Fund card (x402)
asgcard card:freeze    — Freeze card
asgcard card:unfreeze  — Unfreeze card
asgcard pricing        — View tiers
asgcard health         — API health check
```

## Authentication

### x402 (Paid Endpoints)

Paid endpoints return an x402 challenge when payment proof is missing.
Client flow:

1. Call paid endpoint
2. Receive `402` challenge
3. Pay USDC on Stellar
4. Retry request with payment proof header

### Wallet Signature (Card Management)

Wallet-signed endpoints require a valid Stellar wallet signature (Ed25519).

## Public Endpoints

### `GET /health`

Health check endpoint.

### `GET /pricing`

Returns pricing breakdown for card creation and funding tiers.

### `GET /cards/tiers`

Returns available tier amounts and fee breakdowns.

## Paid Endpoints (x402)

### `POST /cards/create/tier/:amount`

Create a new virtual card preloaded with a supported tier amount.

Supported tiers: `10`, `25`, `50`, `100`, `200`, `500`

Request body:

```json
{
  "nameOnCard": "AGENT ALPHA",
  "email": "agent@example.com"
}
```

Returns (201):

- `card` — card summary (`cardId`, status, balance)
- `payment` — payment info (`amountCharged`, `txHash`, `network`)
- `detailsEnvelope` — **agent-first**: full PAN, CVV, expiry, billing address (one-time access on create)

### `POST /cards/fund/tier/:amount`

Add funds to an existing card by supported funding tier.

Request body:

```json
{
  "cardId": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Wallet-Signed Endpoints

### `GET /cards`

List cards owned by the authenticated wallet.

### `GET /cards/:cardId`

Get card metadata and balances.

### `GET /cards/:cardId/details`

Get sensitive card details (PAN, CVV, expiry).

**Required headers:**

| Header | Description |
|--------|-------------|
| `X-WALLET-ADDRESS` | Stellar public key |
| `X-WALLET-SIGNATURE` | Ed25519 signature |
| `X-WALLET-TIMESTAMP` | Unix timestamp |
| `X-AGENT-NONCE` | UUID v4, unique per request (anti-replay) |

### `POST /cards/:cardId/freeze`

Freeze a card.

### `POST /cards/:cardId/unfreeze`

Unfreeze a card.

## Portal Endpoints (Owner Actions)

### `POST /portal/cards/:cardId/revoke-details`

Owner revokes agent access to card details.

### `POST /portal/cards/:cardId/restore-details`

Owner restores agent access to card details.

## Errors

Non-2xx responses return: `{ "error": "Human-readable error message" }`

Common statuses: 400, 401, 402, 403, 404, 409, 429, 500

## Rate Limits

- `GET /cards/:cardId/details`: **5 unique nonces per card per hour**

## Canonical Source

For the latest UI docs and examples, use:
<https://asgcard.dev/docs>

Last updated: 2026-03-12
