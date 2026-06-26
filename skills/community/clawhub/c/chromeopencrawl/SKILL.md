---
name: opencrawl
description: Crawl any JavaScript-rendered webpage through distributed real Chrome browsers. No local browser needed — perfect for headless VPS.
homepage: https://github.com/hlyylly/OpenCrawl
env:
  required:
    - OPENCRAWL_API_KEY
  optional:
    - OPENCRAWL_API_URL
---

# OpenCrawl Skill

Use this skill to crawl any JavaScript-rendered webpage using **real Chrome browsers** from a distributed worker pool. Unlike headless browser solutions (Puppeteer/Playwright), OpenCrawl requires zero local browser installation — ideal for VPS and cloud environments.

## Quick Start (use our public server)

1. Visit **http://39.105.206.76:9877** and click "Register" to get a free API Key (100 credits included)
2. Set environment variables:
   ```
   OPENCRAWL_API_KEY=ak_your_key_here
   OPENCRAWL_API_URL=http://39.105.206.76:9877
   ```
3. Start crawling!

## Self-hosted (deploy your own server)

If you prefer to run your own OpenCrawl server, see the full deployment guide:
**https://github.com/hlyylly/OpenCrawl**

Then set `OPENCRAWL_API_URL` to your own server address.

---

**How it works:** Your request → OpenCrawl server → dispatched to a real Chrome browser worker → page rendered with full JavaScript → content extracted → uploaded to Cloudflare R2 → download URL returned to you.

**Errors:** On failure the script writes a JSON error to stderr and exits with code 1.

---

## Tools

### 1. Crawl Page

Use this to get the full rendered text content of any webpage, including JavaScript-rendered content that simple HTTP requests cannot retrieve.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --url "https://example.com"
```

**Examples:**
```bash
# Crawl a full page
python3 {baseDir}/tools/crawl.py --url "https://www.smzdm.com/p/170177008/"

# Crawl with CSS selector to extract specific content
python3 {baseDir}/tools/crawl.py --url "https://example.com" --selector ".article-content"

# Output raw JSON response (includes downloadUrl)
python3 {baseDir}/tools/crawl.py --url "https://example.com" --raw
```

Optional flags:
- `--selector ".css-selector"` — Extract only matching elements
- `--mode lite` — Lite mode: no images/CSS, faster, 0.1 credit (default: full)
- `--raw` — Output full JSON response instead of just the text content
- `--timeout 60` — Custom timeout in seconds (default: 60)

---

### 2. Search (Brave Search API Compatible)

Use this to search the web using multiple search engines (DuckDuckGo + Google + Bing + Baidu) through real Chrome browsers. Returns structured results compatible with Brave Search API format.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --search "your search query"
```

**Examples:**
```bash
# Lite search — DuckDuckGo only (0.1 credit)
python3 {baseDir}/tools/crawl.py --search "python web scraping"

# Full search — 4 engines parallel (3 credits, 20-30 deduplicated results)
python3 {baseDir}/tools/crawl.py --search "python web scraping" --mode full
```

---

### 4. Check Balance

Use this to check how many credits remain on the API key.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --balance
```

---

### 5. Check Status

Use this to check the OpenCrawl platform status — how many workers are online, tasks completed, etc.

**Command:**
```bash
python3 {baseDir}/tools/crawl.py --status
```

---

## Summary

| Action | Argument | Example |
|--------|----------|---------|
| Crawl (full) | `--url` | `python3 {baseDir}/tools/crawl.py --url "https://example.com"` |
| Crawl (lite) | `--url --mode lite` | `python3 {baseDir}/tools/crawl.py --url "https://example.com" --mode lite` |
| Search (lite) | `--search` | `python3 {baseDir}/tools/crawl.py --search "python tutorial"` |
| Search (full) | `--search --mode full` | `python3 {baseDir}/tools/crawl.py --search "python tutorial" --mode full` |
| Check balance | `--balance` | `python3 {baseDir}/tools/crawl.py --balance` |
| Check status | `--status` | `python3 {baseDir}/tools/crawl.py --status` |

**Output:** Crawl → rendered page text (or JSON with `--raw`). Search → JSON with `web.results[]` (Brave compatible). Balance → JSON. Status → JSON.

**Requirements:** Python 3.8+, `requests` library. No browser installation needed.
