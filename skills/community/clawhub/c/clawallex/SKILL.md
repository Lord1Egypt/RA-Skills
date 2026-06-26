---
name: clawallex-skill
description: "Pay for anything with USDC — virtual cards for any online checkout"
metadata:
  openclaw:
    emoji: "💳"
  requires:
    bins: ["python3"]
---

# Clawallex

Pay for anything with USDC. Clawallex converts your stablecoin balance into virtual cards that work at any online checkout.

## Features

- **Flash Cards** — one-time use virtual cards for single payments
- **Stream Cards** — reloadable cards for subscriptions, top up with `refill`
- **Mode A** — pay from your USDC wallet balance
- **Mode B** — on-chain x402 payment for callers with self-custody wallets (agent or user) — signing is performed by the caller
- **Zero dependencies** — Python 3.9+ stdlib only

## Quick Start

### 1. Set Up Account

**New user — browser signup (recommended):**
```bash
python3 {baseDir}/scripts/clawallex.py signup
```
Returns a URL and token. Show the URL to the user, ask them to open it and click Authorize.
The command polls automatically. If polling fails, retry with the token:
```bash
python3 {baseDir}/scripts/clawallex.py signup-check --token <token>
```

**Existing user — connect with API keys:**

Get your API Key and Secret at [app.clawallex.com/dashboard/settings](https://app.clawallex.com/dashboard/settings), then run:
```bash
python3 {baseDir}/scripts/clawallex.py setup --action connect --api-key YOUR_KEY --api-secret YOUR_SECRET
```

### 2. Verify

```bash
python3 {baseDir}/scripts/clawallex.py wallet          # check balance
python3 {baseDir}/scripts/clawallex.py cards            # list cards
```

## Hard Rules

1. **Setup first** — Run `setup --action status` before any payment. If not configured: use `signup` for new accounts, or `setup --action connect` if the user already has API keys.
2. **Check balance first** — Run `wallet` before `pay` or `subscribe` to verify sufficient funds (Mode A only).
3. **Never expose card secrets** — Decrypted PAN/CVV are STRICTLY for filling checkout forms. NEVER display to the user. Show only `masked_pan` from `card-details`.
4. **Confirm before paying** — Echo amount and description back to user before creating a card.
5. **One command at a time** — Run each command, check output, then proceed.

## Typical Flows

### Payment Flow (Mode A — Wallet Balance)

```
1. setup --action status                                    → check config
2. wallet                                                   → check balance
3. pay --amount 50 --description "OpenAI"                   → create flash card
4. card-details --card-id <ID from step 3>                  → get encrypted card data
5. Decrypt PAN/CVV (HKDF + AES-256-GCM)                    → use ONLY for checkout form
```

### Subscription Flow

```
1. wallet                                                   → check balance
2. subscribe --amount 100 --description "AWS billing"       → create stream card
3. card-details --card-id <ID from step 2>                  → get card for sign-up form
4. refill --card-id <ID> --amount 50                        → top up when balance is low
```

## Command Reference

All commands:

```
python3 {baseDir}/scripts/clawallex.py <command> [args]
```

### Setup & Identity

| User Intent | Command |
|-------------|---------|
| Quick signup — browser-based new account creation (recommended for first-time setup) | `signup` |
| Check signup result with existing token | `signup-check --token TOKEN` |
| Connect account | `setup --action connect --api-key KEY --api-secret SECRET` |
| Check config status | `setup --action status` |
| Get sign-up link | `setup --action register` |
| Check API Key binding | `whoami` |
| Bind client_id | `bootstrap` or `bootstrap --preferred-client-id MY_ID` |

### Payments

| User Intent | Command |
|-------------|---------|
| Pay for something | `pay --amount N --description "X"` |
| Pay with custom expiry | `pay --amount N --description "X" --ttl SECONDS` — flash card only; default 86400 (24 h) |
| Start subscription | `subscribe --amount N --description "X"` |
| Top up card | `refill --card-id CID --amount N` |

### Wallet & Cards

| User Intent | Command |
|-------------|---------|
| Check balance | `wallet` |
| Deposit funds | `recharge-addresses --wallet-id WID` |
| List cards | `cards` — returns mode_code (100=Mode A, 200=Mode B) to determine refill path |
| Check card balance | `card-balance --card-id CID` |
| Batch check balances | `batch-balances --card-ids CID1,CID2` — multiple cards in one call |
| Update card controls | `update-card --card-id CID --client-request-id UUID [--tx-limit] [--allowed-mcc] [--blocked-mcc]` |
| Get card details | `card-details --card-id CID` — returns masked_pan, expiry, balance, first_name, last_name, tx_limit, allowed_mcc, blocked_mcc, encrypted PAN/CVV |
| View transactions | `transactions` |

### Advanced (x402 On-Chain)

| User Intent | Command |
|-------------|---------|
| Get x402 payee address | `x402-address --chain ETH --token USDC` — MUST call before Mode B Refill |

## Setup Flow

When the user wants to use Clawallex for the first time:

1. Run `setup --action status` to check current configuration.
2. If **not configured**, ask: "Do you have a Clawallex account?"
   - **Yes, have API keys**: Ask for API Key and Secret, then run:
     ```
     setup --action connect --api-key KEY --api-secret SECRET
     ```
     This automatically verifies credentials, binds client_id, and saves locally.
   - **No account yet**: Run the browser signup flow:
     ```
     signup
     ```
     This generates a URL and a token — show the URL to the user and ask them to open it and click Authorize.
     The command polls automatically. If polling fails or times out, use the token to retry manually:
     ```
     signup-check --token <token from signup output>
     ```
3. Verify with `wallet` to confirm connection works.

**Signup result statuses** — all returned as `success: true`:
- `pending` — user hasn't authorized yet, call `signup-check` again
- `ok` — credentials saved, ready to use
- `cancelled` — user cancelled, ask if they want to try again
- `already_exists` — account already has API keys, switch to `setup --action connect`

## Mode B Flow (x402 On-Chain, Two-Stage)

Mode B is for **callers with self-custody wallets (agent or user)** (DeFi bots, autonomous purchasing agents). The agent signs on-chain transactions using its own signing system — no human intervention needed.

**Stage 1 — Quote:**
```
pay --amount 200 --description "GPU rental" --mode-code 200 --chain-code ETH --token-code USDC
```
The 402 response is **EXPECTED — it is a quote, NOT an error**. Returns:
- `client_request_id`, `payee_address`, `asset_address`, `x402_reference_id`
- `final_card_amount`, `issue_fee_amount`, `fx_fee_amount`, `fee_amount`, `payable_amount`

Fee structure:
- flash card: `fee_amount = issue_fee_amount + fx_fee_amount`
- stream card: `fee_amount = issue_fee_amount + monthly_fee_amount + fx_fee_amount`

**Agent signs** — construct and sign an **EIP-3009 `transferWithAuthorization`** using your own wallet/signing library and the quote details. Only the resulting signature and your wallet address are needed for Stage 2.
EIP-3009 enables gasless USDC transfers via off-chain signatures. The `authorization` fields map to:
- `from`: your wallet address (the payer)
- `to`: `payee_address` from Stage 1 (system receiving address)
- `value`: `maxAmountRequired` (payable_amount in token minimal units, USDC = 6 decimals)
- `validAfter` / `validBefore`: unix timestamps (seconds) defining the signature validity window
- `nonce`: random 32-byte hex, must be unique per authorization

**Stage 2 — Settle (MUST use same client_request_id):**
```
pay --amount 200 --description "GPU rental" \
  --mode-code 200 \
  --client-request-id "uuid-from-stage-1" \
  --x402-version 1 \
  --payment-payload '{
    "scheme": "exact",
    "network": "ETH",
    "payload": {
      "signature": "0x<agent EIP-3009 signature>",
      "authorization": {
        "from": "0x<agent wallet address>",
        "to": "<payee_address from stage 1>",
        "value": "<maxAmountRequired, e.g. 207590000>",
        "validAfter": "<unix timestamp seconds>",
        "validBefore": "<unix timestamp seconds>",
        "nonce": "0x<random 32-byte hex>"
      }
    }
  }' \
  --payment-requirements '{
    "scheme": "exact",
    "network": "ETH",
    "asset": "<asset_address from stage 1>",
    "payTo": "<payee_address from stage 1>",
    "maxAmountRequired": "<payable_amount × 10^6, e.g. 207590000>",
    "extra": {
      "referenceId": "<x402_reference_id from stage 1>"
    }
  }' \
  --extra '{"card_amount": "200.0000", "paid_amount": "<payable_amount, e.g. 207.5900>"}'
```

**Stage 2 constraints:**
- `--client-request-id` MUST be identical to Stage 1 — a different value creates a NEW order
- `payment_requirements.payTo` MUST equal `payee_address` from Stage 1
- `payment_requirements.asset` MUST equal `asset_address` from Stage 1
- `payment_requirements.maxAmountRequired` MUST equal `payable_amount` × 10^decimals (USDC = 6 decimals)
- `payment_requirements.extra.referenceId` MUST equal `x402_reference_id` from Stage 1
- `extra.card_amount` MUST equal the `--amount`
- `extra.paid_amount` MUST equal `payable_amount` from Stage 1 (`amount + fee_amount`)
- `payment_payload.network` MUST equal `payment_requirements.network`
- `payload.authorization.to` MUST equal `payment_requirements.payTo`
- `payload.authorization.value` MUST equal `payment_requirements.maxAmountRequired`
- Server will force-inject `extra.mode=STANDARD` — any client-provided value is ignored
- If settle is rejected, order stays `pending_payment` — fix params and retry with same `client_request_id`

## Mode B Refill Flow (no 402 challenge)

Mode B refill goes directly to x402 settle — no 402 challenge stage. Caller signs the EIP-3009 authorization independently using their own wallet/signing library; only the resulting signature and wallet address are submitted. Must call `x402-address` first to get `payee_address`.

```
1. x402-address --chain ETH --token USDC                    → get payee_address
2. refill --card-id c_123 --amount 50 \
     --x402-reference-id "<unique reference id>" \
     --x402-version 1 \
     --payment-payload '{
       "scheme": "exact",
       "network": "ETH",
       "payload": {
         "signature": "0x<EIP-3009 signature>",
         "authorization": {
           "from": "0x<agent wallet>",
           "to": "<payee_address from step 1>",
           "value": "<amount × 10^6>",
           "validAfter": "<unix seconds>",
           "validBefore": "<unix seconds>",
           "nonce": "0x<random 32-byte hex>"
         }
       }
     }' \
     --payment-requirements '{
       "scheme": "exact",
       "network": "ETH",
       "asset": "<asset contract address>",
       "payTo": "<payee_address from step 1>",
       "maxAmountRequired": "<amount × 10^6>",
       "extra": { "referenceId": "<x402_reference_id>" }
     }'
```

Mode B refill idempotency key is `x402_reference_id` (not `client_request_id`).
Check `cards` `mode_code` to determine which refill path the card uses.

## How to Talk to the User

### During setup
- "I need your Clawallex API Key and Secret to get started. You can find them at app.clawallex.com/dashboard/settings."
- If no account: "No problem — I can get you a sign-up link."
- After connect: "You're all set! Want to check your balance?"

### During payments
- Always confirm: "I'll create a $50 card for OpenAI API credits, deducted from your wallet balance. Go ahead?"
- After card creation: "Card created! Let me get the card details for checkout."
- Never show PAN/CVV in conversation. Show only masked_pan if asked.

### On errors
- Don't blame the user. Be actionable: "Your wallet balance is $20 but this needs $50. You can deposit more USDC or try a smaller amount."
- 402 response (Mode B): This is expected — explain it's the first step of a two-stage payment, not an error.

## Decrypting Card Sensitive Data

`card-details` returns `encrypted_sensitive_data` with encrypted PAN/CVV:

1. Derive key: `HKDF-SHA256(ikm=api_secret, salt=empty, info="clawallex/card-sensitive-data/v1", length=32)`
2. Decode: `nonce = base64_decode(nonce)`, `raw = base64_decode(ciphertext)`
3. Split: `encrypted_data = raw[:-16]`, `auth_tag = raw[-16:]`
4. Decrypt: `AES-256-GCM(key, nonce, encrypted_data, auth_tag)` → JSON
5. Result: `{"pan": "4111111111111111", "cvv": "123"}`

## Error Recovery

| Error | Cause | Action |
|-------|-------|--------|
| "not configured" | No credentials saved | Run `setup --action connect` with valid credentials |
| "Invalid credentials" | Wrong API Key/Secret | Check at app.clawallex.com/dashboard/settings |
| Insufficient balance | Wallet balance too low | Run `recharge-addresses` for deposit info, or use Mode B |
| 402 response | Mode B Stage 1 (expected) | This is the quote — proceed to Stage 2 with same client_request_id |
| Settle rejected (Mode B) | Invalid x402 params | Order stays `pending_payment` — fix params and retry with same client_request_id |
| Card not found | Wrong card_id | Run `cards` to list valid card IDs |
| Decryption failed | Bad data or apiSecret changed | Re-fetch via `card-details`, verify credentials |

## Output Format

All commands return JSON:
- `success: true` → data in `data` field, next steps in `_hint`
- `success: false` → error message in `error` field

## Key Concepts

- **Flash card**: Created by `pay`. Single-use, auto-destroyed after one transaction. Cannot be refilled.
- **Stream card**: Created by `subscribe`. Reloadable, top up with `refill`.
- **Wallet**: Your USDC balance. Funds all Mode A operations.
- **Mode A** (mode_code=100): Wallet balance deduction (default).
- **Mode B** (mode_code=200): x402 on-chain USDC payment for callers with self-custody wallets (agent or user). Two-stage (quote → sign → settle). Agent signs EIP-3009 independently; only the signature and wallet address are passed to Stage 2.
- **client_id**: The agent's stable identity, separate from the API Key. An agent can have multiple API Keys (for rotation/revocation), but `client_id` never changes. Cards and transactions are isolated per `client_id`. When switching to a new API Key, keep using the same `client_id` — the new key auto-binds on first request. Once bound, it cannot be changed (TOFU). Stored locally at `~/.clawallex/credentials.json`.
