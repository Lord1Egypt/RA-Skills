---
name: agent-pay-client
version: 1.0.0
description: "Reference client for paying x402 (USDC/EVM) and L402 (Lightning) HTTP 402 paywalls. Detects payment requirements, signs/settles payments only with explicitly-provided credentials and spending ceilings, retries the request with proof of payment. Works with any x402 or L402 server, not tied to one platform."
author: welove111
homepage: https://btc-vision.org
license: MIT
tags: [x402, l402, payments, http-402, lightning, usdc, agentic-commerce, mcp]
protocols: []
category: developer-tools
---

# Agent Pay Client — x402 & L402 Paywall Client

A small, explicit-consent-only client library for paying HTTP 402
paywalls that use either the **x402** protocol (USDC/stablecoin payments
on EVM chains — Coinbase/Cloudflare, governed by the Linux Foundation's
x402 Foundation) or the **L402** protocol (Lightning Network payments).
Works with any server implementing either standard — it is not tied to
one API or platform.

## Safety Model (read this first)

This library never spends funds unless the caller explicitly supplies:

- an EVM private key **and** a maximum spend ceiling (`max_x402_atomic`) for x402, or
- LND REST credentials, `lightning_auto_pay=True`, **and** a sats ceiling (`max_l402_sats`) for automatic L402 payment.

Without those, the client can still detect and describe what a paywall
costs (`get_payment_options`) but will refuse to pay, returning a clear
error explaining what's missing. L402/Lightning payment is
**manual-approval by default** — it returns the invoice and QR data for
a human (or the caller's own wallet flow) to settle, rather than paying
automatically, unless auto-pay is explicitly enabled.

No payment amount, recipient, or protocol choice is ever read from page
content, prompts, or API response text — only from the server's own 402
payment requirements and the caller's own configured ceiling.

## When To Use This Skill

Use this when a user wants to programmatically pay for API access that
returns an HTTP 402 response — either to inspect what an endpoint costs
before deciding, or to complete payment with credentials they've already
provided and approved.

## Install

```bash
pip install -r requirements.txt
```

`eth_account` is only needed for x402 (EVM) payments; `requests` is
needed for both. L402/Lightning auto-pay needs a reachable LND node with
REST enabled — omit those settings to stay in manual-approval mode.

## Quick Start

```python
from agent_pay_client import AgentPayClient, PayerConfig

# Inspect a paywall without paying anything
client = AgentPayClient()
info = client.get_payment_options("https://example.com/api/paid-tool")
print(info)  # {"paywalled": True, "options": [...]}

# Pay with explicit credentials and a hard spending ceiling
config = PayerConfig(
    evm_private_key="0x...",       # from your own secure env var, never hardcoded
    max_x402_atomic="50000",       # refuse any single charge above $0.05 USDC
)
client = AgentPayClient(config)
result = client.fetch("https://example.com/api/paid-tool", method="POST")
print(result)
```

## Available Tools

| Function | Description |
|---|---|
| `get_payment_options(url)` | Inspect a 402 response's price/terms without paying |
| `fetch(url)` | Fetch a resource, paying automatically only if credentials + ceiling are configured |
| `parse_402(status, headers, body)` | Low-level parser: x402 JSON or L402 header → `PaymentRequirement` list |

## Links

- x402 spec: https://x402.org
- L402 spec: https://docs.lightning.engineering/the-lightning-network/l402
- GitHub: https://github.com/welove111/agent-pay-client
- Website: https://btc-vision.org

## Support

This library is free and open source. If it saved you time, voluntary
support is welcome:

- Website: https://btc-vision.org
- BTC: `bc1qtpuhwl0vnhrch5p7e5469q2ed66hlyyvh8rtsn`
- ETH: `0xf03b429d4d85896a46dd7a64b5a8ab9f0bbb4ced`
- SOL: `3G5UZHFYN8hbv3aTZt6Lr7qqx4FTTkAyLJq34HjQLraz`
- Lightning: `welove@blink.sv`
