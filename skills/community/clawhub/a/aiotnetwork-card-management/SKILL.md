---
name: Card Management
description: Create and manage virtual cards via MasterPay Global. Supports single-use cards for one-time purchases and multi-use cards for repeated use.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIOT_API_BASE_URL
    primaryEnv: AIOT_API_BASE_URL
---

# Card Management

Use this skill when the user needs to create virtual cards, view card details, or manage card lifecycle (lock, unlock, cancel).

## Configuration

The default API base URL is `https://payment-api-dev.aiotnetwork.io`. All endpoints are relative to this URL.

To override (e.g. for local development):

```bash
export AIOT_API_BASE_URL="http://localhost:8080"
```

If `AIOT_API_BASE_URL` is not set, use `https://payment-api-dev.aiotnetwork.io` as the base for all requests.

## Available Tools

- `list_card_wallets` — List all MasterPay card wallets and balances (required before card creation) | `GET /api/v1/masterpay/wallets` | Requires auth
- `create_single_use_card` — Create a single-use virtual card for a one-time purchase | `POST /api/v1/masterpay/cards/single-use` | Requires auth
- `create_multi_use_card` — Create a multi-use virtual card for repeated purchases | `POST /api/v1/masterpay/cards/multi-use` | Requires auth
- `list_cards` — List all cards in a wallet (defaults to first wallet) | `GET /api/v1/masterpay/wallets/cards` | Requires auth
- `list_cards_by_wallet` — List cards for a specific wallet UUID | `GET /api/v1/masterpay/wallets/:wallet_uuid/cards` | Requires auth
- `get_card` — Get details of a specific card by UUID (includes card ATM PIN, no transaction PIN required) | `GET /api/v1/masterpay/cards/:id` | Requires auth
- `get_card_details` — Get full unmasked card number, CVV, and expiry (sensitive) | `POST /api/v1/masterpay/cards/:id/details` | Requires auth | Requires transaction PIN
- `get_card_types` — Get available card types and their properties | `GET /api/v1/masterpay/cards/types` | Requires auth
- `lock_card` — Lock (block) a card to prevent transactions | `POST /api/v1/masterpay/cards/:id/lock` | Requires auth | Requires transaction PIN
- `unlock_card` — Unlock (reactivate) a previously locked card | `POST /api/v1/masterpay/cards/:id/unlock` | Requires auth | Requires transaction PIN
- `cancel_card` — Permanently cancel (suspend) a card | `POST /api/v1/masterpay/cards/:id/cancel` | Requires auth | Requires transaction PIN
- `list_applied_cards` — List all card applications and their status | `GET /api/v1/cards` | Requires auth
- `get_applied_card` — Get details of a specific card application | `GET /api/v1/cards/:id` | Requires auth
- `apply_card` — Apply for a new payment card (physical or virtual) | `POST /api/v1/cards/apply` | Requires auth

## Recommended Flows

### Create a Virtual Card (MasterPay)

Create a single-use or multi-use virtual card via MasterPay

1. Check KYC status: GET /api/v1/masterpay/kyc/status — must be 'approved' (use get_kyc_status from kyc-identity skill)
2. List wallets: GET /api/v1/masterpay/wallets — verify at least one wallet exists (no wallets means KYC is not yet approved)
3. Submit wallet KYC: POST /api/v1/masterpay/wallets/kyc — required before card creation. Needs profile phone number and id_number set via PUT /profile/document (id_number is sent as orgCode to MasterPay)
4. Create card: POST /api/v1/masterpay/cards/single-use or /multi-use — returns masked PAN and card ATM PIN
5. Get full details: POST /api/v1/masterpay/cards/:id/details (requires transaction PIN) — returns full card number and CVV


### Apply for a Card

Apply for a new physical or virtual card via the card application flow

1. Get card types: GET /api/v1/masterpay/cards/types — see available types (silver, gold, titanium, hybrid_metal, digital_virtual, digital_virtual_2)
2. Apply: POST /api/v1/cards/apply with {card_type, delivery_method, full_name, phone_number, email, address?}
3. Track: GET /api/v1/cards/:id — check application status


## Rules

- KYC must be approved AND wallet KYC must be submitted (POST /masterpay/wallets/kyc) before creating any MasterPay card — card creation fails with NO_WALLETS if KYC is not complete, and MasterPay rejects cards if wallet KYC is missing
- MasterPay card responses include a masked PAN and the card ATM PIN — use /cards/:id/details with transaction PIN for the full card number and CVV
- The card ATM PIN (visible in get_card, list_cards, and card creation responses) is for ATM/POS use — it is different from the transaction PIN used for sensitive operations
- Lock/unlock/cancel operations require transaction PIN verification
- Cancelled cards cannot be reactivated — cancellation is permanent
- Card application (POST /cards/apply) requires card_type (silver/gold/titanium/hybrid_metal/digital_virtual/digital_virtual_2) and delivery_method (delivery/on_the_spot)
- Card application (/cards/apply) is for ordering new cards — use /masterpay/cards/single-use or /multi-use for instant virtual card creation

## Agent Guidance

Follow these instructions when executing this skill:

- Always follow the documented flow order. Do not skip steps.
- If a tool requires authentication, verify the session has a valid bearer token before calling it.
- If a tool requires a transaction PIN, ask the user for it fresh each time. Never cache or log PINs.
- Never expose, log, or persist secrets (passwords, tokens, full card numbers, CVVs).
- If the user requests an operation outside this skill's scope, decline and suggest the appropriate skill.
- If a step fails, check the error and follow the recovery guidance below before retrying.

- The full prerequisite chain is: KYC approved → wallet exists → wallet KYC submitted → card creation. Use `get_kyc_status` from the kyc-identity skill to verify KYC approval, then `list_card_wallets` to confirm a wallet exists. If no wallets exist, KYC is not yet approved. Then submit wallet KYC (POST /masterpay/wallets/kyc) before creating any card — MasterPay rejects card creation without wallet KYC.
- MasterPay card responses (creation, `get_card`, `list_cards`) include the card ATM PIN in the response — no transaction PIN is needed to see it.
- To get the full unmasked card number and CVV, call `get_card_details` with the user's transaction PIN. This is the only way to retrieve the full PAN and CVV.
- The card ATM PIN (for ATM/POS use) is different from the transaction PIN (the user's security PIN for sensitive operations like viewing full card details, locking, unlocking, or cancelling).
- Lock, unlock, and cancel operations all require the transaction PIN.
- Cancelled cards cannot be reactivated. Confirm with the user before cancelling.
