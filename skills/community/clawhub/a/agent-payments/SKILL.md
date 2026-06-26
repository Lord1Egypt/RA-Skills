---
name: agent-payments
description: >-
  Unified payment skill for AI agents. Four payment rails in one skill:
  Stripe for credit card and fiat payments, Coinbase Commerce for accepting
  crypto from customers, Coinbase CDP for crypto wallets and transfers, and
  Spraay x402 for batch crypto payments and payroll. Use when an agent needs
  to accept payments, charge customers, create checkout sessions, accept crypto,
  manage wallets, send transfers, batch pay, run payroll, or create invoices.
version: 1.1.0
homepage: https://spraay.app
metadata:
  openclaw:
    emoji: "💧"
    requires:
      bins:
        - curl
        - jq
      env:
        - SPRAAY_GATEWAY_URL
    primaryEnv: SPRAAY_GATEWAY_URL
    envVars:
      - name: SPRAAY_GATEWAY_URL
        required: true
        description: >-
          Spraay x402 gateway base URL (https://gateway.spraay.app).
          Handles batch payments, payroll, invoices, and price feeds.
      - name: STRIPE_SECRET_KEY
        required: false
        description: >-
          Stripe API secret key for fiat/card payment operations.
          Required only when using Stripe checkout, invoices, or subscriptions.
      - name: COINBASE_COMMERCE_API_KEY
        required: false
        description: >-
          Coinbase Commerce API key for accepting crypto payments from customers.
          Required only when creating crypto checkout charges.
      - name: CDP_API_KEY
        required: false
        description: >-
          Coinbase CDP API key for crypto wallet creation and transfers.
          Required only when creating wallets or sending single transfers.
---

# x402 Agent Payments 💧

Unified payment orchestration for AI agents. Four payment rails, one skill.

| Rail | What It Does | Env Var |
|------|-------------|---------|
| **Stripe** | Accept fiat — cards, invoices, subscriptions | `STRIPE_SECRET_KEY` |
| **Coinbase Commerce** | Accept crypto — BTC, ETH, USDC checkout | `COINBASE_COMMERCE_API_KEY` |
| **Coinbase CDP** | Send crypto — wallets, single transfers | `CDP_API_KEY` |
| **Spraay x402** | Batch send — payroll, multi-recipient, invoices | `SPRAAY_GATEWAY_URL` |

All requests go exclusively to the declared API endpoints for each provider.
No data is sent to any other external services. The skill works with any
combination of rails — set only the env vars you need.

## Important Warnings

**All payment operations involve real funds.** Whether fiat or crypto, every
transaction in this skill moves real money. The agent must always confirm
the following with the user before executing any payment:

- Payment amount and currency are correct
- Recipient (address, email, or account) is intended
- The user understands any associated fees
- For crypto: blockchain transactions are irreversible once confirmed
- For Stripe: card charges are real and will appear on statements
- For Commerce: charges expire after 60 minutes if unpaid

**Never execute payments without explicit user confirmation.**

## Choosing the Right Rail

| Use Case | Rail |
|----------|------|
| Charge a customer in USD | Stripe |
| Create an invoice (fiat) | Stripe |
| Recurring subscription | Stripe |
| Accept BTC/ETH/USDC from a customer | Coinbase Commerce |
| Create an agent crypto wallet | Coinbase CDP |
| Send crypto to one address | Coinbase CDP |
| Pay 10-1000 people at once | Spraay x402 |
| Monthly payroll in USDC | Spraay x402 |
| Invoice a client in crypto | Spraay x402 |

## Rail 1: Stripe — Accept Fiat Payments

Accept credit card payments, create invoices, manage subscriptions.
Requires `STRIPE_SECRET_KEY`.

### Create Checkout Session

**Confirm the product, price, and currency with the user first.**

```bash
curl -X POST "https://api.stripe.com/v1/checkout/sessions" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=payment" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel" \
  -d "line_items[0][price_data][currency]=usd" \
  -d "line_items[0][price_data][unit_amount]=5000" \
  -d "line_items[0][price_data][product_data][name]=Service Payment" \
  -d "line_items[0][quantity]=1"
```

Returns a checkout URL to share with the customer.

### Create Payment Intent

```bash
curl -X POST "https://api.stripe.com/v1/payment_intents" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=5000" \
  -d "currency=usd" \
  -d "payment_method_types[]=card"
```

### Create Invoice

**Confirm invoice details with the user first.**

```bash
curl -X POST "https://api.stripe.com/v1/invoiceitems" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_..." \
  -d "amount=5000" \
  -d "currency=usd" \
  -d "description=Consulting — March 2026"
```

### Create Subscription

```bash
curl -X POST "https://api.stripe.com/v1/subscriptions" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "customer=cus_..." \
  -d "items[0][price]=price_..."
```

### Check Payment Status

```bash
curl "https://api.stripe.com/v1/payment_intents/pi_..." \
  -u "$STRIPE_SECRET_KEY:"
```

### Refund a Payment

**Confirm refund with the user first.**

```bash
curl -X POST "https://api.stripe.com/v1/refunds" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "payment_intent=pi_..."
```

## Rail 2: Coinbase Commerce — Accept Crypto

Accept cryptocurrency payments from customers. They pay in BTC, ETH, USDC,
or other supported coins via a hosted checkout page. Funds settle to your
Coinbase account. Requires `COINBASE_COMMERCE_API_KEY`.

### Create a Charge

**Confirm the amount and currency with the user first.**

```bash
curl -X POST "https://api.commerce.coinbase.com/charges" \
  -H "Content-Type: application/json" \
  -H "X-CC-Api-Key: $COINBASE_COMMERCE_API_KEY" \
  -d '{
    "name": "Service Payment",
    "description": "Payment for consulting services",
    "pricing_type": "fixed_price",
    "local_price": {
      "amount": "100.00",
      "currency": "USD"
    }
  }'
```

Returns `hosted_url` (Coinbase checkout page to share with customer) and
`expires_at` (charges expire after 60 minutes).

### Check Charge Status

```bash
curl "https://api.commerce.coinbase.com/charges/CHARGE_ID" \
  -H "X-CC-Api-Key: $COINBASE_COMMERCE_API_KEY"
```

Status flow: NEW → PENDING → CONFIRMED / FAILED / EXPIRED

### Cancel a Charge

```bash
curl -X POST "https://api.commerce.coinbase.com/charges/CHARGE_ID/cancel" \
  -H "X-CC-Api-Key: $COINBASE_COMMERCE_API_KEY"
```

## Rail 3: Coinbase CDP — Crypto Wallets & Transfers

Create wallets and send crypto. For agent-managed funds and single transfers.
Requires `CDP_API_KEY`.

### Create Wallet

```bash
curl -X POST "https://api.developer.coinbase.com/platform/v1/wallets" \
  -H "Authorization: Bearer $CDP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"network": "base"}'
```

### Send Transfer

**Confirm recipient, amount, and token with the user first.**

```bash
curl -X POST "https://api.developer.coinbase.com/platform/v1/wallets/WALLET_ID/transfers" \
  -H "Authorization: Bearer $CDP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "0xRecipient...",
    "amount": "100",
    "asset": "usdc",
    "network": "base"
  }'
```

### Check Balance

```bash
curl "https://api.developer.coinbase.com/platform/v1/wallets/WALLET_ID/balances" \
  -H "Authorization: Bearer $CDP_API_KEY"
```

## Rail 4: Spraay x402 — Batch Payments & Payroll

Pay multiple recipients in one transaction. 60-80% gas savings vs individual
transfers. Pay-per-call via x402 micropayments, no API key needed.
Uses `SPRAAY_GATEWAY_URL`.

### Batch Payment

**Confirm all recipients, amounts, token, and chain with the user first.**

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/batch-payment" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": [
      {"address": "alice.eth", "amount": "3000"},
      {"address": "bob.base", "amount": "2500"},
      {"address": "0xCCC...999", "amount": "4000"}
    ],
    "token": "USDC",
    "chain": "base",
    "memo": "March 2026 payroll"
  }'
```

If you receive HTTP 402, pay the micropayment and retry with the
`X-PAYMENT` proof header.

### Create Invoice (Crypto)

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/create-invoice" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "0xABC...123",
    "amount": "500",
    "token": "USDC",
    "chain": "base",
    "memo": "March consulting"
  }'
```

### Token Price (Free)

```bash
curl "$SPRAAY_GATEWAY_URL/api/price?symbol=ETH"
```

### Resolve ENS / Basename (Free)

```bash
curl "$SPRAAY_GATEWAY_URL/api/resolve?name=vitalik.eth"
```

Supported chains: Base, Ethereum, Arbitrum, Polygon, BNB Chain, Avalanche,
Solana, Unichain, Plasma, BOB.

## Free Endpoints

No payment or API key required:

- `GET $SPRAAY_GATEWAY_URL/api/price?symbol=ETH` — Token prices
- `GET $SPRAAY_GATEWAY_URL/api/resolve?name=vitalik.eth` — Name resolution
- `GET $SPRAAY_GATEWAY_URL/api/health` — Gateway health check
- `GET $SPRAAY_GATEWAY_URL/api/chains` — Supported chains

## Error Handling

- `402` — x402 payment required. Follow response body instructions.
- `400` — Bad request. Check parameters.
- `401` — Missing or invalid API key (Stripe, Commerce, or CDP).
- `404` — Endpoint not found.
- `500` — Server error. Retry after a moment.

## Tips

- Always confirm with the user before executing any payment.
- Use Stripe to accept fiat from customers.
- Use Commerce to accept crypto from customers.
- Use CDP to create wallets and send single transfers.
- Use Spraay for batch operations — payroll, airdrops, multi-recipient.
- Not all env vars are required — set only the rails you need.
- Check `/api/price` to show USD equivalents for crypto payments.

## Links

- Spraay Docs: https://docs.spraay.app
- Stripe Docs: https://docs.stripe.com
- Coinbase Commerce: https://docs.cdp.coinbase.com/commerce
- Coinbase CDP: https://docs.cdp.coinbase.com
- GitHub: https://github.com/plagtech
