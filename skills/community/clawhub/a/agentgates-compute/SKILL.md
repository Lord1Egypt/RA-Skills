---
name: agentgates-compute
description: "Confidential computers for AI swarms: rent a confidential VM (Intel TDX) for each agent by the hour with USDC over x402 and run a Docker workload on it. No signup; the paying wallet owns the machine."
---

# Agentgates Compute: confidential computers for AI swarms, paid in USDC (x402)

Rent a dedicated confidential VM (Intel TDX) for each agent in your swarm, by
the hour, and run its Docker workload on it: trading swarms, research, data and
backtesting swarms, agents that serve their own APIs. No signup and no API key:
the wallet that pays owns the deployment. Every machine carries a
remote-attestation quote.

## Endpoints (all on https://api.agentgates.ai)

- `GET /api/compute/docs`: the full contract and live prices. Read this first; prices move with gas and are never cached here.
- `GET /api/compute/catalog`: plans and prices, machine-readable JSON.
- `POST /api/compute/deployments`: buy. Body: `{"plan","hours","compose"|"image","env","name"}`.
- `GET /api/compute/deployments/{id}`: read state; `endpoint` and `attestation` appear when `status` is `running`.

Over MCP, with no account and no sign-in: `https://mcp.agentgates.ai/compute`
(Streamable HTTP) lists the plans (`compute_plans`), prices one machine
(`compute_quote`) and returns these docs (`compute_docs`).

## The x402 loop

1. Send the POST with no payment header. The answer is `402` with an
   `accepts` array: each entry is ONE network's own offer with its exact
   `maxAmountRequired` in USDC atomic units, the `asset` contract and the
   `payTo` address. Quoting is free and repeatable; nothing is charged.
2. Sign that entry's amount as an EIP-3009 TransferWithAuthorization
   (EIP-712 domain in the entry's `extra`).
3. Retry the SAME request with the signature in `X-PAYMENT`
   (base64 of the x402 payload). Settlement confirms on-chain, then the
   machine provisions; the billed clock starts at `running`, not at payment.

x402 v2 clients: the same 402 carries a `PAYMENT-REQUIRED` header (CAIP-2
networks). Send the payment in `PAYMENT-SIGNATURE`; the receipt comes back
in `PAYMENT-RESPONSE`.

## Rules that keep you safe

- Read the price from the 402 you are answering, never from a cached quote.
- Your compose must publish a port: a machine that publishes nothing runs
  and bills with no way to reach it.
- Env values are sealed to the enclave and never stored; keep secrets
  re-settable.

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.
