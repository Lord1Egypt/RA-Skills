# Crawleo Endpoint Coverage Checklist

This checklist maps the documented Crawleo surface to this OpenClaw skill package. It is intended for downstream documentation, test, and final assembly verification.

| REST Endpoint | MCP Tool | Contract Entry | Wrapper Method | README Coverage | Example Coverage | Test Coverage | Notes |
|---|---|---|---|---|---|---|---|
| `/search` | `search_web` | `contracts/crawleo-endpoints.json` id `search` | `client.search` / `search(client, params)` | Basic usage, wrapper API, covered capabilities table | `examples/offline-fake-fetch.js` | `test/wrapper-fixtures.test.js`, `test/endpoints.test.js`, `test/client.test.js`, `test/errors.test.js` | `count` appears in examples but is not in the visible parameter table; keep as not specified in Crawleo docs. |
| `/google-search` | `google_search` | `contracts/crawleo-endpoints.json` id `google_search` | `client.googleSearch` / `googleSearch(client, params)` | Wrapper API and covered capabilities table | `examples/offline-fake-fetch.js` | `test/wrapper-fixtures.test.js`, `test/endpoints.test.js`, `test/errors.test.js` | Documented by endpoint docs but absent from the local OpenAPI snapshot. |
| `/google-maps` | `google_maps` | `contracts/crawleo-endpoints.json` id `google_maps` | `client.googleMaps` / `googleMaps(client, params)` | Wrapper API and covered capabilities table | `examples/offline-fake-fetch.js` | `test/wrapper-fixtures.test.js`, `test/endpoints.test.js`, `test/errors.test.js` | Cost differs by source: endpoint docs say 30 credits per request; MCP overview says 10 credits per request. |
| `/crawl` | `crawl_web` | `contracts/crawleo-endpoints.json` id `crawl` | `client.crawl` / `crawl(client, params)` | Wrapper API and covered capabilities table | `examples/offline-fake-fetch.js` | `test/wrapper-fixtures.test.js`, `test/endpoints.test.js`, `test/client.test.js`, `test/errors.test.js` | Error response table is not specified in Crawleo docs. |
| `/headful-browser` | `headful_browser` | `contracts/crawleo-endpoints.json` id `headful_browser` | `client.headfulBrowser` / `headfulBrowser(client, params)` | Wrapper API and covered capabilities table | `examples/offline-fake-fetch.js` | `test/wrapper-fixtures.test.js`, `test/endpoints.test.js`, `test/errors.test.js` | Documented by endpoint docs but absent from the local OpenAPI snapshot; error response table is not specified in Crawleo docs. |

## Verification Surfaces

- `npm run verify:contracts` verifies endpoint and MCP tool coverage in the contract inventory.
- `npm test` verifies wrapper request construction, validation, response parsing, error normalization, live-test skip behavior, and secret redaction offline.
- `npm run test:live` runs the optional live smoke test file; it skips unless both `CRAWLEO_API_KEY` and `CRAWLEO_ENABLE_LIVE_TESTS=1` are set.
- `npm run verify:scaffold` verifies package files, public exports, README/SKILL references, live-test gate documentation, and this coverage checklist.

## Live Verification Status

Live Crawleo calls are intentionally not part of default verification. Optional live tests must require both `CRAWLEO_API_KEY` and `CRAWLEO_ENABLE_LIVE_TESTS=1` before making any request to Crawleo. Without both variables, `npm run test:live` exits 0 with the live test skipped.
