---
name: browser-cdp
description: >
  Real Chrome browser automation via CDP Proxy — access pages with full user login state,
  bypass anti-bot detection, perform interactive operations (click/fill/scroll), extract
  dynamic JavaScript-rendered content, take screenshots.
  Triggers (satisfy ANY one):
  - Target URL is a search results page (Bing/Google/YouTube search)
  - Static fetch (agent-reach/WebFetch) is blocked by anti-bot (captcha/intercept/empty)
  - Need to read logged-in user's private content
  - YouTube, Twitter/X, Xiaohongshu, WeChat public accounts, etc.
  - Task involves "click", "fill form", "scroll", "drag"
  - Need screenshot or dynamic-rendered page capture
metadata:
  author: adapted from eze-is/web-access (MIT licensed)
  version: "1.0.0"
---

## What is browser-cdp?

browser-cdp connects directly to your local Chrome via Chrome DevTools Protocol (CDP), giving the AI agent:

- **Full login state** — your cookies and sessions are carried through
- **Anti-bot bypass** — pages that block static fetchers (search results, video platforms)
- **Interactive operations** — click, fill forms, scroll, drag, file upload
- **Dynamic content extraction** — read JavaScript-rendered DOM
- **Screenshots** — capture any page at any point

## Architecture

```
Chrome (remote-debugging-port=9222)
    ↓ CDP WebSocket
CDP Proxy (cdp-proxy.mjs) — HTTP API on localhost:3456
    ↓ HTTP REST
OpenClaw AI Agent
```

## Setup

### 1. Start Chrome with debugging port

```bash
# macOS — must use full binary path (not `open -a`)
pkill -9 "Google Chrome"; sleep 2
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile \
  --no-first-run &
```

Verify:
```bash
curl -s http://127.0.0.1:9222/json/version
```

### 2. Start CDP Proxy

```bash
node ~/.openclaw/skills/browser-cdp/scripts/cdp-proxy.mjs &
sleep 3
curl -s http://localhost:3456/health
# {"status":"ok","connected":true,"sessions":0,"chromePort":9222}
```

## API Reference

```bash
# List all tabs
curl -s http://localhost:3456/targets

# Open URL in new tab
curl -s "http://localhost:3456/new?url=https://example.com"

# Execute JavaScript
curl -s -X POST "http://localhost:3456/eval?target=TARGET_ID" \
  -d 'document.title'

# JS click (fast, preferred)
curl -s -X POST "http://localhost:3456/click?target=TARGET_ID" \
  -d 'button.submit'

# Real mouse click
curl -s -X POST "http://localhost:3456/clickAt?target=TARGET_ID" \
  -d '.upload-btn'

# Screenshot
curl -s "http://localhost:3456/screenshot?target=TARGET_ID&file=/tmp/shot.png"

# Scroll (lazy loading)
curl -s "http://localhost:3456/scroll?target=TARGET_ID&direction=bottom"

# Navigate
curl -s "http://localhost:3456/navigate?target=TARGET_ID&url=https://..."

# Close tab
curl -s "http://localhost:3456/close?target=TARGET_ID"
```

## Tool Selection: Three-Layer Strategy

| Scenario | Use | Reason |
|----------|------|------|
| Public pages (GitHub, Wikipedia, blogs) | `agent-reach` | Fast, low token, structured |
| **Search results** (Bing/Google/YouTube) | **`browser-cdp`** | agent-reach blocked |
| **Login-gated content** | **`browser-cdp`** | No cookies in agent-reach |
| JS-rendered pages | **`browser-cdp`** | Reads rendered DOM |
| Simple automation, isolated screenshots | `agent-browser` | No Chrome setup |
| Large-scale parallel scraping | `agent-reach` + parallel | browser-cdp gets rate-limited |

**Decision flow:**
```
Public content → agent-reach (fast, cheap)
Search results / blocked → browser-cdp
Still fails → agent-reach fallback + record in site-patterns
```

## Known Limitations

- Chrome must use a **separate profile** (`/tmp/chrome-debug-profile`)
- Same-site parallel tabs may get rate-limited
- Node.js 22+ required (native WebSocket)
- macOS: use **full binary path** to start Chrome, not `open -a`

## Site Patterns & Usage Log

```bash
~/.openclaw/skills/browser-cdp/references/site-patterns/   # per-domain experience
~/.openclaw/skills/browser-cdp/references/usage-log.md    # per-use tracking
```

## Origin

Adapted from [eze-is/web-access](https://github.com/eze-is/web-access) (MIT) for OpenClaw.
A bug in the original (`require()` in ES module, [reported here](https://github.com/eze-is/web-access/issues/10)) is fixed in this version.
