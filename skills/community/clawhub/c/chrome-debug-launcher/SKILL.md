---
name: chrome-debug-launcher
description: Launch two independent Chrome browser instances — one normal and one with remote debugging enabled on port 9222. Activate when user says "打开两个浏览器", "开调试浏览器", "launch chrome debug", or any similar request to open a debug Chrome alongside a normal Chrome.
---

# Chrome Debug Launcher

Launch two independent Chrome instances: one normal, one with remote debugging on port 9222.

## Steps

1. **Kill all Chrome processes**
2. **Launch normal Chrome** (no extra args)
3. **Wait 2 seconds**, then launch debug Chrome

## Commands by Platform

### Windows (PowerShell)

```powershell
# Step 1: Kill Chrome
taskkill /F /IM chrome.exe /T 2>$null
Start-Sleep -Seconds 2

# Step 2: Normal Chrome
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Step 3: Debug Chrome (after 2s)
Start-Sleep -Seconds 2
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList '--remote-debugging-port=9222', '--user-data-dir=C:\selenum\ChromeProfile'
```

### macOS (bash)

```bash
# Step 1: Kill Chrome
pkill -f "Google Chrome" 2>/dev/null; sleep 2

# Step 2: Normal Chrome
open -a "Google Chrome"

# Step 3: Debug Chrome (after 2s)
sleep 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/selenium/ChromeProfile" &
```

## Result

- **Instance 1**: Normal Chrome, default profile, regular use
- **Instance 2**: Debug Chrome, port 9222, isolated user data dir
  - Connect via Selenium/Playwright: `http://localhost:9222`
