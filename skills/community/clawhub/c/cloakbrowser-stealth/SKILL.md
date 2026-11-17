---
name: cloakbrowser-stealth
description: Stealth browser automation using CloakBrowser to bypass bot detection on protected sites. Use when web_fetch fails with anti-bot blocks, CAPTCHA, or access denied errors. Use for scraping reviews, protected pages, or any site that blocks standard Playwright/Puppeteer automation. Not for sites requiring login credentials or solving interactive CAPTCHAs.
---

# CloakBrowser Stealth Fetch

## Quick Start

Fetch content from a protected site:

```bash
cd ~/.openclaw/workspace/skills/cloakbrowser-stealth/scripts
python3 fetch.py "https://example.com" --wait-ms 3000
```

## Common Patterns

### Extract specific elements
```bash
python3 fetch.py "URL" --selector "[data-testid='review-title']" --output text
```

### Full page with screenshot
```bash
python3 fetch.py "URL" --wait-ms 4000 --screenshot /tmp/page.png --output json
```

### Humanize for aggressive detection
```bash
python3 fetch.py "URL" --humanize --wait-ms 5000
```

### JSON output for structured processing
```bash
python3 fetch.py "URL" --output json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['text'][:500])"
```

## When It Works / When It Doesn't

**Use CloakBrowser when:**
- `web_fetch` returns 403, bot challenge, or empty body
- Target uses standard fingerprint detection (WebDriver, plugins, WebGL)
- Reviews, public listings, non-login content

**Don't use when:**
- Site requires login (use session cookies instead)
- Interactive CAPTCHA (hCaptcha, reCAPTCHA v2 checkbox)
- IP-reputation blocks (use proxy, see references/config.md)
- Rate-limited after repeated requests

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success, content extracted |
| 1 | Anti-bot blocked (check output for "blocked: true") |
| 2 | Navigation timeout or error |
| 3 | Script/dependency error |

## Script Reference

- `scripts/fetch.py` — Unified fetch wrapper with anti-bot detection, element extraction, screenshot, JSON/text/html output

For full configuration options, proxy setup, and target site status: see `references/config.md`
