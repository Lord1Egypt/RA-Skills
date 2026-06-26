---
name: Payments & Banking
description: Fund wallets, transfer money, send remittances, and convert currencies. Includes top-up via multiple payment methods and international money transfers.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIOT_API_BASE_URL
    primaryEnv: AIOT_API_BASE_URL
---

# Payments & Banking

Use this skill when the user needs to top up a wallet, send money, make international remittances, or convert currencies.

## Configuration

The default API base URL is `https://payment-api-dev.aiotnetwork.io`. All endpoints are relative to this URL.

To override (e.g. for local development):

```bash
export AIOT_API_BASE_URL="http://localhost:8080"
```

If `AIOT_API_BASE_URL` is not set, use `https://payment-api-dev.aiotnetwork.io` as the base for all requests.

## Available Tools

- `get_balance` — Get current account balance | `GET /api/v1/bank/balance` | Requires auth
- `get_masterpay_balance` — Get MasterPay main wallet balance | `GET /api/v1/masterpay/balance` | Requires auth
- `list_card_wallets` — List all MasterPay card wallets and balances | `GET /api/v1/masterpay/wallets` | Requires auth
- `get_topup_methods` — Get available payment methods for top-up | `GET /api/v1/bank/topup/payment_methods` | Requires auth
- `get_topup_quote` — Get a quote for a top-up amount | `POST /api/v1/bank/topup/quote` | Requires auth
- `initiate_topup` — Start a top-up transaction | `POST /api/v1/bank/topup` | Requires auth
- `get_topup_status` — Check status of a top-up | `GET /api/v1/bank/topup/:id` | Requires auth
- `confirm_topup` — Confirm a pending top-up | `POST /api/v1/bank/topup/:id/confirm` | Requires auth
- `get_transfer_quote` — Get a quote for a transfer | `POST /api/v1/bank/transfer/quote` | Requires auth
- `initiate_transfer` — Start a money transfer | `POST /api/v1/bank/transfer` | Requires auth
- `get_transfer_status` — Check status of a transfer | `GET /api/v1/bank/transfer/:id` | Requires auth
- `confirm_transfer` — Confirm a pending transfer | `POST /api/v1/bank/transfer/:id/confirm` | Requires auth | Requires transaction PIN
- `get_remittance_countries` — Get supported remittance destination countries | `GET /api/v1/bank/transfer/remittance/countries` | Requires auth
- `get_exchange_rate` — Get current exchange rate for a currency pair | `GET /api/v1/bank/transfer/remittance/rate` | Requires auth
- `get_remittance_reference_data` — Get reference data for remittance forms (banks, branches, etc.) | `GET /api/v1/bank/transfer/remittance/reference-data` | Requires auth
- `get_remittance_quote` — Get a quote for an international remittance | `POST /api/v1/bank/transfer/remittance/quote` | Requires auth
- `initiate_remittance` — Start an international remittance | `POST /api/v1/bank/transfer/remittance` | Requires auth
- `get_remittance_status` — Check status of a remittance | `GET /api/v1/bank/transfer/remittance/:id` | Requires auth
- `get_remittance_history` — Get remittance transaction history | `GET /api/v1/bank/transfer/remittance/history` | Requires auth
- `confirm_remittance` — Confirm a pending remittance | `POST /api/v1/bank/transfer/remittance/:id/confirm` | Requires auth | Requires transaction PIN
- `cancel_remittance` — Cancel a pending remittance | `POST /api/v1/bank/transfer/remittance/:id/cancel` | Requires auth
- `list_recipients` — List saved remittance recipients | `GET /api/v1/bank/transfer/remittance/recipients` | Requires auth
- `create_recipient` — Save a new remittance recipient | `POST /api/v1/bank/transfer/remittance/recipients` | Requires auth
- `get_recipient` — Get details of a saved recipient | `GET /api/v1/bank/transfer/remittance/recipients/:recipient_id` | Requires auth
- `update_recipient` — Update a saved recipient's details | `PUT /api/v1/bank/transfer/remittance/recipients/:recipient_id` | Requires auth
- `delete_recipient` — Delete a saved recipient | `DELETE /api/v1/bank/transfer/remittance/recipients/:recipient_id` | Requires auth
- `get_conversion_pairs` — Get available currency conversion pairs | `GET /api/v1/bank/convert/pairs` | Requires auth
- `get_conversion_rate` — Get conversion rate between two currencies | `GET /api/v1/bank/convert/rate` | Requires auth
- `initiate_conversion` — Start a currency conversion | `POST /api/v1/bank/convert` | Requires auth
- `confirm_conversion` — Confirm a pending conversion | `POST /api/v1/bank/convert/:id/confirm` | Requires auth | Requires transaction PIN
- `list_transactions` — List transaction history with pagination | `GET /api/v1/transactions` | Requires auth
- `get_transaction` — Get details of a specific transaction | `GET /api/v1/transactions/:id` | Requires auth
- `download_receipt` — Download a transaction receipt as PDF | `GET /api/v1/transactions/:id/receipt/pdf` | Requires auth

## Recommended Flows

### Top Up Wallet

Add funds to your wallet via available payment methods

1. Get payment methods: GET /api/v1/bank/topup/payment_methods
2. Get quote: POST /api/v1/bank/topup/quote with {amount, currency, payment_method}
3. Initiate: POST /api/v1/bank/topup with quote details
4. Confirm: POST /api/v1/bank/topup/:id/confirm


### Send Remittance

Send money internationally to a recipient

1. Check countries: GET /api/v1/bank/transfer/remittance/countries
2. Get exchange rate: GET /api/v1/bank/transfer/remittance/rate?from=USD&to=PHP
3. Create or select recipient: POST/GET /api/v1/bank/transfer/remittance/recipients
4. Get quote: POST /api/v1/bank/transfer/remittance/quote
5. Initiate: POST /api/v1/bank/transfer/remittance
6. Confirm: POST /api/v1/bank/transfer/remittance/:id/confirm (requires transaction PIN)


## Rules

- All financial operations require authentication
- Top-ups and transfers follow a quote-then-confirm pattern — never skip the quote step
- Transfer, remittance, and conversion confirmations require a transaction PIN — top-up confirmations do not
- Remittances require a saved recipient — create one first if needed
- Exchange rates are indicative and may change between quote and confirmation
- Transaction history is paginated — use page and page_size query parameters

## Agent Guidance

Follow these instructions when executing this skill:

- Always follow the documented flow order. Do not skip steps.
- If a tool requires authentication, verify the session has a valid bearer token before calling it.
- If a tool requires a transaction PIN, ask the user for it fresh each time. Never cache or log PINs.
- Never expose, log, or persist secrets (passwords, tokens, full card numbers, CVVs).
- If the user requests an operation outside this skill's scope, decline and suggest the appropriate skill.
- If a step fails, check the error and follow the recovery guidance below before retrying.

- All financial operations follow a quote-then-confirm pattern. Always get a quote first — never skip directly to initiation.
- Transfer, remittance, and conversion confirmations require a transaction PIN. Top-up confirmations do not require a PIN.
- Remittances require a saved recipient. Create one with `create_recipient` if none exists.
- Exchange rates shown in quotes are indicative. The final rate is locked at confirmation.
- Transaction history is paginated. Use `page` and `page_size` query parameters.
