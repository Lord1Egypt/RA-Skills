# Reference: Parameters

Parameters across Firecrawl operations. "Default" reflects common/typical behavior; confirm exact defaults against the docs.

> Verification needed: confirm exact defaults, value ranges, action types, and proxy modes at https://docs.firecrawl.dev.

## Common request parameters

| Parameter | Used by | Type | Default | Meaning | When to change |
|-----------|---------|------|---------|---------|----------------|
| `url` | scrape, crawl, map | string | — (required) | Target URL (page for scrape; root for crawl/map). | Always set. Use the exact target; avoid internal/loopback hosts (SSRF). |
| `query` | search | string | — (required) | Search query. | Always set for search. |
| `formats` | scrape, `scrapeOptions` | array | `["markdown"]` | Output formats: `markdown`, `html`, `links`, `screenshot`, `summary`, `{type:"json",prompt,schema}`. | Add formats only when needed; each adds cost. |
| `onlyMainContent` | scrape, `scrapeOptions` | boolean | `true` | Strip nav/footer/ads/boilerplate; keep main content. | Set `false` only when you need full page chrome. |
| `waitFor` | scrape, `scrapeOptions` | number (ms) | `0` | Wait before capture so JS can render. | Raise for client-rendered/slow pages; keep as low as works. |
| `actions` | scrape, `scrapeOptions` | array | none | Interaction steps (wait/click/scroll/type/navigate) to reveal gated content. | Use the smallest sequence that exposes the content. |
| `proxy` | scrape, `scrapeOptions` | string/enum | normal | Proxy/stealth mode to bypass blocks. | Enable only when a normal scrape is blocked/empty; may cost more. |
| `maxAge` | scrape, `scrapeOptions` | number (ms) | provider default | Accept cached content newer than this age instead of re-fetching. | Larger for stable content (save cost); small/zero when freshness matters. |
| `limit` | crawl, map, search | number | provider default | Hard cap on pages/URLs/results. | **Always set** to bound cost; start small, widen if needed. |
| `includePaths` | crawl | array (regex/path) | none | Only crawl URLs matching these. | Use to stay within the relevant section. |
| `excludePaths` | crawl | array (regex/path) | none | Skip URLs matching these. | Use to avoid junk (login, cart, tag/archive pages). |
| `scrapeOptions` | crawl, search | object | none | Scrape options applied to each page/result (formats, onlyMainContent, waitFor, etc.). | Minimize `formats` here — it multiplies across pages. For search, include only when you need page bodies. |
| `search` | map | string | none | Filter discovered URLs by keyword/relevance. | Narrow large sites to relevant sections. |

## Structured-extraction format object (inside `formats`)

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `type` | string (`"json"`) | yes | Selects structured JSON extraction. |
| `prompt` | string | recommended | Natural-language instruction describing what to extract. |
| `schema` | object (JSON Schema) | recommended | Constrains the shape/types of the extracted object. |

Provide both `prompt` and `schema`; read the result from `data.json`. Do not use the deprecated `/v2/extract` endpoint.

## Crawl polling (read-side)

`GET /v2/crawl/{id}` takes the job `id` from the start response. Returns `status`, `completed`, `total`, `data`, and an optional `next` cursor/URL for pagination. Keep polling (with backoff) until `status` is `completed`, then follow `next` until exhausted.
