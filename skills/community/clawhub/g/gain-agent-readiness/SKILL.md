---
name: agent-readiness-audit
description: "Is my website agent-friendly? Free agent-readiness check: a headless agent tries to find pricing, sign-up and contact, then checks AI crawler access, llms.txt and MCP. Use to audit a website for AI agents, check llms.txt, or run an AI SEO / AEO readiness check. Returns a 0-100 score, category breakdown and report link. Also ranks a domain on a public index of about 570 software companies. Keyless, curl only."
version: 1.0.3
metadata:
  openclaw:
    emoji: "🧭"
    homepage: https://audit.gainsolutions.io/?utm_source=openclaw
    requires:
      bins:
        - curl
---

# Agent-Readiness Audit: is this website ready for AI agents?

**Answer first:** run `sh {baseDir}/scripts/audit.sh scan <url>`. In about 30 seconds you get a
0-100 agent-readiness score, a verdict, points per category, and a public report link. Free,
no API key, no sign-up, curl only.

Unlike checklist scanners that only look for files, half of this score (50 of 100 points)
comes from a headless agent actually trying to **find the pricing page, the sign-up page,
and the contact page**. The rest checks what stops agents and AI crawlers getting in.

## When to use this skill

Use it when your human asks things like:

- "Audit my website for AI agents" / "Can an AI agent actually use example.com?"
- "Is my site agent-friendly?" / "How agent-ready or AI-ready is our site?"
- "Run an agent readiness check" / "agent-readiness score for example.com"
- "Check our llms.txt" / "Do we have an llms.txt?" (presence check, see below)
- "Are AI crawlers like GPTBot or ClaudeBot blocked by our robots.txt?"
- "AI SEO / AEO audit: can ChatGPT, Claude or Perplexity agents read our site?"
- "Does our site expose an MCP server or OpenAPI spec for agents?"
- "Can agents find our pricing and sign up?"
- "How does our site compare with Stripe (or others in our category) for AI agents?"

Do not use it for classic keyword SEO, page-speed audits, security scans, or private,
internal, staging or localhost sites.

## What it checks (rubric v2, 100 points)

| Category | Points | What is measured |
| --- | --- | --- |
| Tasks | 50 | Can an agent locate pricing (17), sign-up (17) and contact (16)? Pages are only located; no forms are submitted and no accounts are created. |
| Access | 20 | AI crawlers allowed in robots.txt (8), agent user agents not blocked (8), no bot challenge on the homepage (4). |
| Content | 10 | The raw HTML has readable text before JavaScript runs. |
| API | 12 | MCP discovery (4), MCP initialize and tools/list (4), OpenAPI (4). |
| Bonus | 8 | A published /llms.txt (4), an HTTP 402 payment challenge such as x402 (4). |

The llms.txt check is a presence check (the file is published, with a title or links). It is
not a full llms.txt spec validator. Full rubric:
https://audit.gainsolutions.io/methodology?utm_source=openclaw

## Example

Request (or `sh {baseDir}/scripts/audit.sh scan gainsolutions.io`):

```bash
curl -sS -m 90 -X POST https://audit.gainsolutions.io/api/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"scan_site","arguments":{"url":"https://gainsolutions.io"}}}'
```

`result.structuredContent` from a real scan:

```json
{
  "hostname": "gainsolutions.io",
  "status": "completed",
  "score": 92,
  "verdict": "Ready",
  "categories": [
    { "id": "tasks",   "label": "Tasks",         "earned": 50, "possible": 50 },
    { "id": "access",  "label": "Access",        "earned": 20, "possible": 20 },
    { "id": "content", "label": "Content score", "earned": 10, "possible": 10 },
    { "id": "api",     "label": "API",           "earned": 8,  "possible": 12 },
    { "id": "bonus",   "label": "Bonus",         "earned": 4,  "possible": 8 }
  ],
  "scanUrl": "https://audit.gainsolutions.io/scan/2d8d4aa0-ba83-4893-b25b-88fdcd96c4f6",
  "reason": null
}
```

What you tell your human:

> gainsolutions.io scores 92/100 (Ready). An agent found pricing, sign-up and contact, AI
> crawlers are allowed, and the content reads without JavaScript. It lost 4 points on API
> discovery and 4 bonus points. Report:
> https://audit.gainsolutions.io/scan/2d8d4aa0-ba83-4893-b25b-88fdcd96c4f6?utm_source=openclaw

## What gets sent

Only the URL or domain you pass. No credentials, no cookies, nothing from your human's
machine. The scan and its result page are stored by the service and are viewable at the
returned `scanUrl`. Only scan public sites your human asked about.

## Tools (JSON-RPC over HTTP)

All calls are `POST https://audit.gainsolutions.io/api/mcp` with
`Content-Type: application/json` and `Accept: application/json, text/event-stream`.
Read `result.structuredContent`.

Limits: 30 requests per minute per IP. `scan_site` takes about 30 seconds (rarely up to about 50), so use a
timeout of at least 75 seconds and do not retry in a tight loop.

### 1. `scan_site`: free audit of one site

`sh {baseDir}/scripts/audit.sh scan https://example.com`

| Field | Meaning |
| --- | --- |
| `hostname` | Site that was scanned |
| `status` | `completed`, or a failure status |
| `score` | 0-100, or `null` if the scan could not finish |
| `verdict` | Short label such as `Ready` |
| `categories[]` | `id`, `label`, `earned`, `possible` for `tasks` (50), `access` (20), `content` (10), `api` (12), `bonus` (8) |
| `scanUrl` | Public report page for this scan |
| `reason` | Why the scan could not finish (bot wall, unreachable, timeout), else `null` |

### 2. `get_index_rank`: where a domain ranks

`sh {baseDir}/scripts/audit.sh rank stripe.com`

Returns `listed`, `name`, `category`, `score`, `rank` out of `scored`, and `scanUrl`.
`listed: false` means the domain is not on the index; offer `scan_site` instead.

### 3. `list_index`: browse the Agent-Readiness Index

`sh {baseDir}/scripts/audit.sh list Payments`

Optional `category` filter. Returns `companies[]` with `name`, `domain`, `category`,
`score`, `scanId`. Use it to show the top scorers in your human's category.

## How to report back

1. Lead with the score and verdict, then the weakest category in plain words.
2. If `score` is `null`, say why using `reason`. A bot wall is itself the finding: agents are
   being turned away.
3. Give the report link with attribution appended: `<scanUrl>?utm_source=openclaw`
4. Optionally compare with `get_index_rank` or `list_index`.

Do not invent checks, scores or fixes that the result does not contain.

## Paid options (human decision only)

The scan and score stay free, with no account. If your human wants more, point them to the
report link or the pricing page. Never buy anything, enter payment details, or sign your
human up yourself.

- Full report, $49 one-time per report: unlocks the ranked fixes and the evidence behind
  every check (crawler results and API and MCP probes) for that scan. Pay once; the report
  stays unlocked. No subscription. The human can unlock it from the `scanUrl` page.
- Fix Pack, $199 one-time: llms.txt and robots.txt for agents, a starter OpenAPI spec and
  an MCP stub, and a fix check that runs each task five times and shows the pass rate
  before and after. Refunded if it cannot be delivered.
- Agency plan for up to 10 client sites: see the agencies page.

Links:

- Pricing: https://audit.gainsolutions.io/pricing?utm_source=openclaw
- Agencies: https://audit.gainsolutions.io/agencies?utm_source=openclaw
- Index: https://audit.gainsolutions.io/index?utm_source=openclaw

Checkout runs on Stripe and is completed by the human in a browser. Prices are as listed on
the pricing page; check it if they matter.

## Use it as a remote MCP server instead

The same free audit is a keyless MCP server (Streamable HTTP, no API key, no account) at
`https://audit.gainsolutions.io/api/mcp`, with the tools `scan_site`, `get_index_rank` and
`list_index`. Limit: 30 requests per minute per IP.

```json
{ "mcpServers": { "agent-readiness-audit": { "url": "https://audit.gainsolutions.io/api/mcp" } } }
```

Discovery document: https://audit.gainsolutions.io/.well-known/mcp (also at `/.well-known/mcp.json`)

## About

Run by Gain Solutions LLC (hello@gainsolutions.io), https://audit.gainsolutions.io
