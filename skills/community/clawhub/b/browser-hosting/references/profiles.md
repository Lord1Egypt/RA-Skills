# Browser Profiles Reference

## Profile Types

### openclaw (Managed Browser)
- **Description**: Isolated, managed browser instance
- **CDP Port**: Automatically assigned (default: 18800)
- **User Data**: Separate directory, never touches personal browser
- **Use Case**: Secure automation, testing, isolated sessions
- **Color**: Orange (#FF4500)

### chrome (Extension Relay)
- **Description**: Controls existing Chrome tabs via extension
- **CDP URL**: http://127.0.0.1:18792 (default)
- **User Data**: Uses your existing Chrome profile
- **Use Case**: Controlling current browsing session
- **Requirements**: OpenClaw Chrome extension installed and attached

### Custom Remote Profiles
- **Description**: Connect to remote CDP endpoints
- **CDP URL**: Custom URL (e.g., Browserless, remote machines)
- **Authentication**: Supports query tokens and HTTP Basic auth
- **Use Case**: Cloud browser services, remote machine control

## Configuration Examples

### Default Managed Browser
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      }
    }
  }
}
```

### Multiple Profiles
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "profiles": {
      "openclaw": { "cdpPort": 18800, "color": "#FF4500" },
      "work": { "cdpPort": 18801, "color": "#0066CC" },
      "browserless": {
        "cdpUrl": "https://production-sfo.browserless.io?token=YOUR_TOKEN",
        "color": "#00AA00"
      }
    }
  }
}
```

### Extension Relay Only
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "chrome",
    "profiles": {
      "chrome": {
        "cdpUrl": "http://127.0.0.1:18792",
        "color": "#4285F4"
      }
    }
  }
}
```

## Profile Selection Guidelines

- **Use `openclaw`** for: 
  - New automation tasks
  - Sensitive operations requiring isolation
  - Testing that shouldn't affect personal browsing

- **Use `chrome`** for:
  - Controlling currently open tabs
  - Tasks requiring existing logged-in sessions
  - Quick interactions with current browsing context

- **Use custom profiles** for:
  - Cloud browser services (Browserless, etc.)
  - Remote machine automation
  - Specialized browser configurations

## Browser Detection Order

When `executablePath` is not specified, OpenClaw auto-detects in this order:

1. **System default browser** (if Chromium-based)
2. **Google Chrome**
3. **Brave Browser**  
4. **Microsoft Edge**
5. **Chromium**
6. **Chrome Canary**

## Platform-Specific Paths

### macOS
- Brave: `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`
- Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Edge: `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`

### Windows
- Brave: `C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`
- Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- Edge: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

### Linux
- Brave: `/usr/bin/brave-browser`
- Chrome: `/usr/bin/google-chrome`
- Edge: `/usr/bin/microsoft-edge`
- Chromium: `/usr/bin/chromium`

## Security Considerations

- **Local profiles**: Bind only to loopback (127.0.0.1)
- **Remote profiles**: Use HTTPS and short-lived tokens when possible
- **Authentication**: Store tokens in environment variables, not config files
- **Isolation**: Managed profiles never access personal browser data
- **Permissions**: Browser automation requires explicit user consent