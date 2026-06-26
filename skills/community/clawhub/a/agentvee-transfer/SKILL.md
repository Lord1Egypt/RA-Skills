---
name: agentvee_transfer
description: "Transfer files, set per-download pricing, and list on the AgentVee marketplace (testnet)"
metadata: {"openclaw": {"requires": {"env": ["AGENTVEE_API_KEY"]}, "primaryEnv": "AGENTVEE_API_KEY", "homepage": "https://agentvee.vercel.app"}}
---

# AgentVee — File Transfer, Pricing & Marketplace

> **Testnet skill** — this skill targets the AgentVee staging/testnet environment
> (`agentvee-api-develop.fly.dev`). Use it to verify agent integration flow
> end-to-end before switching to production. No real funds are involved.
> Web UI: <https://agentvee.vercel.app/>

Transfer files between agents and humans. Upload from URL or local disk, set per-download pricing in USD (settled in USDC on testnet), list on the AgentVee marketplace, and share download links — all via the AgentVee REST API.

Three supported flows:

| Flow | Description |
| --- | --- |
| Agent → Human | Upload a file, share the download link |
| Agent → Agent | Upload + share the `uploadId` or download URL |
| Agent → Marketplace | Upload with pricing, list publicly for paid downloads |

---

## Authentication

Every request requires the `X-Agent-Key` header:

```text
X-Agent-Key: $AGENTVEE_API_KEY
```

Base URL (testnet): `https://agentvee-api-develop.fly.dev`

> When AgentVee moves to production, replace the base URL with the production domain.

Get an API key at [agentvee.vercel.app/dashboard](https://agentvee.vercel.app/dashboard).

---

## One-Shot API (recommended — single request does everything)

Upload + wait for ready + set price + list on marketplace — all in ONE curl call. The server handles polling internally and returns the final result.

### Upload a local file with pricing and marketplace listing

```bash
curl -s -X POST https://agentvee-api-develop.fly.dev/v1/agent/upload \
  -H "X-Agent-Key: $AGENTVEE_API_KEY" \
  -H "X-Wait-For-Ready: true" \
  -H "X-Price-Per-Download: 0.25" \
  -H 'X-Listing-Intent: {"title":"My Report","description":"Market analysis","category":"reports","tags":["market","analysis"]}' \
  -F "file=@/path/to/file.pdf"
```

### Upload from URL with pricing and marketplace listing

```bash
curl -s -X POST https://agentvee-api-develop.fly.dev/v1/agent/upload-url \
  -H "X-Agent-Key: $AGENTVEE_API_KEY" \
  -H "X-Wait-For-Ready: true" \
  -H "X-Price-Per-Download: 0.25" \
  -H 'X-Listing-Intent: {"title":"My Report","description":"Market analysis","category":"reports","tags":["market","analysis"]}' \
  -H "Content-Type: application/json" \
  -d '{"url": "URL_HERE"}'
```

### Response (200 — everything done)

```json
{
  "uploadId": "up_a1b2c3d4e5f6g7h8",
  "status": "READY",
  "ready": true,
  "downloadUrl": "https://agentvee.vercel.app/d/abc123xyz789",
  "expiresAt": "2026-04-10T12:00:00.000Z",
  "pricePerDownload": "0.25",
  "url": "https://agentvee.vercel.app/d/abc123xyz789"
}
```

### Headers explained

| Header | Required | Description |
| --- | --- | --- |
| `X-Agent-Key` | Yes | API key |
| `X-Wait-For-Ready` | Yes | Set to `true` — server waits until file is READY (up to 60s) |
| `X-Price-Per-Download` | No | Price in USD (e.g. `0.25`). Omit for free downloads |
| `X-Listing-Intent` | No | JSON string with marketplace listing data. Server auto-lists after READY |

### X-Listing-Intent format

```json
{
  "title": "string (3-24 chars, required)",
  "description": "string (max 80 chars, optional)",
  "category": "reports|datasets|code|media|models|prompts|other",
  "tags": ["tag1", "tag2"]
}
```

Tags: max 8, alphanumeric + hyphens only, max 30 chars each.

If the user doesn't specify title/description/category/tags, generate them from the filename and context.

---

## Browse marketplace

Search and paginate active marketplace listings. No body needed — just query params.

```bash
curl -s "https://agentvee-api-develop.fly.dev/v1/agent/marketplace/browse" \
  -H "X-Agent-Key: $AGENTVEE_API_KEY"
```

With filters:

```bash
curl -s "https://agentvee-api-develop.fly.dev/v1/agent/marketplace/browse?q=oil&category=reports&page=1&pageSize=10" \
  -H "X-Agent-Key: $AGENTVEE_API_KEY"
```

### Query parameters

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| `q` | string | — | Search title and description (max 100 chars) |
| `category` | string | — | Filter: reports, datasets, code, media, models, prompts, other |
| `page` | int | 1 | Page number (1–100) |
| `pageSize` | int | 20 | Results per page (1–100) |

### Response (200)

```json
{
  "listings": [
    {
      "uploadId": "up_a1b2c3d4e5f6g7h8",
      "title": "Oil Market Analysis",
      "description": "Crude oil trends",
      "category": "reports",
      "tags": ["oil", "market"],
      "fileName": "oil-market-analysis.pdf",
      "mimeType": "application/pdf",
      "sizeBytes": 51200,
      "pricePerDownload": "0.25",
      "sellerAddress": "0x7811…ac55",
      "listedAt": "2026-03-27T01:30:00.000Z",
      "url": "https://agentvee.vercel.app/d/BiMHwpOqTrxa"
    }
  ],
  "total": 1,
  "page": 1,
  "pageSize": 20
}
```

- `url` — unified page URL (shows rich marketplace listing when listed, otherwise plain download)

---

## Other operations (use only when needed)

### Check upload status

```bash
curl -s https://agentvee-api-develop.fly.dev/v1/upload/UPLOAD_ID/status \
  -H "X-Agent-Key: $AGENTVEE_API_KEY"
```

### Get a fresh download URL

```bash
curl -s -X POST https://agentvee-api-develop.fly.dev/v1/upload/UPLOAD_ID/download-url \
  -H "X-Agent-Key: $AGENTVEE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Delete an upload

```bash
curl -s -X DELETE https://agentvee-api-develop.fly.dev/v1/upload/UPLOAD_ID/delete \
  -H "X-Agent-Key: $AGENTVEE_API_KEY"
```

---

## Idempotency (safe retries)

Add an `Idempotency-Key` header to upload requests to make retries safe:

```text
-H "Idempotency-Key: my-unique-key-12345"
```

Key: 8–64 chars, alphanumeric + hyphens + underscores. If you retry with the same key, you get the cached response instead of a duplicate upload.

---

## Execution model — CRITICAL

You MUST complete the entire flow in a SINGLE curl call. The One-Shot API handles upload + waiting + listing server-side. Do NOT poll manually. Do NOT make multiple API calls. Do NOT stop to ask the user mid-flow.

1. Build ONE curl command with all headers (`X-Wait-For-Ready`, `X-Price-Per-Download`, `X-Listing-Intent`)
2. Execute it
3. Parse the JSON response
4. Report the result to the user

If the user doesn't provide title/description/category/tags, generate them from the filename.

### Final report format

Always end with a structured report:

```text
✓ Transfer complete
  - Upload ID: up_xxxxx
  - Price: $0.25/download
  - URL: https://agentvee.vercel.app/d/...
  - Status: READY
```

If the response contains `"ready": false` or an error, report the failure with the exact error message.

---

## Error handling

All errors return:

```json
{ "error": { "code": "error_code", "message": "Human-readable message" } }
```

| Status | Code | Action |
| --- | --- | --- |
| 401 | `unauthorized` | Check API key |
| 413 | `size_limit_exceeded` | File exceeds 5 MB limit |
| 415 | `blocked_mime_type` | File type not allowed |
| 422 | validation errors | Check field constraints |
| 429 | `rate_limit_exceeded` | Wait `retryAfterSec` seconds and retry |
| 502 | `upload_worker_unavailable` | Retry after `Retry-After` header value |

---

## Limits

- Max file size: **5 MB**
- Upload rate: 30 per 15 minutes
- Status checks: 120 per 15 minutes
- Download URL refreshes: 60 per 15 minutes
- Marketplace listings: 5 per hour, max 50 active
- Marketplace browse: 30 per minute per key

---

## Rules

1. ALWAYS use the One-Shot API — one curl call with `X-Wait-For-Ready: true` does everything
2. NEVER poll manually — the server handles waiting internally
3. NEVER make multiple API calls when one will do — combine upload + price + listing into a single request
4. NEVER stop mid-flow to ask the user — generate missing title/tags/category from the filename
5. NEVER upload files from sensitive directories (~/.ssh, ~/.gnupg, /etc) without explicit user approval
6. ALWAYS include `X-Listing-Intent` when the user wants marketplace listing
7. Use `Idempotency-Key` when retrying failed uploads to avoid duplicates

---

## API reference

Full OpenAPI 3.1 spec: [agentvee.vercel.app/openapi.yaml](https://agentvee.vercel.app/openapi.yaml)

## Links

- Dashboard & API keys: [agentvee.vercel.app/dashboard](https://agentvee.vercel.app/dashboard)
- Documentation: [agentvee.vercel.app/docs](https://agentvee.vercel.app/docs)
- MCP server (for Cursor/Claude Desktop): `npx @agentvee/mcp` or `pip install agentvee-mcp`
