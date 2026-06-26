---
name: browser-hosting
description: OpenClaw browser hosting and automation capabilities for web interaction, scraping, and UI testing. Provides isolated browser profiles, snapshot-based automation, and comprehensive web control through the browser tool. Use when you need to interact with web pages, extract content, automate UI workflows, or perform web testing without affecting your personal browser.
---

# Browser Hosting Skill

This skill provides comprehensive browser automation capabilities through OpenClaw's managed browser system. It enables safe, isolated web interaction with deterministic UI control.

## When to Use This Skill

- **Web scraping** - Extract structured data from websites
- **UI automation** - Automate form filling, clicks, navigation
- **Web testing** - Verify page behavior and functionality  
- **Content extraction** - Get text, screenshots, or PDFs from web pages
- **Browser isolation** - Perform web operations without affecting personal browsing
- **Remote browser control** - Control browsers on other machines via nodes

## Quick Start

### Basic Workflow
```python
# 1. Open a page
openclaw browser --browser-profile openclaw open https://example.com

# 2. Take a snapshot to see interactive elements
openclaw browser --browser-profile openclaw snapshot --interactive

# 3. Perform actions using references from snapshot
openclaw browser --browser-profile openclaw click e12
openclaw browser --browser-profile openclaw type i23 "search term" --submit
```

### Profile Selection
- **`openclaw`**: Isolated managed browser (recommended for automation)
- **`chrome`**: Chrome extension relay (for controlling existing Chrome tabs)

## Core Capabilities

### Browser Profiles
- **Isolated instances**: Each profile has separate user data directory
- **Multiple profiles**: Run `openclaw`, `work`, `remote` simultaneously
- **Remote CDP**: Connect to browsers on other machines
- **Browserless integration**: Use hosted Chromium services

### Snapshot System
Two approaches for reliable UI interaction:

1. **AI Snapshots** (`--format ai`): Numeric references like `[1]`, `[2]`
   - Best for simple, one-off interactions
   - Uses Playwright's aria-ref internally

2. **Role Snapshots** (`--interactive`): Semantic references like `[ref=e12]`
   - **Recommended for automation** - more stable and descriptive
   - Role-based naming: `e`=button, `b`=link, `i`=input, `s`=select
   - Supports iframe scoping with `--frame`

### Automation Actions
- **Navigation**: `open`, `navigate`, `close`
- **Interaction**: `click`, `type`, `press`, `hover`, `drag`, `select`
- **Input**: `fill` (structured form data), file `upload`
- **Waiting**: Intelligent waits for elements, URLs, network idle, JS conditions
- **Debugging**: `highlight`, `trace`, `errors`, `requests`

### Content Extraction
- **Text**: Structured snapshots with references
- **Screenshots**: Full page or element-specific
- **PDF**: Generate PDFs from web pages
- **Network**: Monitor API calls and responses

## Configuration

Browser settings are managed in `~/.openclaw/openclaw.json`. Key options:

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "profiles": {
      "openclaw": { "cdpPort": 18800 },
      "work": { "cdpPort": 18801 },
      "remote": { "cdpUrl": "http://10.0.0.42:9222" }
    }
  }
}
```

See [configuration.md](references/configuration.md) for complete configuration guide.

## Usage Patterns

### Simple Web Scraping
```bash
# Get page content
openclaw browser --browser-profile openclaw open https://news-site.com
openclaw browser --browser-profile openclaw snapshot --interactive --compact
```

### Form Automation
```bash
# Fill out a form
openclaw browser --browser-profile openclaw open https://form-site.com
openclaw browser --browser-profile openclaw snapshot --interactive
openclaw browser --browser-profile openclaw type i1 "John Doe"
openclaw browser --browser-profile openclaw type i2 "john@example.com" 
openclaw browser --browser-profile openclaw click e5  # Submit button
```

### Multi-step Workflows
```bash
# Navigate through multiple pages
openclaw browser --browser-profile openclaw open https://shop.com
openclaw browser --browser-profile openclaw wait --load networkidle
openclaw browser --browser-profile openclaw snapshot --interactive
openclaw browser --browser-profile openclaw click b12  # Product link
openclaw browser --browser-profile openclaw wait --load networkidle
openclaw browser --browser-profile openclaw click e8   # Add to cart
```

## Advanced Features

### Remote Browser Control
Connect to browsers on other machines:
```json
"profiles": {
  "remote-workstation": {
    "cdpUrl": "http://192.168.1.100:9222",
    "color": "#00AA00"
  }
}
```

### Browserless Integration
Use hosted Chromium:
```json
"profiles": {
  "browserless": {
    "cdpUrl": "https://production-sfo.browserless.io?token=YOUR_TOKEN",
    "color": "#00AA00"
  }
}
```

### Node Proxy
Automatic routing to nodes with browser capability:
- No extra config needed if node has browser
- Gateway automatically proxies browser commands
- Use `target="node"` to force specific node

## Security & Isolation

- **Complete isolation**: Managed browsers never access personal profiles
- **Loopback only**: Browser control restricted to localhost
- **Authentication required**: All access requires Gateway auth
- **No persistent sessions**: Clean state between runs (unless configured otherwise)
- **JavaScript execution**: Can be disabled via `browser.evaluateEnabled=false`

## Troubleshooting

### Common Issues
- **References not working**: Always snapshot after navigation - refs change
- **Element not found**: Use `--interactive` snapshots for better reliability  
- **Browser won't start**: Check `executablePath` and permissions
- **Playwright errors**: Install full Playwright package, not just core

### Debugging Workflow
1. `snapshot --interactive` to get current state
2. `highlight <ref>` to verify target location
3. `errors --clear` to check JavaScript errors
4. `requests --filter api --clear` to monitor network
5. `trace start` → reproduce issue → `trace stop` for deep debugging

## Bundled Resources

### Scripts
- [`browser_status.py`](scripts/browser_status.py): Check browser status
- [`browser_snapshot.py`](scripts/browser_snapshot.py): Take snapshots with options
- [`browser_action.py`](scripts/browser_action.py): Perform UI actions

### References
- [`profiles.md`](references/profiles.md): Profile management guide
- [`snapshot-system.md`](references/snapshot-system.md): Complete snapshot reference
- [`configuration.md`](references/configuration.md): Full configuration guide

### Assets
- [`example-workflow.md`](assets/example-workflow.md): Complete workflow examples

## Best Practices

1. **Always use role snapshots** (`--interactive`) for automation
2. **Snapshot before every action** - references aren't stable across navigation
3. **Use wait conditions** before snapshotting dynamic content
4. **Prefer isolated profiles** over extension relay for automation
5. **Validate executable paths** on new systems
6. **Use environment variables** for sensitive configuration (tokens, passwords)

This skill transforms OpenClaw into a powerful web automation platform while maintaining security and reliability through its snapshot-based, reference-driven approach.