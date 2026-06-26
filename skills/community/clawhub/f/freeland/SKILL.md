---
name: freeland
description: Agent-first API for wallet, cards, inbox OTP, Mr. Freeman, eSIM, VPN, and crypto invoices.
version: 1.2.0
homepage: https://freeland.land
metadata: {"openclaw":{"requires":{"env":["FREELAND_API_KEY"]},"primaryEnv":"FREELAND_API_KEY","emoji":"🏴"}}
---

# Freeland

Freeland gives OpenClaw and other agents a real wallet, virtual cards, OTP inbox, Mr. Freeman chat, eSIM, VPN, and crypto invoice flows through one user-owned account.

Primary use cases:
- wallet, cards, and OTP-backed checkout flows
- connectivity services like eSIM and VPN
- platform-funded Mr. Freeman conversations
- invoice creation for collecting USDT

## Authentication

All requests use the same Bearer token.

```bash
Authorization: Bearer $FREELAND_API_KEY
```

Production base URL:

```bash
BASE_URL="https://app.freeland.land/api.php"
```

Recommended helpers:

```bash
freeland_get() {
  local path="$1"
  curl --silent --show-error --get "$BASE_URL" \
    --data-urlencode "path=$path" \
    -H "Authorization: Bearer $FREELAND_API_KEY"
}

freeland_post() {
  local path="$1"
  local body="${2:-{}}"
  curl --silent --show-error -X POST "$BASE_URL?path=$path" \
    -H "Authorization: Bearer $FREELAND_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$body"
}
```

## Trust Model

Freeland is designed for real, user-owned agent operations.

- The user owns the wallet, cards, inbox, connectivity services, and invoice flows.
- The API key grants access to the user's own account surface.
- Wallet balance and card balance are separate values.
- Provider readiness matters. If a service is offline, surface that honestly instead of pretending the flow worked.
- Sensitive outputs like PAN, CVV, billing address, inbox contents, and VPN configs should only be revealed when needed for the active task.

## Autonomy Model

Freeland may be used in approval-based or pre-authorized mode.

- In approval-based mode, ask before issuing cards, topping up cards, withdrawing funds, buying eSIM plans, creating VPN subscriptions, or creating invoices.
- In pre-authorized mode, act only inside the user's stated balance, merchant, service, and spending boundaries.

## Safety Boundaries

- Only use the user's own Freeland resources.
- Never invent billing data, cardholder details, mailbox codes, deposit addresses, or provider states.
- Do not retry balance-moving actions blindly. Read current state first.
- Treat provider failures, fraud checks, issuer declines, KYC gates, geography restrictions, and missing OTPs as hard boundaries.
- Do not expose sensitive card credentials or mailbox contents longer than necessary.
- For unfamiliar merchants, subscriptions, retries, and OTP-backed checkouts, read `references/payment-safety.md` first.
- For eSIM and VPN install or troubleshooting flows, read `references/connectivity.md` first.
- For payment collection and hosted payment links, read `references/invoices.md` first.

## Default Behavior

- Start with `GET /me`.
- If the user asks for account readiness, report mailbox, wallet balance, deposit rail, card state, and service readiness separately.
- Treat `wallet balance`, `card balance`, and `provider readiness` as distinct facts.
- Use `card.id` for Freeland card routes.
- Lead with buyer-side wallet/card workflows. Use invoice creation only when the user explicitly wants to collect payments.
- For VPN, Freeland currently provides subscription plus WireGuard config delivery, not an in-browser tunnel.
- For eSIM, prefer install-ready profiles over re-listing the whole catalog when the user already owns one.

## Core Jobs

### 1. Check account readiness

```bash
freeland_get "/me"
freeland_get "/wallet/balance"
freeland_get "/wallet/deposit-address"
freeland_get "/freeman/status"
freeland_get "/esim/status"
freeland_get "/vpn/status"
```

Important facts to surface:
- account `status`
- `mailboxAddress`
- wallet `balance`
- `depositAddress` status and address
- current `card`, if present
- `Freeman`, `eSIM`, and `VPN` readiness

### 2. Fund the wallet

```bash
freeland_get "/wallet/deposit-address"
freeland_get "/wallet/transactions?limit=20&offset=0"
```

Rules:
- deposits land on the user's USDT TRON rail
- wallet balance credits the net amount that actually reaches the address
- external sender, exchange, and network fees may reduce the credited amount before Freeland receives it

### 3. Issue and use a card

```bash
freeland_post "/cards/issue"
freeland_get "/cards/CARD_ID"
freeland_get "/cards/CARD_ID/balance"
freeland_get "/cards/CARD_ID/sensitive"
freeland_get "/cards/CARD_ID/transactions?limit=20&offset=0"
```

Rules:
- issue only when wallet balance is sufficient
- card routes use the Freeland card `id`
- use the sensitive response for PAN, CVV, expiry, cardholder name, and billing address
- after any merchant error, inspect card transactions before retrying

### 4. Top up a card

```bash
freeland_post "/cards/CARD_ID/topup" '{"amount":10,"currency":"USD"}'
```

Pre-flight:
1. read `GET /wallet/balance`
2. read `GET /cards/CARD_ID`
3. confirm the card is active
4. confirm the wallet covers the requested topup
5. only then send the topup request

### 5. Fetch OTP or receipt emails

```bash
freeland_get "/inbox/latest-otp"
freeland_get "/inbox?limit=20&offset=0"
freeland_get "/inbox/MESSAGE_ID"
```

Use this for 3DS, OTP verification, receipts, and merchant follow-up.

### 6. Talk to Mr. Freeman

```bash
freeland_get "/freeman/status"
freeland_post "/freeman/chat" '{"messages":[{"role":"user","content":"What am I avoiding?"}]}'
```

Mr. Freeman is platform-funded. Do not ask the user for a personal model key for this flow.

### 7. Work with eSIM

```bash
freeland_get "/esim/status"
freeland_get "/esim/plans?country=TR"
freeland_get "/esim/profiles"
freeland_post "/esim/purchase" '{"planId":"PLAN_ID"}'
freeland_get "/esim/profiles/PROFILE_ID"
freeland_post "/esim/profiles/PROFILE_ID/topup" '{"planId":"PLAN_ID"}'
```

Rules:
- only buy or top up when the provider is live
- after purchase, prefer install-ready fields like `qrData`, `iosTapLink`, and `esimPassportUrl`
- if a profile already exists, lead with install or topup instead of re-buying blindly

### 8. Work with VPN

```bash
freeland_get "/vpn/status"
freeland_get "/vpn/servers"
freeland_get "/vpn/subscription"
freeland_post "/vpn/subscription"
freeland_get "/vpn/config/SERVER_ID?protocol=wireguard"
```

Rules:
- VPN is subscription plus WireGuard config delivery
- after activation, help the user install or import the config into WireGuard
- do not describe this as an in-browser VPN tunnel

### 9. Create invoices

```bash
freeland_post "/invoices" '{"amount":25,"currency":"USD","description":"Freelance work","reference":"INV-001","expiresInMinutes":60}'
freeland_get "/invoices?limit=20&offset=0"
```

Use this when the user wants to collect USDT through Freeland.

## Load References When Needed

- Read `references/payment-safety.md` before entering card details on an unfamiliar merchant, when a checkout keeps failing, or when OTP and retry boundaries matter.
- Read `references/connectivity.md` before helping with eSIM install, VPN import, mobile setup, or service troubleshooting.
- Read `references/invoices.md` when the user wants to create hosted invoices, explain invoice lifecycle, or reason about payment collection.

## Good Default Prompt Shapes

- `Check my Freeland account and tell me what is ready: wallet, card, inbox, Freeman, eSIM, and VPN.`
- `Use Freeland to issue a card and top it up if needed. Ask before any merchant checkout unless I say it is pre-authorized.`
- `Use Freeland inbox to fetch the latest OTP and confirm whether the last card payment actually went through.`
- `Use Freeland to buy an eSIM plan for Turkey and then guide me through installation.`
- `Use Freeland to activate VPN and hand me the right WireGuard config for my device.`
- `Use Freeland to create a USDT invoice for $25 and show me the payment link.`

## Scope Note

Freeland combines wallet, cards, inbox, character chat, connectivity services, and invoice collection. Lead with the simplest relevant workflow for the user's task instead of surfacing the whole platform at once.
