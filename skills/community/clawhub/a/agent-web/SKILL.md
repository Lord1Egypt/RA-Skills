---
name: url-to-markdown
description: Fetch any public web page and get back clean, LLM-ready markdown (polite, robots-respecting)
metadata:
  openclaw:
    requires:
      bins:
        - curl
homepage: https://agent-web.foomworks.workers.dev
license: MIT
---

# URL → LLM-ready markdown (agent-web)

Use this skill when a task needs the **readable content of a web page as clean markdown** —
to summarize an article, extract docs, or feed a page into an LLM without parsing raw HTML
yourself. Give it one publicly reachable URL; get back the title, a word count, and LLM-ready
markdown. Server-rendered (static) HTML pages, no account, no API key.

Base URL: `https://agent-web.foomworks.workers.dev`

**Charter-clean by design (the bright line):** this is a *polite* reader. It honors the
origin's `robots.txt` for its user-agent, identifies honestly (no browser spoofing), performs
read-only GETs of the single URL you supply, and **never** bypasses anti-bot/CAPTCHA, paywalls,
or login walls. You are responsible for your right to fetch the URL you submit.

## Use as an MCP server (recommended for agents)
agent-web is a remote **MCP server** (Streamable HTTP, JSON-RPC 2.0) — connect your agent and
the tools load natively, no curl required:

- Endpoint: `https://agent-web.foomworks.workers.dev/mcp`
- Tools (all free, return data directly):
  - `read_url` — fetch a URL → full LLM-ready markdown (title, word count, markdown)
  - `read_url_preview` — the first ~600 characters of the markdown (a cheap look before the full pull)

Discovery manifests: `GET /.well-known/mcp.json` (MCP descriptor), `GET /.well-known/agent-card.json`
(A2A), `GET /openapi.json` (OpenAPI 3.1). The REST endpoints below are available for direct
HTTP/curl use.

## When to use
- "Summarize / extract the content of <URL>"
- "Turn this docs/article page into markdown so I can work with it"
- "Read <URL> and answer a question about it"

## Endpoints (all currently free)
- `GET /read?url=<URL>` — fetch the page → `{ title, words, markdown }`
- `GET /read/preview?url=<URL>` — the first ~600 characters of the markdown
- `POST /mcp` — MCP server (JSON-RPC 2.0): `read_url`, `read_url_preview`
- `GET /health` — service status
- `GET /policy` — the Acceptable-Use Policy (the polite-reader guarantees)
- `GET /stats` — daily usage counters

## Limits & behavior
- **Static HTML only** for now — JavaScript-rendered pages, screenshots, and PDF are a later
  increment (not yet supported).
- A disallowed `robots.txt` path is **refused without fetching**; an unconfirmable `robots.txt`
  (5xx/error) is treated conservatively as disallowed.
- Private/loopback/link-local/internal hosts are blocked (SSRF protection); every redirect hop
  is re-validated. Body cap ~2 MB, fetch timeout ~12 s.
- The service holds no keys and never initiates payments.

## Example
```bash
BASE=https://agent-web.foomworks.workers.dev
# REST
curl -s "$BASE/read?url=https://example.com/"
# MCP (Streamable HTTP, JSON-RPC 2.0)
curl -s -X POST "$BASE/mcp" -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"read_url","arguments":{"url":"https://example.com/"}}}'
```
