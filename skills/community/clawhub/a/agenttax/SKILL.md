---
name: agenttax
description: Tax compliance for AI agent transactions — sales tax, capital gains, nexus monitoring, 1099 tracking.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AGENTTAX_API_KEY
      bins:
        - curl
    primaryEnv: AGENTTAX_API_KEY
    emoji: "🧾"
    homepage: https://agenttax.io
    os:
      - linux
      - darwin
      - win32
---

# AgentTax

Tax compliance tools for AI agent transactions. Use when the user or agent needs to:
- Calculate sales tax or use tax on a transaction
- Log trades for capital gains tracking
- Check tax rates by state
- Configure economic nexus states
- Export 1099-DA data

API docs: https://agenttax.io/api/v1/agents

## Authentication

All requests use the header: `X-API-Key: $AGENTTAX_API_KEY`

Get a free API key (100 calls/month):

```bash
curl -s -X POST https://agenttax.io/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "securepass", "agent_name": "my-agent"}'
```

Save the `api_key.key` from the response — it is only shown once.

## Calculate Sales/Use Tax

Use when an AI agent buys or sells services, compute, API access, SaaS, or digital goods.

```bash
curl -s -X POST https://agenttax.io/api/v1/calculate \
  -H "X-API-Key: $AGENTTAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ROLE",
    "amount": AMOUNT,
    "buyer_state": "STATE",
    "buyer_zip": "ZIP",
    "transaction_type": "TYPE",
    "work_type": "WORK_TYPE",
    "counterparty_id": "COUNTERPARTY",
    "is_b2b": IS_B2B
  }'
```

**Required fields:**
- `role`: `"buyer"` or `"seller"`
- `amount`: transaction amount in USD
- `buyer_state`: 2-letter US state code
- `transaction_type`: one of `compute`, `api_access`, `data_purchase`, `saas`, `ai_labor`, `storage`, `digital_good`, `consulting`, `data_processing`, `cloud_infrastructure`, `ai_model_access`, `marketplace_fee`, `subscription`, `license`, `service`
- `counterparty_id`: identifier for the other party

**Optional fields:**
- `buyer_zip`: 5-digit zip for local rate lookup (recommended — adds city/county tax)
- `work_type`: `compute`, `research`, `content`, `consulting`, `trading` (drives per-state classification)
- `is_b2b`: `true`/`false` (affects rates in MD, IA)
- `seller_remitting`: `true`/`false` (whether seller is collecting tax)

**Response includes:** `total_tax`, `combined_rate`, `jurisdiction`, `audit_trail`, `confidence`, `advisories`.

Sellers: you must configure nexus first (see below) or all calculations return $0.

## Log Trades (Capital Gains)

Use when an agent buys or sells assets (compute tokens, crypto, etc.).

```bash
# Buy
curl -s -X POST https://agenttax.io/api/v1/trades \
  -H "X-API-Key: $AGENTTAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_symbol": "SYMBOL",
    "trade_type": "buy",
    "quantity": QTY,
    "price_per_unit": PRICE
  }'

# Sell (returns realized gain/loss)
curl -s -X POST https://agenttax.io/api/v1/trades \
  -H "X-API-Key: $AGENTTAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_symbol": "SYMBOL",
    "trade_type": "sell",
    "quantity": QTY,
    "price_per_unit": PRICE,
    "accounting_method": "fifo",
    "resident_state": "STATE"
  }'
```

Cost basis methods: `fifo` (default), `lifo`, `specific_id`.

## Get Tax Rates

```bash
# All 51 jurisdictions
curl -s https://agenttax.io/api/v1/rates

# Single state with explanation
curl -s "https://agenttax.io/api/v1/rates?state=TX&explain=true"
```

## Configure Nexus (Sellers Only)

Sellers must set nexus states to get non-zero tax results.

```bash
curl -s -X POST https://agenttax.io/api/v1/nexus \
  -H "X-API-Key: $AGENTTAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "nexus": {
      "TX": { "hasNexus": true, "reason": "Economic nexus" },
      "NY": { "hasNexus": true, "reason": "Physical presence" }
    }
  }'
```

## Health Check

```bash
curl -s https://agenttax.io/api/v1/health
```

## Error Handling

All errors return `{ "success": false, "error": "message", "agent_guide": "https://agenttax.io/api/v1/agents" }`.

- 400: Bad request — check `error` and `errors` fields
- 401: Invalid or missing API key
- 429: Rate limited (free tier: 100 calls/month)
