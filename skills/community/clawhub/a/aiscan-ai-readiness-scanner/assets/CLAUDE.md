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

Endpoint: `https://aiscan.site/api/public/scan`

```bash
curl -X POST https://aiscan.site/api/public/scan \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
```

Or simpler:

```bash
curl 'https://aiscan.site/api/public/scan?url=https://example.com'
```

Rate limit: **5 requests per minute per IP.** Do not loop scans — scan, fix, re-scan.

There is also an MCP server at `https://aiscan.site/api/mcp` exposing `scan_website`, `get_fixes`, and `get_grade` tools if your runtime supports MCP HTTP.

## How to interpret the response

Top-level fields:

- `overallScore` — 0–100 number. Higher is better.
- `level` — 0–5 maturity level. `levelName` is the label.
- `platform.platform` — detected stack (`wordpress`, `shopify`, `nextjs`, `lovable`, `unknown`, …). Use this to decide where files live.
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

1. Filter `checks` where `status` is `"fail"` or `"partial"`. Skip `"na"` and `"pass"`.
2. Group by `dimension` (`discoverability`, `content`, `bot_access`, `capabilities`, `commerce`) and tackle `discoverability` and `bot_access` first — they unlock the rest.
3. For each failing check:
   - Read `remediation` for the plain-English summary.
   - If `fixGuide` is present, follow its ordered steps. Each step may have `code` + `lang` — apply that code to the matching file in the user's repo.
   - Match the file to the detected `platform`:
     - **TanStack/Next.js/Vite app** — edit `public/robots.txt`, `public/llms.txt`, sitemap route, `public/.well-known/*` files.
     - **WordPress** — edit theme `functions.php` or suggest a plugin; robots.txt and sitemap usually need plugin/Yoast settings.
     - **Shopify** — edit `robots.txt.liquid` and theme; some signals are platform-locked.
     - **Static site** — edit files in `public/`, `static/`, or repo root.
4. Never invent fixes. If a check has no `remediation` and no `fixGuide`, surface it to the user and ask how to proceed.
5. After applying changes, **re-scan the same URL** and report the new score so the user sees the improvement. Mention which checks moved from `fail`/`partial` → `pass`.

## Example flow

```
User: run aiscan on https://mysite.com

You:
1. POST /api/public/scan { url: "https://mysite.com" }
2. Report: "Score 52/100 (D). Platform: nextjs. 6 failing checks."
3. List failing checks with their remediation summaries.
4. Ask the user which fixes to apply, or apply the safe ones (robots.txt, llms.txt, sitemap) directly.
5. Re-scan. Report: "Score 78/100 (B). Fixed: llms.txt, sitemap, AI bot allowlist."
```
