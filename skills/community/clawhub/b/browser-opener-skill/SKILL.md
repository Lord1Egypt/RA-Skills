---
name: browser-opener
description: Cross-platform browser opening skill that supports multiple browsers (Chrome, Firefox, Edge, Safari) with URL launching capabilities. Use when Codex needs to open web browsers programmatically for: (1) Launching default browser, (2) Opening specific browsers, (3) Opening URLs with default browser, (4) Opening URLs with specific browsers, (5) Cross-platform browser automation
---

# Browser Opener Skill

This skill provides cross-platform browser opening capabilities with support for multiple browsers.

## Quick Start

Open a URL with the default browser:
```python
# Using the browser opener script
python scripts/open_browser.py --url https://www.google.com
```

Open a URL with a specific browser:
```python
# Open with Chrome
python scripts/open_browser.py --url https://www.google.com --browser chrome

# Open with Firefox
python scripts/open_browser.py --url https://www.google.com --browser firefox

# Open with Edge
python scripts/open_browser.py --url https://www.google.com --browser edge
```

## Supported Browsers

- **Chrome**: `chrome`, `google-chrome`, `google-chrome-stable`
- **Firefox**: `firefox`, `mozilla-firefox`
- **Edge**: `edge`, `microsoft-edge`
- **Safari**: `safari`, `apple-safari`
- **Default**: `default` (uses system default browser)

## Usage Examples

See [examples/](examples/) for comprehensive usage examples including:
- Basic URL opening
- Browser-specific launching
- Batch opening multiple URLs
- Error handling scenarios

## Browser Support Details

For detailed information about browser support on different platforms, see [references/browser_support.md](references/browser_support.md).

## Command Line Options

The `scripts/open_browser.py` script supports the following options:

- `--url`: URL to open (required)
- `--browser`: Browser to use (optional, defaults to 'default')
- `--new-window`: Open in new window (optional)
- `--incognito`: Open in incognito/private mode (optional)
- `--headless`: Open in headless mode (optional, for testing)

## Error Handling

The script includes comprehensive error handling for:
- Invalid URLs
- Browser not found
- Permission issues
- Platform-specific errors