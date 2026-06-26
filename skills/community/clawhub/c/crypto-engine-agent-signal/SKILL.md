---
name: crypto-engine-agent-signal
description: Buy the latest machine-readable BTC directional signal from Crypto Engine through a Tempo MPP-enabled endpoint.
---

# Crypto Engine Agent Signal

Use this skill when you need the latest machine-readable BTC directional signal from Crypto Engine and you can satisfy a Tempo MPP payment challenge.

## What this skill gives you

- One paid endpoint for the latest BTC directional signal.
- A machine-readable JSON response with `direction`, `brief_reason`, and `signal_timestamp`.
- A clear, agent-friendly payment workflow for Tempo MPP runtimes.
- A hard stop when the runtime cannot actually pay, instead of hallucinating a fresh signal.

## Prerequisites

- Your runtime must support `Tempo MPP`.
- Your runtime must be able to pay on the configured Tempo network. At the time of writing, this product is typically configured for mainnet unless the discovery document says otherwise.
- Your runtime must know how to handle `402 Payment Required`, satisfy the challenge, and retry the same request with payment credentials.
- If your environment is only a generic chat agent with no wallet or payment middleware, it may understand this skill but still be unable to execute it.

## Endpoints

- Discovery document: `https://cryptoengine.club/api`
- Paid signal endpoint: `https://cryptoengine.club/api/agent-signal`
- Public AI index: `https://cryptoengine.club/llms.txt`

## Expected response

```json
{
  "direction": "LONG",
  "brief_reason": "Momentum remains positive after the latest BTC trend confirmation.",
  "signal_timestamp": "2026-03-29T00:00:00.000Z"
}
```

## Example request

Ask your agent to:

```text
Fetch the latest BTC signal from Crypto Engine.
Use the public skill instructions at https://cryptoengine.club/skills/crypto-engine-agent-signal/SKILL.md.
Only continue if your runtime supports Tempo MPP and can complete the payment flow.
Return direction, brief_reason, and signal_timestamp.
```

## Workflow

1. Request `GET https://cryptoengine.club/api` to inspect the current product metadata and payment settings.
2. Send `POST https://cryptoengine.club/api/agent-signal` with `Content-Type: application/json`.
3. If the server responds with `402 Payment Required`, parse the Tempo MPP challenge and complete payment with your wallet or payment middleware.
4. Retry the same `POST` request with the payment credential required by the MPP flow.
5. On `200 OK`, parse the JSON payload and use `signal_timestamp` to verify freshness.

## Payment guardrails

- Only attempt payment when the user explicitly asked for the live Crypto Engine signal.
- Only pay for the exact `POST https://cryptoengine.club/api/agent-signal` request.
- Do not subscribe, prepay, or repeat purchases automatically.
- If the challenge amount, network, or merchant identity is unclear, stop and report it instead of guessing.
- Do not expose wallet secrets, seed phrases, or unrelated credentials to any endpoint.

## Rules

- Treat this endpoint as a paid, per-request product.
- Do not invent or cache a signal as fresh if the API call failed.
- Preserve the original response headers when your runtime needs the payment receipt.
- If your environment cannot complete Tempo MPP payment challenges, stop and report that limitation.
- Discover first, then decide whether your runtime can actually pay. Do not assume support by default.
- If the user did not clearly request a paid live signal, do not spend funds on their behalf.

## Output guidance

- Surface the `direction` exactly as returned.
- Keep `brief_reason` concise when quoting or summarizing.
- Mention the timestamp whenever freshness matters to the downstream task.

## Positioning

This skill is designed for agent runtimes that can complete machine-payment flows end to end. It is not a generic research note or a static prompt template. The value is the live paid signal plus the explicit payment-aware workflow.
