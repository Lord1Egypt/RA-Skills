# b2a-commerce

> Business-to-Agent commerce skill for OpenClaw agents

Gives your OpenClaw agent the knowledge and protocols to participate in
the agent economy using x402 — the open internet-native payment protocol
backed by Coinbase, Cloudflare, Google, and Stripe.

## What it includes

- Complete x402 protocol understanding and payment flow
- Pre-transaction safety protocol (4-step verification)
- Spending limit configuration framework
- Wallet safety guidelines
- Transaction logging requirements
- Payment-based attack pattern recognition
- Interoperability guide (x402, Stripe MPP, Google AP2, L402)

## Install

```
clawhub install b2a-commerce
```

## Why agent commerce needs safety built in

Most agents gaining payment capability are being handed a wallet with no
safety framework. b2a-commerce provides the guardrails that should ship
with every payment-enabled agent:

- Spending limits that actually enforce
- Human authorisation thresholds for larger transactions
- Wallet isolation to limit exposure
- Attack pattern recognition specific to payment flows
- Full audit trail for every transaction

Commerce without safety is how agents become expensive liabilities.

## Pro version

b2a-commerce-pro adds multi-wallet management, spending analytics,
service reputation registry, multi-agent payment coordination, Stripe
MPP support, smart spending limits, anomaly detection, and integration
templates for 20+ x402-enabled services.

Coming soon at edvisageglobal.com/ai-tools

## Publisher

**Edvisage Global** — The agent safety company  
[edvisageglobal.com/ai-tools](https://edvisageglobal.com/ai-tools)

## License

MIT
