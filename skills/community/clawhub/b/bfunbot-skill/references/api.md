# BFunBot Agent API — Quick Reference

**Base URL:** `https://api.bfun.bot/agent/v1`  
**Auth:** `X-Api-Key: bfbot_...` header on all requests

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/me` | User profile & wallet addresses |
| GET | `/skills` | List all agent capabilities (no auth required) |
| POST | `/token/create` | Create token on-chain (async) |
| GET | `/jobs/{job_id}` | Poll token creation status |
| GET | `/token/{address}` | Token price & info (`?chain=bsc`) |
| GET | `/tokens/created` | Paginated list of tokens you created |
| GET | `/balance/credits` | BFun.bot Credits balance + agent reload config |
| POST | `/balance/credits/reload` | Reload BFun.bot Credits from trading wallet |
| POST | `/balance/credits/reload/disable` | Emergency disable agent reload (irreversible by agent) |
| GET | `/balance/wallet` | On-chain wallet balances (main + trading, BSC) |
| GET | `/quota` | Daily token creation quota (BSC) |
| GET | `/fees/summary` | Fee earnings summary (BSC) |
| GET | `/fees/earnings` | Per-platform fee breakdown (`?chain=bsc`) |
| GET | `/fees/token` | Per-token fee earnings |

---

## POST /token/create

```json
{
  "name": "MOON",
  "symbol": "MOON",
  "chain": "bsc",
  "description": "...",
  "image_url": "https://...",
  "source_url": "https://x.com/user/status/123",
  "platform": "flap"
}
```

Chain: `bsc` only  
Platform (optional): `flap` · `fourmeme`  
Returns (`202`): `{ "job_id": 12345, "status": "pending", "chain": "bsc", "quota": {...} }`  
Poll `/jobs/{job_id}` until `status` is `completed` or `failed`.

---

## GET /jobs/{job_id}

```json
{
  "job_id": 12345,
  "status": "completed",
  "chain": "bsc",
  "token_address": "0x...",
  "error": null,
  "created_at": "...",
  "completed_at": "..."
}
```

Status: `pending` | `processing` | `completed` | `failed`

---

## GET /balance/credits

```json
{
  "balance_usd": "4.92",
  "balance_usd_cents": 492,
  "agent_reload": {
    "enabled": true,
    "amount_usd": 5.0,
    "daily_limit_usd": 100.0,
    "chains": ["bsc"]
  }
}
```

`agent_reload` is `null` if not configured by the user.

---

## POST /balance/credits/reload

Manually reload BFun.bot Credits from trading wallet. Agent-triggered only (no auto-polling).  
Requires: user has Agent Reload enabled at bfun.bot/credits + key has `reload_enabled`.

```json
{
  "success": true,
  "amount_usd": "5.00",
  "tx_hash": "0x...",
  "new_balance_usd": "9.92",
  "daily_used_usd": "5.00",
  "daily_remaining_usd": "95.00"
}
```

---

## GET /balance/wallet

```json
{
  "evm_main":    { "address": "0x...", "balance_bnb": "0.1", "balance_usdt_bsc": "5.0" },
  "evm_trading": { "address": "0x...", "balance_bnb": "0.0", "balance_usdt_bsc": "0.0" }
}
```

Fields are `null` if wallet not set up or RPC unavailable. Check `*_error` fields.

---

## GET /quota

```json
{
  "chains": [
    {
      "chain": "bsc",
      "free_used_today": 1,
      "free_limit": 3,
      "sponsored_remaining": 2,
      "can_create_paid": true,
      "trading_wallet_balance": "0.01 BNB",
      "trading_wallet_address": "0x..."
    }
  ]
}
```

---

## GET /fees/summary

```json
{
  "bsc": {
    "chain_id": 56,
    "token_count": 12,
    "total_earned_bnb": 0.053
  }
}
```

---

## GET /fees/earnings?chain=bsc

```json
{
  "chain": "bsc",
  "chain_id": 56,
  "flap":     { "total_earned_bnb": 0.042, "earning_token_count": 3 },
  "fourmeme": { "total_earned_bnb": 0.011, "earning_token_count": 1 }
}
```

---

## GET /fees/token?chain=bsc&platform=flap&token_address=0x...

```json
{
  "token_address": "0x...",
  "token_name": "MyToken",
  "token_symbol": "MTK",
  "platform": "flap",
  "chain": "bsc",
  "earned_bnb": 0.021
}
```

Returns `404` if token not found or not owned by the authenticated user.

---

## BFun LLM Gateway

**Base URL:** `https://llm.bfun.bot`  
Same `X-Api-Key` header. Requires `llm_enabled` on API key.

- `POST /v1/messages` — Anthropic format (Claude models)
- `POST /v1/chat/completions` — OpenAI format (all models)
- `GET /v1/models` — list models
- `GET /v1/models/openclaw` — ready-to-paste OpenClaw config (no auth)

---

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Missing or invalid API key |
| 402 | Insufficient BFun.bot Credits or trading wallet balance |
| 403 | Feature not enabled for this key or user |
| 404 | Resource not found |
| 422 | Validation error |
| 429 | Rate limited or daily cap exceeded |
| 500 | Server error — retry |
