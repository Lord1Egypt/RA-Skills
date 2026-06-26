---
name: view-stats
description: Show page-view counts and day-by-day trends for the user's Clawpage pages. Use when the user asks "how many views has my page got", "what's my traffic", "which page is most popular". Covers public named pages, user home page, and short-link clicks. Privacy: only timestamp + page are tracked; no IP, UA, or geo.
---

# view-stats

Clawpage keeps minimal, privacy-respecting view counts (L1):
- Tracked: `<user>.clawpage.ai/p/<name>`, `<user>.clawpage.ai/`, `clawpage.ai/s/<slug>`
- Not tracked: preview domain, /api/*, landing, feedback, bot UAs
- Stored fields: just timestamp and pageKey — no identity signals

> **Management pages:** if embedding stats in a pagecode-protected management page, use `c.stats` from the Clawpage JS SDK — see `${CLAUDE_SKILL_DIR}/use-sdk/SKILL.md`. Raw `fetch('/api/stats/...')` in page JS is forbidden.

Run from any directory with `keys.local.json`:

### Overview (all pages, sorted by total desc)
```bash
npx -y @clawpage.ai/cli stats --overview
```
Returns total views + per-page { total, last7, last30 }.

### Single page daily series
```bash
npx -y @clawpage.ai/cli stats --page hello --days 30      # p:hello
npx -y @clawpage.ai/cli stats --home --days 7             # user home
npx -y @clawpage.ai/cli stats --link aB3kFq9 --days 30    # short link
```

`--days` default 30, max 365. `series` covers the full window (missing days filled with 0).

## What gets counted

- 2xx responses only (404s / errors never count)
- UA-based bot filter: `bot|crawler|spider|curl|wget|headless|scrap|preview|fetch|python-requests|java/|go-http-client|okhttp|httpclient` → skipped
- Empty / missing User-Agent → skipped (treated as bot)

⚠️ Implication: curl / scripted hits will NOT be counted. Open the URL in a real browser to test analytics.

## Error codes

| Code | HTTP | Fix |
|---|---|---|
| `STATS_PAGE_NOT_FOUND` | 404 | No views ever recorded; check the page name / slug is right and that someone actually visited it |
| `INVALID_QUERY` | 400 | `--days` must be integer 1-365 |
| `PERMISSION_DENIED` | 403 | Token doesn't belong to the user subdomain — fix `keys.local.json` |

## Why only L1?

L1 = just timestamp + page. No IP, UA, geo, referer. Means:
- Cannot tell unique visitors, geography, source
- Zero privacy concerns, zero GDPR compliance cost, zero UA-sniffing needed
- Cheap to store (~1 MB per user per year)

L2/L3 (hashed IP, UA, geo) may come later if needed — would require opt-in consent flows.
