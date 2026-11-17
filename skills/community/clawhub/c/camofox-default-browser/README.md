# Camofox Default Browser — Anti-Detection Browser Skill for OpenClaw

---

## Overview

Camofox Default Browser is a skill that configures and uses **Camoufox**, a Firefox fork with C++-level fingerprint spoofing, as the primary browser automation engine inside OpenClaw. Unlike standard Playwright/Chromium setups that get blocked by Cloudflare, bot detectors, and anti-scraping systems, Camoufox patches browser fingerprints at the implementation level before JavaScript ever sees them.

This skill transforms OpenClaw's browsing capability from "easily detectable headless Chrome" into an undetectable Firefox-based automation system that can access Google, Amazon, LinkedIn, and other bot-hardened websites without triggering CAPTCHAs or WAFs.

## Why Camoufox?

Standard browser automation tools leak detectable signals:

- **Headless Chrome** — `navigator.webdriver` is easily detected
- **Playwright/Puppeteer** — browser fingerprint mismatches (WebGL, AudioContext, screen resolution)
- **Stealth plugins** — pattern-based evasion creates fingerprints of their own

Camoufox solves this by patching **Firefox at the C++ level**:
- `navigator.hardwareConcurrency` — spoofed
- WebGL renderer — spoofed
- AudioContext — spoofed
- Screen geometry — spoofed
- WebRTC — spoofed
- User-Agent — realistic Firefox profile

No shims, no wrappers, no tells. Every browser signal matches a real Firefox installation.

## What This Skill Provides

This skill registers **11 automation tools** in OpenClaw, all routed through Camoufox:

| Tool | Description |
|------|-------------|
| `camofox_create_tab` | Create a new anti-detection browser tab |
| `camofox_snapshot` | Get accessibility snapshot with element refs and optional screenshot |
| `camofox_click` | Click elements by ref or CSS selector |
| `camofox_type` | Type text into form fields |
| `camofox_navigate` | Navigate to a URL or use search macros |
| `camofox_scroll` | Scroll page in any direction |
| `camofox_screenshot` | Capture screenshot of the current page |
| `camofox_close_tab` | Close a browser tab |
| `camofox_evaluate` | Execute JavaScript in page context |
| `camofox_list_tabs` | List all open tabs |
| `camofox_import_cookies` | Import Netscape cookie files for authenticated sessions |

## Key Features

### C++ Anti-Detection
Bypasses Google, Cloudflare, Cloudflare Turnstile, and most commercial bot detection services. The fingerprint spoofing happens before the JavaScript sandbox initializes, making it undetectable by client-side checks.

### Token-Efficient Snapshots
Camofox uses accessibility-tree based snapshots instead of raw HTML. This makes responses ~90% smaller than raw HTML dumps while preserving all interactive elements with stable refs (e1, e2, e3).

### Search Macros
Built-in search macros for common websites: `@google_search`, `@youtube_search`, `@amazon_search`, `@reddit_subreddit`, and 10 more.

### Cookie Import
Inject Netscape-format cookie files for authenticated browsing. Useful for scraping behind login walls.

### Proxy + GeoIP
Route traffic through residential proxies with automatic locale/timezone adjustments. GeoIP database included.

### Resource Efficient
Lazy browser launch and idle shutdown keeps memory at ~40MB when idle. Designed to run alongside other services on $5 VPS or shared infrastructure.

### Session Isolation
Separate cookies, storage, and browser contexts per user session. Multiple users on one server stay fully isolated.

## Dependencies

- **Camoufox Binary** — Firefox fork (~300MB), auto-downloaded at install time
- **GTK3 Runtime** — Required by Firefox, needs `libgtk-3-0` and related libraries
- **Xvfb** — Virtual display framebuffer for headless Linux environments
- **Node.js 18+** — Server runtime
- **GeoLite2 Database** — GeoIP-based locale/timezone adjustment (auto-downloaded)

## Installation

### 1. Install Camoufox Browser Plugin

```bash
# Install from ClawHub
openclaw plugins install clawhub:akdira/camofox-default-browser

# Or install from source
git clone https://github.com/jo-inc/camofox-browser
cd camofox-browser
npm install
openclaw plugins install .
```

### 2. Set Environment Variables

```bash
export CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox
```

Or add to OpenClaw config:

```json
"env": {
  "CAMOUFOX_EXECUTABLE": "/root/.cache/camoufox/camoufox"
}
```

### 3. System Dependencies (Linux)

```bash
apt-get install -y libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
  libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libatk-bridge2.0-0 libdrm2 libgbm1 xvfb
```

### 4. Restart Gateway

```bash
# Restart OpenClaw gateway to load the plugin
openclaw gateway restart
```

## Usage

Once installed and configured, use `camofox_*` tools instead of the built-in `browser` tool:

```bash
# Create a tab
camofox_create_tab url="https://linkedin.com"

# Get page snapshot
camofox_snapshot tabId="<tabId>"

# Interact with elements
camofox_click tabId="<tabId>" ref="e3"
camofox_type tabId="<tabId>" ref="e7" text="search query"

# Navigate with search macros
camofox_navigate tabId="<tabId>" macro="@google_search" query="OpenClaw AI agents"

# Close when done
camofox_close_tab tabId="<tabId>"
```

## Security

- Cookie import is **disabled by default** — requires explicit `CAMOFOX_API_KEY` environment variable
- Access control via optional `CAMOFOX_ACCESS_KEY` bearer token
- Session persistence in `~/.camofox/profiles/` (per-user, hashed directories)
- Zero embedded secrets — all credentials are environment variables
- Crash telemetry is anonymized: no page content, cookies, tokens, IPs, or user data

## Published By

**@akdira** — Personal AI Agent Infrastructure

---

*License: MIT*  
*Built on Camoufox (Firefox fork by @nicedayzhu)*  
*Originally by @jo-inc/camofox-browser*
