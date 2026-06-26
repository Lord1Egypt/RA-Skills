---
name: browser-automation
description: "Browser automation via Playwright. Use when pages are JS-rendered, require user interaction (click/fill), or need screenshots. Part of the 3-layer web tool hierarchy: search (SearXNG) → extract (web_fetch) → interact (browser). This is the last resort layer."
---

# Browser Automation

## When to Use This Skill

**Trigger conditions:**
- `web_fetch` returned empty, garbled, or incomplete content
- Target page is JavaScript-rendered (React/Vue/Angular SPAs)
- Need to interact with UI: click buttons, fill forms, navigate flows
- Need a screenshot of a page's current rendered state
- Multi-step flows: login → navigate → scrape
- Extracting structured data from dynamically loaded content

**Do NOT use this skill when:**
- Page is static HTML — `web_fetch` is faster
- Only need to find a URL — `web_search` is the right first step
- You need API data — check if the site has a public API first
- The page requires authentication you don't have

## The 3-Layer Web Tool Hierarchy

```
Layer 1 — Search:    web_search → find URLs
Layer 2 — Extract:   web_fetch → get page content (static pages only!)
Layer 3 — Interact:  browser.py → JS rendering, interaction, screenshots
```

Always try Layer 1 and 2 before reaching for browser automation.

---

## Setup Check

```bash
python3 skills/browser-automation/scripts/init.py
```

Should return `{"ready": true}`. If not, Playwright needs installation.

---

## Scripts

All scripts exit with code 0 on success, 1 on usage error, 2 on browser error.

### screenshot.py — Capture a page

```bash
python3 skills/browser-automation/scripts/screenshot.py <url> [path]
# Default path: /tmp/screenshot.png
```

Returns: `{success, saved, title}`

### scrape.py — Get rendered HTML

```bash
python3 skills/browser-automation/scripts/scrape.py <url>
```

Returns: `{success, title, url, html}` (html truncated to 50k chars)

### extract.py — Pull structured data

```bash
python3 skills/browser-automation/scripts/extract.py <url> <selector>
```

CSS selector targets elements. Extracts up to 50 elements, each with `text`, `href`, `src`, `alt`.

Returns: `{success, count, selector, items[]}`

### interact.py — Click and fill

```bash
# Click
python3 skills/browser-automation/scripts/interact.py click <selector> [url]

# Fill input
python3 skills/browser-automation/scripts/interact.py fill <selector> <value> [url]

# Hover
python3 skills/browser-automation/scripts/interact.py hover <selector> [url]
```

If `url` is provided, navigates there first. Returns: `{success, action, selector, title, url}`

---

## Reference Docs

- `references/selectors.md` — CSS selector syntax and common patterns
- `references/patterns.md` — Login flows, search pagination, infinite scroll, stealth mode, error recovery

---

## Examples

### JS-rendered page (would fail web_fetch)
```bash
# web_fetch gives nothing on HN — use extract
python3 scripts/extract.py "https://news.ycombinator.com" ".titleline > a"
```

### Screenshot a page
```bash
python3 scripts/screenshot.py "https://site.com/dashboard" "/tmp/dashboard.png"
```

### Form login flow
```bash
python3 scripts/interact.py fill "#username" "user@example.com" "https://site.com/login"
python3 scripts/interact.py fill "#password" "secret123"
python3 scripts/interact.py click "button[type=submit]"
python3 scripts/scrape.py "https://site.com/dashboard"
```

### Get structured data from a list
```bash
python3 scripts/extract.py "https://jobs.site.com/postings?q=engineer" ".job-listing h2"
```

---

## Quick Reference

| Task | Command |
|---|---|
| Screenshot | `screenshot.py <url> [path]` |
| HTML | `scrape.py <url>` |
| Data | `extract.py <url> <selector>` |
| Click | `interact.py click <selector> [url]` |
| Fill | `interact.py fill <selector> <value> [url]` |
| Setup check | `init.py` |

---

## Skill Metadata

- **Scripts:** `init.py`, `screenshot.py`, `scrape.py`, `extract.py`, `interact.py`
- **References:** `selectors.md`, `patterns.md`
- **Requires:** Playwright (`pip install playwright && playwright install chromium`)
- **Exit codes:** 0=success, 1=usage error, 2=browser error
