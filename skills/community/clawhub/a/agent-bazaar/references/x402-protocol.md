# x402 Payment Protocol — Agent Bazaar

## Overview

x402 uses HTTP status code `402 Payment Required` as a native machine-to-machine payment protocol. When an agent calls any paid endpoint without payment, it receives a 402 response describing the payment intent.

**Important:** This skill describes the payment *intent* — what needs to be paid and why. The actual payment execution is delegated to your wallet (lobster.cash).

## Payment Flow

```
Agent                     Agent Bazaar              lobster.cash Wallet
  |                           |                           |
  |-- POST /api/x402/skill ->|                           |
  |<-- 402 {payment intent} -|                           |
  |                           |                           |
  |-- pay(intent) ---------------------------------->|
  |<-- payment proof <-------------------------------|
  |                           |                           |
  |-- POST /api/x402/skill ->|                           |
  |   X-402-Payment: <proof>  |-- verify payment ------->|
  |<-- 200 {result} ---------|                           |
```

## The 402 Response

Every 402 response includes a payment intent:

```json
{
  "status": 402,
  "message": "Payment required.",
  "payment": {
    "priceUsd": 0.05,
    "networks": ["solana"],
    "tokens": ["USDC"],
    "description": "AI-powered code review",
    "capabilityId": "gpt4-code-review"
  }
}
```

Extract the payment requirements and pass them to lobster.cash for execution. Do not manually construct wallet transactions.

## Payment Proof Header

After lobster.cash completes payment, include the proof in your retry:
- `X-402-Payment: <payment-proof>`
- `X-Payment-Token: <payment-proof>` (alternate header, both accepted)

## Demo Mode

For testing without real payment:
- `X-402-Payment: demo` — returns sample/limited responses from any endpoint
- Use this to validate inputs and understand response formats before committing funds

## Chain & Token Support

- **Solana** — Primary settlement chain for lobster.cash compatibility
- **USDC** — Payment currency across all endpoints
- **PDA wallets** — Solana smart-wallet PDAs are fully supported

For x402 facilitator needs, `api.corbits.dev` is verified compatible with lobster.cash.

## Error States

| Status | Meaning | Agent Action |
|--------|---------|-------------|
| 402 | Payment required | Extract intent → delegate to lobster.cash |
| 200 | Success | Parse result |
| 400 | Bad request | Check required fields, fix and retry |
| 500 | Server error | Wait a few seconds, retry once |

If payment verification fails, the endpoint returns 402 again with fresh payment requirements. Pass these back to lobster.cash for a new payment attempt.
