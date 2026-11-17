---
name: agentindex-x402
description: >
  Pay-per-call AgentIndex tools on Base USDC (x402): multi-chain wallet/gas
  reads, live web search with
  full-page content, PDF-to-Markdown, web reading, structured extraction,
  weather, crypto, news and MCP discovery. Use when an agent needs current
  web or document data without an account or API key. Works with Hermes +
  PipRail, OpenClaw x402 skills, or any x402 client.
---

# AgentIndex x402

Cheap pay-per-call APIs for agents. **From $0.000001 USDC on Base**. No API key.

Base URL: `https://x402.agentindex.world`

## When to use

| Need | Call (GET unless noted) |
|------|-------------------------|
| Test a real mainnet x402 settlement | `/x402-echo?message=hello` — one atomic USDC ($0.000001) |
| Native + USDC wallet balances | `/wallet-balance?address=0x…&network=base` — $0.0001 |
| Live EVM gas and transfer cost | `/gas-price?network=base` — $0.0001 |
| Five-chain wallet + gas preflight in one call | `/wallet-intelligence?address=0x…` — $0.001 |
| Search the live web + read top 3 pages | `POST /search` body `{"query":"…","include_content":true}` — launch price $0.0001 |
| PDF to clean Markdown | `POST /pdf` body `{"url":"https://…pdf"}` — $0.002 |
| URL to clean Markdown | `POST /web-read` body `{"url":"https://…"}` — $0.002 |
| Web page to a JSON schema | `POST /extract` body `{"url":"https://…","schema":{…}}` — $0.003 |
| Weather for a city | `/weather?city=Paris` |
| BTC/ETH spot price | `/crypto?coins=btc,eth` |
| Tech headlines | `/news?limit=10` |
| Check wallet can afford $0.001 | `/can-pay?address=0x…&amount=0.001` |
| Is this URL an x402 paywall? | `/probe?url=https://…` |
| Find an MCP server by need | `POST /discover` body `{"q":"…"}` |

Free previews: append `/sample` (e.g. `/search/sample`, `/pdf/sample`).

## How to pay

1. Request the URL → HTTP **402** + payment requirements.
2. Sign exact USDC (x402 / EIP-3009) → retry with `Payment-Signature`.
3. **Hermes + PipRail:** `piprail_quote_payment(url)` then `piprail_pay_request(url)`.
4. **OpenClaw:** `x402_fetch` / `x402_pay` on the URL (or Bazaar search then pay).
5. **MCP:** connect to `https://x402.agentindex.world/mcp/` (tools `weather`, `crypto`, `news`, `can_pay`, `probe`, …).

## Discovery

- Catalog for agents: https://x402.agentindex.world/llms.txt
- OpenAPI: https://x402.agentindex.world/openapi.json
- Agent card: https://x402.agentindex.world/agent.json

## Rules

- Prefer the cheapest suitable route: $0.0001 for search and wallet/gas reads,
  $0.001 for weather/crypto/news, and $0.002 for PDF or web reading.
- Do not loop on unpaid 402s from scanners — if you have a funded wallet, pay once.
- Network must be Base mainnet USDC.
