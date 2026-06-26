---
name: datatk-quote-skill
description: Real-time stock market data via QuoteNode API. Query quotes, K-lines, tick trades, Level-2 depth, and trading calendars for US/HK/CN markets.
---

# QuoteNode REST

Use this skill for QuoteNode REST market-data integration. WebSocket is out of scope.

## Project Overview

- QuoteNode is a market-data aggregation service that exposes a unified REST OpenAPI surface to downstream callers.
- Downstream clients authenticate with the `X-API-KEY` header and send JSON request bodies.
- The REST path is handled by OpenAPI authorization middleware, which centralizes `ak`, `endpoint`, `market`, permission, and rate-limit handling.

For background, read:
- `references/architecture.md`

## Quick Start

```bash
# copy example env file, then edit env.json to add your endpoint and apiKey
cp {baseDir}/env.json.example {baseDir}/env.json

# test with a sample request
node {baseDir}/scripts/request.mjs --path /Api/V1/Quotation/Detail --body '{"instrument":"US|AAPL","lang":"en"}'
```

## Workflow

1. Start with `references/openapi.md` to choose the endpoint and request parameters.
2. If you need market codes, enum values, adjustment types, or error codes, read `references/reference.md`.
3. If you need response structure or field meanings, read `references/response.md`.
4. If you need the architectural position of the REST layer in this project, read `references/architecture.md`.

## Script

- `scripts/request.mjs`: generic POST caller for any REST endpoint.

Notes:
- All requests read `endpoint` and `apiKey` from `datatk-quote-skill/env.json`.
- `request.mjs --body` must be valid JSON.
- The script prints the raw JSON response by default. If the HTTP status is not `200`, it prints the status code and response body.
- Get `endpoint` and `apiKey` from the [dataTrack service page](https://www.datatk.com/service).
- Configure `endpoint` and `apiKey` in `datatk-quote-skill/env.json`.
- If you are unsure about parameter values, market codes, or error codes, read `references/reference.md` first. If you are unsure about response fields, read `references/response.md`.
