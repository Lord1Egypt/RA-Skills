---
name: agentbridge
description: "Agent-Browser-Bridge-AI — Anti-detection browser control for AI agents. DOM-first, human-like interactions (Bezier), lead gen, extraction, MCP."
metadata:
  openclaw:
    emoji: "🌉"
    requires:
      bins:
        - agentbridge
      pkgs:
        - browser-agentbridge-ai
---

# AgentBridge 🌉 — Anti-Detection Browser Control for AI Agents

> **The browser that doesn't look like a bot.** Full anti-detection browser bridge for AI agents. DOM-first interactions, human-like mouse movements (Bezier curves), typing jitter, stealth anti-fingerprinting, and **MCP-native** (15 tool + 1 raw tool) integration.

---

## 📋 Complete Feature Reference

### 1. 🕹️ Browser Control

Available via CLI command or MCP tool.

| CLI command | MCP tool | Action |
|-------------|----------|--------|
| `navigate <url>` | `navigate` | Go to any URL with polite waiting |
| `annotate` | `annotate_page` | Screenshot + numbered DOM element tree with refs |
| `click <ref>` | `click_ref` | Click element by numbered ref (found in annotate) |
| `type <ref> <text>` | `type_ref` | Type text into element (clears field first) |
| `press <key>` | _via raw_ | Press keyboard key (Enter/Tab/Escape/...) |
| `scroll [dir] [amount]` | _via raw_ | Scroll viewport (down/up, default 300px) |
| `discover [steps] [px]` | _via raw_ | Scroll step by step and capture each page state |
| `screenshot [--full-page]` | _via raw_ | Capture page screenshot (viewport or full-page) |
| `back` / `forward` | _via raw_ | Browser history with human-like pauses |
| `summary` | _via raw_ | Page metadata: URL, title, interactive element count |

### 2. 📄 Structured Extraction

| CLI command | Extract types available | Details |
|-------------|------------------------|---------|
| `extract article` | `article` | Full article: title + paragraphs + headings |
| `extract table` | `table` | HTML `<table>` + ARIA `role="grid"` |
| `extract form` | `form` | All form fields with labels, types, placeholders |
| `extract listings` | `listings` | Directory/listings: names, ratings, reviews, addresses, phones |
| `extract marketplace` | `marketplace` | E-commerce: titles, prices, images, delivery, sponsored flags |
| Additional types via JSON-RPC | `search-results`, `google-maps`, `custom` (CSS/XPath), `schema` | Accessible via MCP or WebSocket |

Common options: `--limit=N` | `--format=json|csv` | `--out=file.csv`

### 3. 📧 Lead Generation Pipeline

| CLI command | Action |
|-------------|--------|
| `scrape-emails <query>` | 🔥 **Full pipeline**: search engine → visit each result page → extract all emails → save to CSV |
| Options | `--limit=N` (default 20) | `--out=file.csv` | `--engine=google|bing` | `--fast` | `--pages=N` |
| `extract-emails <url>` | Navigate to URL and extract all email addresses found in HTML + visible text |
| `extract-phones <url>` | Navigate to URL and extract phone numbers (uses libphonenumber-js, supports French format +33) |
| `scrape` | Extract marketplace/listing results from current page (alias for `extract marketplace`) |

### 4. 🔍 Visible Text

| CLI command | Options |
|-------------|---------|
| `visibleText` | `--limit=N` | `--filter=TEXT` (pipe-separated) | `--emails` | `--phones` |

Cherry-pick visible DOM text by filter, or extract only emails/phones from visible content.

### 5. 🌐 Web Search

| CLI command | MCP tool | Action |
|-------------|----------|--------|
| `webSearch <query>` | `web_search` | Search Google/Bing, auto-paginate until limit reached, deduplicate results |
| Options | `--limit=N` (default 10) | `--engine=google|bing` | `--pages=N` | `--organic` | `--out=file.json` |
| `siteSearch <query>` | `site_search` | Detect and use the current page's search form automatically |

### 6. 🧍 Human Behavior Emulation

Every interaction goes through the human behavior layer. These commands add extra human-like activity:

| CLI command | What it does |
|-------------|-------------|
| `scan` | Read visible text → scroll → pause → repeat (like a human researcher) |
| `findText <text>` | Search for visible text on page, auto-scrolling until found or max scrolls reached |
| `clickText <text>` | Find visible text AND click it — coordinates first, falls back to agent.click(ref) |
| `idle [ms]` | Pause with random cursor movements — looks human even while "doing nothing" |
| `jitter [radius] [moves]` | Small cursor hesitation movements (default radius 18px, 4 moves) |
| `skim [steps] [px]` | Scroll through content with natural reading pauses |
| `backtrack` | Small upward scroll + pause (emulates re-reading something) |
| `focusCycle [n]` | Press Tab through focusable controls with natural pauses |
| `wait [ms]` | Wait N milliseconds (default: 2000) |

### 7. ⏱️ Timing & Anti-Spam

| CLI command | What it does |
|-------------|-------------|
| `timing get` | Show current human timing profile: consultSpeed, WPM ranges, pause ranges |
| `timing set key=value ...` | Adjust any timing parameter live (`consultSpeed`, `focusedWpmMin/Max`, etc.) |
| `timing reset` | Restore default timing profile |
| `antispam` | Check current page for anti-bot / anti-spam blocking text — non-throwing |

The timing system has 10 adjustable parameters controlling reading speed, pause duration, scroll behavior, and feedback intervals.

### 8. ⚡ Automation

| CLI command | What it does |
|-------------|-------------|
| `run <cmd1> <args1> ...` | Chain multiple commands in sequence, preserving browser state between them |
| `batch <recipe.json>` | Execute multiple commands from a JSON recipe file (lightweight, no variable interpolation) |
| `repl` | Interactive REPL — type commands live, see results instantly |
| `start` | Launch the bridge server |

### 9. 🖥️ Live Viewer

```
Web GUI → http://localhost:8080/viewer
```

Watch the browser in real time. Debug interactions, inspect the page, take over manually when needed.

---

## 🧩 MCP Integration (16 tools)

AgentBridge exposes an MCP server with the following tools:

| Tool | Input | Description |
|------|-------|-------------|
| `browser_status` | — | Check browser connection health, return current URL and page title |
| `navigate` | `{ url, autoAnnotate? }` | Navigate to any http(s) URL |
| `annotate_page` | `{ noImage? }` | Return interactive page elements with stable numeric refs + screenshot URL |
| `click_ref` | `{ ref: number|string }` | Click an element by its numbered ref from annotation |
| `type_ref` | `{ ref, text, clearFirst? }` | Type text into an element by ref |
| `inspect_forms` | — | Map all visible forms: fields, labels, types, options, selectors |
| `fill_form` | `{ values: {} | fields: [] }` | Fill form fields by label/name/query — supports text, select, checkbox, radio, file |
| `submit_form` | `{ query? }` | Submit the active form via submit button or Enter key |
| `site_search` | `{ query, field? }` | Find and use the current page's search form automatically |
| `web_search` | `{ query, engine?, limit?, pages? }` | Search Google/Bing/DuckDuckGo with auto-pagination and dedup |
| `extract_schema` | `{ schema: { fields } }` | Extract structured data via CSS selectors or XPath |
| `extract_marketplace` | `{ limit?, format? }` | Extract e-commerce listing cards with title, price, image, delivery flags |
| `human_timing_get` | — | Current consultation timing profile (10 parameters) |
| `human_timing_set` | `{ consultSpeed?, wpmMin/Max? }` | Adjust timing to speed up or slow down browsing |
| `human_antispam_check` | — | Check page for anti-bot blocking without throwing |
| `browser_command` (raw) | `{ type, payload }` | 🔐 Run ANY bridge command (requires `BRIDGE_MCP_ALLOW_RAW=1`) |

Also exposes a resource (`agentbridge://api`) listing all registered command names, and a prompt template (`browser_task`) for asking agents to complete browser-based goals.

---

## 🛡️ Anti-Detection System

| Feature | How it works (source-verified) |
|---------|-------------------------------|
| **Bezier cursor curves** | Every mouse movement uses cubic Bezier curves with 24-90 adaptive steps — no straight lines |
| **Cursor position tracking** | Server-side cursor state (`_curX`, `_curY`) — every move starts from last known position, never from (0,0) |
| **Click delay** | Random 15-60ms delay between mouse down and mouse up |
| **Typing jitter** | Each character typed with variable per-keystroke delay (15-180ms) |
| **Typing jitter standard dev** | 0.45 of mean delay per character |
| **Timing profile (10 params)** | `consultSpeed` (0.25-8), `focusedWpmMin` (80-500), `focusedWpmMax` (80-650), `skimWpmMin` (100-700), `skimWpmMax` (100-850), `minFocusedMs` (0-120000), `maxFocusedMs` (500-180000), `minSkimMs`, `maxSkimMs`, `feedbackIntervalMs` |
| **Stealth script** | Patches `navigator.webdriver` → `undefined`, injects full `window.chrome` runtime mock, sets `navigator.plugins` with PDF viewer entries, spoofs `languages`, `platform`, `userAgent`, WebGL vendor/renderer, `navigator.hardwareConcurrency` |
| **Cookie auto-accept** | Auto-detects and clicks "Accept all" / "Tout accepter" / "Accepter" on Google, cookie banners, and common consent dialogs |
| **Flash click** | Visual click indicator (green circle animation) — visible when not headless |
| **Anti-spam check** | Inspects page for known anti-bot patterns without throwing — returns clean block/unblock status |
| **Human behavior layer** | Every interaction runs through `humanPreClick` → `humanMove` (Bezier) → click → `flashClick` → `assertNoAntiBot` |

### Stealth patches verified in source (`src/browser/stealth.ts`):

- `navigator.webdriver` → `undefined`
- `window.chrome` mock with `runtime`, `app`, `loadTimes`, `csi`
- `navigator.plugins` → 5 plugins including "Chrome PDF Plugin", "PDF Viewer", "Chrome PDF Viewer"
- `navigator.languages` → `["en-US", "en"]`
- `navigator.platform` → `"Win32"`
- `navigator.hardwareConcurrency` → 4 or 8
- WebGL vendor/renderer spoofing
- `__name` polyfill for esbuild compatibility
- Screen resolution and color depth normalization

---

## 🏆 Anti-Detection Bypass Comparison

| Tool | YouTube | Google Search | JS-heavy sites |
|------|---------|---------------|----------------|
| curl / wget | ❌ 429 / captcha | ❌ Blocked | ❌ JS required |
| Puppeteer-Extra + StealthPlugin | ❌ "Sign in" overlay | ❌ Detected | ⚠️ Partial |
| Playwright + stealth | ❌ Blocked | ❌ Detected | ⚠️ Partial |
| Selenium + undetected-chromedriver | ❌ Blocked | ❌ Detected | ❌ Blocked |
| Camoufox | ❌ Sign-in prompt | ⚠️ Partial | ⚠️ Partial |
| yt-dlp (no cookies) | ❌ LOGIN_REQUIRED | N/A | N/A |
| Tor Browser | ❌ Blocked by most | ❌ CAPTCHA loop | ❌ Blocked |
| **AgentBridge + Chrome CDP** | ✅ **Full access** | ✅ **Works** | ✅ **Works** |

*Tested on Ubuntu 26.04 with Chromium 149 headless via Chrome DevTools Protocol (CDP fallback mode — works without Playwright)*

---

## 🔧 Use Cases

1. **Bug Bounty & Security Research** — Automate recon on authenticated sessions, bypass WAF, extract findings from JS-heavy apps
2. **Lead Generation** — `scrape-emails "AI consultants France" --limit=100 --out=leads.csv --fast`
3. **Web Scraping** — Extract structured data from JS-rendered sites (marketplaces, directories, SERPs)
4. **Market Research** — Competitor price monitoring, product catalog scraping, directory extraction
5. **AI Training Data** — Collect real-world content from protected sites without getting blocked
6. **YouTube Research** — Access video metadata, descriptions, comments, and channel data without cookie/login wall
7. **SaaS Automation** — Fill multi-step forms, navigate dashboards, extract reports
8. **Data Pipelines** — Integrate with Claude, Cursor, Windsurf via MCP, or build custom workflows with `run` / `batch`

---

## 🚀 Quick Start

```bash
# 1. Install from npm
npm install -g browser-agentbridge-ai
npm run build

# 2. Start the bridge server
agentbridge start
# → WebSocket: ws://localhost:8080/ws/browser-bridge
# → Live GUI:  http://localhost:8080/viewer

# 3. Navigate to any page
agentbridge navigate https://example.com

# 4. Analyze the page (returns numbered elements)
agentbridge annotate

# 5. Interact with numbered elements
agentbridge click 3
agentbridge type 5 "hello world"
agentbridge press Enter

# 6. Extract content
agentbridge extract article --format=json
agentbridge extract-emails https://example.com/contact

# 7. Full lead generation pipeline
agentbridge scrape-emails "AI consultants France" --limit=50 --out=leads.csv --fast

# 8. Web search with results
agentbridge webSearch "latest AI security tools 2026" --limit=20 --out=results.json

# 9. Interactive REPL
agentbridge repl
```

### Without Playwright (CDP Fallback)

Works on any system with Chrome — no Playwright dependency:

```bash
# Launch Chrome headless with remote debugging
google-chrome --headless=new --no-sandbox --remote-debugging-port=9222 &
sleep 2

# Get the WebSocket URL
WS_URL=$(curl -s http://127.0.0.1:9222/json/version | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['webSocketDebuggerUrl'])")

# Point AgentBridge at the running Chrome instance
export CHROME_CDP_URL="$WS_URL"
export BRIDGE_HEADLESS=true
npx agentbridge start
```

### MCP Integration

```bash
# Start the MCP server (stdin/stdout transport for Claude/Cursor/Windsurf)
npm run mcp
```

Connects 16 tools to any MCP-compatible host.

---

## 🔗 Quick Links

- **ClawHub**: https://clawhub.ai/alexandre-leng/agentbridge
- **npm**: `npm install -g browser-agentbridge-ai`
- **GitHub**: https://github.com/alexandre-leng/Agent-Browser-Bridge-AI
- **Author**: Alexandre Leng (@alexandre-leng)

---

## 📦 Requirements

- **Node.js** ^18.0.0
- **Browser**: Chromium (via Playwright) OR any Chrome-based browser via CDP fallback
- **RAM**: ~100MB for bridge server + browser process
- **Playwright**: Optional — the CDP fallback works on systems where Playwright isn't supported (e.g., Ubuntu 26.04)

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
