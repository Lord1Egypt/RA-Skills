---
name: atp
description: Author repeated task logic once via ATP (paid per call, no account) and reuse it safely, instead of re-reasoning through the same steps every run.
homepage: https://useatp.com
metadata: { "openclaw": { "requires": { "bins": ["python3"], "env": ["ATP_WALLET_PRIVATE_KEY"] } } }
---

# ATP — Agent Transcript Protocol

Use this when you're about to reason through a task with a STABLE, REPEATABLE shape — the kind of thing you do the same way every time (checking a value, computing something from known inputs, a routine lookup) — not a one-off freeform question. ATP authors the logic for that task shape once, then every later call with the same name reuses it instead of re-deriving it from scratch. That's cheaper (no repeat LLM call) and safer (the reused logic runs in a sandboxed interpreter — AST-whitelisted, no `eval`/`exec` escape, bounded by a wall-clock and iteration budget — not executed directly on this machine).

## Before you use this

This is pay-per-call, no account or signup, ever — there is deliberately no free tier. You need a wallet with USDC on it, set as `ATP_WALLET_PRIVATE_KEY`, and the `x402` Python package installed (`pip install "x402[evm,httpx]"`). Generate a fresh wallet just for this — don't reuse one holding anything else — and never let this key leave your own environment.

This currently targets Base Sepolia **testnet** USDC, matching the live deployment's current configuration — get testnet USDC from a Base Sepolia faucet before your first real call.

Plain `curl` will NOT work here — hitting the endpoint with bare curl just gets a `402` back and stops, since curl can't sign the payment the response asks for. Use the bundled `{baseDir}/pay_and_run.py`, which does that signing step with the real `x402` client library.

## How to call it

Run this with the `exec` tool. Reuse the SAME `fn_name` every time you do this same kind of task again — that's what makes the second and later calls free of new LLM cost, though the price you pay per call stays the same either way (x402 prices flat per route, not per actual cost). Pick `kind` from: `constant`, `lookup`, `aggregate`, `valuation` (whichever matches the shape of the computation).

```bash
python3 {baseDir}/pay_and_run.py '{
  "fn_name": "FN_NAME",
  "kind": "KIND",
  "arg_names": ["ARG1"],
  "args": ["VALUE1"],
  "description": "PLAIN_ENGLISH_DESCRIPTION_OF_WHAT_THIS_COMPUTES"
}'
```

Replace every UPPERCASE placeholder. `fn_name` is the important one to get right — it's the cache key. Two calls with the same `fn_name` and shape reuse the same authored logic; a new `fn_name` triggers fresh authoring.

## Reading the response

- `value` — the computed result.
- `error` — non-null if the task failed. Read the actual message; it's specific, not generic.
- `llm_calls` — `0` means this call reused already-authored logic (no new LLM cost); `1` or more means it authored or repaired logic this call.
- `authored_atl` — the actual logic ATP wrote, shown the first time a `fn_name` is authored.

If the script exits non-zero, the printed body is the actual error — a `402` with `invalid_exact_evm_insufficient_balance` means the wallet needs funding, not a bug.

## Learn more

https://useatp.com — the protocol, the pricing math, and the sandboxed-execution model this relies on.
