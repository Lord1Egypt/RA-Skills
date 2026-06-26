# Setup Guide — Chrome AI Action

Detailed setup instructions for the Chrome AI Action bridge.

---

## Quick Start / 快速开始

The skill handles everything automatically. Just run:

```bash
node <skill_dir>/scripts/startup.js
```

This will:
1. Auto-install the `chrome-ai-action` npm package globally
2. Start the bridge on `127.0.0.1:9876`
3. If Chrome is not running with CDP, auto-launch it with correct parameters
4. Return when everything is ready

---

## Manual Chrome Launch

If you prefer to start Chrome manually instead of letting the bridge auto-launch:

### Windows

```powershell
# Close all Chrome instances first
taskkill /F /IM chrome.exe

# Start with remote debugging
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-ai-profile"
```

### macOS

```bash
killall "Google Chrome"
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-ai-profile
```

### Linux

```bash
killall chrome google-chrome
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-ai-profile
```

### Verify Chrome is Running

```bash
curl http://127.0.0.1:9222/json/version
```

Expected response (JSON with browser version and WebSocket URL).

---

## Verify the Bridge

```bash
# Health check
curl http://127.0.0.1:9876/health

# Expected:
# {"status":"ok","cdpConnected":true,"cdpPort":9222,"bridgePort":9876,"uptime":...}
```

---

## Manual Bridge Start

```bash
# If installed globally
chrome-ai-action

# With custom port
chrome-ai-action --port 9877
```

---

## Environment Variables / 环境变量

| Variable | Default | Description |
|---|---|---|
| `CAA_BRIDGE_PORT` | `9876` | Bridge HTTP server port |
| `CAA_STARTUP_TIMEOUT` | `30000` | Max wait for bridge ready (ms) |
| `CHROME_PATH` | auto-detect (Win/Mac/Linux) | Custom Chrome executable path |
| `CHROME_USER_DATA_DIR` | OS-dependent | Chrome profile directory |
| `CHROME_CDP_PORT` | `9222` | Chrome remote debugging port |
| `BRIDGE_PORT` | `9876` | Bridge HTTP port |

### Platform-specific Chrome paths searched:

- **Windows**: `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`, `C:\Program Files\...`, `%LOCALAPPDATA%\...`, Scoop
- **macOS**: `/Applications/Google Chrome.app/...`, `~/Applications/...`
- **Linux**: `google-chrome`, `google-chrome-stable`, `chromium`, `chromium-browser`, snap

---

## Troubleshooting / 故障排除

| Symptom | Cause | Fix |
|---|---|---|
| Bridge starts but no CDP | Chrome not running | Wait 3s — auto-launch will retry |
| `EADDRINUSE` | Port 9876 already in use | Kill existing process or set `CAA_BRIDGE_PORT` |
| `MODULE_NOT_FOUND` | Dependencies not installed | Run `npm install -g chrome-ai-action` |
| Port conflicts | | `chrome-ai-action --port 9877` |
