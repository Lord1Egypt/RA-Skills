---
name: browser-cli
description: Control Chrome browsers from the terminal via the AIPex extension. Use this skill when the agent needs to manage browser tabs, search page elements, click buttons, fill forms, capture screenshots, or download content — all through shell commands without an MCP client.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    emoji: "🖥️"
    homepage: https://github.com/AIPexStudio/browser-cli
    os: [macos, linux, windows]
---

# browser-cli — Terminal Browser Control

`browser-cli` is a command-line tool that controls Chrome browsers through the AIPex extension's WebSocket daemon. It translates shell commands into browser actions — managing tabs, clicking elements, filling forms, capturing screenshots, and more.

**Architecture:**
```
browser-cli ──WebSocket──▶ aipex-daemon ──WebSocket──▶ AIPex Chrome Extension ──▶ Browser APIs
```

The daemon auto-spawns on first use and self-terminates when idle. No manual setup beyond initial extension connection.

---

## When to Use This Skill

Use this skill when the user wants to:

- Control a Chrome browser from the terminal without an MCP client
- Open, close, switch, or organize browser tabs via CLI
- Search for page elements and interact with them (click, fill, hover)
- Capture screenshots of browser tabs
- Automate browser workflows in shell scripts or CI pipelines
- Download page content as markdown or images
- Request human input during automated browser tasks
- Manage AIPex skills from the command line

**Trigger phrases:** "browser-cli", "control browser from terminal", "browser automation CLI", "click element from shell", "terminal browser control", "command line browser", "shell browser automation"

---

## Prerequisites

- **Node.js >= 18** installed
- **AIPex Chrome extension** installed and connected to the daemon
- `browser-cli` installed globally: `npm install -g browser-cli`

### First-time Setup

After installing, connect the AIPex extension to the daemon:

1. Open Chrome → AIPex extension icon → **Options**
2. Set WebSocket URL to `ws://localhost:9223/extension`
3. Click **Connect**
4. Verify: `browser-cli status`

---

## Command Groups

### tab — Manage browser tabs

```bash
browser-cli tab list                         # List all open tabs
browser-cli tab current                      # Get the active tab
browser-cli tab new https://example.com      # Open a new tab
browser-cli tab switch 42                    # Switch to tab by ID
browser-cli tab close 42                     # Close a tab
browser-cli tab info 42                      # Get tab details
browser-cli tab organize                     # AI-powered tab grouping
browser-cli tab ungroup                      # Remove all tab groups
```

### page — Inspect and interact with page content

```bash
browser-cli page search "button*" --tab 123              # Search elements by glob pattern
browser-cli page search "{input,textarea}*" --tab 123    # Search multiple element types
browser-cli page screenshot                               # Screenshot active tab
browser-cli page screenshot-tab 123 --send-to-llm true   # Screenshot with LLM analysis
browser-cli page metadata --tab 123                       # Get page metadata
browser-cli page scroll-to "#main-content"                # Scroll to element
browser-cli page highlight "button.submit"                # Highlight element
browser-cli page highlight-text "p" "important"           # Highlight text in content
```

### interact — Click, fill, hover, and type

```bash
browser-cli interact click btn-42 --tab 123                         # Click by UID
browser-cli interact fill input-5 "hello world" --tab 123           # Fill input by UID
browser-cli interact hover menu-3 --tab 123                         # Hover by UID
browser-cli interact form --tab 123 --elements '[{"uid":"in-1","value":"foo"}]'  # Batch fill
browser-cli interact editor editor-1 --tab 123                     # Get editor content
browser-cli interact upload --tab 123 --file-path /path/to/file    # Upload file
browser-cli interact computer --action left_click --coordinate "[500,300]"  # Pixel-level click
```

### download — Save content locally

```bash
browser-cli download markdown --text "# Notes" --filename notes    # Save as markdown
browser-cli download image --data "data:image/png;base64,..."      # Save image
browser-cli download chat-images --messages '[...]' --folder imgs   # Batch save images
```

### intervention — Request human input

```bash
browser-cli intervention list                                       # List intervention types
browser-cli intervention info voice-input                           # Get type details
browser-cli intervention request voice-input --reason "Need input"  # Request intervention
browser-cli intervention cancel                                     # Cancel active request
```

### skill — Manage AIPex skills

```bash
browser-cli skill list                                    # List all skills
browser-cli skill load my-skill                           # Load skill content
browser-cli skill info my-skill                           # Skill details
browser-cli skill run my-skill scripts/init.js            # Execute skill script
browser-cli skill ref my-skill references/guide.md        # Read skill reference
browser-cli skill asset my-skill assets/icon.png          # Get skill asset
```

### Standalone commands

```bash
browser-cli status    # Check daemon + extension connection
browser-cli update    # Self-update to latest version
```

---

## Workflow: Search, Interact, Verify

The recommended pattern for browser automation:

```bash
# 1. Discover tabs
browser-cli tab list

# 2. Search for elements (fast, no screenshot needed)
browser-cli page search "{button,input,link}*" --tab 123

# 3. Interact using UIDs from search results
browser-cli interact click btn-submit --tab 123
# or
browser-cli interact fill input-email "user@example.com" --tab 123

# 4. Verify visually (only when needed)
browser-cli page screenshot
```

### Login form example

```bash
browser-cli page search "{input,textbox}*" --tab 123
browser-cli interact fill input-email "user@example.com" --tab 123
browser-cli interact fill input-pass "secret" --tab 123
browser-cli page search "*[Ll]ogin*" --tab 123
browser-cli interact click btn-login --tab 123
```

### Shell script example

```bash
#!/bin/bash
browser-cli tab new https://example.com
sleep 2
TAB_ID=$(browser-cli tab current | jq '.data.id')
browser-cli page search "link*" --tab "$TAB_ID"
browser-cli page screenshot
```

---

## Global Options

| Option | Default | Description |
|--------|---------|-------------|
| `--port <n>` | `9223` | Daemon WebSocket port |
| `--host <h>` | `127.0.0.1` | Daemon host address |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER_CLI_WS_URL` | `ws://127.0.0.1:9223/cli` | Override daemon WebSocket URL |
| `BROWSER_CLI_CONNECT_TIMEOUT` | `60000` | Connection timeout (ms) |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Daemon not running` | Run any command to auto-spawn, or check with `browser-cli status` |
| `Extension is not connected` | Open AIPex Options → WebSocket URL `ws://localhost:9223/extension` → Connect |
| Port 9223 in use | Use `--port 9224` and update extension URL |
| Timeout after 60s | Verify extension is connected. Increase with `BROWSER_CLI_CONNECT_TIMEOUT=120000` |
| 0 search results | Try different patterns. Fall back to `page screenshot --send-to-llm true` + `interact computer` |
| Wrong results | Verify tab ID with `browser-cli tab list` |
