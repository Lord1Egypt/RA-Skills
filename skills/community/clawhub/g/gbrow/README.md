# Gbrow

A full-featured headless browser for [OpenClaw](https://github.com/openclaw/openclaw) agents. Built on Playwright and Bun.

Instead of taking screenshots and sending them to expensive vision models, Gbrow reads pages through the browser's **accessibility tree**. It's fast, free, and way more reliable.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Bun](https://img.shields.io/badge/Bun-1.3+-fbf0df)](https://bun.sh)
[![Playwright](https://img.shields.io/badge/Playwright-latest-2EAD33)](https://playwright.dev)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-purple)](https://github.com/openclaw/openclaw)

## The Problem

Most browser tools for AI agents take screenshots, upload them to GPT-4o or Claude, and wait for a description. That works, but it's slow (3-10 seconds per page), costs money (~$0.01 per read), and breaks when API keys expire.

## How Gbrow Does It Differently

Gbrow uses Playwright's `ariaSnapshot()` — the same structured data that screen readers use. Instead of a picture of the page, you get a clean text tree:

```
@e1 [heading] "Welcome to Example" [level=1]
@e2 [link] "Get Started"
@e3 [button] "Sign in"
@e4 [textbox] "Search"
```

Each element gets a ref (`@e1`, `@e2`, etc.) that you can click, fill, or inspect directly. No vision model, no API calls, no cost.

## Install

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/ashish797/Gbrow.git
cd Gbrow && bash setup.sh
```

The setup script installs Bun (if needed), pulls dependencies, and installs Chromium. Takes about 30 seconds.

## Usage

Start the server:

```bash
bun run src/server.ts
```

Then send commands over HTTP:

```bash
PORT=$(python3 -c "import json; print(json.load(open('.gstack/browse.json'))['port'])")
TOKEN=$(python3 -c "import json; print(json.load(open('.gstack/browse.json'))['token'])")

# Navigate
curl -s -X POST "http://127.0.0.1:${PORT}/command" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"command":"goto","args":["https://news.ycombinator.com"]}'

# Read the page
curl -s -X POST "http://127.0.0.1:${PORT}/command" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"command":"snapshot","args":["-i"]}'

# Click an element
curl -s -X POST "http://127.0.0.1:${PORT}/command" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"command":"click","args":["@e3"]}'
```

## Commands

### Navigation
| Command | Description |
|---------|-------------|
| `goto <url>` | Navigate to URL |
| `back` / `forward` / `reload` | History navigation |
| `url` | Current URL |

### Reading
| Command | Description |
|---------|-------------|
| `snapshot [-i\|-c\|-d N]` | Accessibility tree with element refs |
| `text` | Cleaned page text |
| `html [selector]` | Raw HTML |
| `links` | All links as "text -> href" |
| `forms` | Form fields as JSON |

### Interaction
| Command | Description |
|---------|-------------|
| `click <ref>` | Click element by ref (e.g. `@e3`) |
| `fill <ref> <text>` | Fill an input field |
| `type <ref> <text>` | Type with keyboard events |
| `select <ref> <value>` | Select dropdown value |
| `press <key>` | Press a key (Enter, Tab, etc.) |
| `scroll <direction>` | Scroll the page |

### Inspection
| Command | Description |
|---------|-------------|
| `js <expr>` | Run JavaScript on the page |
| `css <sel> <prop>` | Get computed CSS value |
| `attrs <ref>` | Element attributes as JSON |
| `is <prop> <ref>` | Check state (visible, enabled, etc.) |

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
| `pdf` | Save page as PDF |
| `responsive <w> <h>` | Set viewport size |

### Snapshot Flags
| Flag | What it does |
|------|-------------|
| `-i` | Interactive elements only (buttons, links, inputs) |
| `-c` | Compact — remove empty structural nodes |
| `-d N` | Limit tree depth to N levels |
| `-s <sel>` | Scope to a CSS selector |
| `-D` | Diff against previous snapshot |
| `-a` | Annotated screenshot with ref overlays |

## How It Works

```
Your Agent  ---HTTP--->  Gbrow Server  --->  Chromium (headless)
                                    |
                                    v
                          Accessibility Tree
                          (structured text + refs)
```

1. Agent sends a command (goto, snapshot, click, etc.)
2. Gbrow server receives it, runs it through Playwright
3. For reading, it uses `ariaSnapshot()` — not screenshots
4. Result is structured text with clickable refs
5. Agent can click refs, fill forms, navigate — all without vision models

## Why Not Just Use Playwright Directly?

You can. But Gbrow gives you:

- **Persistent server** — browser stays alive between commands
- **Auth token** — only authorized callers can use it
- **Tab management** — open, switch, close tabs
- **Ref system** — structured interaction without CSS selectors
- **Auto-shutdown** — kills itself after 30 minutes of inactivity
- **Docker-friendly** — handles sandboxing issues automatically

## Comparison

| Feature | Gbrow | Vision-based tools | Raw Playwright |
|---------|-------|-------------------|----------------|
| Page reading | Accessibility tree | Screenshot + GPT-4o | Manual extraction |
| Cost per page | Free | ~$0.01 | Free |
| Speed | < 100ms | 3-10s | Varies |
| API key needed | No | Yes | No |
| Click method | `@ref` | CSS selector | CSS selector |
| Tab management | Built-in | No | Manual |
| Persistent server | Yes | No | No |
| OpenClaw integration | Yes | Varies | No |

## Docker

Gbrow works in Docker out of the box. The `setup.sh` script handles Chromium sandboxing automatically.

If you're running manually in Docker, set `chromiumSandbox: false` in the browser launch options.

## Credits

Built on [gstack](https://github.com/garrytan/gstack) by [Gary Tan](https://github.com/garrytan). Adapted for OpenClaw under the MIT license.

## License

MIT
