---
name: chrome-cdp-remote
description: Control Chrome/Chromium via CDP (Chrome DevTools Protocol) — open tabs, navigate URLs, take screenshots, execute JS. Supports local and remote machines via SSH tunnel.
tags: [browser, automation, cdp, chrome, screenshots, devtools, remote]
---

# Chrome CDP Remote Control

Use when: automating browser tasks programmatically — navigate pages, capture screenshots, run searches, execute JavaScript — without a full Playwright/Puppeteer dependency.

---

## Setup: Launch Chrome with CDP enabled

### Linux
```bash
google-chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir=~/.config/chrome-cdp
```

### macOS
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/.config/chrome-cdp"
```

Note: Use a dedicated `--user-data-dir` (e.g. `~/.config/chrome-cdp`) — Chrome 126+ blocks CDP on the default profile by design. Log in with your Google account once to enable sync.

Note: On macOS, omit `--user-data-dir` only if you don't need sync — it gives you your real profile with extensions and custom shortcuts.

### Verify CDP is running
```bash
curl http://localhost:9222/json/version
```
Should return browser version and a `webSocketDebuggerUrl`.

### Kill and relaunch
```bash
pkill -f 'chrome.*remote-debugging-port=9222'
sleep 2
# relaunch with flags above
```

---

## Setup: Remote machine via SSH tunnel (recommended)

Forward the remote machine's CDP port to localhost:
```bash
ssh -L 9223:localhost:9222 user@remote-host -N &
```
Then use `PORT = 9223` in your scripts. Works great over Tailscale.

---

## macOS: Raycast Script Command

Save as `~/.config/raycast/scripts/chrome-cdp.sh` and `chmod +x`:

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Chrome CDP
# @raycast.mode silent
# @raycast.icon 🌐
# @raycast.description Launch Chrome with CDP enabled

pkill -f "Google Chrome.*remote-debugging-port" 2>/dev/null
sleep 1

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/.config/chrome-cdp" &

echo "Chrome CDP started on port 9222"
```

---

## Python: WebSocket control pattern

Install dependency (once):
```bash
pip install websocket-client
```

```python
import json, urllib.request, websocket, time, base64

PORT = 9222  # use 9223 if connecting via SSH tunnel

def send_recv(ws, method, params, msg_id):
    """Send a CDP command and wait for its response, draining intermediate events."""
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
    for _ in range(30):
        msg = json.loads(ws.recv())
        if msg.get("id") == msg_id:
            return msg
    return None

# Open a new tab
req = urllib.request.Request(f"http://localhost:{PORT}/json/new", method="PUT")
tab = json.loads(urllib.request.urlopen(req).read())

# Connect via WebSocket — origin header is required
ws = websocket.WebSocket()
ws.connect(tab["webSocketDebuggerUrl"], origin=f"http://localhost:{PORT}")
ws.settimeout(15)

msg_id = 1
send_recv(ws, "Page.enable", {}, msg_id); msg_id += 1

# Navigate to a URL
send_recv(ws, "Page.navigate", {"url": "https://example.com"}, msg_id); msg_id += 1
time.sleep(5)  # wait for page load

# Take a screenshot
# Use fromSurface + scale=2 on Retina/HiDPI displays (e.g. MacBook Pro)
result = send_recv(ws, "Page.captureScreenshot", {
    "format": "jpeg",
    "quality": 70,
    "fromSurface": True,
    "scale": 2  # remove on non-Retina displays
}, msg_id); msg_id += 1

img = base64.b64decode(result["result"]["data"])
with open("/tmp/cdp_screenshot.jpg", "wb") as f:
    f.write(img)

ws.close()
print("Screenshot saved.")
```

---

## Custom search engine shortcuts (bangs)

If Chrome is launched with a real user profile, custom search engine shortcuts are available.

Configure in Chrome → Settings → Search engine → Manage search engines.

Example — add Perplexity as `!ppx`:
- Shortcut: `!ppx`
- URL: `https://www.perplexity.ai/search?q=%s`

Trigger via address bar: type `!ppx` then Tab, then your query.

When controlling via CDP from a different machine, use the full URL directly:
```
https://www.perplexity.ai/search?q=YOUR+QUERY
https://www.google.com/search?q=YOUR+QUERY
```

---

## CDP patterns

- Never connect to `ws://localhost:9222/devtools/browser` directly — always fetch `http://localhost:9222/json/list` and use `webSocketDebuggerUrl` from the target tab
- `Runtime.enable` and `Page.enable` must be called before any `Runtime.evaluate` or `Page.navigate`
- `Network.responseReceived` doesn't include body — call `Network.getResponseBody` with requestId after response completes
- Block URLs before navigate: call `Network.setBlockedURLs` before `Page.navigate`, not after

---

## Pitfalls

- `--remote-allow-origins=*` is required — omitting it causes `403 Forbidden` on WebSocket handshake
- Chrome 126+ blocks CDP on the default profile — always use a dedicated `--user-data-dir`
- Always filter `ws.recv()` by message ID — CDP sends intermediate events between your command and its response
- SSH tunnel holds the port after Chrome dies — kill the tunnel before relaunching (`kill %1` or `pkill ssh`)
- macOS: omit `--user-data-dir` only if you want your real profile with bangs/extensions (and don't mind Chrome not starting if already open)
- Chromium-based alternatives (Helium, Brave, etc.) support CDP but may behave inconsistently — Chrome is most reliable
