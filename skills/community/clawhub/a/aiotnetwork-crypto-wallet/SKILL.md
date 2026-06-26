---
name: Crypto Wallet
description: Discover supported cryptocurrencies, generate deposit addresses, and withdraw crypto to external wallets.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIOT_API_BASE_URL
    primaryEnv: AIOT_API_BASE_URL
---

# Crypto Wallet

Use this skill when the user needs to deposit cryptocurrency into their wallet or withdraw to an external address.

## Configuration

The default API base URL is `https://payment-api-dev.aiotnetwork.io`. All endpoints are relative to this URL.

To override (e.g. for local development):

```bash
export AIOT_API_BASE_URL="http://localhost:8080"
```

If `AIOT_API_BASE_URL` is not set, use `https://payment-api-dev.aiotnetwork.io` as the base for all requests.

## Available Tools

- `get_coins` — List all supported cryptocurrencies | `GET /api/v1/wallet/coins` | Requires auth
- `get_coin_networks` — List supported blockchain networks for a specific coin | `GET /api/v1/wallet/coins/:coin_id/networks` | Requires auth
- `get_deposit_address` — Generate or retrieve a deposit address for a coin on a specific network | `POST /api/v1/wallet/deposit/address` | Requires auth
- `get_withdraw_quote` — Get a quote for a crypto withdrawal (fees, limits) | `POST /api/v1/wallet/withdraw/quote` | Requires auth
- `initiate_withdraw` — Start a crypto withdrawal to an external address | `POST /api/v1/wallet/withdraw` | Requires auth
- `get_withdraw_status` — Check the status of a crypto withdrawal | `GET /api/v1/wallet/withdraw/:id` | Requires auth
- `confirm_withdraw` — Confirm a pending crypto withdrawal | `POST /api/v1/wallet/withdraw/:id/confirm` | Requires auth | Requires transaction PIN

## Recommended Flows

### Deposit Crypto

Generate a deposit address and fund your wallet with crypto

1. List coins: GET /api/v1/wallet/coins — find the coin you want to deposit
2. Get networks: GET /api/v1/wallet/coins/:coin_id/networks — choose the blockchain network
3. Get address: POST /api/v1/wallet/deposit/address with {coin_id, network_id} — returns deposit address
4. Send crypto to the returned address from your external wallet


### Withdraw Crypto

Send crypto from your wallet to an external address

1. Get quote: POST /api/v1/wallet/withdraw/quote with {coin_id, network_id, amount, address}
2. Initiate: POST /api/v1/wallet/withdraw with quote details
3. Confirm: POST /api/v1/wallet/withdraw/:id/confirm (requires transaction PIN)
4. Track: GET /api/v1/wallet/withdraw/:id — monitor until completed


## Rules

- Always verify the correct network before depositing — sending to the wrong network will lose funds
- Withdrawal follows a quote-then-confirm pattern — confirmation requires a transaction PIN
- Deposit addresses are deterministic — the same coin+network always returns the same address

## Agent Guidance

Follow these instructions when executing this skill:

- Always follow the documented flow order. Do not skip steps.
- If a tool requires authentication, verify the session has a valid bearer token before calling it.
- If a tool requires a transaction PIN, ask the user for it fresh each time. Never cache or log PINs.
- Never expose, log, or persist secrets (passwords, tokens, full card numbers, CVVs).
- If the user requests an operation outside this skill's scope, decline and suggest the appropriate skill.
- If a step fails, check the error and follow the recovery guidance below before retrying.

- Always verify the user selected the correct blockchain network before generating a deposit address. Sending to the wrong network will permanently lose funds.
- Withdrawal follows: get quote → initiate → confirm with transaction PIN. The confirmation step requires a 4-digit transaction PIN. Never skip the quote step.
- Deposit addresses are deterministic — the same coin + network always returns the same address.
