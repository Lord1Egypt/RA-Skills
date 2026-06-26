# Crawleo OpenClaw Skill

A self-contained OpenClaw skill package for Crawleo web intelligence capabilities: Bing-powered web search, Google Search, Google Maps place search, URL crawling/content extraction, and Headful Browser crawling for protected or heavily dynamic sites.

## Status

This package is contract-backed and includes offline-tested REST wrapper helpers for every documented Crawleo endpoint in this milestone:

- `/search`
- `/google-search`
- `/google-maps`
- `/crawl`
- `/headful-browser`

Live Crawleo calls require `CRAWLEO_API_KEY`. Default verification is offline and must not call Crawleo, require credentials, or consume credits.

Current source of truth:

- Machine-readable endpoint contract: `contracts/crawleo-endpoints.json`
- Human-readable endpoint contract: `contracts/crawleo-endpoints.md`
- Endpoint coverage checklist: `contracts/coverage-checklist.md`
- Final assembly report: `contracts/final-assembly-report.md`
- Skill metadata: `skill.json`
- Skill instructions: `SKILL.md`

## Installation and Setup

Use Node.js 18 or newer.

Install from npm:

```bash
npm install openclaw-crawleo-skill
```

For local development from this repository:

```bash
npm install
```

This package currently has no runtime dependencies.

## Installing as an OpenClaw Skill

### From ClawHub

Install the `crawleo` skill from ClawHub, then restart or reload the OpenClaw session so the skill registry is refreshed.

After installation, verify OpenClaw can see the skill:

```bash
openclaw skills info crawleo
```

Expected result: the skill is listed as eligible and shows `primaryEnv: CRAWLEO_API_KEY`.

OpenClaw understands the skill metadata:

```yaml
primaryEnv: CRAWLEO_API_KEY
requires.env: [CRAWLEO_API_KEY]
```

So if the key is missing, OpenClaw can prompt the user to provide `CRAWLEO_API_KEY` before running live Crawleo calls.

### Local personal-skill install

If you are installing from this repository or from the npm package manually, copy the skill folder into OpenClaw's personal skills directory:

```bash
mkdir -p ~/.agents/skills/crawleo
cp -R SKILL.md README.md LICENSE skill.json package.json contracts examples src test scripts ~/.agents/skills/crawleo/
openclaw skills info crawleo
```

On Windows PowerShell, the target directory is usually:

```powershell
$target = "$env:USERPROFILE\.agents\skills\crawleo"
New-Item -ItemType Directory -Force $target
Copy-Item SKILL.md,README.md,LICENSE,skill.json,package.json $target
Copy-Item contracts,examples,src,test,scripts $target -Recurse
openclaw skills info crawleo
```

## Configuring `CRAWLEO_API_KEY`

Live Crawleo calls require `CRAWLEO_API_KEY`. The key is sent with Crawleo's documented `x-api-key` header by default.

Set the variable in the same environment that runs OpenClaw.

### macOS / Linux shell

```bash
export CRAWLEO_API_KEY="sk_..."
openclaw tui
```

To make it persistent, add the `export` line to your shell profile, such as `~/.zshrc` or `~/.bashrc`, then restart the shell.

### Windows PowerShell

For the current terminal only:

```powershell
$env:CRAWLEO_API_KEY = "sk_..."
openclaw tui
```

For future terminals:

```powershell
[Environment]::SetEnvironmentVariable("CRAWLEO_API_KEY", "sk_...", "User")
```

Then close and reopen the terminal before starting OpenClaw.

### Verifying the key

Run the optional live smoke test only when you intentionally want to make a real Crawleo request:

```bash
CRAWLEO_API_KEY="sk_..." CRAWLEO_ENABLE_LIVE_TESTS=1 npm run test:live
```

Never print, echo, log, serialize, commit, or include the API key in examples, errors, test output, or debug output. The wrapper errors are designed to redact configured secrets before serialization.

## Basic Usage

```js
import { createCrawleoClient } from 'openclaw-crawleo-skill';

const client = createCrawleoClient({
  apiKey: process.env.CRAWLEO_API_KEY
});

const results = await client.search({
  query: 'ai agents',
  max_pages: 1
});
```

For tests and offline examples, inject `fetch` so no network request is made:

```js
import { createCrawleoClient } from 'openclaw-crawleo-skill';

const client = createCrawleoClient({
  apiKey: 'test-key',
  fetch: async (url, init) => ({
    ok: true,
    status: 200,
    headers: new Map([['content-type', 'application/json']]),
    async text() {
      return JSON.stringify({ url: url.toString(), method: init.method });
    }
  })
});

await client.crawl({ urls: ['https://example.com'], markdown: true });
```

## Wrapper API

Create one client and call endpoint-specific methods with endpoint parameters.

### Bing-powered web search

```js
await client.search({
  query: 'machine learning',
  max_pages: 1,
  device: 'desktop',
  markdown: true
});
```

### Google Search

```js
await client.googleSearch({
  q: 'best CRM software',
  gl: 'us',
  hl: 'en',
  type: 'search',
  num: 10
});
```

### Google Maps

```js
await client.googleMaps({
  q: 'restaurants in Paris',
  hl: 'fr'
});
```

### URL crawling and extraction

```js
await client.crawl({
  urls: ['https://example.com'],
  markdown: true,
  render_js: false
});
```

### Headful Browser crawling

```js
await client.headfulBrowser({
  urls: 'https://example.com',
  country: 'us',
  output_format: 'markdown',
  screenshot: false
});
```

Top-level wrapper functions are also exported for advanced composition. They accept a configured client object plus endpoint parameters, not raw credentials:

```js
import { createCrawleoClient, googleSearch } from 'openclaw-crawleo-skill';

const client = createCrawleoClient({ apiKey: process.env.CRAWLEO_API_KEY });
await googleSearch(client, { q: 'AI agents', type: 'news' });
```

## Covered Crawleo Capabilities

| REST Endpoint | MCP Tool | Wrapper Method | Required Params | Documented Cost / Notes |
|---|---|---|---|---|
| `/search` | `search_web` | `client.search` | `query` | 10 credits per page via `max_pages`; example-only `count` behavior is not specified in Crawleo docs. |
| `/google-search` | `google_search` | `client.googleSearch` | `q` | 10 credits per request; documented endpoint is absent from the local OpenAPI snapshot. |
| `/google-maps` | `google_maps` | `client.googleMaps` | `q` | Endpoint docs say 30 credits per request; MCP overview says 10 credits per request. Preserve this as a source conflict. |
| `/crawl` | `crawl_web` | `client.crawl` | `urls` | 1 credit per URL when `render_js=false`; 10 credits per URL when `render_js=true`. |
| `/headful-browser` | `headful_browser` | `client.headfulBrowser` | `urls` | 50 credits per URL; failed requests cost 0 credits; documented endpoint is absent from the local OpenAPI snapshot. |

Validation is intentionally bounded to the contract. The wrapper checks required parameters and explicit documented enums such as `device`, Google Search `type` and `tbs`, and Headful Browser `output_format`. It does not invent undocumented limits.

## Error Handling

The package exports `CrawleoError` and `CRAWLEO_ERROR_CODES` for stable diagnostics.

```js
import { CrawleoError, CRAWLEO_ERROR_CODES } from 'openclaw-crawleo-skill';

try {
  await client.googleSearch({ q: 'AI agents', type: 'videos' });
} catch (error) {
  if (error instanceof CrawleoError) {
    console.error(error.toJSON());
  }
}
```

Stable error codes include:

| Code | Meaning |
|---|---|
| `CRAWLEO_CONFIG_MISSING_API_KEY` | Live call attempted without an API key. |
| `CRAWLEO_CONFIG_MISSING_FETCH` | No `fetch` implementation is available. |
| `CRAWLEO_VALIDATION_ERROR` | Wrapper input failed documented required-field or enum validation. |
| `CRAWLEO_HTTP_BAD_REQUEST` | Crawleo returned HTTP 400. |
| `CRAWLEO_HTTP_AUTH` | Crawleo returned HTTP 401. |
| `CRAWLEO_HTTP_PAYMENT_REQUIRED` | Crawleo returned HTTP 402, typically insufficient credits. |
| `CRAWLEO_HTTP_FORBIDDEN` | Crawleo returned HTTP 403, such as inactive account or expired subscription. |
| `CRAWLEO_HTTP_RATE_LIMIT` | Crawleo returned HTTP 429. |
| `CRAWLEO_HTTP_UPSTREAM` | Crawleo returned a 5xx or otherwise unmapped HTTP failure. |
| `CRAWLEO_RESPONSE_MALFORMED_JSON` | Crawleo returned a successful response that could not be parsed as JSON. |
| `CRAWLEO_TRANSPORT_ERROR` | Fetch failed before an HTTP response was received. |

`CrawleoError.toJSON()` includes structured fields such as `code`, `endpoint`, `status`, `field`, and redacted `details`. It must not include raw API key values.

## Offline Verification

Run the default offline checks:

```bash
npm test
npm run verify:contracts
npm run verify:examples
npm run verify:scaffold
```

These commands must not call `https://api.crawleo.dev`, require `CRAWLEO_API_KEY`, or consume Crawleo credits.

Optional live smoke tests are available but are disabled unless both variables are present:

```bash
CRAWLEO_API_KEY=... CRAWLEO_ENABLE_LIVE_TESTS=1 npm run test:live
```

Without both variables, `npm run test:live` skips the live test and exits successfully.

## Optional Crawleo MCP Companion

Crawleo documents an MCP endpoint at:

```text
https://api.crawleo.dev/mcp
```

This package uses REST wrappers as the primary execution path. MCP setup is optional companion context, not the primary implementation path for this milestone.

## Contract and Ambiguity Policy

Use `contracts/crawleo-endpoints.json` as the implementation source of truth. Crawleo endpoint-specific docs take precedence over the local OpenAPI snapshot when the OpenAPI snapshot omits a documented endpoint.

When a default, limit, parameter, error table, or response field is unclear, write `not specified in Crawleo docs` rather than inventing behavior.

Known source issues preserved from the contract inventory:

- `/google-search` and `/headful-browser` are documented by endpoint docs but absent from the local OpenAPI snapshot.
- Google Maps cost differs by source: endpoint docs say 30 credits per request; MCP overview says 10 credits per request.
- `/search` examples include `count`, but the visible parameter table does not document it.

## Development Roadmap

- S02: package scaffold, metadata, README, and offline scaffold verification.
- S03: Crawleo REST client and endpoint wrappers with offline tests.
- S04: complete user documentation, examples, and endpoint coverage checklist.
- S05: offline wrapper tests and optional live-test gating.
- S06: final package integration proof.
