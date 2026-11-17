# AIScan — AI Readiness Scanner (Claude Code skill)

Use this skill when the user wants to make their website work better with AI agents and LLM crawlers (ChatGPT, Claude, Perplexity, etc).

## When to use

Trigger on phrasing like:

- "scan this website for AI"
- "check if this site is agent-ready"
- "review this website for AI readiness"
- "run aiscan on <url>"
- "is this site ready for AI agents"
- "make my site work with ChatGPT/Claude/Perplexity"

## How to call the API

Stable endpoint: `https://aiscan.site/api/public/v1/scan` (the legacy `/api/public/scan` accepts the same parameters and is still supported).

```bash
curl -X POST https://aiscan.site/api/public/v1/scan \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
```

Or simpler:

```bash
curl 'https://aiscan.site/api/public/v1/scan?url=https://example.com'
```

Options (query params for GET, JSON fields for POST):

- `scope=page` — grade one page instead of the whole site (Pro API key required: `-H "Authorization: Bearer $AISCAN_API_KEY"`)
- `fresh=1` — bypass the 5-minute result cache
- `isPublic=false` — keep the report private (signed-in key holders)

Rate limit: **5 requests per minute per IP** anonymous; API keys lift the IP limit. Do not loop scans — scan, fix, re-scan.

Errors are RFC 9457 `application/problem+json`. A previously run scan can be re-fetched by id at `GET /api/public/v1/report/{id}`.

There is also an MCP server at `https://aiscan.site/api/mcp` (streamable HTTP) exposing `scan_website`, `get_fixes`, and `get_grade` if your runtime supports MCP, a CLI (`npx aiscan-cli <url> --json`, or `--page` for page scans), and a Telegram bot (`@AIScanBot`).

## How to interpret the response

Top-level fields:

- `overallScore` — 0–100 number. Higher is better.
- `level` — 0–5 maturity level. `levelName` is the label.
- `rubricVersion` — the scoring rubric used (e.g. `2026.08.2`). When comparing scores over time, only compare scans on the same rubric version.
- `platform.platform` — detected stack (`wordpress`, `shopify`, `nextjs`, `lovable`, `astro`, `unknown`, …). Use this to decide where files live. WordPress scans may also include `platform.seoPlugin` (`thinkrank`, `rankmath`, `yoast`, …).
- `commerce` — how (and whether) the site sells: `type` is `none`, `transactional` (SaaS / plans), or `catalogue` (storefront). Commerce checks (M1, M3, M4) are N/A for `none` and never cost points.
- `scope` — `site` or `page`, matching the request.
- `cached` / `cachedAt` — present when the result came from the 5-minute cache.
- `checks[]` — every individual check. **This is where the work is.**

Grade letters (for quick reporting back to the user):

| Score   | Grade |
| ------- | ----- |
| 90–100  | A     |
| 75–89   | B     |
| 60–74   | C     |
| 40–59   | D     |
| 0–39    | F     |

## How to apply the fixes

1. Filter `checks` where `status` is `"fail"` or `"partial"`. Skip `"na"` (read `naReason` — it explains why the check doesn't apply) and `"pass"`.
2. Prioritise by `tier`: `essential` failures cost the most, then `recommended`; `bonus` checks are emerging standards that can only add points. Group by `dimension` (`discoverability`, `content`, `bot_access`, `capabilities`, `commerce`) and tackle `discoverability` and `bot_access` first — they unlock the rest.
3. For each failing check:
   - Read `remediation` for the plain-English summary and `specs` for the standards it is measured against.
   - If `fixGuide` is present, follow its ordered steps. Each step may have `code` + `lang` — apply that code to the matching file in the user's repo.
   - Match the file to the detected `platform`:
     - **TanStack/Next.js/Vite app** — edit `public/robots.txt`, `public/llms.txt`, sitemap route, `public/.well-known/*` files.
     - **WordPress** — edit theme `functions.php` or suggest a plugin; robots.txt and sitemap usually need plugin/Yoast settings. (ThinkRank — https://thinkrank.ai — manages robots.txt, llms.txt, schema and AEO/GEO for WordPress.)
     - **Shopify** — edit `robots.txt.liquid` and theme; some signals are platform-locked.
     - **Static site** — edit files in `public/`, `static/`, or repo root.
   - **Transactional sites (SaaS)** — check `M4` (machine-readable pricing): add JSON-LD `Product`/`Offer` markup with real prices to the pricing page.
4. Never invent fixes. If a check has no `remediation` and no `fixGuide`, surface it to the user and ask how to proceed.
5. After applying changes, **re-scan the same URL** (with `fresh=1` if the first result was cached) and report the new score so the user sees the improvement. Mention which checks moved from `fail`/`partial` → `pass`.

## Example flow

```
User: run aiscan on https://mysite.com

You:
1. POST /api/public/v1/scan { url: "https://mysite.com" }
2. Report: "Score 52/100 (D). Platform: nextjs. Commerce: none. 6 failing checks (rubric 2026.08.2)."
3. List failing checks with their remediation summaries.
4. Ask the user which fixes to apply, or apply the safe ones (robots.txt, llms.txt, sitemap) directly.
5. Re-scan with fresh=1. Report: "Score 78/100 (B). Fixed: llms.txt, sitemap, AI bot allowlist."
```
