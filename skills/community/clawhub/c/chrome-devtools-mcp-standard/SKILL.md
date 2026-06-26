---
name: chrome-devtools-mcp
description: >
  Standard browser automation for agents via Chrome DevTools MCP — official Google
  project giving AI agents full Chrome DevTools access. 29 tools for input automation,
  navigation, performance traces, Lighthouse audits, network inspection, debugging,
  and emulation. Replaces cloud-hosted browser tools (Browserbase, browser_*) as the
  primary browser automation standard. Use when you need to automate or inspect web
  pages, take screenshots, run performance audits, analyze network traffic, debug JS,
  fill forms, or emulate mobile viewports.
keywords:
  - browser automation
  - chrome devtools
  - MCP browser
  - web scraping
  - screenshots
  - performance audit
  - lighthouse
  - network inspection
  - form filling
  - use chrome-devtools-mcp
  - replace browser tools
  - use browser
---

# Chrome DevTools MCP

**Official Google project** — gives AI coding agents full Chrome DevTools access via the Model Context Protocol (MCP).
Free, open-source, runs locally with your own Chrome browser. No cloud dependency, no usage limits.

## Install

### Prerequisites
- **Node.js** v20.19+ (check: `node --version`)
- **Google Chrome** stable (check: `which google-chrome` or `which chromium-browser`)
  - On Ubuntu/Debian: `wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install -y ./google-chrome-stable_current_amd64.deb`
  - On macOS: Install from google.com/chrome or `brew install --cask google-chrome`
  - On ARM64 Linux: Use `chromium-browser` or Chrome for Testing

### Install the MCP Server
```bash
npm i -g chrome-devtools-mcp
```

Or run directly with npx (no global install):
```bash
npx -y chrome-devtools-mcp@latest
```

### MCP Server Config
Add to your agent's MCP config (config.yaml, .mcp.json, etc.):

**Standard config:**
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]
    }
  }
}
```

**Slim mode** (lightweight, basic browser tasks only, lower resource usage):
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--slim", "--headless", "--no-usage-statistics"]
    }
  }
}
```

**Claude Code plugin** (MCP + skills):
```bash
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
/plugin install chrome-devtools-mcp
```

**OpenClaw** (in config.yaml):
```yaml
mcp:
  servers:
    chrome-devtools:
      command: npx
      args: ["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"]
```

## Tool Categories (29 Tools)

### Input Automation (9 tools)
- `click` — Click elements by uid from snapshot
- `drag` — Drag one element onto another
- `fill` — Type text into input/textarea/select
- `fill_form` — Fill out multiple form fields at once
- `handle_dialog` — Accept/dismiss browser dialogs
- `hover` — Hover over an element
- `press_key` — Press keys or shortcuts (Enter, Ctrl+A, etc.)
- `type_text` — Type into focused input with optional submit key
- `upload_file` — Upload file through file input element

### Navigation (6 tools)
- `navigate_page` — Navigate to URL
- `new_page` — Open new browser page/tab
- `close_page` — Close page by index
- `list_pages` — List all open pages
- `select_page` — Switch active page
- `wait_for` — Wait for condition (selector, text, network, etc.)

### Debugging (6 tools)
- `take_snapshot` — Get page accessibility tree with element UIDs
- `take_screenshot` — Screenshot of page or element (PNG/JPEG)
- `evaluate_script` — Run arbitrary JS in page context
- `list_console_messages` — Get console.log/warn/error output
- `get_console_message` — Get specific console message details
- `lighthouse_audit` — Run full Lighthouse audit (performance, a11y, SEO, best practices)

### Performance (4 tools)
- `performance_start_trace` — Start Chrome performance trace recording
- `performance_stop_trace` — Stop trace and get results
- `performance_analyze_insight` — Get actionable performance insights from trace
- `take_memory_snapshot` — Capture heap snapshot for memory analysis

### Network (2 tools)
- `list_network_requests` — Get all network requests (URL, status, timing, size)
- `get_network_request` — Get details for specific request

### Emulation (2 tools)
- `emulate` — Emulate device (mobile/tablet), geolocation, CPU throttling, network throttling
- `resize_page` — Resize viewport to specific dimensions

## Standard Workflow

### 1. Navigate and Snapshot
```
navigate_page(url) → get page loaded
take_snapshot() → get element tree with UIDs
```

### 2. Interact
```
click(uid) → click an element
fill(uid, value) → fill a form field
press_key("Enter") → submit form
wait_for({type: "selector", selector: ".result"}) → wait for result
```

### 3. Inspect
```
take_snapshot() → see updated page state
list_console_messages() → check for JS errors
list_network_requests() → check API calls
take_screenshot() → visual verification
```

### 4. Debug / Audit
```
evaluate_script("document.querySelector('.price').textContent") → extract data
lighthouse_audit() → full performance/SEO/a11y audit
performance_start_trace() → start perf trace
```

## Decision Rules

**Use Chrome DevTools MCP when:**
- You need to navigate, click, fill forms, or take screenshots of web pages
- You need to inspect console errors, network requests, or page state
- You need performance analysis (traces, Lighthouse audits)
- You need to emulate mobile devices or throttle network/CPU
- You need reliable, local browser automation with no usage limits
- The built-in `browser_*` tools fail (Browserbase limits, timeouts)

**Still use built-in `browser_*` tools when:**
- The MCP server isn't installed or Chrome isn't available
- You're on a headless server without display (use `--headless` flag with MCP)
- Quick one-off URL content extraction (prefer `web_extract` or `web_search` first)

**MCP vs dev-browser:**
- Chrome DevTools MCP is the **primary standard** — use it first
- `dev-browser` is a fallback for scripts and repeatable workflows
- Avoid cloud browser services (Browserbase, Browser Use) — they have usage limits and cost money

## Troubleshooting

**Chrome not found:**
```bash
# Ubuntu/Debian amd64:
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Or use Chrome for Testing:
npx @puppeteer/browsers install chrome@stable

# macOS:
brew install --cask google-chrome
```

**Node.js version too old:**
```bash
node --version  # needs v20.19+
# Use nvm to upgrade:
nvm install 22
nvm use 22
```

**MCP server won't connect:**
- Ensure Chrome is installed and accessible in PATH
- Try `npx -y chrome-devtools-mcp@latest --headless` for headless environments
- Check `--no-usage-statistics` flag to disable Google telemetry
- For OpenClaw, verify MCP config in config.yaml

## References
- GitHub: https://github.com/ChromeDevTools/chrome-devtools-mcp
- Tool reference: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
- Slim mode: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md
- Troubleshooting: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md
