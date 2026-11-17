---
name: agentgates-inference
description: "Ask confidential or open models in the standard chat format, one request one x402 USDC payment, priced before the model runs; prepaid balances and bearer keys for volume."
---

# Agentgates Inference: models by the request, paid in USDC (x402)

Ask models in the standard chat format. Confidential models run in attested
hardware; an open tier is cheaper and carries no attestation, and every model
names its tier. One request, one USDC payment. No signup: the paying wallet
is the customer.

## Endpoints (all on https://api.agentgates.ai)

- `GET /api/inference/docs`: models, live prices, and the full contract. Read this first; prices move with gas and are never cached here.
- `GET /api/inference/catalog`: models and prices, machine-readable JSON.
- `POST /api/inference/chat`: ask. Body: `{"model","messages","max_tokens"}`.
- `POST /api/inference/credits`: prepay a balance so one on-chain settle covers many requests.

## The x402 loop

1. POST with no `X-PAYMENT` header: `402` with an `accepts` array; each
   entry is one network's own offer for YOUR body. Quoting is free and
   repeatable.
2. Sign that entry's amount as an EIP-3009 TransferWithAuthorization.
3. Retry the same request with the signature in `X-PAYMENT`. The answer
   carries the completion and the settlement.

## What a request costs

You pay for the tokens the provider counts, at the model's input and output
rates, plus one settle per x402 request. The 402 asks for the ceiling (your
prompt and your `max_tokens`); what the tokens did not cost comes back to
your balance.

## Cheaper at volume

Prepay a balance (`POST /api/inference/credits`) and then ask with an
`X-Wallet-Auth` header and NO payment header: the settle happens once for
the whole top-up. A wallet can also mint revocable bearer API keys on its
prepaid balance, so plain `Authorization: Bearer` clients work; the mint
contract is in `GET /api/inference/docs`.

## Rules that keep you safe

- Give reasoning models room: a ceiling too small can end at
  `finishReason: "length"` with little or no `content`, billed at its tokens.
- A serve failure is a free replay, never a refund.

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.
