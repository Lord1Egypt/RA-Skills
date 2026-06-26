---
name: beatport-dl-with-browser-tool
description: Download purchased tracks from Beatport using the openclaw headless browser tool (CDP). Handles login, authentication via NextAuth, enabling downloads in headless Chrome, and saving files locally. Use when the user asks to download music, tracks, or files from Beatport, or manage their Beatport purchases/library. Triggers on phrases like "download from beatport", "beatport download", "download my tracks", "get my beatport music".
---

# Beatport Download via Browser Tool

Download purchased Beatport tracks through the openclaw headless browser using CDP (Chrome DevTools Protocol).

## Prerequisites

- openclaw browser running on `127.0.0.1:9222`
- Beatport credentials (username + password)
- `ws` module at `/opt/homebrew/lib/node_modules/openclaw/node_modules/ws`
- Node.js runtime

## Authentication Flow

Beatport uses a dual-auth system:

1. **account.beatport.com** — Django session (`sessionid` cookie)
2. **www.beatport.com** — NextAuth (`__Secure-next-auth.session-token` cookie)

### Login Steps

1. Navigate to `https://account.beatport.com/` via CDP `Page.navigate`
2. Fill username/password via `Runtime.evaluate` (use native input setters to bypass React controlled inputs)
3. Submit the login form
4. On the www.beatport.com tab, sign in via NextAuth:

```javascript
// In browser context on www.beatport.com
fetch("/api/auth/csrf").then(r => r.json()).then(csrf => {
  const fd = new URLSearchParams();
  fd.append("csrfToken", csrf.csrfToken);
  fd.append("username", "USER");
  fd.append("password", "PASS");
  fd.append("callbackUrl", "https://www.beatport.com/");
  // Create hidden form and submit (fetch redirect fails cross-origin)
  const form = document.createElement("form");
  form.method = "POST";
  form.action = "/api/auth/signin/beatport";
  form.style.display = "none";
  for (const [k, v] of Object.entries(Object.fromEntries(fd))) {
    const inp = document.createElement("input");
    inp.type = "hidden"; inp.name = k; inp.value = v;
    form.appendChild(inp);
  }
  document.body.appendChild(form);
  form.submit();
});
```

5. Verify login: `Account menu` button should appear in navbar (no `Create Account or Log In` button)

## Key URLs

| Page | URL | Purpose |
|------|-----|---------|
| Cart | `https://www.beatport.com/cart` | Items pending purchase |
| Library | `https://www.beatport.com/library` | Purchased tracks (may show Upgrade for free accounts) |
| Downloads | `https://www.beatport.com/library/downloads` | Download queue |
| Checkout | `https://www.beatport.com/checkout` | Payment page |

**Note:** `/my-beatport/downloads` and `/my-beatport/collection` return 404. The correct paths are `/library` and `/library/downloads`.

## Enabling Downloads in Headless Chrome

Headless Chrome cancels downloads by default. Enable via CDP on the **browser-level** WebSocket:

```javascript
// Browser-level WS: ws://127.0.0.1:9222/devtools/browser/<id>
ws.send(JSON.stringify({
  id: 1,
  method: "Browser.setDownloadBehavior",
  params: {
    behavior: "allowAndName",
    downloadPath: "/path/to/download/dir/",
    eventsEnabled: true
  }
}));
```

Get browser ID from `http://127.0.0.1:9222/json/version` → `webSocketDebuggerUrl`.

## Downloading Tracks

### Step 1: Add tracks to download queue

On `/library`, each track has a re-download icon (`svg[data-testid='icon-re-download']`). Click each one to add to the download queue:

```javascript
var icons = document.querySelectorAll("svg[data-testid='icon-re-download']");
icons.forEach(function(icon, i) {
  setTimeout(function() { icon.closest("button, div").click(); }, i * 500);
});
```

### Step 2: Download from queue page

Navigate to `/library/downloads`. All queued tracks appear with a "Download All" button.

### Step 3: Click Download All

Enable browser downloads first (see above), then click:

```javascript
var btn = [...document.querySelectorAll("button")].find(b => b.innerText.includes("Download All"));
if (btn) btn.click();
```

The download arrives as a zip file (e.g. `beatport_tracks_2026-04.zip`).

### Step 4: Unzip and clean up

```bash
cd /path/to/download/dir
unzip -o beatport_tracks_*.zip -d tmp/
mv tmp/*.mp3 .
rm -rf tmp/ beatport_tracks_*.zip
```

### Download URL Format

```
https://zips.beatport.com/v1/download?token=<JWT_TOKEN>
```
The token is single-use and expires quickly. Always capture fresh from events.

### Download URL Format

```
https://zips.beatport.com/v1/download?token=<JWT_TOKEN>
```

The token is single-use and expires quickly. Always capture it fresh from the `Page.downloadWillBegin` event.

## API Access

### Access Token

```bash
curl -s -H "Cookie: <cookies>" \
  "https://www.beatport.com/_next/data/<buildId>/en/library/downloads.json" \
  | jq -r '.pageProps.accessToken'
```

### Library Data

```bash
curl -s -H "Cookie: <cookies>" \
  "https://www.beatport.com/_next/data/<buildId>/en/library.json" \
  | jq '.pageProps.dehydratedState.queries[].state.data.results[] | {name, id, artists}'
```

### Build ID

```bash
curl -s "https://www.beatport.com/" | grep -o '"buildId":"[^"]*"' | head -1
```

Current buildId (subject to change): `PWoDyRo_P5V8lNYu_92bX`

## Common Pitfalls

1. **Cross-domain navigation fails with `Page.navigate`** — Use `location.href = "..."` via `Runtime.evaluate` instead
2. **React controlled inputs don't respond to `.value =`** — Use native input value setter:
   ```javascript
   var input = document.querySelector("input[name=username]");
   var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
   nativeSetter.call(input, "username");
   input.dispatchEvent(new Event("input", { bubbles: true }));
   ```
3. **Node.js string escaping in `-e`** — Use `String.raw\`...\`` template literals, or write code to a file and run with `node file.js`
4. **Free account download limit** — 20 downloads per track. "Unlimited re-downloads" requires Beatport Streaming subscription
5. **CDP exec timeout** — openclaw kills long-running node processes (~10s). Keep CDP operations short; use `background: true` + `process poll` for longer waits
6. **`curl` path** — Use `/usr/bin/curl`, not `/opt/homebrew/bin/curl` (may not exist)

## CDP Helper Pattern

Write scripts to files to avoid shell escaping issues:

```javascript
// scripts/beatport-cdp.js
const WS = require("/opt/homebrew/lib/node_modules/openclaw/node_modules/ws");
const http = require("http");

function getPage(filter) {
  return new Promise((resolve) => {
    http.get("http://127.0.0.1:9222/json", (res) => {
      let body = "";
      res.on("data", (c) => body += c);
      res.on("end", () => {
        const pages = JSON.parse(body).filter(p => p.type === "page");
        resolve(filter ? pages.find(filter) || pages[0] : pages[0]);
      });
    });
  });
}

function cdpEval(ws, expression) {
  return new Promise((resolve) => {
    ws.send(JSON.stringify({ id: Date.now(), method: "Runtime.evaluate", params: { expression, returnByValue: true } }));
    ws.on("message", (m) => {
      const d = JSON.parse(m.toString());
      if (d.id && d.result) { resolve(d.result); }
    });
  });
}

async function screenshot(ws, path) {
  return new Promise((resolve) => {
    ws.send(JSON.stringify({ id: Date.now(), method: "Page.captureScreenshot", params: { format: "png" } }));
    ws.on("message", (m) => {
      const d = JSON.parse(m.toString());
      if (d.id && d.result && d.result.data) {
        require("fs").writeFileSync(path, Buffer.from(d.result.data, "base64"));
        resolve();
      }
    });
  });
}

module.exports = { getPage, cdpEval, screenshot };
```

## Format Compatibility

- **CDJ-2000**: MP3 or WAV
- Beatport download options: MP3, WAV, AIFF, FLAC
- Default is MP3; select WAV/AIFF on cart page or account settings if needed for CDJ compatibility
