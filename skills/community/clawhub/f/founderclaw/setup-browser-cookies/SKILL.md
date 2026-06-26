---
name: setup-browser-cookies
description: >
  Import cookies from your real Chromium browser into the headless browse session.
  Interactive picker UI lets you select which cookie domains to import.
  Use before QA testing authenticated pages.
  Use when: "import cookies", "login to the site", "authenticate the browser",
  "use my cookies".
---

# Setup Browser Cookies

Import cookies from your real browser into the headless session. Skip the login flow entirely.

## Why

QA testing authenticated pages requires login. Instead of automating the login flow (slow, flaky, 2FA), just import your existing cookies from Chrome/Firefox/Edge.

## Step 1: Check Browse is Running

```bash
BROWSE="founderclaw/browse/dist/browse"
CONTAINER=1 $BROWSE url
```

If no page loaded yet:

```bash
CONTAINER=1 $BROWSE goto https://yourapp.com
```

## Step 2: Import Cookies

### Option A: Interactive Picker (Recommended)

Opens a web UI where you select which domains to import:

```bash
CONTAINER=1 $BROWSE cookie-import-browser
```

This:
1. Reads cookies from your default browser's profile
2. Opens a picker UI showing all cookie domains
3. You select which domains to import
4. Selected cookies are loaded into the headless session

### Option B: Import from Specific Browser

```bash
CONTAINER=1 $BROWSE cookie-import-browser chrome
CONTAINER=1 $BROWSE cookie-import-browser firefox
CONTAINER=1 $BROWSE cookie-import-browser edge
```

### Option C: Import from JSON File

If you exported cookies manually:

```bash
CONTAINER=1 $BROWSE cookie-import /path/to/cookies.json
```

Cookie JSON format:
```json
[
  {
    "name": "session_id",
    "value": "abc123",
    "domain": ".example.com",
    "path": "/",
    "httpOnly": true,
    "secure": true
  }
]
```

### Option D: Filter by Domain

```bash
CONTAINER=1 $BROWSE cookie-import-browser chrome --domain example.com
```

Only imports cookies matching the specified domain.

## Step 3: Verify

```bash
CONTAINER=1 $BROWSE goto https://yourapp.com
CONTAINER=1 $BROWSE text
```

You should see the authenticated version of the page. No login needed.

Check imported cookies:

```bash
CONTAINER=1 $BROWSE cookies
```

## Supported Browsers

| Browser | Profile Location |
|---------|-----------------|
| Chrome | `~/Library/Application Support/Google/Chrome` (macOS) |
| Firefox | `~/Library/Application Support/Firefox` (macOS) |
| Edge | `~/Library/Application Support/Microsoft Edge` (macOS) |
| Chromium | `~/.config/chromium` (Linux) |

## Troubleshooting

**"No cookies found"** — Make sure the browser is closed (cookies DB may be locked). Or try a different browser.

**"Permission denied"** — Cookie databases are protected. Close the browser first, or run with appropriate permissions.

**"Cookies imported but page still shows login"** — The session may have expired on the server. Re-login in your real browser, then re-import.

## Important

- Imported cookies carry your real session. The headless browser can access your authenticated accounts.
- Don't import cookies on shared/untrusted systems.
- Cookies expire — re-import if the session times out.
