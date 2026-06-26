# Browser Configuration Guide

## Configuration File Location

Browser settings are stored in `~/.openclaw/openclaw.json` under the `browser` section.

## Basic Configuration Structure

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "color": "#FF4500",
    "headless": false,
    "noSandbox": false,
    "attachOnly": false,
    "executablePath": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "profiles": {
      "openclaw": { "cdpPort": 18800, "color": "#FF4500" },
      "work": { "cdpPort": 18801, "color": "#0066CC" },
      "remote": { "cdpUrl": "http://10.0.0.42:9222", "color": "#00AA00" }
    }
  }
}
```

## Key Configuration Options

### Core Settings

- **`enabled`**: Enable/disable browser functionality (default: `true`)
- **`defaultProfile`**: Default profile to use (`"chrome"` or `"openclaw"`)
- **`color`**: Default UI color for browser windows
- **`headless`**: Run browser in headless mode (default: `false`)
- **`noSandbox`**: Disable sandbox (useful for Docker, default: `false`)
- **`attachOnly`**: Never start local browser; only attach to existing instances (default: `false`)
- **`executablePath`**: Override auto-detected browser executable path

### Profile Configuration

Profiles define different browser instances or connection methods:

#### Local Managed Profiles
```json
"profiles": {
  "openclaw": { 
    "cdpPort": 18800, 
    "color": "#FF4500" 
  }
}
```

- **`cdpPort`**: CDP port for local browser instance (auto-assigned if not specified)
- **`color`**: UI color for this profile

#### Remote CDP Profiles
```json
"profiles": {
  "remote": { 
    "cdpUrl": "http://10.0.0.42:9222", 
    "color": "#00AA00" 
  }
}
```

- **`cdpUrl`**: URL to remote CDP endpoint
- Supports authentication: `https://user:pass@host:port` or `https://host:port?token=xyz`

#### Browserless Integration
```json
"profiles": {
  "browserless": {
    "cdpUrl": "https://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
    "color": "#00AA00"
  }
}
```

## Platform-Specific Executable Paths

### macOS
```json
{
  "browser": {
    "executablePath": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  }
}
```

### Windows
```json
{
  "browser": {
    "executablePath": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  }
}
```

### Linux
```json
{
  "browser": {
    "executablePath": "/usr/bin/brave-browser"
  }
}
```

## Port Allocation and Networking

### Default Port Scheme
- Gateway port: `18791` (default)
- Browser control service: Gateway port + 2 = `18793`
- Chrome extension relay: Gateway port + 1 = `18792`
- Local CDP ports: `18800-18899` (auto-assigned)

### Custom Gateway Ports
If you change `gateway.port`, browser ports adjust automatically:
- Gateway port `9000` → Browser control `9002`, Relay `9001`, CDP `9010+`

## Security Configuration

### Authentication for Remote CDP
```json
// HTTP Basic Auth
"cdpUrl": "https://username:password@remote-host:9222"

// Query Token (recommended)
"cdpUrl": "https://remote-host:9222?token=your-api-token"
```

### Environment Variables for Secrets
Instead of hardcoding tokens in config:
```bash
export BROWSERLESS_TOKEN="your-token-here"
```
Then reference in config:
```json
"cdpUrl": "https://production-sfo.browserless.io?token=${BROWSERLESS_TOKEN}"
```

## Node Browser Proxy Configuration

For remote browser control via nodes:

### On Node Host
```json
{
  "nodeHost": {
    "browserProxy": {
      "enabled": true  // default: true
    }
  }
}
```

### On Gateway
```json
{
  "gateway": {
    "nodes": {
      "browser": {
        "mode": "auto"  // "auto", "off", or "required"
      }
    }
  }
}
```

## Playwright Requirements

Some advanced features require Playwright:

### Features Requiring Playwright
- Navigate/act operations
- AI snapshots (`--format ai`)
- Element screenshots
- PDF generation
- Advanced waiting conditions

### Installing Playwright
```bash
# Standard installation
npm install -g playwright
npx playwright install chromium

# Docker installation
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

### Docker Configuration
Set environment variables for persistent browsers:
```yaml
environment:
  - PLAYWRIGHT_BROWSERS_PATH=/home/node/.cache/ms-playwright
volumes:
  - openclaw_home:/home/node
```

## Troubleshooting Configuration

### Common Issues

1. **"Browser disabled" error**
   - Check `browser.enabled: true` in config
   - Restart Gateway after config changes

2. **Browser not starting**
   - Verify `executablePath` points to valid browser
   - Check permissions on executable
   - Try `noSandbox: true` for containerized environments

3. **Remote CDP connection failures**
   - Verify network connectivity to CDP endpoint
   - Check authentication credentials
   - Ensure CDP is enabled on remote browser

4. **Playwright features unavailable**
   - Install full Playwright package (not just playwright-core)
   - Restart Gateway after installation

### Validation Commands
```bash
# Check current config
openclaw config get browser

# Test browser status
openclaw browser --browser-profile openclaw status

# Validate executable path
openclaw config validate browser.executablePath
```

This configuration guide covers all aspects of setting up and managing OpenClaw's browser hosting capabilities for both local and remote scenarios.