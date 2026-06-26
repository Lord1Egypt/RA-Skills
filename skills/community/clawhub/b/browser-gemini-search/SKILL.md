---
name: browser-gemini-search
description: Use Google Gemini (gemini.google.com) to search the web via OpenClaw's browser control. Activates when user asks to search something using Gemini, or wants to browse to Gemini. Uses the user's existing Chrome session via Chrome MCP (profile="user"). Prerequisites: (1) Chrome must be running with remote debugging enabled (--remote-debugging-port=9222), (2) user profile must be connected and approved when prompted. If browser is not connected, guide user to start Chrome with debugging port first.
---

# Browser Gemini Search

Use OpenClaw's browser tool to control the user's Chrome and search Gemini.

## Workflow

1. **Ensure browser is connected**
   - Run `browser(action="start", profile="user", target="host")`
   - If `attachOnly` error or timeout: Chrome is not running with debugging port
     - Ask user to run: `& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`
     - Then retry connection

2. **Find or open Gemini tab**
   - Run `browser(action="tabs", profile="user", target="host")` to list open tabs
   - Look for existing Gemini tab (URL contains `gemini.google.com`)
   - If found: `browser(action="focus", targetId="<id>", profile="user", target="host")`
   - If not found: open new tab via `browser(action="navigate", url="https://gemini.google.com", target="host")`

3. **Wait for page load**
   - Run `browser(action="snapshot", profile="user", target="host")` to verify page is ready
   - Look for the input textbox (usually `textbox` with placeholder like "Ask Gemini" or "输入双子座的提示")

4. **Type the search query**
   - Use `browser(action="act", kind="type", ref="<textbox_ref>", text="<user's search query>", profile="user", target="host")`
   - Then `browser(action="act", kind="click", ref="<send_button_ref>", profile="user", target="host")` to send

5. **Read Gemini's response**
   - Wait 5-10 seconds for response to generate
   - Run `browser(action="snapshot", profile="user", target="host")` to read the answer
   - Present the answer to the user

## Quick reference

```python
# Step 1: connect
browser(action="start", profile="user", target="host")

# Step 2: find tab or navigate
browser(action="tabs", profile="user", target="host")
browser(action="focus", targetId="11", profile="user", target="host")  # if found
browser(action="navigate", url="https://gemini.google.com", target="host")  # if not found

# Step 3 & 4: type and send
browser(action="act", kind="type", ref="1_1236", text="search query here", profile="user", target="host")
browser(action="act", kind="click", ref="2_2", profile="user", target="host")  # send button

# Step 5: read response
browser(action="snapshot", profile="user", target="host")
```

## Common issues

- **"Chrome MCP existing-session attach timed out"**: Chrome debugging port not enabled. User must restart Chrome with `--remote-debugging-port=9222`.
- **SSRF blocked URL**: The Gemini domain must be in `browser.ssrfPolicy.hostnameAllowlist` in openclaw.json. Add if missing: `*.google.com`
- **Tab focus fails**: Use correct `targetId` from `tabs` output
- **Input ref changes**: Re-run snapshot to get fresh refs after page navigation
