---
name: chromium
description: Launch a persistent headless Chromium with remote debugging (CDP) for browser automation — page navigation, clicks, form filling, screenshots, and cookie import. Use when the user asks to open a website, browse, click, read page content, or work with a browser.
---

# Chromium (persistent headless profile)

## What it does

- Launches headless Chromium with a **persistent profile** (logins, cookies, localStorage survive restarts).
- Exposes Chrome DevTools Protocol (CDP) on `127.0.0.1` for browser tool integration.
- Supports cookie import for pre-authenticated sessions.

## Quick start

### 1. Launch Chromium

```bash
~/.openclaw/workspace/skills/chromium/scripts/start_chromium.sh
```

Environment variables (all optional):

| Variable | Default | Description |
|---|---|---|
| `CHROMIUM_PROFILE_DIR` | `$HOME/.openclaw/workspace/chromium-profile` | User data directory |
| `CHROMIUM_DEBUG_PORT` | `18801` | CDP remote debugging port |
| `CHROMIUM_LOG_FILE` | `$HOME/.openclaw/workspace/logs/chromium.log` | Log file path |
| `CHROMIUM_BIN` | auto-detect (`chromium`, `chromium-browser`, `google-chrome`) | Browser binary |

### 2. Verify CDP is ready

```bash
curl -s http://127.0.0.1:18801/json/version
```

If you get JSON with `Browser` and `webSocketDebuggerUrl` — it's ready.

### 3. Use browser tools

```
browser navigate url=https://example.com
browser wait --load networkidle
browser snapshot
```

## Browser tool cheatsheet

| Action | Command |
|---|---|
| Open page | `browser navigate url=<URL>` |
| Wait for load | `browser wait --load networkidle` |
| Read page content | `browser snapshot` |
| Click element | `browser click ref=<ref>` |
| Type text | `browser type ref=<ref> text=<text>` |
| Scroll to element | `browser scrollintoview <ref>` |
| Take screenshot | `browser screenshot` |
| Run JavaScript | `browser evaluate --fn "document.title"` |

## Snapshot format — important

**Always use the default snapshot format** (no extra parameters):

```
browser snapshot
```

**Do NOT use:**
- `refs=aria` — returns accessibility tree without actionable refs
- `depth=2` or other depth limits — truncates DOM and hides content

The default AI format returns full page text with refs (e12, e293, etc.) suitable for click/type.

## Working with dynamic pages (SPAs)

Single-page apps (React, Next.js, etc.) continuously update the DOM. Refs become stale between snapshots.

**After every navigation:**
```
browser wait --load networkidle
browser snapshot
```

**Before clicking:**
```
browser scrollintoview <ref>
browser click <ref>
```

**If click fails** ("Element not found or not visible"):
1. Take a fresh `browser snapshot` — never reuse old refs
2. Use `browser screenshot` to see the visual state
3. For links, navigate directly by URL instead of clicking
4. As a last resort, use JavaScript: `browser evaluate --fn "document.querySelector('...').click()"`

## Cookie import (pre-authenticated sessions)

To use a site that requires login, export cookies from a browser where you're already logged in and import them:

**Step 1 — Export cookies** (in your regular browser):
- Install [Cookie-Editor](https://cookie-editor.com/) extension
- Go to the target site (make sure you're logged in)
- Export cookies as JSON, save as `cookies.json`
- Copy to server: `scp cookies.json server:/tmp/`

**Step 2 — Import:**

```bash
python3 ~/.openclaw/workspace/skills/chromium/scripts/import_cookies.py \
  /tmp/cookies.json \
  --domain example.com
```

**Step 3 — Verify** by navigating to the site and checking if you're logged in.

## Data locations

| What | Path |
|---|---|
| Browser profile | `$CHROMIUM_PROFILE_DIR` (default: `~/.openclaw/workspace/chromium-profile`) |
| Launch log | `$CHROMIUM_LOG_FILE` (default: `~/.openclaw/workspace/logs/chromium.log`) |

## Troubleshooting

If CDP doesn't respond within 3 seconds after launch, check the log:

```bash
cat ~/.openclaw/workspace/logs/chromium.log
```

Common issues:
- **"Address already in use"** — another Chromium is running. The script kills previous instances automatically, but you can run `pkill -f "chromium.*remote-debugging"` manually.
- **SingletonLock** — stale lock file. The script removes it if Chromium isn't running.
- **No `chromium` binary** — set `CHROMIUM_BIN` to the correct path (e.g., `/usr/bin/google-chrome`).

## Requirements

- Chromium, Chromium Browser, or Google Chrome installed on the host
- Python 3 (for cookie import script)
- OpenClaw with browser tool support
