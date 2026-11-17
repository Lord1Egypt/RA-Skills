---
name: connskill-growth
description: Buy market data and real-world actions per call with USDC (x402, no signup, no API key) from agent.connskill.com - keyword volume by location, Google SERP snapshots with AI-overview and PAA blocks, site audits with a real crawl, backlinks, competitors, SMS verification numbers, receive-only inboxes, GDPR-compliant LLM chat hosted in Germany, and a trust check for other x402 sellers. Use when an agent needs SEO or SERP data, a phone number or inbox for a verification, EU-hosted inference, or wants to vet an x402 seller before paying it.
license: MIT
compatibility: Node 18+. Free endpoints need nothing. Paid endpoints need a Base wallet holding USDC (X402_WALLET_KEY) - use a dedicated, small wallet.
metadata:
  openclaw:
    primaryEnv: X402_WALLET_KEY
    requires:
      bins: ["node"]
    envVars:
      - name: X402_WALLET_KEY
        required: false
        description: Private key (0x...) of a Base wallet holding USDC. Optional - without it only free endpoints work.
      - name: X402_MAX_USD
        required: false
        description: Hard cap per paid call in USD (default 1.00).
    install:
      - id: node
        kind: node
        package: "@connskill/mcp-growth-services"
        bins: ["connskill-growth-mcp"]
        label: MCP server (optional, same tools as this skill)
  hermes:
    tags: [seo, serp, x402, usdc, sms, email, llm, gdpr, trust]
    homepage: https://agent.connskill.com
---

# CONNSKILL Growth Services (x402)

One origin, 57 endpoints, one price each, paid per call in USDC on Base via the
x402 protocol. No account, no API key. The first request returns HTTP 402 with the
price; the client pays and retries. Prices and the full catalogue are always live:

- `https://agent.connskill.com/openapi.json` - schemas, prices, `info.x-guidance`
- `https://agent.connskill.com/.well-known/x402` - every paid endpoint with its price
- `https://agent.connskill.com/llms.txt` - short human/agent readme

## Two ways to call

**Preferred: the MCP server** (tools generated live from the spec, pays for you):
`npx -y @connskill/mcp-growth-services` with env `X402_WALLET_KEY` and `X402_MAX_USD`.

**Without MCP: the bundled script** (same payment path, prints JSON):

```bash
node scripts/x402-call.mjs prices                                   # free: catalogue with prices
node scripts/x402-call.mjs GET  /v1/locations '{"q":"germany"}'     # free
node scripts/x402-call.mjs POST /v1/keyword-ideas '{"keyword":"agent commerce","location":"Germany"}'
```

For paid calls the script needs `npm i x402-fetch viem` once and `X402_WALLET_KEY`
set. Keep `X402_MAX_USD` at or below what a single call may cost (most are 0.03-0.20).

## What to call for what

| Need | Endpoint | Price |
|---|---|---|
| Keyword ideas around a seed | `POST /v1/keyword-ideas {keyword, location?}` | 0.03 |
| Volume/CPC for up to 1000 keywords | `POST /v1/keyword-metrics {keywords[], location?}` | 0.15 |
| Same keywords across up to 30 locations, one payment | `POST /v1/keyword-metrics-multi {keywords[], locations[]}` | 0.15 x locations |
| Google SERP snapshot incl. AI overview, PAA, featured snippet | `POST /v1/serp-report {keyword, location?, depth?}` | 0.10-0.50 |
| Site audit: traffic, ranked keywords, competitors, backlinks, real on-page crawl | `POST /v1/site-audit {target}` | 1.00 |
| Backlinks / competitors / domain rank / traffic estimate | `POST /v1/backlinks-report`, `/v1/competitors`, `/v1/domain-rank`, `/v1/traffic-estimate` | 0.08-0.20 |
| Vet another x402 seller (live 402, USDC inflow, self-dealing share) | `POST /v1/trust-check {origin}` | 0.05 |
| Phone number for an SMS verification (quote first, free) | `GET /sms/v1/sms-quote?service=...` then `POST /sms/v1/sms-order` | 0.25-3.00 |
| Receive-only inbox for 7 days | `POST /mail/v1/mail-inbox` then `POST /mail/v1/mail-messages` (free) | 0.50 |
| GDPR-compliant chat completion hosted in Germany (tool use supported) | `POST /ai/v1/eu-chat {messages[], model?, tools?}` | 0.10 |
| Text embeddings, EU-hosted | `POST /ai/v1/eu-embed {input}` | 0.05 |

Locations are country/city names or DataForSEO codes; `GET /v1/locations?q=germany` lists countries and languages for free.
Ask for the free quote/catalogue endpoint before any paid call when the price is a range.

## Rules of thumb

- Never put a main wallet's key in `X402_WALLET_KEY`. Fund a dedicated wallet with a few USDC.
- A 402 response is the price list, not an error: read `accepts[0].amount` (micro-USDC).
- Deliveries are idempotent: a paid response can be re-fetched with the same payment
  header within 24 h if the connection dropped (`redelivery`).
- If you want an endpoint that does not exist yet, post it to `POST /v1/wishlist` (free).
