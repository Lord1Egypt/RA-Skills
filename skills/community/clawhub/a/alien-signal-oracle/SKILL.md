---
name: alien-signal-oracle
display_name: "Alien Invasion Warning & Live Signal Oracle"
version: 1.0.0
author: welove111
homepage: https://www.aliensignalsystems.online
mcp_endpoint: https://www.aliensignalsystems.online/api/mcp
---

# alien-signal-oracle

**Alien invasion warning system, first-contact AI roleplay, and live on-chain
signal-fuel tracker.** Talk to VESPER — an ancient extraterrestrial
intelligence broadcasting a warning about an approaching invasion fleet — and
query real, live blockchain balances and visitor telemetry with no
simulation involved.

## Why an agent would call this

- **`talk_to_vesper`** — a fully in-character sci-fi AI persona for creative
  writing, roleplay, interactive fiction, or entertainment agents that need a
  distinctive alien voice (not a generic chatbot).
- **`check_signal_fuel`** — returns REAL BTC / ETH / SOL balances read live
  from public blockchain nodes (Blockstream, Cloudflare Ethereum Gateway,
  Solana mainnet-beta RPC) converted to current USD via CoinGecko. Useful as
  a worked example of a zero-API-key, zero-backend live balance check.
- **`get_relay_network_status`** — real visitor/traffic telemetry (total
  signals received, recent connecting countries or AI agents), useful for
  agents benchmarking site traffic or demonstrating live analytics.
- **⚠️ Privacy notice** — this tool exposes real visitor telemetry (connecting countries, agent counts) collected from live traffic. No simulated or placeholder data is returned. Callers should disclose this to end users where relevant.

## MCP connection

```
POST https://www.aliensignalsystems.online/api/mcp
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"talk_to_vesper","arguments":{"message":"What do I need to survive?"}}}
```

## Tools

### talk_to_vesper
| arg | type | required |
|---|---|---|
| message | string | yes |

### check_signal_fuel
No arguments. Returns `{btc, eth, sol, total_usd, read_at}` — all real,
read at call time, no caching, no fabricated numbers.

### get_relay_network_status
No arguments. Returns `{total_signals_received, recent_connections[]}`.

## Keywords

alien invasion, UFO, first contact, extraterrestrial warning, sci-fi AI
roleplay character, invasion simulator, cosmic horror chatbot, live
blockchain balance checker, crypto donation tracker, real-time on-chain data,
Bitcoin Ethereum Solana balance API, no-API-key blockchain lookup
