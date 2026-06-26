# x402 Agent Payments 💧

Unified payment orchestration for AI agents. Four rails, one skill.

- **Stripe** — Accept fiat: cards, invoices, subscriptions
- **Coinbase Commerce** — Accept crypto: BTC, ETH, USDC checkout
- **Coinbase CDP** — Send crypto: wallets, single transfers
- **Spraay x402** — Batch send: payroll, multi-recipient, invoices

## Important

**All operations involve real funds.** Crypto transactions are irreversible.
Card charges are real. Always confirm with the user before executing.

## Install

```
clawhub install agent-payments
```

Or from GitHub:

```
clawhub install github:plagtech/agent-payments-x402
```

## Requirements

- `curl` and `jq`
- Set the env vars for the rails you need:
  - `SPRAAY_GATEWAY_URL` — batch payments, payroll, invoices (x402 pay-per-call)
  - `STRIPE_SECRET_KEY` — card and fiat payments
  - `COINBASE_COMMERCE_API_KEY` — accept crypto from customers
  - `CDP_API_KEY` — crypto wallets and single transfers
- Works with any combination — set only what you need

## Quick Start

Ask your agent:

- "Send payroll: alice.eth (3000) and bob.base (2500) on Base"
- "Create a Stripe checkout for $50"
- "Accept a $100 crypto payment from a client"
- "Create a new crypto wallet on Base"
- "Transfer 100 USDC to 0xABC..."
- "What's the price of ETH?"

## Links

- Spraay Docs: https://docs.spraay.app
- Stripe Docs: https://docs.stripe.com
- Coinbase Commerce: https://docs.cdp.coinbase.com/commerce
- Coinbase CDP: https://docs.cdp.coinbase.com
- GitHub: https://github.com/plagtech

Built by [@plag](https://warpcast.com/plag)
