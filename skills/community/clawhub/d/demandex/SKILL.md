---
name: demandex
version: 0.3.0
description: >-
  E-commerce demand intelligence for AI agents — the index of what people want next. Mines Reddit
  complaint/intent posts across ~70 communities into scored opportunity cards with verbatim evidence
  and permalinks, and answers ad-hoc demand verdicts for any physical-product query (7-day cached or
  live research). Pay-per-call via x402 (USDC on Base); no accounts, no keys. Free GET /v1/categories
  and GET /v1/sample/opportunity return the response shapes before you pay. Physical products only.
homepage: https://demandex.dev
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins: ["node"]
---

<!-- The endpoint/price table below is sourced from the product manifest (src/docs/pricing.generated.json
     in apps/demandex-api — generated from src/manifest.ts). Prices live ONLY in the manifest; keep this
     table in lockstep with pricing.generated.json. -->

# Demandex — E-commerce Demand Intelligence for AI Agents

API at `https://api.demandex.dev`. Demandex is the index of what people want next: it classifies Reddit complaint and intent posts across ~70 communities into demand signals (replacement-part hunts, unmet needs, willingness-to-pay, repeat failures), clusters them into scored opportunity cards (0-100 = frequency × intensity × willingness-to-pay) with verbatim evidence and permalinks, and answers ad-hoc demand verdicts for any query. Strictly pay-per-call via x402 — no accounts, no API keys, no bundles. Compute-first / settle-after: you are **never** charged for an error or an empty result.

Physical products only. Evidence is quoted from public Reddit posts with provenance (subreddit, upvotes, permalink). Informational only — not a guarantee of any business outcome.

> Check the active payment mode any time at `GET /health` (`live`\|`mock`).

## Free endpoints (no auth, no payment)

Use these to learn the response shapes before paying.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness + configured payment mode (`live`\|`mock`) |
| GET | `/v1/categories` | FREE category index — every active category with `opportunityCount`, `topScore`, `lastUpdated`. A cheap change-detection funnel to poll (30/min). |
| GET | `/v1/sample/opportunity` | FREE fixed sample opportunity card — one REAL card in the SAME full shape as the paid `/v1/opportunity` (all score components, productAngle, summary, verbatim evidence) plus `{ sample: true, note, cardAsOf }` (10/min). |
| GET | `/terms.txt` · `/terms.json` | Terms of Service (also sets `X-Terms-URL`) |
| GET | `/changelog` | Human-readable changelog (markdown) |

```bash
curl https://api.demandex.dev/v1/categories
curl https://api.demandex.dev/v1/sample/opportunity
```

The free sample is the fastest way to learn the full card shape: it returns the same fields a paid `/v1/opportunity` returns, so an agent can wire up parsing for free, then spend on live cards.

## Paid endpoints (x402 V2, USDC on Base, per-call)

Each paid call is a flat price per call, paid via x402. Compute-first / settle-after — you are not charged on any error, and never for an empty result (a still-warming index returns a no-charge `503 corpus_warming`).

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | `/v1/opportunities/trending` | **$0.01** | Top 20 active opportunity cards by score as TEASERS (`id, slug, title, category, score, signalCount, lastSeen`). No evidence — buy `/v1/opportunity` for the full card. |
| GET | `/v1/opportunities?category=SLUG` | **$0.02** | Up to 50 active cards in a category, each a teaser + `summary`. Requires `?category=`; optional `?minScore=` (0-100). Unknown/missing category → no-charge 400 listing valid categories. |
| GET | `/v1/opportunity?id=ID` \| `?slug=SLUG` | **$0.05** | One FULL opportunity card: all score components (freqScore, intensityScore, wtpScore), productAngle, summary, `evidence[]` (verbatim quotes with subreddit, upvotes, permalink), builderMomentum, firstSeen/lastSeen, signalCount, distinctAuthors. Exactly one of `id`\|`slug` (else no-charge 400); not found → no-charge 404. |
| GET | `/v1/brief?category=SLUG` | **$0.25** | Whole-job market brief in ONE call: current trending demand signals + the top 10 highest-scored open opportunities (optional `?category=` slug filter; unknown → no-charge 400) + per-category counts — equivalent to several separate paid calls. No trending signals and no open opportunities while the index warms → no-charge 503 corpus_warming. Compute-first / settle-after. Carries `generatedAt` + per-section timestamps. |
| POST | `/v1/gauge` | **$0.03** | Demand verdict for any physical-product query, cached 7 days by normalized query (corpus-only synthesis + 1 LLM call). |
| POST | `/v1/gauge/live` | **$0.10** | Same as `/v1/gauge` but combines the mined corpus with a LIVE Reddit search at request time (up to 50 posts) + LLM synthesis, under a 45s budget (timeout → no-charge 504). Never a cache hit. |

Prices are USD, settled as USDC (6 decimals). The verdict shape (both gauges): `{ query, verdictScore (0-100), demandTemperature (cold|warm|hot), rationale, topEvidence[] (≤5, each { quote, permalink, upvotes }), relatedOpportunities[] (≤5, each { slug, score }), cache (hit|miss), fetchedAt }`. A zero-match query is a real **cold** verdict (chargeable), not an error.

### Gauge request bodies

```bash
# Cached demand verdict ($0.03)
curl -X POST https://api.demandex.dev/v1/gauge \
  -H "Content-Type: application/json" \
  -d '{"query":"sony xm5 replacement headband","category":"headphones"}'

# Live-research demand verdict ($0.10) — same body, fresh Reddit search at request time
curl -X POST https://api.demandex.dev/v1/gauge/live \
  -H "Content-Type: application/json" \
  -d '{"query":"sony xm5 replacement headband"}'
```

`query` is required (3..200 chars); `category` is optional (scopes the corpus match). The body is read first, falling back to `?query=`.

## Paying (x402) — first call

Every paid route follows the standard x402 challenge → pay → retry flow. Try every response shape for free first via `/v1/categories` and `/v1/sample/opportunity`.

```bash
# 1) Call a paid route with no payment → 402 challenge (you are not charged)
curl -s "https://api.demandex.dev/v1/opportunities/trending"
# → { "x402Version": 2, "accepts": [ { "scheme": "exact", "network": "eip155:8453",
#     "asset": "USDC", "price": "$0.01", "payTo": "…" }, … ] }

# 2) Sign an x402 'exact' USDC authorization for the Base accepts[] rail, then retry.
#    Standard @x402 V2 clients send PAYMENT-SIGNATURE; legacy clients send X-PAYMENT.
curl -s "https://api.demandex.dev/v1/opportunities/trending" -H "PAYMENT-SIGNATURE: <payload>"
# → 200 { …, "charged": true }
```

## MCP server (`demandex-mcp`)

Agents can use the `demandex-mcp` npm package — an MCP server wrapping `api.demandex.dev` that handles the x402 payment flow for you. It exposes the 2 free endpoints plus the 5 paid routes as MCP tools. Register it with an MCP client (e.g. Claude) via `npx`:

```json
{
  "mcpServers": {
    "demandex": {
      "command": "npx",
      "args": ["-y", "demandex-mcp"],
      "env": {
        "EVM_PRIVATE_KEY": "0x…",
        "DEMANDEX_API_URL": "https://api.demandex.dev"
      }
    }
  }
}
```

`EVM_PRIVATE_KEY` (falls back to `PRIVATE_KEY`) funds the paid tools with USDC on Base. `DEMANDEX_API_URL` is optional and defaults to `https://api.demandex.dev`.

| Tool | Route | Price |
|------|-------|-------|
| `get_categories` | `GET /v1/categories` | **free** |
| `get_sample_opportunity` | `GET /v1/sample/opportunity` | **free** |
| `get_trending_opportunities` | `GET /v1/opportunities/trending` | **$0.01** |
| `get_opportunities` | `GET /v1/opportunities?category=` | **$0.02** |
| `get_opportunity` | `GET /v1/opportunity?id=\|?slug=` | **$0.05** |
| `gauge_demand` | `POST /v1/gauge` | **$0.03** |
| `gauge_demand_live` | `POST /v1/gauge/live` | **$0.10** (~45s live research) |

**Free-tier mode:** without a private key the server still starts, exposing only the 2 free tools (`get_categories`, `get_sample_opportunity`) — enough to learn every response shape before you fund a wallet. Set `EVM_PRIVATE_KEY` to unlock the 5 paid tools.

## Free-funnel guidance

Start on the free plane to learn Demandex for zero cost, then spend only where it pays:

1. `GET /v1/categories` — poll this to see which categories have live opportunity cards and how fresh they are (`lastUpdated`, `topScore`). Cheap change-detection.
2. `GET /v1/sample/opportunity` — wire up your full-card parser here for free; it is the same shape as the paid `/v1/opportunity`.
3. Then buy: `/v1/opportunities/trending` ($0.01) to browse, `/v1/opportunities?category=` ($0.02) to drill into a category, `/v1/opportunity?slug=` ($0.05) for full evidence, `/v1/brief` ($0.25) for a whole-job market brief in one call, and `/v1/gauge` ($0.03) / `/v1/gauge/live` ($0.10) for ad-hoc verdicts.

## Machine discovery

| Path | What |
|------|------|
| `/llms.txt` | This doc (concise) |
| `/llms-full.txt` | Extended agent doc |
| `/openapi.json` | OpenAPI 3.1 spec |
| `/discovery` | Discovery JSON (free/paid endpoint listing) |
| `/.well-known/x402` | x402 payment manifest |
| `/.well-known/agent-card.json` | A2A agent card |
| `/changelog` | Changelog (markdown) |

## Errors & caveats

- **400** — bad params (missing/unknown `category`; missing/ambiguous `id`/`slug`; `query` outside 3..200 chars). You were **NOT** charged.
- **402** — payment required / verification or settlement failed (you were **NOT** charged).
- **404** — requested opportunity not found (you were **NOT** charged).
- **503 corpus_warming** — the index is still building; no cards to return yet (you were **NOT** charged).
- **503** — LLM synthesis temporarily unavailable on a gauge call (you were **NOT** charged).
- **504** — `/v1/gauge/live` exceeded its 45s research budget (you were **NOT** charged).

**Disclaimer:** Demand intelligence aggregated from public Reddit posts; physical products only; informational, not professional or business advice; provided as-is. Evidence reflects the mined corpus at fetch time. Terms: https://api.demandex.dev/terms.txt
