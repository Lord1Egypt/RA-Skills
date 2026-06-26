---
name: full-webpage-screenshot
description: "Capture full-page screenshots of websites with lazy-load support. Use when: user wants to screenshot a webpage, take a website screenshot, capture a full page, or needs visual documentation of a website. Supports scrolling to trigger lazy-loaded content."
license: MIT
metadata:
  openclaw:
    emoji: "📸"
    requires:
      bins: ["node"]
      setup: "cd ~/.openclaw/skills/full-webpage-screenshot/scripts && npm install"
---

# Full Webpage Screenshot

Capture complete webpage screenshots using Puppeteer, including content that loads dynamically on scroll.

## When to Use

✅ **USE this skill when:**

- "Screenshot this website"
- "Take a screenshot of example.com"
- "Capture the full page"
- "Get a visual of this webpage"
- "截个网页图"
- "给这个网站截屏"

## When NOT to Use

❌ **DON'T use this skill when:**

- Screenshotting local files → use system screenshot tools
- Capturing specific elements only → use browser DevTools
- Video/screenshots of interactions → use screen recording
- Need for authenticated pages → manual browser required

## Setup

First-time setup (installs Puppeteer):

```bash
cd ~/.openclaw/skills/full-webpage-screenshot/scripts
npm install
```

## Commands

### Basic Screenshot

```bash
cd ~/.openclaw/skills/full-webpage-screenshot/scripts
node screenshot.js "https://example.com" ~/workspace/screenshot.png
```

### Custom Viewport (Mobile/Desktop)

```bash
# Mobile view
cd ~/.openclaw/skills/full-webpage-screenshot/scripts
VIEWPORT_WIDTH=375 VIEWPORT_HEIGHT=812 node screenshot.js "https://example.com" mobile.png

# Desktop HD
VIEWPORT_WIDTH=1920 VIEWPORT_HEIGHT=1080 node screenshot.js "https://example.com" desktop.png
```

### Slow-Loading Pages

```bash
cd ~/.openclaw/skills/full-webpage-screenshot/scripts
WAIT_AFTER=5000 node screenshot.js "https://slow-site.com" screenshot.png
```

## Options

| Variable | Default | Description |
|----------|---------|-------------|
| `VIEWPORT_WIDTH` | 1280 | Browser viewport width |
| `VIEWPORT_HEIGHT` | 800 | Browser viewport height |
| `SCROLL_DELAY` | 100 | Delay between scroll steps (ms) |
| `WAIT_AFTER` | 2000 | Wait after page load (ms) |

## Output

Returns JSON:
```json
{
  "success": true,
  "path": "/path/to/screenshot.png",
  "width": 1280,
  "height": 4352
}
```

## Quick Responses

**"Screenshot this site"**

```bash
cd ~/.openclaw/skills/full-webpage-screenshot/scripts
node screenshot.js "$URL" ~/workspace/screenshot.png
```

**"Mobile screenshot"**

```bash
cd ~/.openclaw/skills/full-webpage-screenshot/scripts
VIEWPORT_WIDTH=375 VIEWPORT_HEIGHT=812 node screenshot.js "$URL" mobile.png
```

## Notes

- Requires Node.js 18+
- First run needs `npm install` in scripts/
- Automatically scrolls to trigger lazy-loaded content
- Supports all modern web features (JS, CSS, fonts)
