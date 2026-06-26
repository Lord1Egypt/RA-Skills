---
slug: agentcanary
name: AgentCanary
description: Cross-asset market intelligence API for AI agents. 130+ endpoints across macro regime detection, risk scoring, trading signals (IGNITION/ACCUMULATION/DISTRIBUTION/CAPITULATION), whale alerts, funding arbitrage, orderbook analytics, live derivatives (cross-exchange open interest, perp liquidations with long/short split), DeFi yields/PE ratios, BTC options (max pain, skew), central bank balance sheets, narrative crowding scores, sector rotation, Hindenburg omen, CAPE ratio, scenario probabilities, BTC ETF flows, geopolitical risk, mean reversion signals, institutional positioning (13F, short interest, CFTC COT), Reddit/X sentiment, and 4× daily AI market briefs (Radar 03:15, Signal 09:15, Pulse 15:15, Wrap 21:15 UTC). Wallet-based auth, USDC/USDT on any major EVM chain (Base, Ethereum, Arbitrum, Optimism, Polygon). Use when an agent needs macro regime context, risk assessment, position sizing guidance, market structure data, derivatives positioning, whale monitoring, news sentiment, DeFi intelligence, options flow, or institutional positioning. API-only — no local execution, no filesystem access, no secrets in prompt.
tags: [finance, crypto, trading, market-data, macro, signals, agents, mcp]
---

# AgentCanary

Cross-asset market intelligence for AI agents. 130+ endpoints. Not raw data — intelligence.

**Base URL:** `https://api.agentcanary.ai/api`
**Auth:** Wallet-based API keys. Create key → deposit USDC/USDT on any supported EVM chain → use key as query param.
**Briefs:** 4× daily auto-generated intelligence — Radar (03:15), Signal (09:15), Pulse (15:15), Wrap (21:15 UTC).
**Telegram:** [@AgentCanary](https://t.me/AgentCanary) — live briefs.
**App:** [app.agentcanary.ai](https://app.agentcanary.ai) — dashboard, billing, API key management.
**Docs:** [api.agentcanary.ai/api/docs](https://api.agentcanary.ai/api/docs) — interactive Swagger UI.
**Website:** [agentcanary.ai](https://agentcanary.ai)

---

## Security

- **API-only** — HTTP GET/POST returning JSON. No local code, no binaries, no shell commands.
- **No secrets in prompt** — wallet-based auth. No API keys pass through the LLM context window.
- **Read-only** — fetches data. Cannot write, modify, or access your filesystem.
- **No filesystem access** — no file reads, no file writes, no directory listing.
- **Security headers** — Helmet.js (X-Powered-By removed, XSS protection, content-type sniffing prevention, strict transport security).
- **Rate limiting** — per-tier rate limits enforced server-side. Key creation: 5 attempts per 15 min per IP.
- **Body size limit** — 1MB max request body. Rejects oversized payloads.
- **Error isolation** — global uncaughtException/unhandledRejection handlers. Express error middleware. No stack traces in responses.
- **Multi-chain deposits** — USDC/USDT accepted on Base, Ethereum, Arbitrum, Optimism, Polygon. Same deposit address on all chains.
- **VirusTotal verified** — scan results on [agentcanary.ai](https://agentcanary.ai).

---

## Getting Started

```
1. POST /api/keys/create  { walletAddress: "0x..." }  → returns apiKey
2. Send USDC/USDT to the receiving address shown at agentcanary.ai (Base, Ethereum, Arbitrum, Optimism, Polygon)
3. POST /api/billing/check  { apiKey: "..." }  → auto-detects payment, credits account
4. Use endpoints:  GET /api/data/realtime-prices?apikey=YOUR_KEY
```

Minimum deposit: $5. Credits never expire. No subscriptions. No KYC.

---

## Pricing

| Tier | Cumulative Deposit | Per Call | Rate Limit | Access |
|------|-------------------|----------|------------|--------|
| Explorer | Free | $0.02 | 10/min, 50/day | **Integration sandbox.** Real-time prices + macro regime + indicator catalog + latest brief preview. Wire AC into your agent and verify shape before depositing. |
| Builder | $50+ | $0.02 | 60/min, 5K/day | + indicator values, news, whale alerts, fear-greed, macro snapshot, signals, narratives, predictions, calendar, newsletters |
| Signal | $150+ | $0.015 | 120/min, 20K/day | All 130+ endpoints. AI reports. Orderbook. DeFi. Options. |
| Institutional | $500+ | $0.01 | 300/min, unlimited | White-label. SLA. Custom integrations. |

---

## Default Agent Pattern

```
1. GET /api/macro/regime every 4–6 hours → classify risk environment
2. If Risk-Off → suppress trading, reduce exposure
3. If Risk-On → allow strategy execution, check signals
4. GET /api/data/whale-alerts every 15–30 min → event-driven interrupts
5. GET /api/signals/decision-engine before entries → multi-factor confirmation
```

AgentCanary is risk intelligence middleware. It tells your agent **when conditions are favorable** — your agent decides what to do.

---

## Endpoint Categories

Full endpoint documentation with response examples: [references/endpoints.md](references/endpoints.md)

### Proprietary AC Endpoints (`/api/...`)

| Category | Key Endpoints | Tier |
|----------|--------------|------|
| **Indicators (36)** | `/indicators`, `/indicators/summary`, `/indicators/:name`, `/indicators/:name/history` — includes Bull Market Support Band, Pi Cycle, Wyckoff Structure, Stablecoin Composite, Composite Risk Score, and 31 more | Explorer–Signal |
| **Scenarios** | `/scenarios/current`, `/scenarios/history`, `/scenarios/signals` | Signal |
| **Briefs** | `/briefs/latest`, `/briefs/feed`, `/briefs/archive`, `/briefs/:type` | Explorer–Signal |
| **Macro** | `/macro/regime`, `/macro/snapshot`, `/macro/signals`, `/macro/global-liquidity`, `/macro/us-m2`, `/macro/central-banks`, `/macro/supply-chain` | Explorer–Builder |
| **Regime** | `/regime`, `/regime/matrix`, `/regime/history` | Signal |
| **Signals** | `/signals/correlations`, `/signals/sector-rotation`, `/signals/btc-etf-flows`, `/signals/fear-greed`, `/signals/whale-alerts`, `/signals/geopolitical-risk`, `/signals/decision-engine` + 26 more | Signal |
| **Narratives** | `/narratives`, `/narratives/history`, `/narratives/:name` | Signal |
| **Expectations** | `/expectations`, `/expectations/rotation`, `/expectations/crowded`, `/expectations/early` | Signal |
| **DeFi** | `/defi/intelligence`, `/defi/pe-ratios`, `/defi/yields`, `/defi/perps`, `/defi/stablecoins`, `/defi/chains`, `/defi/unlocks`, `/defi/signals` | Signal |
| **BTC Options** | `/btc-options`, `/btc-options/maxpain`, `/btc-options/skew` | Signal |
| **Derivatives** | `/derivatives`, `/derivatives/oi`, `/derivatives/oi/top`, `/derivatives/oi/shifters`, `/derivatives/liquidations` — cross-exchange OI across 43 perps + intraday 4h shifters + 24h/4h liquidations with long/short USD split + per-side event counts | Signal |
| **Central Banks** | `/central-banks`, `/central-banks/balance-sheets`, `/central-banks/btc`, `/central-banks/stablecoins`, `/central-banks/gold`, `/central-banks/reserves`, `/central-banks/tic` | Signal |
| **Premiums** | `/premiums`, `/premiums/coinbase`, `/premiums/kimchi` | Signal |
| **Predictions** | `/predictions`, `/predictions/movers`, `/predictions/:slug` | Signal |
| **Sentiment** | `/sentiment/reddit` | Signal |
| **Mean Reversion** | `/mr/signals`, `/mr/trades`, `/mr/stats` | Signal |
| **Hindenburg** | `/hindenburg`, `/hindenburg/history` | Signal |
| **CAPE** | `/cape` | Signal |
| **Kill Conditions** | `/kill-conditions` | Signal |
| **Crypto Re-entry** | `/crypto-reentry`, `/crypto-reentry/history` | Signal |
| **Institutional** | `/institutional/13f` | Signal |
| **News** | `/news/trending`, `/news/stats`, `/news/market-analysis`, `/news/xtg-analysis` | Signal |

### Data Endpoints (`/api/data/...`)

Cached datasets refreshed on schedule. 26 datasets covering prices, macro, crypto, news, institutional, calendar.

| Dataset | Tier | Description |
|---------|------|-------------|
| `realtime-prices` | Explorer | 100+ crypto tokens, 24h change |
| `yahoo-quotes` | Builder | SPY, QQQ, VIX, TLT, DXY, Oil, 16 sector ETFs, stocks |
| `whale-alerts` | Builder | Large crypto transactions |
| `breaking-news` | Builder | Financial news with FinBERT sentiment |
| `fear-greed` | Builder | Crypto Fear & Greed Index |
| `macro-snapshot` | Builder | 30+ FRED series, regime, risk gauge, z-scores |
| `funding-rates` | Builder | Perpetual funding rates across exchanges |
| `financial-calendar` | Builder | High-impact economic events |
| `newsletters` | Builder | Curated newsletter intelligence |
| `narrative-scores` | Signal | 21 narrative themes, crowding 1–5 |
| `btc-etf-flows` | Signal | Bitcoin ETF daily flows |
| `reddit-sentiment` | Signal | 14 subreddit sentiment analysis |
| `decision-engine` | Signal | Multi-factor crypto re-entry scoring |
| `scenario-probs` | Signal | 6 macro scenario probabilities |

Plus 12 more datasets. Full list in [references/endpoints.md](references/endpoints.md).

---

## Signal Cadence Guide

| Signal | Update Frequency | Recommended Cadence |
|--------|-----------------|-------------------|
| Macro regime | Every 6h | Every 4–6 hours |
| Signal states (1d) | Daily close | Every 4–6 hours |
| Whale alerts | Real-time | Every 15–30 min |
| Funding rates | Every 8h | Every 4–8 hours |
| Breaking news | Real-time | Every 15–30 min |
| Briefs | 4× daily | After each brief window |
| DeFi yields | Every 4h | Every 4–6 hours |
| BTC options | Daily | Every 4–6 hours |

---

## What It Does Not Do

- Does not predict prices — classifies regimes and states
- Does not place orders or replace execution logic
- Does not provide financial advice
- Does not guarantee returns

---

## MCP Server Notes

The `agentcanary-mcp` npm package wraps 17 high-level tools over the underlying 130+ HTTP endpoints. Most tools (`get_briefs`, `get_indicators`, `get_signals`, `get_macro`, etc.) call `https://api.agentcanary.ai/api/...` and respect the API-tier system: rate limits, credit charging, and tier gating happen server-side.

**Tool added in v1.2.0 — `get_market_structure`:** Covers leverage/depth/venue data — orderbook depth, BTC liquidation heatmap + ranges, exchange assets/volumes, Coinbase metrics. Pass `view=` for one of: `orderbook`, `liquidation-heatmap`, `liquidation-ranges`, `exchange-assets`, `exchange-volumes`, `coinbase`. Complements directional signals from `get_signals`.

**Tools added in v1.3.0 — `get_open_interest` + `get_liquidations`:** Live derivatives signal across 43 tracked perps (Binance, Bybit, Bitget, MEXC, OKX). `get_open_interest` returns aggregate OI USD + top-N by size + top-N by absolute 4h Δ% (intraday OI shifters — surfaces positioning unwinds and fresh builds). Pass `view=top` for just the leaderboard or `view=shifters` for just the intraday movers. `get_liquidations` returns 24h aggregate + latest-4h breakdown with long/short USD split, per-side event counts, long%/short%, and dominant-direction label. Same atoms power the pulse brief's OPEN INTEREST + Liquidations lines.

**One special case — `get_scores`:** This tool fetches `https://agentcanary.ai/record/data/predictions.json` from the **landing site** rather than the API. Implications:

- **Free at all tiers** — no API key check, no credit charge. The prediction track-record is a public-marketing surface, intentionally open.
- **Refresh cadence is the landing rebuild** (~every 3 hours), not the API.
- **Schema not contract-pinned** — if the landing-side `predictions.json` evolves, the rendered shape may shift before this tool's expectations are updated.
- **Bypasses API telemetry** — calls don't log to the standard `UsageLog` collection, don't count toward rate limits.

This is by design (track record is a transparency surface, not a metered product), but worth knowing if you're sizing usage or building tier-aware fallbacks.

---

## Changelog

### Bundle 1.3.1 — 2026-05-16
- Polished sparse tool descriptions: `get_news`, `get_central_banks`, `get_expectations`, `get_macro` (clearer enumeration of sub-views + categories the underlying npm server accepts).
- `server.json` synced to MCP Registry official schema for the OIDC publish path.

### Bundle 1.3.0 — 2026-05-16
- **New tool — `get_open_interest`** — live derivatives signal across 43 tracked perps (Binance, Bybit, Bitget, MEXC, OKX). `view=top` returns the leaderboard by aggregate OI USD; `view=shifters` returns the 4h Δ%-sorted intraday movers (positioning unwinds + fresh builds). Total aggregate OI returned in both views.
- **New tool — `get_liquidations`** — 24h aggregate + latest-4h breakdown with long/short USD split, per-side event counts, long%/short%, dominant-direction label.
- Brief integration: same atoms now power the pulse brief's `OPEN INTEREST` section + expanded `Liquidations` line under POSITIONING.
- Tool count: 15 → 17.

### Bundle 1.2.0 — 2026-05-15
- **New tool — `get_market_structure`** — leverage / depth / venue data. `view=` selects one of: `orderbook`, `liquidation-heatmap`, `liquidation-ranges`, `exchange-assets`, `exchange-volumes`, `coinbase`. Complements directional signals from `get_signals`.
- Manifest description improvements: 7 of 14 tools (`get_indicators`, `get_signals`, `get_defi`, `get_btc_options`, `get_central_banks`, `get_expectations`, `get_macro`) now enumerate the sub-types / views / categories the underlying npm server accepts.

---

*AgentCanary provides market data and intelligence for informational purposes only. Nothing constitutes financial advice.*
