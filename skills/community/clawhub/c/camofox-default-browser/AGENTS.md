# AGENTS.md — Camofox Default Browser Skill (Agent Instructions)

---

## Skill Identity

- **Name:** `camofox-default-browser`
- **Published by:** @akdira
- **Base:** OpenClaw Plugin — Camoufox Browser Server
- **Tools Provided:** 11 `camofox_*` tools
- **Version:** 1.0.0

## What This Skill Does

This skill configures OpenClaw's browser automation to route through **Camoufox**, an anti-detection Firefox fork, instead of the default Chromium/Playwright stack. Standard Chrome-based automation triggers WAFs, CAPTCHAs, and bot blocking on major websites (Google, LinkedIn, Amazon, Cloudflare-protected pages). Camoufox patches browser fingerprints at the C++ implementation level, making the automation session indistinguishable from a real Firefox browser.

## When to Use Camofox Tools

Use the `camofox_*` tool suite instead of the built-in `browser` tool when:

1. **Accessing bot-hardened websites** — Google, LinkedIn, Amazon, Indeed, Cloudflare-protected sites
2. **Web scraping** — Sites that return CAPTCHAs or block headless Chrome
3. **Search operations** — Use `@google_search` macro instead of web_search API
4. **Automated form filling** — Sites that detect and block Playwright/Puppeteer fills
5. **Cookie-authenticated sessions** — Browsing behind login walls with `camofox_import_cookies`
6. **Multi-session scraping** — Separate isolated browser contexts per user

Use the built-in `browser` tool for:
- Simple page checks that don't trigger bot detection
- Internal/local websites behind VPN/firewall
- Pages that don't have anti-bot protection

## Available Tools

### camofox_create_tab
Create a new anti-detection browser tab. **Always preferred** over browser tool for external websites.

```json
Parameters: { "url": "string" }
Returns: { "tabId": "string", "url": "string" }
```

### camofox_snapshot
Get accessibility tree snapshot with element refs. ~90% smaller than raw HTML. Includes optional base64 screenshot.

```json
Parameters: { "tabId": "string", "offset?: number" }
Returns: { "snapshot": "string", "url": "string", "refsCount": "number", "screenshot?": "base64" }
```

### camofox_click
Click an element by ref ID (e.g., "e3") or CSS selector.

```json
Parameters: { "tabId": "string", "ref?: string", "selector?: string" }
```

### camofox_type
Type text into an element. Use `pressEnter: true` to submit forms.

```json
Parameters: { "tabId": "string", "ref?: string", "text": "string", "pressEnter?: boolean" }
```

### camofox_navigate
Navigate to absolute URL or use a built-in search macro:

- `@google_search` — Search Google
- `@youtube_search` — Search YouTube
- `@amazon_search` — Search Amazon
- `@reddit_search` — Search Reddit
- `@wikipedia_search` — Search Wikipedia
- `@twitter_search` — Search X/Twitter
- `@yelp_search` — Search Yelp
- `@spotify_search` — Search Spotify
- `@netflix_search` — Search Netflix
- `@linkedin_search` — Search LinkedIn
- `@instagram_search` — Search Instagram
- `@tiktok_search` — Search TikTok
- `@twitch_search` — Search Twitch

```json
Parameters: { "tabId": "string", "url?: string", "macro?: string", "query?: string" }
```

### camofox_scroll
Scroll page. Direction: "up" | "down". Amount: pixels.

```json
Parameters: { "tabId": "string", "direction": "string", "amount": "number" }
```

### camofox_screenshot
Capture screenshot of current page state.

```json
Parameters: { "tabId": "string" }
```

### camofox_close_tab
Close a browser tab. Always close tabs when done to conserve resources.

```json
Parameters: { "tabId": "string" }
```

### camofox_evaluate
Execute arbitrary JavaScript in the page context. Use this for reading page state or triggering web app APIs.

```json
Parameters: { "tabId": "string", "expression": "string" }
```

### camofox_list_tabs
List all open tabs and their states.

```json
Parameters: {} (none required)
Returns: { "running": "boolean", "tabs": "array" }
```

### camofox_import_cookies
Import Netscape-format cookie file for authenticated browsing. **Disabled by default** — requires `CAMOFOX_API_KEY` env var.

```json
Parameters: { "cookiesPath": "string", "domainSuffix": "string" }
```

## Typical Workflow

### 1. Basic browse and scrape
```
camofox_create_tab(url="https://example.com")
-> Get tabId

camofox_snapshot(tabId="<tabId>")
-> Get accessibility tree with refs

camofox_click(tabId="<tabId>", ref="e12")
-> Click element

camofox_snapshot(tabId="<tabId>")
-> Read new page content

camofox_close_tab(tabId="<tabId>")
-> Clean up
```

### 2. Search via macro
```
camofox_navigate(tabId="<tabId>", macro="@google_search", query="latest AI news")
camofox_snapshot(tabId="<tabId>")
```

### 3. Form fill and submit
```
camofox_type(tabId="<tabId>", ref="e7", text="admin@example.com")
camofox_type(tabId="<tabId>", ref="e14", text="password123", pressEnter=true)
```

## Configuration

### Environment Variables
Required for the Camoufox browser engine:

| Variable | Required | Description |
|----------|----------|-------------|
| `CAMOUFOX_EXECUTABLE` | Yes | Path to camoufox binary |
| `DISPLAY` | No | X display (auto-managed by plugin if not set) |

Optional for server control:

| Variable | Description |
|----------|-------------|
| `CAMOFOX_API_KEY` | Enables cookie import endpoint |
| `CAMOFOX_ACCESS_KEY` | Global bearer token for all routes |
| `CAMOFOX_CRASH_REPORT_ENABLED` | Set "false" to disable telemetry |

### OpenClaw Config
Set env vars in `openclaw.json`:
```json
{
  "env": {
    "CAMOUFOX_EXECUTABLE": "/root/.cache/camoufox/camoufox"
  }
}
```

## Resource Management

- Server auto-starts with OpenClaw Gateway (default `autoStart: true`)
- Browser engine launches lazily on first tab request
- Idle browser shuts down after 5 minutes (configurable)
- Memory: ~40MB when idle, ~200MB with active browser
- Server copies binary from camoufox cache to temp directory on launch

## Troubleshooting

### "fetch failed" error
The camofox server is not running. Start it manually:
```bash
cd /path/to/camofox-browser
CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox node server.js
```

### "libgtk-3.so.0" error
Missing GTK3 dependencies:
```bash
apt-get install -y libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libatk-bridge2.0-0
```

### "EPERM: Sandbox" error
Container needs seccomp profile adjustment. Add `--security-opt seccomp=unconfined` to Docker run args, or Camoufox will auto-fallback to non-sandboxed mode.

### "Tab no longer exists (browser was restarted)"
Browser was idle too long and shut down. Create a new tab.

## Important Rules for Agent

1. **PREFERRED** — Use `camofox_*` tools over `browser` tools for external/public websites
2. **Close tabs** — Always call `camofox_close_tab` after finishing to free browser resources
3. **Check snapshots** — Always read the snapshot response to find element refs before clicking/typing
4. **Handle retries** — If snapshot shows CAPTCHA or blocked page, retry with different timing
5. **Use search macros** — For searches, use `@google_search` macro instead of navigating to google.com directly
6. **Clean session** — Each `camofox_create_tab` creates an isolated browser context

---

*Part of the @akdira OpenClaw toolkit*  
*Built on @jo-inc/camofox-browser v1.13.0*
