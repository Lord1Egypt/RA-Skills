---
name: chrome-relay
version: 1.0.0
description: |
  Control the user's local Chrome browser via OpenClaw Browser Relay extension. Use when:
  (1) User asks to control/access their browser
  (2) User wants to automate browser actions (click, type, navigate, screenshot)
  (3) User wants to read page content from a specific Chrome tab
  (4) User wants to use existing logged-in sessions on websites
  (5) User provides a Chrome tab URL and wants you to interact with it
  
  Not for: headless browser automation without user session (use browser tool with default profile)
---

# Chrome Relay Browser Control

Control the user's local Chrome browser through the OpenClaw Browser Relay extension. This provides access to the user's real logged-in browser sessions.

## Setup (First Time)

If user doesn't have Browser Relay extension installed:

1. **Get extension path:**
   ```
   ~/.openclaw/browser/chrome-extension
   ```
   Or run: `open ~/.openclaw/browser/chrome-extension` (macOS)

2. **Install in Chrome:**
   - Open `chrome://extensions`
   - Enable "Developer mode" (top right)
   - Click "Load unpacked"
   - Select the extension folder

3. **Get Gateway token:**
   ```
   openclaw config get gateway.auth.token
   ```

4. **Configure extension:**
   - Click extension icon → Settings
   - Enter the gateway token
   - Save

5. **Connect:**
   - Open the Chrome tab you want controlled
   - Click the extension icon to attach (badge shows ON)

## Usage

### Check Connected Tabs
```bash
openclaw browser tabs --profile chrome-relay
```

Or use the tool:
```
browser(action=tabs, profile=chrome-relay)
```

### Read Page Content
```
browser(action=snapshot, profile=chrome-relay, targetId=<targetId>)
```

### Navigate
```
browser(action=navigate, profile=chrome-relay, targetId=<targetId>, url="https://...")
```

### Interact with Page

**Note:** aria-ref based selectors have reliability issues in chrome-relay mode. Prefer JavaScript evaluation for complex interactions:

```javascript
// Click element
browser(action=act, kind=evaluate, profile=chrome-relay, 
  fn="document.querySelector('selector').click()")

// Type in input
browser(action=act, kind=evaluate, profile=chrome-relay, 
  fn="document.querySelector('input').value = 'text'")

// Get element info
browser(action=act, kind=evaluate, profile=chrome-relay, 
  fn="document.querySelector('selector').innerText")
```

### Limitations

- aria-ref selectors may timeout; use JavaScript evaluate instead
- Extension must be attached (icon shows ON) for each tab
- Only works with Chrome browser
- Connection port: 18792

## Troubleshooting

**Red ! badge on extension:**
- Gateway not running → start with `openclaw gateway start`
- Token mismatch → verify token in extension settings

**Can't find element:**
- Page may have loaded new DOM → re-snapshot
- Use browser devtools console to find selectors first
