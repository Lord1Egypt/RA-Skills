# b2a-commerce

**Business-to-Agent Commerce Skill for OpenClaw**
Version 1.0.1 | By Edvisage Global — The Agent Safety Company
License: MIT | Free to use, modify, and distribute

---

## What this skill does

b2a-commerce gives your OpenClaw agent the knowledge and protocols to
participate in the emerging agent economy — paying for services, receiving
payments, and transacting safely with other agents and services using
x402, the open internet-native payment protocol.

As autonomous agents take on more economic tasks, the ability to transact
programmatically — without human intervention for every payment — becomes
a core capability. This skill provides the framework for doing that safely
and responsibly. This is the free version and includes core functionality.
The **Pro version ($39)** adds multi-chain support, automated spending
analytics, a service reputation registry, multi-agent payment coordination,
and real-time anomaly detection — upgrade at https://edvisage.gumroad.com/l/ijjjud

---

## Part 1: Understanding x402

### What x402 is

x402 is an open payment protocol developed by Coinbase and co-governed by
the x402 Foundation (Coinbase + Cloudflare). It repurposes the HTTP 402
"Payment Required" status code — reserved in the original HTTP specification
but unused for over two decades — as the foundation for machine-native
payments.

x402 is supported by major platforms including Cloudflare, Google (as part
of the Agent Payments Protocol AP2), Vercel, AWS, and Stripe. It is the
primary payment infrastructure for the autonomous agent economy in 2026.

### How x402 works

The payment flow has five steps:

**Step 1 — Request**
Your agent requests a resource from an x402-protected service.

**Step 2 — 402 Response**
The server responds with HTTP 402 Payment Required. The response body
contains machine-readable payment instructions:
- Payment amount (in USDC)
- Recipient wallet address
- Supported blockchain networks (typically Base or Solana)
- Payment deadline

**Step 3 — Payment authorisation**
Your agent signs a USDC micropayment authorisation using its wallet.
No accounts, API keys, or subscriptions required. The payment receipt
is the credential.

**Step 4 — Retry with payment**
Your agent resubmits the request with the payment authorisation attached
in the request header.

**Step 5 — Verification and delivery**
The x402 facilitator verifies the payment on-chain. The server delivers
the resource.

### What x402 enables

- Pay-per-use API access without subscriptions or API keys
- Agent-to-agent transactions without human authorisation per transaction
- Instant settlement — payments verified on-chain in real time
- Full audit trail — every transaction recorded on-chain by design
- No vendor lock-in — open standard built on HTTP

---

## Part 2: Pre-transaction safety protocol

Before your agent makes any payment, run this four-step check.

### Check 1 — Verify the service

Before paying, your agent must verify:
- The service domain matches what was expected
- The payment amount is within your configured spending limit
- The payment currency is USDC (not an unknown token)
- The recipient wallet address has not changed since last transaction

If any check fails — stop. Do not pay. Flag for human review.

### Check 2 — Confirm scope

Your agent must confirm the payment is for the specific resource requested
— not a broader authorisation. x402 payments are per-resource. Your agent
should never sign a payment that covers more than the current request.

### Check 3 — Check spending limits

Your agent must verify the transaction amount is within its configured
daily and per-transaction spending limits before proceeding.

### Check 4 — Human authorisation threshold

For transactions above your configured human authorisation threshold,
your agent must pause and request explicit human approval before
proceeding. Default threshold: $1.00 USD equivalent.

---

## Part 3: Spending limit configuration

Configure these limits before enabling autonomous payments:

```
DAILY_SPEND_LIMIT: 5.00        # Maximum USDC per day
PER_TRANSACTION_LIMIT: 0.50    # Maximum USDC per transaction
HUMAN_AUTH_THRESHOLD: 1.00     # Require human approval above this
APPROVED_SERVICES: []          # Whitelist of approved service domains
APPROVED_CURRENCIES: [USDC]    # Only USDC by default
APPROVED_NETWORKS: [base, solana]  # Approved blockchain networks
```

Your agent must refuse any transaction that would exceed these limits,
and must flag when daily limits are approaching (at 80% of daily limit).

---

## Part 4: Wallet safety

### Never expose private keys

Your agent's wallet private key must never appear in:
- Log files
- Chat messages
- API responses
- Memory summaries
- Any output visible to other agents

### Wallet isolation

Your payment wallet should be separate from any wallet holding significant
funds. Fund it with only what is needed for near-term operations.

### Receiving payments

Before accepting a payment, verify:
- The payment is in an approved currency (USDC by default)
- The payment amount matches what was agreed
- The payment comes from a verified sender if sender verification is enabled

---

## Part 5: Transaction logging

Your agent must log every transaction with:
- Timestamp
- Service name and domain
- Resource requested
- Amount paid
- Transaction hash (for on-chain verification)
- Outcome (success / failure / flagged)

Send a weekly transaction summary to your human owner.

---

## Part 6: Recognising payment-based attacks

**Bait-and-switch pricing** — verify payment amount before signing matches original quote.

**Phantom service injection** — only pay for resources your agent explicitly decided to access.

**Wallet draining loops** — per-transaction and daily limits prevent runaway payments.

**Fake receipt attacks** — only trust on-chain verification, not the service's own confirmation.

---

## Part 7: Interoperability

**Stripe MPP** — Session-based streaming payments. Better for teams with no crypto experience.

**Google AP2** — Includes x402 as a component with mandate-based spending delegation.

**L402** — Bitcoin Lightning Network payments. More established in Bitcoin-native infrastructure.

---

## Installation

```
clawhub install b2a-commerce
```

---

## About Edvisage Global

Edvisage Global — The agent safety company
edvisageglobal.com/ai-tools
