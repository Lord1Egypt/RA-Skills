---
name: synapseai-wallet
description: SynapseAI Wallet — AI agent custodial USDC spending layer with x402 payments. Register a wallet, set spending policies, and make on-chain payments via Privy server wallets.
homepage: https://wallet.synapseai.pro
metadata: {"clawdbot":{"emoji":"💰","requires":{"services":["supabase"]}}}
---

# SynapseAI Wallet

Give your AI agent a managed USDC wallet with policy-enforced spending and automatic x402 on-chain payments.

## Authentication

All requests (except `/register-agent`) use Bearer token:

```
Authorization: Bearer <registration_token>
```

## URLs

| Service | URL |
|---------|-----|
| Edge Functions (register, query) | `https://api.synapseai.pro/functions/v1` |
| x402 Proxy (payments) | `https://wallet.synapseai.pro/api/app` |

## Flow

```
1. Register   → POST /register-agent      → get registration_token
2. Bind       → Owner opens bind_url       → Privy wallet created
3. Wait       → Poll /query-balance with Bearer token until 200
4. Pay        → POST /x402-proxy           → policy check + on-chain payment
```

## Commands

### Register agent (no auth)

```http
POST {EDGE_URL}/register-agent
{
  "agent_name": "MyBot",
  "description": "Research assistant that purchases API credits",
  "capabilities": ["api_purchase", "subscription"]
}
```

Response:

```json
{
  "agent_id": "agt_abc123",
  "wallet_id": "wal_xyz789",
  "status": "PENDING_USER_BIND",
  "registration_token": "reg_def456",
  "bind_url": "/bind?token=reg_def456"
}
```

After registration, tell owner to open `https://wallet.synapseai.pro/bind?token=reg_def456`

### Check balance (Bearer token)

```http
GET {EDGE_URL}/query-balance
Authorization: Bearer <registration_token>
```

```json
{
  "agent_id": "agt_abc123",
  "currency": "USDC",
  "available_balance": 100.0,
  "today_spent": 12.5
}
```

### Check policy (Bearer token)

```http
GET {EDGE_URL}/query-policy
Authorization: Bearer <registration_token>
```

```json
{
  "agent_id": "agt_abc123",
  "policy": {
    "daily_limit": 100,
    "tx_limit": 25,
    "approval_threshold": 10,
    "merchant_whitelist": ["openai_api", "anthropic_api"],
    "blocked_actions": ["withdraw", "transfer", "swap"]
  }
}
```

### Make x402 payment (Recommended)

Policy check + automatic on-chain USDC payment via Privy server wallet. Gas paid by x402 facilitator.

```http
POST {PROXY_URL}/x402-proxy
Authorization: Bearer <registration_token>
{
  "target_url": "https://api.example.com/premium",
  "merchant": "openai_api",
  "amount_hint": 5.0,
  "purpose": "GPT-4 API credits for task #42",
  "metadata": {"task_id": "42"}
}
```

Three possible outcomes:

- `"status": "ALLOW"` — payment executed, `target_data` + `payment_proof` returned
- `"status": "REQUIRE_APPROVAL"` — on hold, owner will be notified via dashboard
- `"status": "REJECT"` — denied, check `reason` field

### Direct payment (Edge Function alternative)

For internal balance deductions without x402:

```http
POST {EDGE_URL}/request-payment
Authorization: Bearer <registration_token>
{
  "merchant": "openai_api",
  "amount": 5.0,
  "purpose": "GPT-4 API credits"
}
```

## Policy rules

- `tx_limit` — max amount per single payment
- `daily_limit` — max total spending per day
- `approval_threshold` — payments >= this need owner approval
- `merchant_whitelist` — only listed merchants are allowed
- `blocked_actions` — forbidden purpose keywords

## Error handling

All errors return `{"error": "..."}` with appropriate HTTP status:

| Code | Meaning |
|------|---------|
| 400  | Bad request |
| 401  | Missing or invalid Bearer token |
| 404  | Agent or wallet not found |
| 500  | Server error |

## Architecture

```
Agent SDK
  ├── Edge Functions (Deno/Supabase)
  │     ├── register-agent     ← no auth, creates agent + empty wallet
  │     ├── query-balance      ← Bearer token, returns wallet state
  │     ├── query-policy       ← Bearer token, returns spending rules
  │     ├── request-payment    ← Bearer token, internal balance deduction
  │     └── receive-webhook    ← Bearer token, audit logging
  │
  └── Next.js API (Node.js)
        └── /api/app/x402-proxy ← Bearer token, policy + on-chain payment
              ↓
        Privy Server Wallet → x402 facilitator → USDC on Base
```

## Notes

- Always check `/query-policy` before paying to know your limits.
- Use `x402-proxy` for external API payments — it handles everything in one call.
- Use clear `purpose` strings — the owner sees these in the dashboard.
- If `REQUIRE_APPROVAL`, don't block — continue other tasks and check back later.
- Never try to bypass the proxy — direct on-chain payments won't be policy-checked.
- The wallet resets `today_spent` at midnight UTC daily.
