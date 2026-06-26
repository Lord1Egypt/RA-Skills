---
name: free-web-search-js
description: Web search & content fetching via Playwright + HTTP — zero API keys. Searches Bing CN (domestic) or DDG (international), auto-fetches top page contents. For real-time search, fact-checking, news, tutorials, documentation lookup.
version: 29.1.0
license: MIT
author: free-web-search-js
trigger_keywords:
  - search
  - find
  - look up
  - 搜索
  - 查一下
  - 找一下
tools:
  - name: search
    description: Search + auto-fetch; Bing CN via Playwright, DDG via HTTP
    script: scripts/search.js
    parameters:
      query:
        type: string
        description: "Search query"
        required: true
      max:
        type: integer
        description: "Max results 1-30, default 10"
        required: false
      region:
        type: string
        description: "Region: auto/cn/intl, defaults to auto (IP detection)"
        required: false
  - name: fetch
    description: Fetch page content by URL, HTTP first with headed fallback
    script: scripts/fetch.js
    parameters:
      urls:
        type: string
        description: "URLs to fetch, space-separated"
        required: true
      max-len:
        type: integer
        description: "Max chars per page, default 12000"
        required: false
---

# free-web-search-js

Pure search — no rewriting, no filtering, noise handled by the AI. Uses real browser automation (Playwright) for Bing CN anti-bot, with HTTP fallback for international queries. Zero API keys required.

## Quick start

```bash
# Search (auto-fetches top 3 page contents)
node scripts/search.js "silver price"
node scripts/search.js "how to deploy docker" --max=5
node scripts/search.js "xxx" --region=cn
node scripts/search.js "xxx" --fetch=5         # fetch top 5
node scripts/search.js "xxx" --no-fetch        # search only

# Fetch specific URLs
node scripts/fetch.js "https://example.com/page1" "https://example.com/page2"
```

## Architecture

```
Domestic (CN IP):
  Playwright headless → Bing CN → home page for cookie → search box submit
  → 0 results? fallback to DDG HTML
  → auto-fetch top N page contents

International:
  Pure HTTP → DDG HTML parse
  → fetch fails? fallback to Playwright request
  → DDG empty? fallback to Bing
  → auto-fetch top N page contents
```

## Install

All dependencies are installed upfront by the setup script. **The skill never runs `npm install` or `pip install` at runtime.** This avoids audit flags and supply-chain risks.

### Prerequisites

| Dependency | Purpose | Size |
|---|---|---|
| Node.js >= 18 | Runtime | — |
| cheerio | HTML parsing | small |
| commander | CLI arg parsing | small |
| iconv-lite | GBK charset conversion | small |
| playwright | Browser automation | ~50 MB |
| Chromium (Playwright) | Browser engine for Bing search + headed fetch | ~150 MB |

### One-command setup

```bash
# Linux / macOS
bash scripts/setup.sh

# Windows
powershell -File scripts/setup.ps1
```

The scripts auto-detect region and use `npmmirror.com` mirrors inside China for faster downloads.

### Manual install

```bash
cd skills/free-web-search-js
npm install
npx playwright install chromium    # ~150 MB

# Verify
node scripts/check-env.js
```

If you already have Chrome/Chromium installed:

```bash
export CHROMIUM_EXECUTABLE_PATH="/path/to/chrome"
node scripts/check-env.js
```

`check-env.js` will confirm whether the provided executable is usable.

### Environment variables

| Variable | Purpose |
|---|---|
| `CHROMIUM_EXECUTABLE_PATH` | Path to system Chrome/Chromium, skips 150 MB download |
| `PLAYWRIGHT_DOWNLOAD_HOST` | Mirror for Chromium download (auto-set by setup script) |
| `BROWSER_DAEMON_IDLE_MS` | Daemon idle timeout in ms (default 600000 = 10 min) |

## Search engines

| Engine | Method | Region | Notes |
|---|---|---|---|
| Bing CN | Playwright search box submit | Domestic | Visits home page first for cookie, then types into search box |
| DDG | Playwright search box submit | International | Full browser automation |

### Strategy

| Region | Search | Fetch |
|---|---|---|
| Domestic | Bing CN, fallback DDG | Auto-fetch top 3 |
| International | DDG HTML, fallback Playwright request; DDG empty→Bing | Auto-fetch top 3 |

### IP detection

On each search, three probes run in parallel — first responder wins:

| Probe | Service | Logic |
|---|---|---|
| 1 | `myip.ipip.net` / `cip.cc` | Reachable from China |
| 2 | `ipinfo.io` / `ipapi.co` | International |
| 3 | `cn.bing.com` | Reachable → likely CN |
| Fallback | — | Defaults to domestic |

Override with `--region=cn` or `--region=intl` if your proxy causes misdetection.

## Fetch mode

After search, auto-fetches the top N results (default 3).

| Tier | Method | Speed | Notes |
|---|---|---|---|
| 1 | Lightweight HTTP + cheerio | Fast | No browser launch |
| 2 | Playwright headed | Slower | Full JS rendering |

Tier 1 enhancements:
- JSON API response detection with structured content extraction
- JSON-LD (`<script type="application/ld+json">`) articleBody/description
- `__NEXT_DATA__` embedded data extraction
- Meta tag fallback (og:description / description)
- Auto GBK charset detection & conversion

## Deduplication

Smart dedup: domain + path stem (ignores www/m subdomains, tracking params, trailing slash, .html suffix). Bing redirect URLs (`bing.com/ck/`) auto-decoded.

## Browser daemon (optional, ~70% faster)

Avoid 1.5s+ browser launch overhead by reusing a persistent Chromium instance:

```bash
node scripts/browser-daemon.js            # Start (run with & or as background job)
node scripts/browser-daemon.js --status   # Show status
node scripts/browser-daemon.js --stop     # Stop
```

The daemon auto-exits after **10 minutes of inactivity** (configurable via `BROWSER_DAEMON_IDLE_MS`). Activity is tracked via a `.browser-heartbeat` file that `search.js` and `fetch.js` touch on each connection. The daemon checks the heartbeat every 60 seconds.

## Verification & troubleshooting

```bash
cd skills/free-web-search-js
node scripts/check-env.js
node scripts/search.js "OpenClaw" --max 2 --region cn --fetch 0
node scripts/search.js "OpenClaw" --max 2 --region intl --fetch 0
```

Common issues:
- `node_modules not found` → run `npm install`
- `Executable doesn't exist ...` → run `bash scripts/setup.sh` or set `CHROMIUM_EXECUTABLE_PATH`
- `browserType.launch ... closed` → headless+no-sandbox is default; run `node scripts/check-env.js` to diagnose
- 0 search results → try `--region=cn` / `--region=intl`, or `--fetch 0` to test search alone

## Privacy & network

- Searches connect to Bing CN / DDG HTML / Sogou directly from the skill's runtime — no intermediate proxy
- The daemon heartbeat file (`.browser-heartbeat`) and endpoint file (`.browser-endpoint`) are written to the skill root directory
- No analytics, no telemetry, no third-party logging beyond the search engine's own server logs
- Headed warm-up fetches: Cookie warm-up for Bing uses a headed browser context to obtain session cookies from the search engine home page; no cookies are persisted to disk between sessions

## Known limitations

- **First domestic search slower**: Chromium cold start takes 3–6s; daemon avoids this
- **Bing CN instant answers**: Weather/calculator cards don't use `li.b_algo`, return 0 results
- **Sogou HTTP unstable**: No cookie, easily blocked by anti-crawl
- **JS-required pages**: HTTP tier returns empty for SPA pages — headed tier catches them
- **Region-specific sites**: Some domestic sites time out from international IPs
- **Proxy interference**: IP detection may misclassify behind proxies — use `--region` to override
- **DDG blocked in China**: DDG HTML is not reachable from mainland China; domestic strategy avoids it
