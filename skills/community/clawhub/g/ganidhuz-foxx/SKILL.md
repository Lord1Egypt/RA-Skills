---
name: ganidhuz-foxx
description: >
  🦊 Ganidhuz-FoxX (Firefox + X combined lol). Browse X/Twitter using a real
  logged-in Firefox session via cookie injection. Supports profile viewing,
  tweet fetching, searching, and scrolling feeds — no API key, no bot blocks.
license: MIT
---

# Ganidhuz-FoxX 🦊

Browse X/Twitter through Firefox with your real session cookies. Built because Chromium kept getting bot-blocked by X.

## Requirements

- Python 3.7+
- Playwright: `pip install playwright && playwright install firefox`
- Firefox installed with an active X/Twitter login
- Xvfb display (for headless servers): `Xvfb :1 &`

## Setup

### 1. Export your X cookies

Close Firefox first, then:

```bash
bash scripts/export-x-cookies.sh
# Cookies saved to secrets/x-cookies.json by default
# Override: FOXX_COOKIES_OUT=/custom/path.json bash scripts/export-x-cookies.sh
```

Custom Firefox profile path:
```bash
FIREFOX_PROFILE_PATH=/path/to/profile bash scripts/export-x-cookies.sh
```

### 2. Health check

```bash
bash scripts/check-firefox-env.sh
```

## Usage

Run a plan file:

```bash
DISPLAY=:1 python3 scripts/playwright-firefox-control.py --plan /tmp/foxx-plan.json
```

## Plan Examples

### View a profile

```json
{
  "needs_gui": true,
  "gui_reason": "site_only_action",
  "url": "https://x.com/elonmusk",
  "cookies_path": "secrets/x-cookies.json",
  "steps": [
    {"action": "wait", "ms": 4000},
    {"action": "screenshot", "path": "/tmp/foxx-profile.png"}
  ],
  "close_delay_ms": 3000
}
```

### Search tweets (live)

```json
{
  "needs_gui": true,
  "gui_reason": "site_only_action",
  "url": "https://x.com/search?q=AI+agents&src=typed_query&f=live",
  "cookies_path": "secrets/x-cookies.json",
  "steps": [
    {"action": "wait", "ms": 4000},
    {"action": "screenshot", "path": "/tmp/foxx-search.png"}
  ],
  "close_delay_ms": 3000
}
```

### Fetch a tweet

```json
{
  "needs_gui": true,
  "gui_reason": "site_only_action",
  "url": "https://x.com/user/status/123456789",
  "cookies_path": "secrets/x-cookies.json",
  "steps": [
    {"action": "wait", "ms": 3000},
    {"action": "content", "selector": "article"},
    {"action": "screenshot", "path": "/tmp/foxx-tweet.png"}
  ],
  "close_delay_ms": 3000
}
```

## Plan Options

| Field | Default | Description |
|---|---|---|
| `needs_gui` | required | Must be `true` to launch browser |
| `gui_reason` | required | One of: `login`, `captcha`, `mfa`, `visual_verification`, `site_only_action` |
| `url` | required | Starting URL |
| `cookies_path` | optional | Path to exported cookies JSON |
| `close_delay_ms` | `3000` | Wait (ms) before closing browser - validate result first |
| `validation_screenshot` | `/tmp/firefox-openclaw-validate.png` | Auto-taken final screenshot before close |
| `storage_state_path` | optional | Save session state to this path after run |

## Supported Step Actions

- `goto` - navigate to URL
- `click` - click element by selector
- `fill` - fill input by selector
- `type` - type text with delay
- `press` - press keyboard key
- `wait` - wait ms
- `wait_for_selector` - wait for element
- `screenshot` - take screenshot
- `content` - extract inner text from element

## Behaviour Rules

- Always wait for page load (`wait` step, min 3000ms recommended)
- A validation screenshot is always taken before closing
- Browser waits `close_delay_ms` before closing - verify result is correct
- If cookies expired (redirects to login), re-run `export-x-cookies.sh`
- Always close browser after task - don't leave it idle
