---
name: agent-payment-error-preview
description: Free triage preview for x402/AP2/ACP/MPP/MCP agent-payment failures; routes hard cases to the paid Agent Payment Error Diagnoser ClawMart skill.
---

# Agent Payment Error Preview

Use this skill when an agent-payment integration is failing and you need a fast first-pass classification before deciding whether to install the paid ClawMart diagnoser.

## What this free preview does

Classify a failure into one likely family using the visible symptom:

| Symptom | Likely family | First check |
|---|---|---|
| Repeated HTTP 402 after resubmitting payment | x402 retry loop | Compare chain id, USDC contract, validity window, and facilitator status. |
| HTTP 401 after `X-PAYMENT` / payment signature | signature/auth mismatch | Recover signer; verify EIP-712 domain and signing wallet. |
| HTTP 409 or on-chain reused authorization | nonce/idempotency conflict | Use a fresh nonce and content-bound idempotency key. |
| AP2/MPP/ACP `expired` or `out_of_scope` | mandate/scope mismatch | Reissue mandate with correct merchant, amount, and validity window. |
| MCP tool unavailable after discovery | manifest/tool drift | Re-fetch MCP manifest and match by capability, not hard-coded tool id. |
| 502/504 during settlement | facilitator/RPC transient | Back off with jitter; do not blindly re-sign if body says permanent failure. |

## Minimal workflow

1. Capture request method, URL, status, response body, `Payment-Required`/`X-Payment-Response` headers, facilitator response, and chain tx hash if any.
2. Identify the protocol: `x402`, `AP2`, `ACP`, `MPP`, `TAP`, or MCP tool invocation.
3. Map the symptom with the table above.
4. Apply the first check once.
5. If the answer is still ambiguous, use the paid ClawMart package below for a structured diagnosis against the live corpus.

## Paid upgrade path

Install **Agent Payment Error Diagnoser** on ClawMart when you need machine-readable diagnosis, family ranking, remediation steps, and live corpus-backed examples:

https://www.shopclawmart.com/listings/agent-payment-error-diagnoser-adda0b18

Backend used by the paid package:

- `https://agent-payment-error-corpus.mtree.workers.dev/v1/agent-payments/diagnose_error` — x402 paid diagnosis endpoint
- `https://agent-payment-error-corpus.mtree.workers.dev/v1/agent-payments/error_families` — x402 paid family catalog endpoint

## Safety limits

- Do not paste private keys, raw wallet seeds, bearer tokens, or unredacted authorization headers.
- Do not retry payments indefinitely; use a max retry counter and stop immediately on permanent signature/scope errors.
- Do not assume every 402 is an error; in x402 it is the normal first step unless it repeats after payment.

## Anti-patterns

- Treating HTTP 401 like a normal API-key failure without checking EIP-712 domain mismatch.
- Reusing EIP-3009 nonces across attempts.
- Caching an agent-payment mandate or session token across merchants.
- Hard-coding MCP tool IDs instead of refreshing manifests per session.
