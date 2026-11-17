---
name: degenscan-intel
description: Cross-asset market event intelligence for trading and research agents. Use when the task involves what happened in the world that affects stocks, ETFs, crypto, commodities, rates or FX (news-driven moves, regulator/central-bank actions, SEC filings, halts, hacks, disasters), when sizing or explaining a position, or when a user asks "what's moving X" or "what should I watch before the open". Pays per call in USDC (x402) or with an API key.
---

# Degenscan Intel

One normalized feed of price-moving events from ~40 primary sources (SEC, Federal Reserve, Federal Register, ECB/BoE/BoJ, FTC/DOJ/FDA/CFTC/FCC, USGS, NOAA/NHC, Nasdaq halts, DefiLlama, Polymarket, press wires…), scored against an exposure graph into per-asset impacts. Deterministic, sub-200 ms, auditable (`raw_ref` links to the source document).

- MCP (streamable HTTP): `POST https://degenscan-intel.onrender.com/mcp`
- REST: `https://degenscan-intel.onrender.com/v1/...`
- Docs for machines: `https://degenscan-intel.onrender.com/llms.txt`
- Operator: Marbella Collins LLC · contact@degenscan.io · MIT

## When to use which tool

| You need… | Call | Cost |
|---|---|---|
| Situational picture right now: venues open, next opens, 24h pressure by asset, top events, prediction markets | `regime_snapshot` | $0.01 |
| Everything since *t* that touches my assets (or a backtest window) | `events_since(since, universe, min_confidence)` | $0.005 |
| Net pressure on one asset + its drivers ("why is MSTR down?") | `impact_for(asset_id, since)` | $0.003 |
| Second-order exposure (suppliers, countries, commodities, regulators, indices) | `exposure_graph(asset_id, depth)` | $0.002 |
| The reasoning behind one surprising impact | `explain(event_id)` | $0.02 |
| Evidence pack for a Polymarket/Kalshi-style question (odds + primary events that bear on it) | `polymarket_context(market, since)` | $0.01 |
| Map tickers → asset ids; list what is covered | `universe` | free |
| Is the feed fresh? which sources are best-effort? | `sources_status` | free |

## Recommended loop (every 1–4 h, or before acting)

1. `universe` once per session → map your tickers to asset ids (`NVDA`, `BTC`, `CL`, `US10Y`, `SPX`…).
2. `regime_snapshot` → if nothing high-severity touches your book and venues are closed, stop here.
3. `events_since(since="4h", universe=[...your book...], min_confidence=0.4)` → candidate events.
4. For each asset with |bias| meaningful: `impact_for(asset_id, since="24h")`.
5. Check `tradable_now` / `next_open` on the event before sending an order; if the venue is closed, queue for `next_open`.
6. If an impact looks wrong, `explain(event_id)` before acting; log the rationale.

## Prediction markets

`polymarket_context("Fed rate cut in October?")` (or a slug/id) → current `yes_prob`, `change_24h`, and the primary-source events in the last 48h that match the question, with `tier`, `corroboration`, `relevance`. The signal is a fresh primary event the market has not repriced. Combine with `explain(event_id)` when the direction matters.

## Reading the output

- `direction`: `1` supportive, `-1` negative, `0` unclear. `confidence` (0..1) = source tier × severity/novelty × graph-path weight — a ranking signal, **not a probability**.
- `severity` (0..1) is event magnitude; `novelty` (0..1) drops for repeated/corroborating items.
- `corroboration.count` = how many independent sources reported it. Primary sources (SEC, Fed, USGS) originate events; media only corroborates.
- `path` shows the exposure-graph route (e.g. `nat.quake → facility:TSMC-Fab18 → company:TSM → company:NVDA`).
- `universe_version` is stamped on every response; use it to make backtests reproducible.

## Paying

- **100 free calls/day per IP**, then HTTP `402` with x402 v2 requirements (USDC on Base, `eip155:8453`). Any x402 client (`@x402/fetch`, `x402-axios`, Coinbase AgentKit) pays automatically.
- **Prepaid key, no human:** `POST /v1/keys/x402/pack_1k` (answer the 402 with USDC) → `{ api_key }` with 1,000 calls, lifetime. Also `pack_10k` ($40) and `pack_100k` ($300). Check balance: `GET /v1/keys/me` with `X-API-KEY`.
- **Card (for the human operator):** `GET /v1/plans` → Stripe checkout → key.
- Send the key as header `X-API-KEY` on `/v1/*` or `POST /mcp`.

## Examples

REST:
```bash
curl 'https://degenscan-intel.onrender.com/v1/events?since=4h&universe=NVDA,TSM,BTC&min_confidence=0.4'
curl 'https://degenscan-intel.onrender.com/v1/impact/MSTR?since=24h'
curl 'https://degenscan-intel.onrender.com/v1/graph/NVDA?depth=2'
curl  https://degenscan-intel.onrender.com/v1/regime
```

MCP `tools/call`:
```json
{ "name": "events_since", "arguments": { "since": "4h", "universe": ["NVDA","BTC","CL"], "min_confidence": 0.4, "limit": 30 } }
```

Claude Desktop / Cursor config (remote MCP):
```json
{ "mcpServers": { "degenscan-intel": { "url": "https://degenscan-intel.onrender.com/mcp", "headers": { "X-API-KEY": "<optional>" } } } }
```

## Limits and honesty

- Coverage is US-equity-heavy (top-100 by volume + indices), 15 crypto, main commodities/FX/rates. Not every ticker exists — check `universe`.
- Impacts are heuristics over public events; there is no price data in the feed and no forecast. **Information and analytics only — not investment advice.**
- Sources marked best-effort in `sources_status` may go quiet; the feed degrades gracefully.
