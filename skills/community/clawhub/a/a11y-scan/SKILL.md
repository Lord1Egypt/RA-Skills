---
name: accessibility-scan
description: Scan any public web page for WCAG 2.2 (ADA) accessibility issues — honest about what automated testing can and cannot catch
metadata:
  openclaw:
    requires:
      bins:
        - curl
homepage: https://a11y-scan.foomworks.workers.dev
license: MIT
---

# WCAG accessibility scan (a11y-scan)

Use this skill when a task needs to **check a web page for accessibility (WCAG 2.2 / ADA) issues** —
auditing a site, reviewing your own markup, or flagging problems before a launch. Give it one
publicly reachable URL; get back the objective issues a static-HTML scan can find, each mapped to
its WCAG Success Criterion with a concrete fix, plus an honest summary.

Base URL: `https://a11y-scan.foomworks.workers.dev`

**Honest by design (the bright line).** This reports exactly what automated testing finds AND what
it *cannot* catch — color contrast, keyboard operation, focus, JavaScript-rendered content, and
meaning all need a real browser, assistive technology, and human review (~30–57% of WCAG is
automatable). A clean scan is **not** a determination of conformance or legal compliance, and this
service never claims otherwise. Charter-clean: honors `robots.txt`, identifies honestly, read-only
GET, never bypasses anti-bot/CAPTCHA/paywalls.

## Use as an MCP server (recommended for agents)
a11y-scan is a remote **MCP server** (Streamable HTTP, JSON-RPC 2.0) — connect your agent and the
tools load natively, no curl required:

- Endpoint: `https://a11y-scan.foomworks.workers.dev/mcp`
- Tools (all free, return data directly):
  - `scan_url_accessibility` — scan a URL → findings (WCAG SC, impact, count, how-to-fix) + summary + coverage note
  - `scan_url_accessibility_preview` — summary + top issues only (a quick look before the full report)

Discovery manifests: `GET /.well-known/mcp.json` (MCP descriptor), `GET /openapi.json` (OpenAPI 3.1).

## When to use
- "Check <URL> for accessibility / WCAG / ADA issues"
- "What accessibility problems does <URL> have, and how do I fix them?"
- "Audit this page's markup for missing alt text / labels / heading structure"

## What it checks (static-HTML subset)
Missing image alt text (1.1.1), unlabeled form controls (1.3.1/4.1.2), page language (3.1.1),
document title (2.4.2), heading order (1.3.1/2.4.6), empty links/buttons (2.4.4/4.1.2), positive
tabindex (2.4.3), zoom-blocking viewport (1.4.4/1.4.10), iframe titles (4.1.2), timed meta-refresh
(2.2.1/2.2.4), duplicate ids. It does **not** evaluate color contrast, keyboard/focus, or
JS-rendered content (a deeper, browser-based scan is on the roadmap).

## Endpoints (all currently free)
- `GET /scan?url=<URL>` — full findings + summary + coverage note + disclaimer
- `GET /scan/preview?url=<URL>` — summary + top issues only
- `POST /mcp` — MCP server (JSON-RPC 2.0): `scan_url_accessibility`, `scan_url_accessibility_preview`
- `GET /health` · `GET /policy` · `GET /stats`

## Limits & behavior
- **Static HTML only** — it analyzes the page source; it does not run JavaScript or a browser.
- A disallowed `robots.txt` path is **refused without fetching**; an unconfirmable `robots.txt`
  (5xx/error) is treated conservatively as disallowed.
- Private/loopback/link-local/internal hosts are blocked (SSRF protection); every redirect hop is
  re-validated. Body cap ~2 MB, fetch timeout ~12 s. The service holds no keys and never pays.

## Example
```bash
BASE=https://a11y-scan.foomworks.workers.dev
# REST
curl -s "$BASE/scan?url=https://example.com/"
# MCP (Streamable HTTP, JSON-RPC 2.0)
curl -s -X POST "$BASE/mcp" -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"scan_url_accessibility","arguments":{"url":"https://example.com/"}}}'
```
