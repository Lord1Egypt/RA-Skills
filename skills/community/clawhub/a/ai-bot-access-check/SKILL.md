---
name: ai-bot-access-check
description: Check whether AI crawlers and search bots (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Googlebot, Google-Extended, bingbot, Applebot-Extended, CCBot) can reach a web page, and whether robots.txt or the server/firewall blocks each one. Use when someone asks why ChatGPT, Claude, Perplexity or Google AI Overviews cannot see, read or cite their site, asks to audit robots.txt for AI bots, or wants to know if their host or Cloudflare blocks AI crawlers.
license: MIT
metadata:
  author: Mantas Tamošaitis
  homepage: https://seopaslaugos.io/en/tools/ai-bot-access-checker
  version: 1.3.0
---

# AI bot access check

Free public API, no key. One request checks 13 crawlers against one page.

## Run the check

```bash
curl -s "https://tools.seopaslaugos.io/v1/check?url=<page>&format=text"
```

- `<page>` can be a bare domain (`example.com`) or a full URL (`https://example.com/pricing`). URL-encode it if it has a query string.
- Add `&bots=GPTBot,ClaudeBot` to check a subset.
- Drop `&format=text` to get JSON (fields: `baseline`, `robotsTxt`, `bots[]` with `robots.allowed`, `robots.rule`, `server.verdict`, `server.status`, `server.note`, `access`).
- Limit: 20 checks a minute per IP; the same URL is cached for 10 minutes.

If the agent supports MCP, the same check is the `check_ai_bot_access` tool on `https://tools.seopaslaugos.io/mcp` (Streamable HTTP).

## Read the result

Each bot gets one `access` value:

| access | Meaning | What to tell the user |
|---|---|---|
| `allowed` | robots.txt allows it and the server answers it like a browser | Nothing to fix for this bot |
| `blocked_by_robots` | A Disallow rule applies; `robots.rule` and `robots.group` show which | Edit robots.txt if the block is not intended. If `robots.vendorNote` is set (ChatGPT-User, Perplexity-User), say the vendor may still fetch the page |
| `blocked_by_server` | robots.txt allows it, but the server or firewall refuses the User-Agent (403, 429, dropped connection, challenge/captcha page) | Fix it at the host/CDN: security rules (ModSecurity), rate limits, Cloudflare AI crawler settings. robots.txt changes will not help |
| `inconclusive` | The firewall also refuses a fake Googlebot, so it verifies crawler IPs | Cannot be decided from outside: check the firewall's bot settings or logs, and URL Inspection in Search Console / Bing Webmaster Tools |
| `suspicious` | HTTP 200 but a much smaller response than a browser gets | Open the page as that bot and look for a stripped or block page |
| `page_error` | A normal browser fails too | The page itself is broken or blocks datacenter traffic |

If `robots.source` is `cloudflare_managed`, the rule was added by Cloudflare's Managed robots.txt, not the site's file: tell the user to change it in the Cloudflare dashboard.

Also report `baseline.noindex` when it is true: a noindex page is excluded from Google results regardless of bot access.

## Which bots matter for what

- Citations in ChatGPT: OAI-SearchBot (ChatGPT search). ChatGPT-User fetches pages live when a user asks; OpenAI says robots.txt may not apply to it.
- Citations in Claude: Claude-SearchBot, Claude-User.
- Citations in Perplexity: PerplexityBot. Perplexity-User fetches live; Perplexity says it generally ignores robots.txt.
- Google AI Overviews and AI Mode: Googlebot. Google-Extended only controls Gemini use and does not remove a site from Search.
- Training only: GPTBot, ClaudeBot, CCBot, Google-Extended, Applebot-Extended. Blocking these does not stop search citations.

## Limits to state honestly

Requests come from Cloudflare with each bot's published User-Agent, not from the vendors' IP ranges. That catches robots.txt rules and User-Agent blocks (most hosting firewalls). Firewalls that verify crawler IPs show up as `inconclusive`; do not report them as confirmed blocks.

## About

Built and maintained by Mantas Tamošaitis, an SEO specialist in Lithuania who works on AI search visibility for service businesses and e-shops. Web version and docs: [AI Bot Access Checker](https://seopaslaugos.io/en/tools/ai-bot-access-checker). More about AI search work: [seopaslaugos.io](https://seopaslaugos.io/en).
