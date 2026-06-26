# Cloudflare /crawl API Reference

## Endpoint
```
POST https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl
GET  https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl/{job_id}
DELETE https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl/{job_id}
```

## Auth
`Authorization: Bearer <API_TOKEN>` — token needs Browser Rendering Read + Edit.

## POST body (start crawl)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | *required* | Starting URL |
| `limit` | number | 10 | Max pages (max 100,000) |
| `depth` | number | 100,000 | Max link depth from start URL |
| `source` | string | `"all"` | `all`, `sitemaps`, `links` |
| `formats` | string[] | `["html"]` | `html`, `markdown`, `json` (can combine) |
| `render` | boolean | `true` | `false` = fast HTML fetch, no JS. Free during beta. |
| `maxAge` | number | 86400 | R2 cache seconds (max 604800 = 7 days) |
| `modifiedSince` | number | — | Unix timestamp; only crawl pages modified after |
| `options.includeExternalLinks` | boolean | false | Follow external domain links |
| `options.includeSubdomains` | boolean | false | Follow subdomain links |
| `options.includePatterns` | string[] | — | Wildcard: `*` (not `/`), `**` (any) |
| `options.excludePatterns` | string[] | — | Higher priority than include |
| `jsonOptions.prompt` | string | — | AI extraction prompt (requires `json` format) |
| `jsonOptions.response_format` | object | — | JSON schema for structured extraction |
| `jsonOptions.custom_ai` | object | — | BYO model instead of Workers AI |

### Render-related options (when render=true)
- `rejectResourceTypes` — block images/fonts/stylesheets
- `waitForSelector` — CSS selector to wait for (SPA support)
- `gotoOptions` — Puppeteer goto options
- `setExtraHTTPHeaders` — custom headers for authenticated crawls
- HTTP basic auth and cookies also supported

## GET response (poll/retrieve)

```json
{
  "success": true,
  "result": {
    "id": "job-uuid",
    "status": "completed|running|errored|cancelled_due_to_timeout|cancelled_due_to_limits|cancelled_by_user",
    "browserSecondsUsed": 1.23,
    "total": 50,
    "finished": 50,
    "skipped": 0,
    "records": [
      {
        "url": "https://...",
        "status": "completed|queued|disallowed|skipped|errored|cancelled",
        "markdown": "...",
        "html": "...",
        "json": { ... },
        "metadata": {
          "status": 200,
          "title": "Page Title",
          "url": "https://...",
          "lastModified": "..."
        }
      }
    ],
    "cursor": 10
  }
}
```

### GET query params
- `limit` — max records to return
- `cursor` — pagination cursor (returned when >10MB)
- `status` — filter: `queued`, `completed`, `disallowed`, `skipped`, `errored`, `cancelled`

## Lifecycle
- Max runtime: 7 days
- Results available: 14 days after completion
- Polling tip: use `?limit=1` for lightweight status checks

## Cost
- `render: true` — uses Browser Rendering minutes (paid)
- `render: false` — fast HTML fetch, currently **free during beta**
- `formats: ["json"]` — uses Workers AI tokens (paid)
