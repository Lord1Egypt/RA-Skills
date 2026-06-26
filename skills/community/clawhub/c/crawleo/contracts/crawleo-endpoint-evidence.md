# Crawleo Endpoint Contract Evidence

This file records the source evidence for S01 before the structured contract inventory is authored. Endpoint-specific Crawleo docs are treated as authoritative where the local OpenAPI snapshot is narrower.

## Source Set

- Crawleo docs index: `.gsd/research/crawleo-docs/llms.txt.txt` / `https://docs.crawleo.dev/llms.txt`
- REST introduction: `.gsd/research/crawleo-docs/md/introduction.md` / `https://docs.crawleo.dev/api-reference/introduction.md`
- Authentication: `.gsd/research/crawleo-docs/md/authentication.md` / `https://docs.crawleo.dev/authentication.md`
- MCP overview: `.gsd/research/crawleo-docs/md/overview.md` / `https://docs.crawleo.dev/mcp/overview.md`
- OpenAPI snapshot: `.gsd/research/crawleo-docs/openapi.json.json` / `https://docs.crawleo.dev/openapi.json`

## Cross-Source Conflict Notes

- The endpoint-specific docs and docs index list five REST capabilities: `/search`, `/google-search`, `/google-maps`, `/crawl`, and `/headful-browser`.
- The local OpenAPI snapshot currently lists only `/search`, `/google-maps`, and `/crawl`.
- S01 therefore keeps `/google-search` and `/headful-browser` because they are documented on endpoint-specific Crawleo docs pages and in the docs index.
- Where fields are not explicitly documented, downstream contract files must use the phrase `not specified in Crawleo docs` rather than inventing behavior.

## REST Endpoint Evidence

### `/search` — Bing Search API

- Source doc: `.gsd/research/crawleo-docs/md/search.md`
- Source URL: `https://docs.crawleo.dev/api-reference/endpoint/search.md`
- Endpoint evidence: `GET https://api.crawleo.dev/search`
- Authentication evidence: required `x-api-key` header; docs also allow `Authorization: Bearer YOUR_API_KEY`.
- Required query parameter: `query` string.
- Documented optional parameters include:
  - `max_pages` integer, default `1`; each page costs 10 credits.
  - `setLang` string language code examples: `en`, `es`, `fr`, `de`.
  - `cc` string country code examples: `US`, `GB`, `DE`.
  - `geolocation` string; docs mention `random` for randomized geolocation.
  - `device` string, default `desktop`; documented options: `desktop`, `mobile`, `tablet`.
  - SERP toggles: `copilot_answer`, `questions_answers`, `related_queries`, `sidebar`, `direct_answer`; each default `true`.
  - Page-content toggles: `raw_html`, `enhanced_html`, `page_text`, `markdown`; each default `false` in the endpoint doc.
  - `auto_crawling` boolean, default `false`.
- Example evidence: basic search request uses `https://api.crawleo.dev/search?query=machine%20learning&count=10` even though `count` is not listed in the visible parameter table; this must be marked as an ambiguity before implementation.
- Response evidence fields include `query`, `pages_fetched`, `pages`, `total_results`, `search_results`, result `title`, `link`, `date`, `snippet`, `source`, `related_queries`, `page_content`, `enhanced_html`, `page_markdown`, and `credits`.
- Error response table: not specified in Crawleo docs.
- MCP mapping: `search_web` from MCP overview.

### `/google-search` — Google Search API

- Source doc: `.gsd/research/crawleo-docs/md/google-search.md`
- Source URL: `https://docs.crawleo.dev/api-reference/endpoint/google-search.md`
- Endpoint evidence: `GET https://api.crawleo.dev/google-search`
- Cost evidence: 10 credits per request.
- Authentication evidence: required `x-api-key` header; docs also allow `Authorization: Bearer YOUR_API_KEY`.
- Required query parameter: `q` string.
- Documented optional parameters include:
  - `gl` string, default `us`; ISO 3166-1 alpha-2 examples include `us`, `gb`, `eg`, `de`, `fr`.
  - `hl` string, default `en`; IETF language tag examples include `en`, `ar`, `fr`, `de`.
  - `tbs` string; documented values include `qdr:h`, `qdr:d`, `qdr:w`, `qdr:m`, `qdr:y`.
  - `page` integer, default `1`; 1-indexed.
  - `num` integer, default `10`; documented range `1–100`.
  - `type` string, default `search`; documented values: `search`, `news`, `images`, `places`, `shopping`.
- Response evidence fields include `parameters`, `google_search_results`, result `title`, `link`, `snippet`, `position`, `knowledgeGraph`, `peopleAlsoAsk`, `relatedSearches`, and `answerBox`.
- Error evidence: `400` missing `q`, `401` invalid/missing API key, `402` insufficient credits, `429` rate limit exceeded, `500` internal server error.
- MCP mapping: endpoint doc states tool name `google_search`; MCP overview also lists `google_search`.

### `/google-maps` — Google Maps API

- Source doc: `.gsd/research/crawleo-docs/md/google-maps.md`
- Source URL: `https://docs.crawleo.dev/api-reference/endpoint/google-maps.md`
- Endpoint evidence: `GET https://api.crawleo.dev/google-maps`
- Cost evidence: endpoint doc says 30 credits per request; MCP overview says `google_maps` costs 10 credits per request. Preserve this as a source conflict until resolved.
- Authentication evidence: required `x-api-key` header; docs also allow `Authorization: Bearer YOUR_API_KEY`.
- Required query parameter: `q` string; accepts business names, landmarks, addresses, keywords, and category + location queries.
- Documented optional parameters include:
  - `hl` string ISO 639-1 language code; examples include `en`, `ar`, `fr`, `de`.
  - `ll` string location bias in format `@latitude,longitude,zoomz`; zoom range documented as `1z` to `21z`.
  - `placeId` string Google Place ID for direct lookup.
  - `cid` string Google numeric business/customer ID for direct business lookup.
- Parameter combination evidence includes `q` only, `q + hl`, `q + ll`, `q + ll + hl`, `q + placeId`, `q + placeId + hl`, `q + cid`, and `q + cid + hl`.
- Response evidence fields include `parameters`, `google_maps_results`, result `position`, `title`, `address`, `rating`, `ratingCount`, `phoneNumber`, `website`, `type`, `types`, `priceLevel`, `placeId`, `cid`, `latitude`, `longitude`, `openingHours`, `thumbnailUrl`, and `credits`.
- Error evidence: `400` missing `q`, `401` invalid/missing API key, `403` inactive account or expired subscription, `429` credits exhausted or concurrent request limit reached, `500` internal server error.
- MCP mapping: `google_maps` from MCP overview.

### `/crawl` — Crawler API

- Source doc: `.gsd/research/crawleo-docs/md/crawler.md`
- Source URL: `https://docs.crawleo.dev/api-reference/endpoint/crawler.md`
- Endpoint evidence: `GET https://api.crawleo.dev/crawl`
- Authentication evidence: required `x-api-key` header; docs also allow `Authorization: Bearer YOUR_API_KEY`.
- Required query parameter: `urls` string; accepts a single URL or comma-separated list.
- Documented optional parameters include:
  - `render_js` boolean, default `false`; `true` browser rendering costs 10 credits per URL, `false` HTTP request costs 1 credit per URL.
  - `geolocation` string ISO 3166-1 alpha-2 country code.
  - Output toggles: `raw_html` default `false`, `enhanced_html` default `true`, `page_text` default `false`, `markdown` default `true`.
  - Screenshot toggles: `screenshot` default `false`, `screenshot_full_page` default `false`; screenshots are only available when `render_js=true`, and `screenshot=true` without JavaScript rendering is ignored.
- Response evidence fields include `results`, per-result `url`, `status_code`, `raw_html`, `enhanced_html`, `markdown`, `page_text`, `screenshot`, `error`, plus top-level `credits` and `successful_pages`.
- Error response table: not specified in Crawleo docs.
- MCP mapping: `crawl_web` from MCP overview.

### `/headful-browser` — Headful Browser API

- Source doc: `.gsd/research/crawleo-docs/md/headful-browser.md`
- Source URL: `https://docs.crawleo.dev/api-reference/endpoint/headful-browser.md`
- Endpoint evidence: `GET https://api.crawleo.dev/headful-browser`
- Cost evidence: 50 credits per URL; failed requests cost 0 credits.
- Authentication evidence: required `x-api-key` header; docs also allow `Authorization: Bearer YOUR_API_KEY`.
- Required query parameter: `urls` string; accepts one or more URLs as a single URL or comma-separated list.
- Documented optional parameters include:
  - `country` string, default `us`; supported examples include `us`, `gb`, `de`, `fr`, `jp`, `in`, `br`, `ca`, `au`, and more.
  - `output_format` string, default `markdown`; documented values: `markdown`, `enhanced_html`, `raw_html`, `page_text`.
  - `screenshot` boolean, default `false`; screenshot is returned as a URL.
- Response evidence fields include `status`, `data`, per-item `url`, `markdown`, `raw_html`, `enhanced_html`, `page_text`, `screenshot`, `blocked`, `credits_used`, and `credits_remaining`.
- Error response table: not specified in Crawleo docs.
- MCP mapping: endpoint doc states tool name `headful_browser`; MCP overview also lists `headful_browser`.

## MCP Tool Evidence

- Source doc: `.gsd/research/crawleo-docs/md/overview.md`
- Source URL: `https://docs.crawleo.dev/mcp/overview.md`
- MCP endpoint: `https://api.crawleo.dev/mcp`
- Documented tools:
  - `search_web` — Bing-powered web search with auto-crawling; cost 10 credits per page of results.
  - `google_search` — Google SERP data; cost 10 credits per request.
  - `google_maps` — Google Maps places/business search; MCP overview says 10 credits per request, conflicting with endpoint doc's 30 credits per request.
  - `crawl_web` — URL crawling/content extraction; cost 1 credit per URL for HTTP request and 10 credits per URL for browser rendering.
  - `headful_browser` — premium headed browser crawling; cost 50 credits per URL.

## OpenAPI Evidence

- Source file: `.gsd/research/crawleo-docs/openapi.json.json`
- Source URL: `https://docs.crawleo.dev/openapi.json`
- Paths present in the local snapshot: `/search`, `/google-maps`, `/crawl`.
- Paths absent from the local snapshot but present in endpoint docs and docs index: `/google-search`, `/headful-browser`.

## Downstream Contract Rules

- Use Crawleo-only naming and branding.
- Use endpoint-specific docs over OpenAPI when OpenAPI omits an endpoint.
- Preserve source conflicts, especially Google Maps cost discrepancy, instead of choosing silently.
- Use `not specified in Crawleo docs` for missing error tables, undocumented defaults, unclear ranges, or example-only parameters not listed in parameter tables.
- Do not include any live Crawleo calls in default verification.
