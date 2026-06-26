# AlphaLens API Reference

## Authentication

```bash
API="https://api-production.alphalens.ai"
```

Send `API-Key: $KEY` on all requests. The `KEY` variable is already defined in SKILL.md.

## Base URLs

- Production: `https://api-production.alphalens.ai`
- OpenAPI spec: `https://api-production.alphalens.ai/openapi.json`
- Docs: `https://api-production.alphalens.ai/docs`

## Public Endpoints

### Organization Resolution

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/entities/organizations/by-domain/{domain}` | Resolve company by domain → returns `organization_id` |
| `GET /api/v1/entities/organizations/{organization_id}` | Get full organization details |

### Organization Enrichment

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/entities/organizations/{id}/products` | List company's products |
| `GET /api/v1/entities/organizations/{id}/funding` | Funding rounds and investors |
| `GET /api/v1/entities/organizations/{id}/growth-metrics` | Headcount, web traffic, LinkedIn, job openings |
| `GET /api/v1/entities/organizations/{id}/people` | Founders and leadership |
| `GET /api/v1/entities/organizations/{id}/addresses` | HQ and branch locations |

### Search

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/search/organizations/{id}/similar` | Find similar organizations |
| `GET /api/v1/search/organizations/search` | Free-text org discovery |
| `GET /api/v1/search/organizations/search-customers` | By customer-base description |
| `GET /api/v1/search/products/search` | Free-text product discovery |
| `GET /api/v1/search/products/search-customers` | By customer-base description |
| `GET /api/v1/search/products/{id}/similar` | Find similar products |
| `GET /api/v1/search/locations/suggest` | Location typeahead |
| `GET /api/v1/search/locations/metadata` | Location metadata |

### Pipeline

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/pipelines/{id}/organizations` | Add organization to pipeline |
| `GET /api/v1/pipelines/{id}/items` | List pipeline items |
| `GET /api/v1/pipelines/{id}/items/{item_id}/status` | Check item readiness |
| `GET /api/v1/pipelines/{id}/items/{item_id}/values` | Read item values |
| `POST /api/v1/pipelines/{id}/documents` | Submit document to pipeline |
| `POST /api/v1/pipelines/{id}/documents-binary-data` | Submit binary data to pipeline |

## Pipeline Operations

Always inspect before mutating. Follow this order:

1. Inspect existing items: `GET /api/v1/pipelines/{pipeline_id}/items`
2. Add organizations: `POST /api/v1/pipelines/{pipeline_id}/organizations` with `{"organization_id": 123}`
3. Poll readiness: `GET /api/v1/pipelines/{pipeline_id}/items/{item_id}/status` — wait for `is_ready: true`
4. Read values: `GET /api/v1/pipelines/{pipeline_id}/items/{item_id}/values`

Submit documents via `POST /api/v1/pipelines/{pipeline_id}/documents` or `documents-binary-data`.

Collections and custom questions are managed in the [AlphaLens web interface](https://app.alphalens.ai), not via the public API.

## Common Filters

All search endpoints support:

| Parameter | Description |
|------------|-------------|
| `is_headquarters` | **Always set to `true`** — filters to HQ only and returns much higher quality matches. Only omit if the user explicitly asks for all locations. |
| `country_keys` | ISO country codes, e.g., `["US", "GB"]` |
| `region_keys` | State/region codes, e.g., `["NEW_YORK-US"]` |
| `year_founded_min/max` | Company age filter |
| `employee_count_range_min/max` | Company size filter |
| `skip` | Pagination offset |
| `limit` | Page size (max 100, default 24). **Always use `50`** — the default of 24 misses too much. |

## Not Available in Public API

These internal endpoints are **not** available:

- `GET /api/v1/entities/organizations/search-by-name/{name}` — use `by-domain` instead
- `GET /api/v1/collections/*` — collections are managed in the AlphaLens web UI
- `POST /api/v1/custom-questions/*` — custom questions are configured in the AlphaLens web UI
- Reindex endpoints — not available externally

For collections and custom questions, users should configure them in the [AlphaLens web interface](https://app.alphalens.ai).