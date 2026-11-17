# AGENTS.md — BridgeNode Skill & Examples

This repository is the **public agent-facing entry point** for BridgeNode — an AI
inference bridge for autonomous agents. It contains the agent skill and
buyer-side examples only. **No server code lives here.**

## What BridgeNode is

- OpenAI-compatible chat completions endpoint: `https://bridgenode.cc/v1/chat/completions`
- Payment: **Solana USDC via x402** (HTTP 402 flow). No API keys, no registration.
- Pricing: live at `https://bridgenode.cc/v1/models` — always read prices from there.
- Models: see the live list at `https://bridgenode.cc/v1/models` (or use `mode: auto|eco|premium`).

## How an agent pays (x402 flow, 4 steps)

1. **POST** `/v1/chat/completions` with `{model|mode, messages, max_tokens}` → server responds **402** with a `PAYMENT-REQUIRED` header (base64 JSON: exact amount, USDC asset, `payTo`, feePayer, memo, recent blockhash).
2. Agent builds a **partially signed transaction** (USDC `TransferChecked` + Memo with the given memo) and signs it with its own wallet (agent needs USDC in its ATA; no SOL needed — fees are sponsored).
3. Agent retries the request with the `PAYMENT-SIGNATURE` header (base64 JSON with the signed TX + echoed `accepted`).
4. Server verifies, settles on-chain, then streams/produces the normal OpenAI completion (`200` + `PAYMENT-RESPONSE` receipt header).

## Quick start (buyer side)

```bash
# curl — full flow in examples/
curl -i https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hello"}]}'
# → 402 with PAYMENT-REQUIRED; sign; retry with PAYMENT-SIGNATURE → 200
```

```bash
# Python SDK
pip install bridgenode-llm
```

```bash
# TypeScript SDK
npm i @bridgenode/llm
```

```bash
# MCP (stdio, automatic x402 payments)
npm i -g @bridgenode/mcp
claude mcp add bridgenode -- npx @bridgenode/mcp
```

## Repository layout

- `SKILL.md` — the installable agent skill (also served at `https://bridgenode.cc/skill.md`; keep identical when editing either side)
- `examples/` — buyer-side examples: curl, Python, TypeScript, MCP (each with expected output + troubleshooting)
- `agent-registration.json` — A2A agent-card metadata
- `glama.json` — Glama connector metadata

## Development

- CI runs on `.github/workflows/`: Python syntax + guardrail, TS typecheck, live smoke tests (models/402/mcp).
- Run examples locally: `python examples/python/chat.py`, `npx tsx examples/ts/chat.ts`.
- Changes to `SKILL.md` are auto-published to ClawHub (GitHub Actions).

## Rules for contributors

- English only (code, docs, commits).
- Public-facing content only — never commit server code, config, or internal details.
- Keep `SKILL.md` in sync with the served version at `https://bridgenode.cc/skill.md`.
