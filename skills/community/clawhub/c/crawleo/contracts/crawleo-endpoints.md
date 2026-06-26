# Crawleo Endpoint Contract Inventory

This contract inventory is the S01 handoff artifact for downstream implementation and documentation. It is source-backed by Crawleo endpoint-specific docs, the Crawleo MCP overview, the Crawleo docs index, authentication docs, and the local OpenAPI snapshot.

## Contract Rules

- Base REST URL: `https://api.crawleo.dev`
- Primary authentication: `CRAWLEO_API_KEY` sent as `x-api-key`.
- Alternate authentication documented by Crawleo: `Authorization: Bearer YOUR_API_KEY`.
- Never print, log, echo, or persist API key values.
- Endpoint-specific Crawleo docs are authoritative where the local OpenAPI snapshot is narrower.
- Missing defaults, ranges, error tables, or unclear example-only fields must say: `not specified in Crawleo docs`.
- Default verification must not call Crawleo or consume credits.

## Source Conflict Summary

- Endpoint docs and docs index cover `/search`, `/google-search`, `/google-maps`, `/crawl`, and `/headful-browser`.
- Local OpenAPI snapshot covers only `/search`, `/google-maps`, and `/crawl`.
- `/google-search` and `/headful-browser` remain in scope because Crawleo endpoint docs and docs index document them.
- Google Maps cost conflicts by source: endpoint doc says 30 credits per request; MCP overview says 10 credits per request.
- `/search` examples include `count=10`, but the visible parameter table does not list `count`; treat `count` as example-only/ambiguous until verified.

## MCP Mapping

MCP endpoint: `https://api.crawleo.dev/mcp`

| MCP Tool | REST Endpoint | Documented Cost |
|---|---|---|
| `search_web` | `/search` | 10 credits per page of results |
| `google_search` | `/google-search` | 10 credits per request |
| `google_maps` | `/google-maps` | 10 credits per request in MCP overview; conflicts with endpoint doc cost of 30 credits per request |
| `crawl_web` | `/crawl` | 1 credit per URL for HTTP request; 10 credits per URL for browser rendering |
| `headful_browser` | `/headful-browser` | 50 credits per URL |

## Endpoint Contracts

### `/search` — Bing Search API

- Method: `GET`
- URL: `https://api.crawleo.dev/search`
- MCP tool: `search_web`
- Purpose: Bing-powered real-time web search with optional auto-crawling and content extraction for LLM/RAG workflows.
- Sources:
  - `.gsd/research/crawleo-docs/md/search.md` / `https://docs.crawleo.dev/api-reference/endpoint/search.md`
  - `.gsd/research/crawleo-docs/md/overview.md` / `https://docs.crawleo.dev/mcp/overview.md`
  - `.gsd/research/crawleo-docs/openapi.json.json` / `https://docs.crawleo.dev/openapi.json`
- Cost: 10 credits per page via `max_pages` / MCP `search_web` cost. Exact cost behavior for example-only `count` is `not specified in Crawleo docs`.

#### Parameters

| Location | Name | Type | Required | Default | Limits / Enum | Notes |
|---|---|---:|---:|---|---|---|
| header | `x-api-key` | string | yes | — | — | Crawleo API key; Bearer auth is also documented. |
| query | `query` | string | yes | — | — | Search query string. |
| query | `max_pages` | integer | no | `1` | `not specified in Crawleo docs` | Maximum pages to fetch; each page costs 10 credits. |
| query | `setLang` | string | no | — | examples: `en`, `es`, `fr`, `de` | Language code. |
| query | `cc` | string | no | — | examples: `US`, `GB`, `DE` | Country code. |
| query | `geolocation` | string | no | — | `random` documented | Geographic location. |
| query | `device` | string | no | `desktop` | `desktop`, `mobile`, `tablet` | Device simulation. |
| query | `copilot_answer` | boolean | no | `true` | — | Include Copilot answers. |
| query | `questions_answers` | boolean | no | `true` | — | Include People Also Ask. |
| query | `related_queries` | boolean | no | `true` | — | Include related searches. |
| query | `sidebar` | boolean | no | `true` | — | Include sidebar data. |
| query | `direct_answer` | boolean | no | `true` | — | Include direct answers. |
| query | `raw_html` | boolean | no | `false` | — | Return raw HTML. |
| query | `enhanced_html` | boolean | no | `false` | — | Return cleaned HTML. |
| query | `page_text` | boolean | no | `false` | — | Return plain text. |
| query | `markdown` | boolean | no | `false` | — | Return Markdown. |
| query | `auto_crawling` | boolean | no | `false` | — | Crawl result URLs automatically. |
| query | `count` | integer | no | `not specified in Crawleo docs` | `not specified in Crawleo docs` | Appears in examples but not in visible parameter table. |

#### Examples

- `GET /search?query=machine%20learning&count=10`
- `GET /search?query=AI%20agents&auto_crawling=true&markdown=true`

#### Response Shape

Top-level fields include `query`, `pages_fetched`, `pages`, `total_results`, `search_results`, `related_queries`, and `credits`. Result/page fields include `title`, `link`, `date`, `snippet`, `source`, `page_content`, `enhanced_html`, and `page_markdown`.

#### Errors / Ambiguities

- Error response table: `not specified in Crawleo docs`.
- `count` appears in examples but not the visible parameter table.

### `/google-search` — Google Search API

- Method: `GET`
- URL: `https://api.crawleo.dev/google-search`
- MCP tool: `google_search`
- Purpose: Real-time Google SERP data including web, news, images, places, shopping, knowledge graph, People Also Ask, related searches, and answer boxes.
- Sources:
  - `.gsd/research/crawleo-docs/md/google-search.md` / `https://docs.crawleo.dev/api-reference/endpoint/google-search.md`
  - `.gsd/research/crawleo-docs/md/overview.md` / `https://docs.crawleo.dev/mcp/overview.md`
- Cost: 10 credits per request.

#### Parameters

| Location | Name | Type | Required | Default | Limits / Enum | Notes |
|---|---|---:|---:|---|---|---|
| header | `x-api-key` | string | yes | — | — | Crawleo API key; Bearer auth is also documented. |
| query | `q` | string | yes | — | — | Search query. |
| query | `gl` | string | no | `us` | ISO 3166-1 alpha-2 examples: `us`, `gb`, `eg`, `de`, `fr` | Country. |
| query | `hl` | string | no | `en` | IETF language examples: `en`, `ar`, `fr`, `de` | Language. |
| query | `tbs` | string | no | — | `qdr:h`, `qdr:d`, `qdr:w`, `qdr:m`, `qdr:y` | Freshness filter. |
| query | `page` | integer | no | `1` | 1-indexed; upper bound `not specified in Crawleo docs` | Result page. |
| query | `num` | integer | no | `10` | `1–100` | Results per page. |
| query | `type` | string | no | `search` | `search`, `news`, `images`, `places`, `shopping` | Result vertical. |

#### Examples

- `GET /google-search?q=best%20CRM%20software&gl=us&hl=en&num=10`
- `GET /google-search?q=AI&type=news&tbs=qdr:d`
- `GET /google-search?q=coffee&type=places&gl=us`
- `GET /google-search?q=laptop&type=shopping`

#### Response Shape

Top-level fields include `parameters`, `google_search_results`, `knowledgeGraph`, `peopleAlsoAsk`, `relatedSearches`, and `answerBox`. Result fields include `title`, `link`, `snippet`, and `position`.

#### Errors / Ambiguities

| Status | Meaning |
|---:|---|
| 400 | Missing required parameter `q` |
| 401 | Invalid or missing API key |
| 402 | Insufficient credits |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

- `/google-search` is absent from the local OpenAPI snapshot but present in endpoint-specific docs and docs index.

### `/google-maps` — Google Maps API

- Method: `GET`
- URL: `https://api.crawleo.dev/google-maps`
- MCP tool: `google_maps`
- Purpose: Google Maps business/place/landmark search with structured place data.
- Sources:
  - `.gsd/research/crawleo-docs/md/google-maps.md` / `https://docs.crawleo.dev/api-reference/endpoint/google-maps.md`
  - `.gsd/research/crawleo-docs/md/overview.md` / `https://docs.crawleo.dev/mcp/overview.md`
  - `.gsd/research/crawleo-docs/openapi.json.json` / `https://docs.crawleo.dev/openapi.json`
- Cost: endpoint doc says 30 credits per request; MCP overview says 10 credits per request.

#### Parameters

| Location | Name | Type | Required | Default | Limits / Enum | Notes |
|---|---|---:|---:|---|---|---|
| header | `x-api-key` | string | yes | — | — | Crawleo API key; Bearer auth is also documented. |
| query | `q` | string | yes | — | — | Business name, landmark, address, keyword, or category + location query. |
| query | `hl` | string | no | `not specified in Crawleo docs` | ISO 639-1 examples: `en`, `ar`, `fr`, `de` | Language code. |
| query | `ll` | string | no | — | `@latitude,longitude,zoomz`, zoom `1z–21z` | Location bias. |
| query | `placeId` | string | no | — | — | Google Place ID lookup. |
| query | `cid` | string | no | — | — | Google numeric business/customer ID lookup. |

Documented combinations: `q`, `q + hl`, `q + ll`, `q + ll + hl`, `q + placeId`, `q + placeId + hl`, `q + cid`, `q + cid + hl`.

#### Examples

- `GET /google-maps?q=restaurants%20in%20Paris&hl=fr`
- `GET /google-maps?q=coffee%20shops&ll=%4048.8566%2C2.3522%2C15z&hl=fr`
- `GET /google-maps?q=Le%20Comptoir&placeId=ChIJLU7jZClu5kcR4PcOOO6p3I0`

#### Response Shape

Top-level fields include `parameters`, `google_maps_results`, and `credits`. Place result fields include `position`, `title`, `address`, `rating`, `ratingCount`, `phoneNumber`, `website`, `type`, `types`, `priceLevel`, `placeId`, `cid`, `latitude`, `longitude`, `openingHours`, and `thumbnailUrl`.

#### Errors / Ambiguities

| Status | Meaning |
|---:|---|
| 400 | Missing required query parameter `q` |
| 401 | Invalid or missing API key |
| 403 | Inactive account or expired subscription |
| 429 | Credits exhausted or concurrent request limit reached |
| 500 | Internal server error |

- Cost conflict: endpoint doc says 30 credits per request; MCP overview says 10 credits per request.
- Default for `hl` is `not specified in Crawleo docs`.

### `/crawl` — Crawler API

- Method: `GET`
- URL: `https://api.crawleo.dev/crawl`
- MCP tool: `crawl_web`
- Purpose: Direct URL crawling with optional JavaScript rendering, extraction, screenshots, and multiple output formats.
- Sources:
  - `.gsd/research/crawleo-docs/md/crawler.md` / `https://docs.crawleo.dev/api-reference/endpoint/crawler.md`
  - `.gsd/research/crawleo-docs/md/overview.md` / `https://docs.crawleo.dev/mcp/overview.md`
  - `.gsd/research/crawleo-docs/openapi.json.json` / `https://docs.crawleo.dev/openapi.json`
- Cost: 1 credit per URL when `render_js=false`; 10 credits per URL when `render_js=true`.

#### Parameters

| Location | Name | Type | Required | Default | Limits / Enum | Notes |
|---|---|---:|---:|---|---|---|
| header | `x-api-key` | string | yes | — | — | Crawleo API key; Bearer auth is also documented. |
| query | `urls` | string | yes | — | single URL or comma-separated URLs | URL(s) to crawl. |
| query | `render_js` | boolean | no | `false` | — | Browser rendering; increases cost to 10 credits per URL. |
| query | `geolocation` | string | no | — | ISO 3166-1 alpha-2 examples: `us`, `gb`, `de` | Geolocation country. |
| query | `raw_html` | boolean | no | `false` | — | Return raw HTML. |
| query | `enhanced_html` | boolean | no | `true` | — | Return cleaned HTML. |
| query | `page_text` | boolean | no | `false` | — | Return plain text. |
| query | `markdown` | boolean | no | `true` | — | Return Markdown. |
| query | `screenshot` | boolean | no | `false` | Only available when `render_js=true` | Capture screenshot. |
| query | `screenshot_full_page` | boolean | no | `false` | Requires screenshot flow | Capture full page. |

#### Examples

- `GET /crawl?urls=https://example.com&markdown=true`
- `GET /crawl?urls=https://example.com&render_js=true&screenshot=true`

#### Response Shape

Top-level fields include `results`, `credits`, and `successful_pages`. Per-result fields include `url`, `status_code`, `raw_html`, `enhanced_html`, `markdown`, `page_text`, `screenshot`, and `error`.

#### Errors / Ambiguities

- Error response table: `not specified in Crawleo docs`.

### `/headful-browser` — Headful Browser API

- Method: `GET`
- URL: `https://api.crawleo.dev/headful-browser`
- MCP tool: `headful_browser`
- Purpose: Premium headed browser crawling with anti-bot evasion, SOAX residential proxies, screenshots, and multiple output formats.
- Sources:
  - `.gsd/research/crawleo-docs/md/headful-browser.md` / `https://docs.crawleo.dev/api-reference/endpoint/headful-browser.md`
  - `.gsd/research/crawleo-docs/md/overview.md` / `https://docs.crawleo.dev/mcp/overview.md`
- Cost: 50 credits per URL; failed requests cost 0 credits.

#### Parameters

| Location | Name | Type | Required | Default | Limits / Enum | Notes |
|---|---|---:|---:|---|---|---|
| header | `x-api-key` | string | yes | — | — | Crawleo API key; Bearer auth is also documented. |
| query | `urls` | string | yes | — | single URL or comma-separated URLs | URL(s) to crawl. |
| query | `country` | string | no | `us` | examples: `us`, `gb`, `de`, `fr`, `jp`, `in`, `br`, `ca`, `au`, and more | Residential proxy country. |
| query | `output_format` | string | no | `markdown` | `markdown`, `enhanced_html`, `raw_html`, `page_text` | Output format. |
| query | `screenshot` | boolean | no | `false` | — | Return screenshot URL. |

#### Examples

- `GET /headful-browser?urls=https://example.com&output_format=markdown`
- `GET /headful-browser?urls=https://example.com&screenshot=true`

#### Response Shape

Top-level fields include `status`, `data`, `credits_used`, and `credits_remaining`. Per-item fields include `url`, `markdown`, `raw_html`, `enhanced_html`, `page_text`, `screenshot`, and `blocked`.

#### Errors / Ambiguities

- `/headful-browser` is absent from the local OpenAPI snapshot but present in endpoint-specific docs and docs index.
- Error response table: `not specified in Crawleo docs`.

## Verification

Structured JSON should parse with:

```bash
node -e "JSON.parse(require('fs').readFileSync('contracts/crawleo-endpoints.json','utf8')); console.log('valid json')"
```

Full S01 contract verification will be added in `scripts/verify-contracts.js` and run with:

```bash
node scripts/verify-contracts.js
```
