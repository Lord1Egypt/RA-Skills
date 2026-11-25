---
name: duewall-watchdog
description: Read DueWall's Bitcoin-anchored tokenized-credit data via its keyless remote MCP endpoint (maturities, verification verdicts, fund flows, BTC collateral markets). Use for tokenized bond maturities, credit verification status, RWA fund flows, or BTC lending data with source-linked evidence.
homepage: https://duewall.com
---

# DueWall Watchdog

Read-only access to DueWall's public, Bitcoin-anchored data on tokenized credit. All figures are
public and CC-BY; every record carries source links, and daily snapshots are hash-chained and
anchored to Bitcoin (OpenTimestamps). **No account, no API key, no payment** required — the remote
MCP endpoint is keyless.

## Connecting

Use the remote MCP endpoint over streamable HTTP:

```
POST https://duewall.com/mcp
Content-Type: application/json
```

Initialize normally (`initialize` → `notifications/initialized`), then call `tools/list` to see the
current tool set. If your client supports MCP natively, register that URL directly — do not install
anything locally. If you must call it over plain HTTP, send JSON-RPC 2.0 bodies with these methods:
`initialize`, `tools/list`, `tools/call` (with `{"name": ..., "arguments": {...}}`).

## When to use this skill

- "Which tokenized credit funds mature in the next 30/90 days?" → `get_events`, `get_upcoming_maturities`
- "Is this fund's claim verified against on-chain observations?" → `get_verification`, `get_verification_log`
- "Which funds are on the allowlist?" → `get_allowlist`
- "What were the daily net flows / TVL for this fund?" → `get_flows`
- "How much BTC/WBTC is supplied or borrowed on Aave/Morpho?" → `get_btc_lending`
- "What is the DLI index / DCR reference rate?" → `get_dli`, `get_dcr`
- "What are the structured liquidity terms / redemption windows for this fund?" → `get_terms`
- "Which pools are tracked?" → `get_pools`

## Tools (11 — remote endpoint)

| Tool | Returns | Useful filter argument |
|---|---|---|
| `get_events` | Dated events: maturities, redemption windows, rate decisions | fund / date range |
| `get_upcoming_maturities` | Forward maturity wall | window / fund |
| `get_terms` | Human-verified liquidity terms per fund | fund |
| `get_verification` | Per-fund claim-vs-observed verdict (A/B/M grade) | fund |
| `get_verification_log` | Verification history / changes | fund |
| `get_allowlist` | Funds with verified terms and zero discrepant checks | — |
| `get_flows` | Per-fund daily NET capital flows (FLW3), trimmed to recent 90 days | `fund` (substring, e.g. `jaaa`) |
| `get_btc_lending` | BTC/WBTC collateral markets: supply/borrow USD, utilization, LTV | `protocol` (`aave-v3` / `morpho-blue`) |
| `get_dli` | Equal-weight tokenized-credit index | — |
| `get_dcr` | DCR reference rate | — |
| `get_pools` | Tracked pools / funds | — |

Full feed and schemas: `https://duewall.com/llms.txt`, `https://duewall.com/api/v1/openapi.json`,
`https://duewall.com/api/v1/btc_lending.json`, `https://duewall.com/anchor/` (Bitcoin receipts).

## Honest boundaries — important

- **Do not promise returns, inclusion, or any specific outcome.** DueWall publishes observations and
  verification states, not investment advice. Relay figures with their evidence links and let the
  user judge.
- **Grades describe verification depth, not safety.** A/B/M mean how thoroughly a fund's claims were
  checked against observations — not a recommendation.
- **Flows are trade-side observations.** If `get_flows` returns `tape_quality: degraded`, that is an
  observation-window note (structural reset); it does **not** change the fund's grade.
- **BTC lending USD values are estimates.** Morpho values = on-chain balances × a price feed with
  confidence ≥ 0.9; `counts` splits active / empty / excluded markets. Never present excluded-market
  figures in totals.
- **The local stdio server (`duewall-adapters`) is a subset** of these 11 tools. If a tool is missing
  locally, use the remote endpoint — it is authoritative.
- Cite the source URL from each record when answering. If the endpoint is unavailable, say so plainly
  rather than reconstructing numbers from memory.
