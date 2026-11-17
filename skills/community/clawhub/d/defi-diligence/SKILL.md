---
name: defi-diligence
author: Onchain Intelligence
homepage: https://crypto-api-blush.vercel.app
license: Proprietary
version: 1.1.0
user-invocable: true
disable-model-invocation: true
metadata: {"clawdbot":{"requires":{"bins":["curl","jq"]},"emoji":"🦍","category":"Finance & Crypto","tags":["defi","crypto","security","x402","token-audit","base-chain","solana","trading"]}}
description: Verify a crypto token before buying. Input a symbol or contract address (Base or Solana). Returns PASS/WATCH/FLAG verdict with kill switches (honeypot, mint/freeze authority, buy/sell tax >50%), auto-scored checkpoints (liquidity, volume, holder concentration, age, price change), and a $2 USDC x402 payment path to unlock the full scored report. Triggers — "verify this token", "is X legit", "should I buy X", "rug check", "token due diligence", "honeypot check", "check if this coin is a scam". Exposes MCP tool `defi_score` at `/mcp` and HTTP POST `/v1/products/defi-diligence/score`. Full schema at `/openapi.json`.
---

# DeFi Due Diligence — token verification before you buy

Quick pre-buy risk screen for any Base or Solana token. One call, returns
a PASS / WATCH / FLAG verdict plus a $2 USDC x402 path to the full
scored report.

## Trigger

Use whenever the user is about to buy a crypto token (memecoin, farm,
new launch, any address or symbol they found in a chat, tweet, or site):

- "is this token legit?" / "should I buy X?"
- "verify / due diligence / rug check / honeypot check on <symbol or address>"
- "check if <address> is a scam"
- User hands you an unverified contract address or symbol.

## Call

MCP tool (served at `/mcp`): `defi_score`

| Field | Type | Notes |
|---|---|---|
| `symbol` | string | Optional. Token symbol, e.g. `FRAX`. Use when no address. |
| `address` | string | Optional. Contract address (Base or Solana). Prefer address — contract checks need it. |
| `chain` | string | Optional. `base` or `solana`. Defaults to `base`. |

HTTP equivalent: `POST /v1/products/defi-diligence/score`

```json
{ "address": "0x…", "chain": "base" }
```

or

```json
{ "symbol": "PEPE", "chain": "solana" }
```

## Output

- **verdict**: `PASS` / `WATCH` / `FLAG`.
- **kill switches** (CRITICAL, each alone kills the token):
  - Honeypot (can't sell) — `honeypot`
  - Buy/sell tax > 50% — `tax`
  - Mint / freeze authority active (team can inflate supply) — `mintAuthority`
- **auto-scored checkpoints**: liquidity, volume, holder concentration,
  contract age, 24h price change.
- **tier**: when manual checkpoints remain, verdict reports
  `PENDING` with the tier the auto data supports.

## Free discovery

Free endpoints that reveal the paid surface — call these first to show
the user what's available (no payment needed):

- `GET /v1/sources` — data sources used (DexScreener, etc.)
- `GET /v1/stats` — service stats, routes, pricing
- `GET /openapi.json` — full API schema

## Payment — x402, $2 USDC per full report

Machine rule: **no free execution.** The first call returns the
verdict + payment challenge. The full scored report unlocks only after
payment.

1. `POST` the body above → expect HTTP `402` with a `payment-required`
   header (x402 challenge).
2. Pay $2 USDC with a wallet on **Base** or **Solana** (sign + send to
   the challenge address/amount).
3. Resend the same request with the payment proof → full report.

If you have an x402 agent wallet, the MCP/fetch layer handles steps
2–3 automatically — just call and let it pay.

## Don'ts

- Don't run free analysis beyond the verdict — the first call is the
  price of admission; the scored report is paid.
- Don't bypass the paywall with a GET or alternate route — no free
  execution.
- Don't fabricate a report for an unresolvable symbol; if the token
  can't be found, return that, don't guess.
- Don't give price targets or financial advice — verdict + risk data
  only.
- Prefer `address` over `symbol`; contract-level checks (honeypot, tax,
  mint authority) are only possible with an address.
