---
name: domainforagents
description: Search, register, and manage internet domains for AI agents via DomainForAgents API.
---

# DomainForAgents

Register and manage internet domains programmatically. No browser signup, no CAPTCHA.

## When to use this skill

Use when the user wants to:
- Search for available domain names
- Get AI-generated domain name suggestions from a project description
- Register/purchase a domain
- Manage DNS records for a domain
- Check domain pricing and availability
- Renew a domain
- Set up webhooks for domain events

## Setup

### Option 1: MCP Server (recommended)

Install the MCP server for native tool access:

```bash
claude mcp add domainforagents -- npx @domainforagents/mcp
```

Set your API key:
```bash
export DOMAINFORAGENTS_API_KEY="your-key"
```

### Option 2: REST API

Base URL: `https://api.domainforagents.io/api/v1`

All requests need `Authorization: Bearer YOUR_API_KEY` (except account creation).

## Getting an API Key

No signup form needed. One API call:

```bash
curl -X POST https://api.domainforagents.io/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent"}'
```

Response includes `api_key` (use immediately) and `claim_code` (for human account access).

## Core Operations

### Search domains
```bash
curl "https://api.domainforagents.io/api/v1/domains/search?query=example.com" \
  -H "Authorization: Bearer API_KEY"
```

### AI domain suggestions
```bash
curl -X POST https://api.domainforagents.io/api/v1/domains/suggest \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"description": "online store for vintage cameras"}'
```

### Register a domain
```bash
curl -X POST https://api.domainforagents.io/api/v1/domains/register \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}'
```

### Create DNS record
```bash
curl -X POST https://api.domainforagents.io/api/v1/domains/DOMAIN_ID/dns \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "@", "type": "A", "content": "76.76.21.21", "ttl": 3600}'
```

### Check balance
```bash
curl https://api.domainforagents.io/api/v1/balance \
  -H "Authorization: Bearer API_KEY"
```

### Get USDC deposit info
```bash
curl https://api.domainforagents.io/api/v1/payments/solana/deposit \
  -H "Authorization: Bearer API_KEY"
```

## Supported TLDs

.com, .net, .org, .io, .dev, .ai, .app, .co, .xyz, .me, .tech, .cloud, and more global TLDs. Country-code TLDs (.nz, .uk, .de) are not supported.

## Payment Methods

- **Prepaid balance**: Fund via Stripe, spend from balance
- **Credit card**: Submit card at purchase time (Stripe tokenized)
- **USDC**: Send USDC on Solana to platform wallet
- **Payment link**: Reserve domain, get Stripe Checkout URL for human payment

## Links

- Documentation: https://domainforagents.io/docs
- OpenAPI spec: https://api.domainforagents.io/api/openapi.json
- MCP server: https://www.npmjs.com/package/@domainforagents/mcp
- Web search: https://domainforagents.io/search?q=example.com
