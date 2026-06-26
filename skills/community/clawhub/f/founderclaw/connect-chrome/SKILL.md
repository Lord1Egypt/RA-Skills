---
name: connect-chrome
description: >
  Launch real Chrome controlled by the agent with a Side Panel extension.
  Watch every action in real time in a visible browser window.
  Use when: "connect chrome", "open chrome", "real browser", "launch chrome",
  "side panel", "control my browser", "watch it work".
---

# Connect Chrome — Real Browser with Side Panel

Launch a visible Chrome window controlled by the agent. You see every click, every navigation, every action in real time.

## Requirements

- **Bun** v1.0+ and the browse binary built (see browse skill)
- Desktop environment or X11 forwarding (can't run headed Chrome on a headless server without display)

## Step 0: Pre-flight Cleanup

Kill any stale browse servers and clean Chromium profile locks:

```bash
# Kill existing browse server
pkill -f "browse.*server" 2>/dev/null || true
sleep 1

# Clean Chromium profile locks
PROFILE_DIR="$HOME/.founderclaw/chromium-profile"
mkdir -p "$PROFILE_DIR"
for LF in SingletonLock SingletonSocket SingletonCookie; do
  rm -f "$PROFILE_DIR/$LF" 2>/dev/null || true
done
echo "Pre-flight cleanup done"
```

## Step 1: Connect

Set the browse binary path, then connect:

```bash
BROWSE="founderclaw/browse/dist/browse"
$BROWSE connect
```

This launches Chromium in headed mode with:
- A visible window you can watch (not your regular Chrome)
- A golden shimmer line at the top of every page (shows which window is controlled)
- Side Panel extension auto-loaded
- Port 34567 for extension communication

After connecting, verify:

```bash
$BROWSE status
```

Confirm output shows `Mode: headed`.

## Step 2: Guide to Side Panel

Tell the user:

> Chrome is launched. You should see Playwright's Chromium (not your regular Chrome) with a golden shimmer line at the top.
>
> To open the Side Panel:
> 1. Look for the **puzzle piece icon** (Extensions) in the toolbar
> 2. Click it, find **founderclaw browse**, click the **pin icon**
> 3. Click the pinned icon — the Side Panel opens on the right
> 4. You should see a live activity feed

If the extension isn't visible:
> 1. Go to `chrome://extensions`
> 2. Look for "founderclaw browse" — it should be listed
> 3. If not, click "Load unpacked" and point to `founderclaw/browse/extension/`
> 4. Pin it from the puzzle piece menu

## Step 3: Demo

```bash
$BROWSE goto https://news.ycombinator.com
```

Wait 2 seconds, then:

```bash
$BROWSE snapshot -i
```

Tell the user: "Check the Side Panel — every command appears in the activity feed in real time."

## Commands

| Command | What it does |
|---------|-------------|
| `$BROWSE connect` | Launch headed Chrome with extension |
| `$BROWSE disconnect` | Close headed Chrome, return to headless |
| `$BROWSE focus` | Bring Chrome to foreground |
| `$BROWSE status` | Check connection status |

## What You Can Do

- Run any skill (qa, design-review, benchmark) and watch it work in real time
- Use the sidebar chat to control the browser with natural language
- All browse commands work in headed mode — same API, visible execution

## Troubleshooting

**"No display"** — Headed mode needs a display. On a remote server, set up X11 forwarding or VNC.

**"Already connected"** — Run the cleanup step first, then reconnect.

**Extension not loading** — Check `chrome://extensions`, load manually from the extension directory.
