---
name: chrome-devtools-mcp-manager
description: Manage chrome-devtools-mcp service and OpenClaw's built-in Chrome browser for MCP-based browser automation. Use when user needs to use chrome-devtools-mcp functionality, ensure the browser is ready for MCP operations, or manage the browser/MCP lifecycle.
---

# Chrome DevTools MCP Manager

Manage OpenClaw's built-in Chrome browser and chrome-devtools-mcp integration for browser automation via MCP protocol.

## Overview

This skill manages two components:
1. **OpenClaw's Built-in Chrome** (`openclaw` profile) - The browser instance
2. **chrome-devtools-mcp** - The MCP server that exposes browser control tools

## Architecture

```
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│   OpenClaw      │────▶│  Built-in Chrome    │◀────│  chrome-devtools│
│   (browser tool)│     │  (CDP Port 18800)   │     │  -mcp (MCP srv) │
└─────────────────┘     └─────────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │  MCP Client     │
                                                │  (mcporter etc) │
                                                └─────────────────┘
```

### Built-in Chrome (openclaw profile)
- **CDP Port**: 18800
- **Managed by**: OpenClaw's `browser` tool
- **Auto-start**: Yes, via `browser(action: "open")`
- **Profile isolation**: Separate user data directory

### chrome-devtools-mcp
- **Type**: MCP (Model Context Protocol) server
- **Transport**: stdio (not HTTP)
- **Lifecycle**: Runs per MCP client session
- **Connection**: Connects to Chrome via CDP on port 18800

## Component Status Check

### 1. Check Built-in Chrome Status

```javascript
browser({
  action: "status",
  profile: "openclaw"
})
```

**Expected running state:**
```json
{
  "enabled": true,
  "profile": "openclaw",
  "running": true,
  "cdpReady": true,
  "cdpPort": 18800,
  "cdpUrl": "http://127.0.0.1:18800"
}
```

### 2. Verify CDP Endpoint

```powershell
Invoke-WebRequest -Uri "http://localhost:18800/json/version" -Method GET
```

**Expected response:**
```json
{
  "Browser": "Chrome/134.0.0.0",
  "Protocol-Version": "1.3",
  "User-Agent": "Mozilla/5.0...",
  "V8-Version": "...",
  "WebKit-Version": "...",
  "webSocketDebuggerUrl": "ws://localhost:18800/devtools/browser/..."
}
```

### 3. Check MCP Server Status

Since chrome-devtools-mcp runs as a stdio service per MCP client session, there's no persistent process to check. Instead, verify the MCP configuration is correct.

## Managing Built-in Chrome

### Start Built-in Chrome

```javascript
// Open a blank page to start Chrome
browser({
  action: "open",
  profile: "openclaw",
  url: "about:blank"
})

// Or navigate to a specific URL
browser({
  action: "open",
  profile: "openclaw",
  url: "https://chat.deepseek.com/"
})
```

### Stop Built-in Chrome

```javascript
browser({
  action: "stop",
  profile: "openclaw"
})
```

### Restart Built-in Chrome

```javascript
// Stop first
browser({ action: "stop", profile: "openclaw" })

// Then start
browser({ action: "open", profile: "openclaw", url: "about:blank" })
```

## MCP Server Configuration

### For mcporter CLI

Configure mcporter to use chrome-devtools-mcp:

```bash
# Add MCP server to mcporter
mcporter server add chrome-devtools \
  --command "npx" \
  --args "chrome-devtools-mcp@latest,--browserUrl,http://127.0.0.1:18800,--no-usage-statistics"

# Or with auto-connect (Chrome will be started if not running)
mcporter server add chrome-devtools \
  --command "npx" \
  --args "chrome-devtools-mcp@latest,--autoConnect,--no-usage-statistics"
```

### For Claude Desktop / Other MCP Clients

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browserUrl", "http://127.0.0.1:18800",
        "--no-usage-statistics"
      ]
    }
  }
}
```

### Environment Variables

```powershell
# Disable usage statistics
$env:CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS = "1"

# Enable debug logging
$env:DEBUG = "*"
```

## Complete Setup Workflow

### First-Time Setup

1. **Verify built-in Chrome is ready:**
   ```javascript
   const status = await browser({ action: "status", profile: "openclaw" })
   if (!status.cdpReady) {
     await browser({ action: "open", profile: "openclaw", url: "about:blank" })
   }
   ```

2. **Test CDP connection:**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:18800/json/version"
   ```

3. **Configure MCP client** (mcporter, Claude Desktop, etc.)

4. **Test MCP connection:**
   ```bash
   mcporter call chrome-devtools.list_pages
   ```

### Daily Usage Pattern

1. **Ensure Chrome is running** (before MCP operations):
   ```javascript
   const status = await browser({ action: "status", profile: "openclaw" })
   if (!status.cdpReady) {
     await browser({ action: "open", profile: "openclaw", url: "about:blank" })
     await new Promise(r => setTimeout(r, 2000))  // Wait for startup
   }
   ```

2. **Use MCP tools** via mcporter or other MCP client

3. **Keep Chrome running** for subsequent operations

## Available MCP Tools

Once connected via chrome-devtools-mcp, these tools are available:

### Page Management
- `list_pages` - List all open tabs/pages
- `new_page` - Create new tab
- `select_page` - Switch to specific tab
- `close_page` - Close a tab
- `navigate_page` - Navigate to URL / back / forward / refresh

### Interaction
- `click` - Click element by uid
- `fill` - Fill input field
- `type_text` - Type text
- `press_key` - Press keyboard key
- `select_option` - Select dropdown option

### Inspection
- `take_snapshot` - Get accessibility tree snapshot
- `take_screenshot` - Capture screenshot
- `evaluate_script` - Execute JavaScript
- `wait_for` - Wait for text/element

### Browser State
- `get_browser_state` - Get cookies, localStorage, etc.
- `set_browser_state` - Set cookies, localStorage, etc.

## Integration with Other Skills

### Example: deepseek-web-query

This skill uses chrome-devtools-mcp via mcporter:

```bash
# 1. Ensure Chrome is running (via browser tool)
# 2. Use mcporter to call MCP tools
mcporter call chrome-devtools.navigate_page type: "url" url: "https://chat.deepseek.com/"
mcporter call chrome-devtools.take_snapshot
mcporter call chrome-devtools.type_text text: "查询内容"
mcporter call chrome-devtools.press_key key: "Enter"
mcporter call chrome-devtools.evaluate_script function: '() => document.body.innerText'
```

## Troubleshooting

### "CDP not ready"

**Symptoms:** `browser({ action: "status" })` shows `cdpReady: false`

**Solutions:**
1. Restart Chrome:
   ```javascript
   browser({ action: "stop", profile: "openclaw" })
   browser({ action: "open", profile: "openclaw", url: "about:blank" })
   ```
2. Check for port conflicts:
   ```powershell
   Get-NetTCPConnection -LocalPort 18800
   ```

### "Cannot connect to Chrome" from MCP

**Symptoms:** MCP server fails to connect

**Solutions:**
1. Verify CDP endpoint is accessible:
   ```powershell
   curl http://localhost:18800/json/version
   ```
2. Check Windows Firewall isn't blocking localhost
3. Ensure Chrome was started with remote debugging enabled (built-in profile does this automatically)

### MCP server exits immediately

**This is normal behavior!** The MCP server:
- Waits for JSON-RPC messages on stdin
- Exits when stdin closes (client disconnects)
- Is designed to be launched per-session by MCP clients

### Port 18800 conflicts

**Check what's using the port:**
```powershell
Get-NetTCPConnection -LocalPort 18800 | 
  Select-Object LocalPort, State, OwningProcess, @{Name="ProcessName";Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).Name}}
```

**Kill conflicting process:**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 18800).OwningProcess | Stop-Process -Force
```

## Best Practices

1. **Always check Chrome status first** before MCP operations
2. **Reuse browser sessions** - Don't close Chrome between operations
3. **Use `about:blank` for quick startup** when you don't need a specific page
4. **Configure MCP client once** - The config persists across sessions
5. **Handle login states** in your automation logic (e.g., deepseek-web-query handles DeepSeek login)

## Quick Reference

| Task | Command |
|------|---------|
| Check Chrome status | `browser({ action: "status", profile: "openclaw" })` |
| Start Chrome | `browser({ action: "open", profile: "openclaw", url: "about:blank" })` |
| Stop Chrome | `browser({ action: "stop", profile: "openclaw" })` |
| Test CDP | `Invoke-WebRequest http://localhost:18800/json/version` |
| Add MCP to mcporter | `mcporter server add chrome-devtools --command "npx" --args "..."` |
| List MCP pages | `mcporter call chrome-devtools.list_pages` |

## References

- [chrome-devtools-mcp GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw Browser Tool](https://docs.openclaw.ai/tools/browser)
