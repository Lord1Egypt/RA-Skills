---
name: cardzero
version: 1.4.0
description: "CardZero — the first payment wallet built for AI agents. Create USDC wallets on Base L2, make payments, pay x402 paywalls, pay other agents, check balance, view transactions, and run A2A jobs with on-chain escrow (ERC-8183). Human owner sets spending rules via Dashboard; agent pays autonomously within limits. Use when agent needs to: 'pay for API access', 'send USDC', 'pay 402 paywall', 'create a wallet', 'check my balance', 'make a payment', 'buy with crypto', 'agent wallet', 'autonomous payment', 'micropayment', 'pay another agent', 'agent-to-agent payment', 'A2A payment', 'hire another agent', 'job escrow', 'pay on delivery'."
tags: [payment, wallet, usdc, web3, agent, x402, base, micropayment, autonomous, crypto, a2a, escrow, erc-8183, job]
requires:
  - CARDZERO_API_URL: CardZero API base URL (e.g. https://api.cardzero.ai)
  - CARDZERO_API_KEY: Your API Key (received from Owner after they claim the wallet)
  - CARDZERO_WALLET_ID: Your wallet ID (set after wallet creation)
metadata:
  openclaw:
    requires:
      env:
        - CARDZERO_API_URL
        - CARDZERO_API_KEY
        - CARDZERO_WALLET_ID
      bins:
        - curl
    primaryEnv: CARDZERO_API_KEY
    emoji: "\U0001F4B3"
    homepage: https://cardzero.ai
---

# CardZero Payment Wallet

> **Beta** — Smart contract audit in progress. Recommended wallet balance: < $100 USDC.

You have a CardZero payment wallet on Base (Coinbase L2). This wallet holds USDC and lets you make on-chain payments within rules set by your Owner (the human who manages your wallet).

## Capabilities

1. **Create a new wallet** — Register a wallet for your Owner to claim
2. **Check balance** — Query your current USDC balance
3. **Make payments** — Send USDC to any address (merchants, services, or other agents)
4. **Pay x402 paywalls** — Automatically pay for HTTP 402-protected resources
5. **Agent-to-agent payments** — Pay another CardZero agent directly by their wallet address
6. **View payment history** — See recent transactions
7. **A2A Jobs (ERC-8183)** — Hire another CardZero agent under on-chain escrow: budget locks until deliverable is approved by an Evaluator. Built-in 2% platform fee + 5% evaluator fee.

## Authentication

All endpoints except **Create Wallet** require your API Key:

```
Authorization: Bearer czapi_xxxxxxxx_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

You receive this API Key from your Owner after they claim the wallet. Store it as `CARDZERO_API_KEY`.

## Wallet Lifecycle

A wallet goes through two stages:

1. **You create it** → You get a `walletId` and a one-time `claimKey` (no API Key needed)
2. **Your Owner claims it** → They get an API Key and give it to you as an Agent Configuration block
3. **You start operating** → Use the API Key for all subsequent requests

Until your Owner claims the wallet and gives you the API Key, you cannot make payments or check balance.

### Agent Configuration

After claiming, your Owner will give you a block like this:

```
== CardZero Agent Configuration ==
API Key:   czapi_a1b2c3d4_e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4
Wallet ID: wallet_7370ee785775
API URL:   https://api.cardzero.ai/v1
```

When you receive this, extract and save:
- `CARDZERO_API_KEY` — the API Key (starts with `czapi_`)
- `CARDZERO_WALLET_ID` — the wallet ID
- `CARDZERO_API_URL` — the API base URL

## Rules

### Before every payment
- Tell the user the **amount**, **recipient address**, and **reason** before sending
- If the user hasn't confirmed, ask for confirmation first

### When something goes wrong
- `INSUFFICIENT_BALANCE` → Tell the user your balance is too low and suggest they add funds
- `WALLET_FROZEN` → Tell the user your wallet has been frozen by the Owner and you cannot make payments until they unfreeze it
- `NO_SESSION_KEY` → This is rare — session keys are auto-managed by CardZero. If this persists, ask the Owner to contact support
- `WALLET_NOT_ACTIVE` → The wallet hasn't been claimed yet; remind the user to claim it with the claimKey you provided
- `INVALID_API_KEY` → Your API Key is invalid or has been revoked; ask the Owner to check

### Spending limits
Your Owner may set per-transaction and daily spending limits. If a payment exceeds these limits, the chain will reject it. When this happens, explain the limit to the user and suggest a smaller amount.

### Config Summary
Your Owner may paste a **Config Summary** block that looks like this:

```
== CardZero Wallet Summary ==
Address: 0xff0A...6F9
Status: Active
Balance: 142.50 USDC
Rules:
  - Per-tx limit: 5.00 USDC
  - Daily limit: 50.00 USDC
  - Frozen: No
Session Keys: 1 active (earliest expiry 2026-03-18)
```

When you receive this, parse it to understand your current spending context. Use the limits to proactively check before attempting a payment that would fail.

## API Reference

Base URL: `${CARDZERO_API_URL}/v1`

---

### 1. Create Wallet

**No authentication required** — this is the first step before you have an API Key.

```
POST /v1/wallets
Content-Type: application/json

{
  "name": "optional display name"
}
```

**Response (201):**
```json
{
  "id": "wallet_7370ee785775",
  "chainAddress": "0xa1f2...70D0",
  "claimKey": "czk_a1b2c3d4e5f6g7h8_i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
  "name": "My Agent Wallet",
  "status": "pending"
}
```

**After creating a wallet, you MUST:**
1. Save the `id` as your `CARDZERO_WALLET_ID`
2. Tell the Owner the `claimKey` clearly — this is the only time it's shown
3. Tell the Owner the `chainAddress` so they can send USDC to it
4. Explain: "Go to the CardZero Dashboard, enter this claim key, and set up your username and password to activate the wallet. The key expires in 7 days. After claiming, you'll get an Agent Configuration block — paste it back to me so I can start making payments."

**Example message to Owner:**
> I've created a CardZero wallet for you. Here's what you need to do:
>
> **Wallet address:** `0xa1f2...70D0`
> **Claim key:** `czk_a1b2c3d4e5f6g7h8_i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2`
>
> Go to the CardZero Dashboard and enter this claim key to activate the wallet. The key is valid for 7 days and can only be used once. After claiming, you'll see an **Agent Configuration** block — copy it and paste it back to me so I can start making payments.

---

### 2. Check Balance

**Requires API Key.**

```
GET /v1/wallets/{walletId}/balance
Authorization: Bearer {CARDZERO_API_KEY}
```

**Response (200):**
```json
{
  "walletId": "wallet_7370ee785775",
  "balance": "42.50",
  "currency": "USDC"
}
```

**Errors:**
- `WALLET_NOT_ACTIVE` — Wallet hasn't been claimed yet
- `WALLET_NOT_FOUND` — Invalid walletId
- `INVALID_API_KEY` — API Key is invalid or revoked
- `FORBIDDEN` — API Key is not bound to this wallet

---

### 3. Make Payment

**Requires API Key.** The wallet is automatically determined from your API Key — do NOT include `walletId` in the request body.

```
POST /v1/payments
Content-Type: application/json
Authorization: Bearer {CARDZERO_API_KEY}

{
  "to": "0x1234567890123456789012345678901234567890",
  "amount": "2.50",
  "currency": "USDC",
  "memo": "Payment for API access",
  "idempotencyKey": "unique-key-to-prevent-duplicates"
}
```

**Response (201):**
```json
{
  "paymentId": "pay_abc123def456",
  "status": "confirmed",
  "txHash": "0xabc123...",
  "remainingBalance": "40.00",
  "amount": "2.50",
  "to": "0x1234567890123456789012345678901234567890"
}
```

**Fields:**
- `to` — Recipient Ethereum address (0x-prefixed, 42 characters)
- `amount` — USDC amount as a string (e.g. "2.50")
- `currency` — Must be `"USDC"`
- `memo` — Optional note for the payment
- `idempotencyKey` — Optional; prevents duplicate charges if you retry

**Important:** Do NOT include `walletId` in the request body. Your API Key already identifies which wallet to use.

**Errors:**
- `WALLET_NOT_FOUND` — Invalid walletId
- `WALLET_NOT_ACTIVE` — Wallet hasn't been claimed
- `WALLET_FROZEN` — Owner froze the wallet
- `INSUFFICIENT_BALANCE` — Not enough USDC
- `NO_SESSION_KEY` — Internal signing key unavailable (auto-managed, rarely seen)
- `UNSUPPORTED_CURRENCY` — Only USDC is supported
- `CHAIN_ERROR` — On-chain transaction failed (may include "spend limit exceeded" for tx/daily limits)
- `INVALID_API_KEY` — API Key is invalid or revoked

**After a successful payment**, use `remainingBalance` to track your funds without a separate balance query.

**Fee disclosure:** A 2% service fee is automatically deducted from your wallet on each payment. For example, a $5.00 payment costs $5.10 total ($5.00 to the recipient + $0.10 fee). The fee is handled on-chain — you do not need to calculate or add it manually.

---

### 4. Pay for x402-Protected Resources

**Requires API Key.** Use this when you receive an HTTP `402 Payment Required` response from a service that supports the x402 payment protocol.

```
POST /v1/x402/pay
Content-Type: application/json
Authorization: Bearer {CARDZERO_API_KEY}

{
  "url": "https://api.example.com/premium-data",
  "maxAmount": "1.00",
  "recipient": "0x1234567890123456789012345678901234567890",
  "network": "eip155:8453",
  "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
}
```

**Response (201):**
```json
{
  "paymentId": "pay_abc123def456",
  "txHash": "0xabc123...",
  "paymentHeader": "eyJ0eXBlIjoieDQwMiIs...",
  "type": "x402",
  "amount": "1.00",
  "to": "0x1234...",
  "remainingBalance": "41.00"
}
```

**Fields:**
- `url` — The URL that returned 402 (stored as memo for records)
- `maxAmount` — Maximum USDC amount to pay
- `recipient` — Merchant's Ethereum address (from the 402 response)
- `network` — Chain identifier: `eip155:8453` (Base Mainnet) or `eip155:84532` (Base Sepolia)
- `asset` — USDC contract address (from the 402 response)

**How to use x402:**
1. Make your original HTTP request to the protected resource
2. If you receive a `402 Payment Required` response, extract `recipient`, `maxAmount`, `network`, and `asset` from the response headers/body
3. Call `POST /v1/x402/pay` with those values plus the original `url`
4. Take the `paymentHeader` from the response
5. Retry your original request with the header: `X-PAYMENT: {paymentHeader}`

**Errors:** Same as Make Payment above, plus:
- `UNSUPPORTED_NETWORK` — Network not supported (must be Base)
- `UNSUPPORTED_ASSET` — Only USDC is supported

---

### 5. View Payment History


**Requires API Key.**

```
GET /v1/wallets/{walletId}/payments?limit=10&offset=0
Authorization: Bearer {CARDZERO_API_KEY}
```

**Response (200):**
```json
{
  "payments": [
    {
      "id": "pay_abc123def456",
      "wallet_id": "wallet_7370ee785775",
      "to_address": "0x1234...",
      "amount": "2.50",
      "memo": "Payment for API access",
      "tx_hash": "0xabc123...",
      "status": "confirmed",
      "created_at": 1710000000
    }
  ]
}
```

**Query parameters:**
- `limit` — Number of records (default: 20, max recommended: 50)
- `offset` — Skip N records for pagination

**Payment status values:** `pending`, `confirmed`, `failed`

**Errors:**
- `FORBIDDEN` — API Key is not bound to this wallet

---

### 6. Check Payment Status

**No authentication required** — payment IDs are unguessable.

```
GET /v1/payments/{paymentId}
```

Returns the same shape as a single payment object from the history endpoint.

---

## A2A Jobs (ERC-8183 escrow) — v1.4.0

Use Jobs when you need a Provider Agent to deliver something specific (vs a simple payment). Budget is escrowed on-chain until the Evaluator approves delivery — guaranteeing the Provider gets paid only on completion, and the Client gets a refund on expiry.

**Provider must be a CardZero wallet** (Sprint 9 MVP). Fees: 2% platform + 5% evaluator. CardZero runs the Evaluator EOA in MVP; rules are auto-evaluated where possible.

### 7. Create Job (Client side)

```bash
curl -X POST "$CARDZERO_API_URL/v1/jobs" \
  -H "Authorization: Bearer $CARDZERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "providerAddress": "0xabc...",
    "budgetUsdc": "10000000",
    "expiredAt": 1715000000,
    "title": "Translate report to Japanese",
    "description": "Output JSON {translated: string} matching schema",
    "evaluatorRule": {
      "type": "http_check",
      "url": "https://provider.example.com/output",
      "expectedStatus": 200
    }
  }'
```

Response: `{ jobId, onchainJobId, metadataHash, createTxHash }`. Job is in `open` state; budget is NOT yet locked.

### 8. Fund Job (Client side)

```bash
curl -X POST "$CARDZERO_API_URL/v1/jobs/$JOB_ID/fund" \
  -H "Authorization: Bearer $CARDZERO_API_KEY"
```

Locks `budgetUsdc` from your wallet. Status: `open` → `funded`. Two on-chain UserOps (USDC.approve + Jobs.fund).

### 9. Submit Deliverable (Provider side)

```bash
curl -X POST "$CARDZERO_API_URL/v1/jobs/$JOB_ID/submit" \
  -H "Authorization: Bearer $CARDZERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contentHash": "0xa1b2c3...",
    "contentURI": "https://example.com/deliverable.json"
  }'
```

`contentHash` is keccak256 of canonical content. Status: `funded` → `submitted`. Evaluator auto-runs and finalizes within minutes (cron + on-demand).

### 10. Check Job

**No authentication required.**

```bash
curl "$CARDZERO_API_URL/v1/jobs/$JOB_ID"
```

Returns full Job state: status, evaluation outcome, all four lifecycle tx hashes.

### 11. Refund Expired Job (Client side)

If Provider doesn't deliver before `expiredAt`:

```bash
curl -X POST "$CARDZERO_API_URL/v1/jobs/$JOB_ID/refund" \
  -H "Authorization: Bearer $CARDZERO_API_KEY"
```

Returns full budget. Only works post-expiry.

### Job lifecycle

```
open → funded → submitted → completed (Provider gets paid)
                          ↘ rejected  (Client refunded)
            ↘ expired (Client refunds via /refund)
```
