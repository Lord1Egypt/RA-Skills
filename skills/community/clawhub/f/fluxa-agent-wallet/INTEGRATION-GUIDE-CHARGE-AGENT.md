# Integration Guide — Charge Agent

## Overview

When your service needs to charge AI agents for usage (API fees, subscriptions, service costs, etc.), register your own Agent ID and create **Payment Links** with specific amounts. Agents pay via the x402 protocol.

## How It Works

```
Your Service                         Agent
  |                                    |
  |-- Return payment link URL -------->|
  |                                    |-- curl URL → get 402 payload
  |                                    |-- x402 payment flow
  |<-- X-Payment header + request -----|
  |-- Verify payment, deliver service->|
```

## Setup — Register Your Service as an Agent

Your service needs its own Agent ID to create payment links:

```bash
curl -X POST https://agentid.fluxapay.xyz/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "My Service",
    "client_info": "MyService Backend v1.0"
  }'
```

Save the returned `agent_id`, `token`, and `jwt`.

## Create a Payment Link for a Specific Charge

```bash
fluxa-wallet paymentlink-create \
  --amount "5000000" \
  --desc "API usage fee - March 2026" \
  --max-uses 1
```

Return the payment link URL to the agent. The agent pays it using the x402 flow.

For payment link management (create, list, update, delete), see [PAYMENT-LINK.md](PAYMENT-LINK.md).

For how agents pay a payment link, see the "Paying TO a Payment Link" section in [PAYMENT-LINK.md](PAYMENT-LINK.md) and [X402-PAYMENT.md](X402-PAYMENT.md).
