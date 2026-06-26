---
name: Gbrow
description: Full-featured headless browser for OpenClaw agents. Navigate, snapshot with accessibility tree (@ref clicks), tabs, JS execution, cookie import. No vision model needed — free, fast, reliable.
tools:
  - gbrow
---

# Gbrow — The Browser Your AI Agent Actually Needs

A full-featured headless browser powered by [Playwright](https://playwright.dev/) and [Bun](https://bun.sh/). Uses the **accessibility tree** for page reading — not expensive vision models.

## Why Gbrow?

| Traditional (screenshots + vision) | Gbrow (accessibility tree) |
|---|---|
| Screenshot → upload to GPT-4o → wait → read | `ariaSnapshot()` → instant structured text |
| ~$0.01 per page read | **Free** |
| 3-10 seconds per page | **< 100ms** |
| Fails on API key issues | **Always works** |
| Click by fragile CSS selector | **Click by @ref** (`@e1`, `@e2`, etc.) |

## Quick Setup

```bash
# Clone and install
git clone https://github.com/ashish797/Gbrow.git ~/.openclaw/workspace/skills/Gbrow
cd ~/.openclaw/workspace/skills/Gbrow
bash setup.sh
```

Or one-liner:
```bash
curl -fsSL https://raw.githubusercontent.com/ashish797/Gbrow/main/setup.sh | bash
```

## How It Works

### 1. Start the server
```bash
cd ~/.openclaw/workspace/skills/Gbrow
bun run src/server.ts
```

### 2. Read the page (accessibility tree)
The snapshot gives you a structured view with clickable refs:
```
@e1 [heading] "Welcome" [level=1]
@e2 [link] "Get Started"
@e3 [button] "Sign in"
@e4 [textbox] "Search"
```

### 3. Click by ref
```
click @e2     → clicks "Get Started"
fill @e4 "query"  → types into search box
```

## Commands

### Navigation
| Command | Description | Example |
|---------|-------------|---------|
| `goto <url>` | Navigate to URL | `goto https://example.com` |
| `back` | History back | `back` |
| `forward` | History forward | `forward` |
| `reload` | Reload page | `reload` |
| `url` | Print current URL | `url` |

### Reading
| Command | Description | Example |
|---------|-------------|---------|
| `snapshot` | Accessibility tree with @refs | `snapshot -i` (interactive only) |
| `text` | Cleaned page text | `text` |
| `html [selector]` | Raw HTML | `html .article` |
| `links` | All links as "text → href" | `links` |
| `forms` | Form fields as JSON | `forms` |

### Interaction
| Command | Description | Example |
|---------|-------------|---------|
| `click <ref>` | Click element | `click @e3` |
| `fill <ref> <text>` | Fill input | `fill @e4 "hello"` |
| `select <ref> <value>` | Select dropdown | `select @e5 "option1"` |
| `type <ref> <text>` | Type with keyboard | `type @e4 "search term"` |
| `press <key>` | Press key | `press Enter` |
| `scroll <direction>` | Scroll page | `scroll down` |

### Inspection
| Command | Description | Example |
|---------|-------------|---------|
| `js <expr>` | Run JavaScript | `js document.title` |
| `css <sel> <prop>` | Computed CSS | `css .box color` |
| `attrs <ref>` | Element attributes | `attrs @e1` |
| `is <prop> <ref>` | State check | `is visible @e3` |

### Tabs
| Command | Description |
|---------|-------------|
| `tabs` | List open tabs |
| `tab N` | Switch to tab N |
| `newtab` | Open new tab |
| `closetab` | Close current tab |

### Visual
| Command | Description |
|---------|-------------|
| `screenshot` | Take screenshot |
| `responsive <w> <h>` | Set viewport size |
| `pdf` | Save page as PDF |

## Snapshot Flags

| Flag | Description |
|------|-------------|
| `-i` | Interactive elements only (buttons, links, inputs) |
| `-c` | Compact (remove empty structural nodes) |
| `-d N` | Limit tree depth |
| `-s <sel>` | Scope to CSS selector |
| `-D` | Diff against previous snapshot |
| `-a` | Annotated screenshot with ref overlays |

## HTTP API

All commands go through the HTTP API:

```bash
# Get port and token from state file
PORT=$(python3 -c "import json; print(json.load(open('.gstack/browse.json'))['port'])")
TOKEN=$(python3 -c "import json; print(json.load(open('.gstack/browse.json'))['token'])")

# Send command
curl -s -X POST "http://127.0.0.1:${PORT}/command" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"command":"goto","args":["https://example.com"]}'
```

## Architecture

```
┌─────────────┐     HTTP      ┌──────────────────┐
│  OpenClaw   │ ──────────▶  │  Gbrow Server    │
│  Agent      │              │  (Bun + Playwright)│
└─────────────┘              └────────┬─────────┘
                                      │
                                      ▼
                              ┌──────────────────┐
                              │  Chromium         │
                              │  (headless)       │
                              └──────────────────┘
                                      │
                                      ▼
                              ┌──────────────────┐
                              │ Accessibility     │
                              │ Tree (ariaSnapshot)│
                              └──────────────────┘
```

No vision models. No API calls. Just structured text from the browser's accessibility layer.

## Credits

Built on top of [gstack](https://github.com/garrytan/gstack) by Gary Tan (Y Combinator). Adapted for OpenClaw with permission under MIT license.

## License

MIT
