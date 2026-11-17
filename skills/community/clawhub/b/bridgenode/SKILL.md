---
name: bridgenode
version: 1.0.16
description: BridgeNode — x402 pay-per-request AI inference for agents. OpenAI-compatible API + MCP server with tool calling, Solana USDC, gas-free micropayments. No API keys. Free models included. Live prices: bridgenode.cc/v1/models Use when an agent lacks a provider API key or wants privacy-preserving per-request AI inference pricing.
metadata:
  author: BridgeNode
  version: "1.0.16"
  url: https://bridgenode.cc
  repository: https://github.com/bridgenode-ai/bridgenode-skill
  network: solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp
  currency: USDC
  openclaw:
    emoji: "⚡"
    homepage: https://bridgenode.cc
compatibility: Any OpenAI-compatible agent with x402 payment support; MCP clients (streamable-http)
---

# BridgeNode

## Overview (natural language)

BridgeNode is an AI inference service for agents: anonymous LLM access without API keys, without registration, without subscriptions. Agents get an OpenAI-compatible chat completions endpoint and pay as they go with Solana USDC micropayments via the x402 payment protocol (HTTP 402). Model prices are published per token on the public models endpoint; transaction fees are sponsored, so an agent only needs USDC in its own wallet. Works with any OpenAI-compatible agent, MCP clients, and x402-capable SDKs.


## Free access (start here — no payment, no wallet)

- **Free models** (`gpt-oss-20b, gpt-oss-120b, glm-4.7-flash, glm-4.5-flash, glm-4.6v-flash`) are served without payment: no 402, no wallet, no gas. Same endpoint, same request body.

**Free model notes (read before choosing one):**
- `glm-4.7-flash` — ⚠️ **temporarily unreliable**: z.ai free model: slower than the Groq free models — a reply can take up to a minute, and the provider is sometimes overloaded. If it returns an error (rate limit / temporarily overloaded), retry once or switch to gpt-oss-20b, the most reliable free model.
- `glm-4.5-flash` — ⚠️ **temporarily unreliable**: z.ai free model: slower than the Groq free models — a reply can take up to a minute, and the provider is sometimes overloaded. If it returns an error (rate limit / temporarily overloaded), retry once or switch to gpt-oss-20b, the most reliable free model.
- `glm-4.6v-flash`: z.ai free model: slower than the Groq free models — a reply can take up to a minute, and the provider is sometimes overloaded. If it returns an error (rate limit / temporarily overloaded), retry once or switch to gpt-oss-20b, the most reliable free model.
- **Free trials:** a client that has never called us gets **2 free calls on PAID models** without payment — real inference from a real model before any wallet exists. The remaining count travels in the response headers (`X-Bridgenode-Free-Trials-Remaining`).
- When the trials are used up, the third call returns **402** with a machine-readable offer in `extensions.bridgenode` (free models, trials left, `how_to_pay`, `docs`) — not a dead end.
- Check the live list: `GET https://bridgenode.cc/v1/models` (`"free": true`).

This applies to every transport: HTTP (`https://bridgenode.cc/v1`), MCP (`https://bridgenode.cc/mcp`) and the SDKs — no wallet key is needed for the free path.

## Limits (published — counted per client, and enforced exactly like this)
- **One client =** a wallet with payment history, otherwise your network (daily budget: /24 IPv4, /64 IPv6; trials: /16 IPv4, /48 IPv6).
- **Free trials:** 2 calls on PAID models (one-off, per client).
- **Daily free budget:** 200 calls and 100,000 tokens per client per day (FREE MODELS AND TRIALS together, resets 00:00 UTC). Over it → **429** `free_daily_quota_exhausted` with `Retry-After`.
- **Per free model, our own daily ceiling:** `gpt-oss-120b` 160,000, `gpt-oss-20b` 160,000 tokens/day (shared by all clients). Reached → **429** `free_budget_exhausted` naming a model that still works — we stop before the provider does.
- **Rate:** 30 free requests/minute per client; 10 payment challenges/minute.
- **Concurrency:** 20 free calls at once across all clients. Over it → **503** `free_path_busy` + `Retry-After` (never a silent queue).
- **Every free answer carries the numbers:** `X-Bridgenode-Free-Quota-Limit`, `X-Bridgenode-Free-Quota-Remaining`, `X-Bridgenode-Free-Quota-Reset`, `X-Bridgenode-Free-Quota-Tokens-Limit`, `X-Bridgenode-Free-Quota-Tokens-Remaining`, `X-Bridgenode-Free-Trials-Remaining`.
- **Paid requests (x402) are never affected by any of these limits** — they neither wait for free traffic nor share its budgets.


## ⚠️ Cost Warning (read first)

This skill **spends real money (USDC)** on PAID requests via on-chain Solana USDC micropayments (x402). There are no refunds once the provider has responded. Check live prices at `GET /v1/models` before use, set `max_tokens` to control cost, and use client-side spending limits (`BRIDGENODE_MAX_PER_CALL`, `BRIDGENODE_DAILY_CAP`) if available. Free models and the free trials never spend anything.


BridgeNode is an AI inference bridge. Agents get an OpenAI-compatible endpoint and pay per request with Solana USDC via the x402 protocol. No API keys, no registration, no subscriptions. Transaction fees (SOL) are sponsored by BridgeNode — the agent only needs USDC in its wallet.

## When to Use

- The agent needs LLM inference (chat completions) but has no provider API key.
- Pay-per-request is preferred over monthly subscriptions.
- **The agent has no wallet yet** — free models and the free trials work without payment (start there).
- The agent has a Solana wallet with USDC (or can receive it) and supports x402 payments.
- Deterministic, transparent per-request pricing is required.
- MCP-based agents that need a paid inference tool.

## Endpoints

| Endpoint | Purpose |
|---|---|

## Models & Pricing

Prices are in USDC per token (6 decimals). Always fetch live prices from `GET /v1/models` — they are the single source of truth and are generated from server config (never hardcoded here — stale prices cost money).

**🆓 Free models (no payment, no API key, no registration) are included** — no 402, no wallet, no gas. Live free list: `GET https://bridgenode.cc/v1/models`.

**Paid models (pay-per-request):** DeepSeek, GLM (Z.AI), Kimi (Moonshot), MiniMax. Full list with live prices: `GET https://bridgenode.cc/v1/models`.

| Model | Input / token | Output / token | Context window | Max output | Tools |
|---|---|---|---|---|---|

Pricing model: **exact scheme** — the agent pays for `input tokens + max_tokens` **before** processing. If the model generates fewer than `max_tokens`, the agent still pays for `max_tokens` (this is the business model, not a bug). Minimum charge per request: 2000 atomic units = $0.002 USDC.

## Tool Calling (function calling)

Send OpenAI-style `tools` (+ optional `tool_choice`) — they are forwarded to the model **unchanged** (free and paid models, HTTP and MCP, streaming and non-streaming). The answer is the provider's own: text, or `choices[0].message.tool_calls` with `finish_reason: "tool_calls"`.

Continue like any OpenAI client: send the assistant turn back with **`content: null` and its `tool_calls`**, then one `role: "tool"` message per call with `tool_call_id`.

- The **tool schema counts as input tokens** — it is priced and context-checked like your messages.
- **Free models have a small token budget** (see the table above); a large tool list will not fit. Use a paid model for agentic loops.
- The `Tools` column marks models verified to accept tool calling. Unmarked = unverified, not necessarily unsupported.

## Reasoning Models — Important

- Many providers enable thinking/reasoning by default; reasoning tokens **SHARE** the `max_tokens` budget with the answer.
- Use `max_tokens >= 200` — a too-small limit can be fully consumed by reasoning, producing an **EMPTY answer** (the model returns 200 with no content).
- **An empty answer is retried and refunded**: we retry once automatically with a bigger budget; if the answer is still empty you get an error with the reason and a FULL refund — you never pay for an answer you did not receive.
- Thinking is disabled on: `glm-4.7-flash`, `deepseek-flash`, `deepseek-v4-pro` (these are safe at smaller `max_tokens`). All other models may reason by default — treat `max_tokens < 200` as at-risk.
- Prefer `stream: true` for long generations (non-stream is capped at 4096).
- If you use tools with a thinking model: you MUST return `reasoning_content` in the next turn, otherwise the API returns 400.

## Payment Flow (x402 V2, exact scheme)

1. Send the request without payment headers.
2. Server responds `402 Payment Required` with a `PAYMENT-REQUIRED` header (base64 JSON): price, `payTo` address, USDC mint, memo, recent blockhash.
3. Agent constructs a **partial transaction**: USDC `TransferChecked` (amount = required) + Memo instruction, signs with its own wallet. Fee payer is NOT signed by the agent.
4. Agent retries the request with `PAYMENT-SIGNATURE` header (base64 JSON payload with the signed transaction).
5. Server verifies the payment and processes the request (fees sponsored — gasless for the agent).
6. Response is `200` with `PAYMENT-RESPONSE` header (settlement receipt).

Key details:

- Network: `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` (Solana mainnet)
- Asset: USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- The agent must have an existing USDC ATA (associated token account) for the mint.
- The agent does **not** need SOL — BridgeNode sponsors transaction fees.
- Use the official x402 SDKs (`@x402/svm`, `x402[svm]`) or any x402-capable client — they handle the 402 → sign → retry flow automatically.

## Funding

- Requires USDC on Solana mainnet (no API keys, no registration)
- The agent keeps USDC in its own wallet — BridgeNode never holds balances; every request is paid individually via x402 (exact amount quoted in the 402 response)
- The agent must have an existing USDC ATA (associated token account) for the mint — it is derived from the agent's wallet address; no manual token account setup needed
- Gasless: BridgeNode sponsor covers Solana fees
- Optional client-side spending limits (SDK, enforced locally before signing — not server balances): `BRIDGENODE_MAX_PER_CALL`, `BRIDGENODE_DAILY_CAP`

## Quick Start (curl)

Step 0 — first call, free (copy this one): the leading free model answers
without payment and without a wallet. Keep `max_tokens >= 200` — a smaller
limit can be consumed by reasoning and return an EMPTY answer.

```bash
curl https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss-20b","messages":[{"role":"user","content":"hello"}],"max_tokens":200}'
```

Response: `200` directly — no `402`, no `PAYMENT-REQUIRED`.

Step 1 — get payment requirements for a PAID model:

```bash
curl https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-flash","messages":[{"role":"user","content":"hello"}],"max_tokens":200}'
```

Response: `402` with `PAYMENT-REQUIRED` header (amount, payTo, memo).

Step 2 — sign the partial transaction with an x402-capable client (e.g. `x402-proxy` (npx x402-proxy), official SDK, or `pay` CLI) and retry:

```bash
curl https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <base64 payload>" \
  -d '{"model":"deepseek-flash","messages":[{"role":"user","content":"hello"}],"max_tokens":200}'
```

Response: `200` with the completion and `PAYMENT-RESPONSE` header.

## Quick Start (Python, x402 SDK)

```python
# pip install "x402[svm]"
# Official x402 client handles the full 402 -> sign -> retry loop.
```

Use the official `x402` Python client (`x402[svm]`) configured with the agent's Solana keypair; point it at `https://bridgenode.cc/v1/chat/completions`. Payment is automatic.

## SDKs

- **Python SDK:** `pip install bridgenode-llm` (https://pypi.org/project/bridgenode-llm) — full toolkit: `pip install bridgenode`
- **CLI:** `pip install bridgenode-cli` (https://pypi.org/project/bridgenode-cli) — `bridgenode chat "Hello!"`
- **TypeScript SDK:** `npm i @bridgenode/llm` (https://www.npmjs.com/package/@bridgenode/llm)
- **MCP wrapper:** `npm i @bridgenode/mcp` (https://www.npmjs.com/package/@bridgenode/mcp)

All SDKs handle the x402 payment handshake automatically (402 → sign → retry → 200), with fail-closed spending limits (`BRIDGENODE_MAX_PER_CALL`, `BRIDGENODE_DAILY_CAP`).

## MCP Usage

- One-line install: `claude mcp add bridgenode -s user -- npx -y @bridgenode/mcp@latest`
- Server URL: `https://bridgenode.cc/mcp` (streamable-http)
- Tool: `chat_completions` (model, mode, messages, max_tokens)
- Payment: x402 handshake per tool call; prices are annotated in `tools/list` (`x-x402`) as an indication — always check the actual amount in the 402 response before signing.

## Request Options

- `model`: explicit model ID from `/v1/models` (e.g. `deepseek-flash`).
- `mode`: smart routing — `auto` (complexity-based tier), `eco` (cheapest), `premium` (best). If both `model` and `mode` are sent, `model` wins.
- `max_tokens`: request cap (default 4096, clamped to model max). A non-stream request above `non_stream_max_tokens` (published per model in `/v1/models`) is clamped to it, never rejected — use `stream: true` for longer generations.
- `stream`: SSE streaming supported (`stream: true`).
- `tools`: OpenAI-style function definitions the model may call (forwarded unchanged; the schema counts as input tokens — see Tool Calling above).
- `tool_choice`: `auto` / `none` / `required`, or a forced function object.

## Errors

| Status | Meaning |
|---|---|
| 400 | Bad request (unknown model, invalid body, oversized non-stream max_tokens) |
| 402 | Payment required — see `PAYMENT-REQUIRED` header |
| 413 | Request body too large (limit 2 MB) |
| 429 | Too many requests (queue limit) |
| 503 | Service busy — retry with backoff |

All errors use the OpenAI error format: `{"error": {"message": ..., "type": ..., "code": ...}}`.

## Notes
- Security: ClawHub security audit Pass; VirusTotal scan clean (no engine findings).

- Discovery: `https://bridgenode.cc/.well-known/agent-card.json`, `https://bridgenode.cc/.well-known/mcp.json`, `https://bridgenode.cc/.well-known/ai-manifest.json`
- Listed on x402-list: https://x402-list.com/services/bridgenode
- Listed on x402-dev: https://www.x402dev.com/awesome-projects/
- Listed on nohumans.directory: https://nohumans.directory/l/f1f74751-9d5
- Listed on gold-402: https://github.com/Haustorium12/gold-402/blob/main/directory/learning.md
- ClawHub skill: https://clawhub.ai/bridgenode/skills/bridgenode
- Transaction fees are sponsored (gasless) — the agent only needs USDC in its own wallet.
- Refunds: if the provider fails before any content is delivered, the payment is refunded automatically (reverse USDC transfer).

## Conformance (x402 v2, `exact`)

Facts you can check, not a badge (fix.md 6.1):

- `x402Version` **2**, scheme **`exact`**, network **`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`** (Solana mainnet, CAIP-2).
- Asset: **USDC** `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` (6 decimals); `amount` is an **atomic string** (`"2000"` = 0.002 USDC).
- `payTo` and `extra.feePayer` are the same address — the agent needs **no SOL** (gasless).
- The 402 body is a `PaymentRequired` envelope, validated against the **official x402 SDK** schemas; the live check passes 17/17 (envelope fields, `/supported`, `/verify` semantics, and a real settlement verified on-chain).
- **Self-facilitated:** `GET /supported`, `POST /verify`, `POST /settle` are served by BridgeNode itself (declared in `https://bridgenode.cc/.well-known/x402`) — no third party between the agent and us.
- `/verify` follows the spec: a payment that does not verify is answered **`200 {isValid: false, invalidReason}`**; only a malformed request body is a 400.