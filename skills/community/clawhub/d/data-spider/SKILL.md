---
name: data-spider
description: Scrape any webpage and extract structured data as JSON, table, or list. Supports schema-guided extraction.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🕷️"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Data Spider

Scrape and extract structured data from any webpage. Supports schema-guided extraction to match a specific data shape, or auto-detection of structure. Returns data as JSON object, table (columns + rows), or flat list depending on your chosen format.

## When to Use

- Extracting product information or pricing from pages
- Gathering statistics and figures from articles
- Building datasets from web sources
- Schema-guided extraction to match your data model
- Research and competitive analysis

## Usage Flow

1. Provide a webpage `url`
2. Optionally provide a `schema` object — data will be extracted to match that exact shape
3. Optionally set `format`: `json` (default), `table`, or `list`
4. AIProx routes to the data-spider agent
5. Returns structured data in the requested format, plus summary and source URL

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request — JSON with Schema

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "url": "https://example.com/pricing",
    "schema": {"free_tier": null, "pro_price": null, "enterprise": null},
    "format": "json"
  }'
```

### Response — JSON

```json
{
  "data": {"free_tier": "$0/month, 1000 API calls", "pro_price": "$29/month", "enterprise": "custom pricing"},
  "summary": "SaaS pricing page with three tiers.",
  "source": "https://example.com/pricing",
  "format": "json"
}
```

## Make Request — Table

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "extract pricing tiers as a table",
    "url": "https://example.com/pricing",
    "format": "table"
  }'
```

### Response — Table

```json
{
  "columns": ["Plan", "Price", "API Calls"],
  "rows": [
    ["Free", "$0/month", "1,000"],
    ["Pro", "$29/month", "50,000"],
    ["Enterprise", "Custom", "Unlimited"]
  ],
  "summary": "Three-tier SaaS pricing.",
  "source": "https://example.com/pricing",
  "format": "table"
}
```

### Response — List

```json
{
  "items": ["$0/month — Free tier, 1000 API calls", "$29/month — Pro, 50,000 calls", "Enterprise — custom pricing"],
  "summary": "SaaS pricing tiers extracted as flat list.",
  "source": "https://example.com/pricing",
  "format": "list"
}
```

## Trust Statement

Data Spider fetches and analyzes webpage contents via URL. Content is processed transiently and not stored. Analysis is performed by Claude via LightningProx. Respects robots.txt and rate limits. Your spend token is used for payment only.
