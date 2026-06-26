---
name: agentfuel-api
description: Use AgentFuel to call Replicate, Anthropic, and ElevenLabs APIs using a single crypto-funded key. Generate a free af_ key, create an invoice to get a unique USDT deposit address, then proxy all AI API calls through the AgentFuel gateway. No per-service accounts required.
emoji: ⚡
version: 1.3.0
tags:
  - api
  - crypto
  - replicate
  - anthropic
  - elevenlabs
  - payments
requires:
  env:
    - AGENTFUEL_KEY
---

# AgentFuel API

AgentFuel is a crypto-funded API credit broker for AI agents. One `af_` key gives you access to Replicate, Anthropic (Claude), and ElevenLabs — funded with USDT on Ethereum. No credit cards. No per-service accounts.

**Base URL:** `https://agentfuel.dev/v1`
**Auth:** `Authorization: Bearer $AGENTFUEL_KEY` header, OR `?key=$AGENTFUEL_KEY` query param
**Pricing:** 1,000 credits = $1 USD

---

## Check Balance

**With header auth (curl/exec):**
```bash
curl https://agentfuel.dev/v1/balance \
  -H "Authorization: Bearer $AGENTFUEL_KEY"
```

**With query param (web_fetch — no custom headers needed):**
```
web_fetch: https://agentfuel.dev/v1/balance?key=YOUR_AF_KEY
```

Returns: `{ "credits": 12500, "key": "af_..." }`

---

## Get Credits (USDT Invoice)

**With query param (web_fetch):**
Use `web_fetch` with POST isn't supported — use the invoice endpoint via query param:
```
web_fetch: https://agentfuel.dev/v1/invoice?key=YOUR_AF_KEY&amount_usd=10
```

**With header auth (curl/exec):**
```bash
curl -X POST https://agentfuel.dev/v1/invoice \
  -H "Authorization: Bearer $AGENTFUEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount_usd": 10}'
```

Returns: `{ "invoice_id": 1, "address": "0x...", "amount_usd": 10, "expires_at": "..." }`

Send exact USDT amount to the address (ERC-20, Ethereum). Credits applied after ~6 confirmations (~2 min).

---

## Transfer Credits Between Keys

```bash
curl -X POST https://agentfuel.dev/v1/transfer \
  -H "Authorization: Bearer $AGENTFUEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to": "af_recipient_key_here", "amount": 1000}'
```

Auth is the SENDER's key. Returns 402 if insufficient credits.

---

## Calling Anthropic (Claude)

```bash
curl -X POST https://agentfuel.dev/v1/anthropic/messages \
  -H "Authorization: Bearer $AGENTFUEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4-6", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello"}]}'
```

Available models: `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`, `claude-opus-4-6`

## Calling Replicate

```bash
curl -X POST https://agentfuel.dev/v1/replicate/predictions \
  -H "Authorization: Bearer $AGENTFUEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "black-forest-labs/flux-schnell", "input": {"prompt": "..."}}'
```

## Calling ElevenLabs

```bash
curl -X POST "https://agentfuel.dev/v1/elevenlabs/text-to-speech/VOICE_ID" \
  -H "Authorization: Bearer $AGENTFUEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "model_id": "eleven_turbo_v2_5"}' \
  --output speech.mp3
```

---

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Invalid key | Check af_ prefix, use header or ?key= param |
| 402 | Insufficient credits | Create invoice, deposit USDT |
| 429 | Rate limited | Wait 60s |
| 502 | Upstream error | Retry after 10s |
