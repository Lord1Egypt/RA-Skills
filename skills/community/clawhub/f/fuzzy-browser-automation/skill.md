---
name: browser-automation
description: "Automate any web browser task with OpenClaw's built-in Playwright browser control. Use when: (1) scraping dynamic pages, (2) filling forms and submitting, (3) taking screenshots or PDFs, (4) clicking through multi-step flows, (5) monitoring changing web content, (6) automating logins. Triggers on phrases like browse this, scrape, automate web, fill form, take screenshot, click this button, browser control, open webpage."
---

# Browser Automation

Control a Chromium browser directly from OpenClaw — navigate, click, type, snapshot, screenshot, extract data. Works with both the sandboxed OpenClaw-managed browser and your logged-in user browser (with profile="user").

## Browser Selection

| Target | When to Use |
|--------|-------------|
| `sandbox` (default) | OpenClaw's clean browser — no cookies, no login state |
| `host` | Browser running on the host machine |
| `node` | Browser on a paired remote node |

| Profile | When to Use |
|---------|-------------|
| (omit) | Clean OpenClaw-managed browser |
| `profile="user"` | Your own browser with active logins (requires you present) |

## Core Actions

### `snapshot` — Inspect the Page

```json
browser(action="snapshot", target="sandbox")
```

Returns the full page DOM as a structured tree. Use refs="aria" for screen-reader-friendly selectors, refs="role" (default) for role+name based refs.

```json
browser(
  action="snapshot",
  target="sandbox",
  refs="aria"
)
```

### `screenshot` — Capture the Page

```json
browser(action="screenshot", target="sandbox")
```

For full-page screenshots:
```json
browser(
  action="screenshot",
  target="sandbox",
  fullPage=true
)
```

### `navigate` — Open a URL

```json
browser(action="navigate", target="sandbox", url="https://news.ycombinator.com")
```

### `act` — Interact with Elements

The `act` action is the workhorse. It combines `ref` (what to target) + `kind` (action type) + `request` (action details).

**Click:**
```json
browser(
  action="act",
  target="sandbox",
  ref="aria:Submit",
  request={"kind": "click"}
)
```

**Type:**
```json
browser(
  action="act",
  target="sandbox",
  ref="id:search-box",
  request={"kind": "type", "text": "openclaw browser automation"}
)
```

**Press a key:**
```json
browser(
  action="act",
  target="sandbox",
  ref="id:search-box",
  request={"kind": "press", "key": "Enter"}
)
```

**Hover:**
```json
browser(
  action="act",
  target="sandbox",
  ref="css:.dropdown-menu",
  request={"kind": "hover"}
)
```

**Select from dropdown:**
```json
browser(
  action="act",
  target="sandbox",
  ref="id:country-select",
  request={"kind": "select", "values": ["South Africa"]}
)
```

**Wait for element:**
```json
browser(
  action="act",
  target="sandbox",
  ref="aria:Loading",
  request={"kind": "wait", "timeMs": 5000}
)
```

## Locator Reference (ref types)

| Prefix | Example | Best For |
|--------|---------|----------|
| `aria:` | `aria:Submit` | Accessible labels, buttons with text |
| `id:` | `id:email-input` | Unique element IDs |
| `css:` | `css:.card:nth-child(2)` | Complex CSS selectors |
| `role:` | `role:button[name="Submit"]` | Semantic role selectors |
| `text:` | `text:Get Started` | Visible text content |
| `xpath:` | `xpath://button[@class="btn"]` | Fallback for complex paths |

For stable refs across calls, prefer `refs="aria"` in snapshots — these use ARIA labels that rarely change.

## Recipes

### Recipe 1: Scrape a Dynamic Page

```json
// 1. Navigate
browser(action="navigate", target="sandbox", url="https://news.ycombinator.com/news")

// 2. Wait for content to load
browser(
  action="act",
  target="sandbox",
  loadState="networkidle",
  ref="css:.itemlist",
  request={"kind": "wait", "timeMs": 3000}
)

// 3. Snapshot to extract structured data
browser(action="snapshot", target="sandbox", refs="aria")
```

### Recipe 2: Fill and Submit a Form

```json
// 1. Navigate to form
browser(action="navigate", target="sandbox", url="https://example.com/contact")

// 2. Fill inputs
browser(action="act", target="sandbox", ref="id:name",    request={"kind": "fill", "text": "Alice Smith"})
browser(action="act", target="sandbox", ref="id:email",   request={"kind": "fill", "text": "alice@example.com"})
browser(action="act", target="sandbox", ref="id:message", request={"kind": "fill", "text": "Hi, I'd like to know more..."})

// 3. Click submit
browser(action="act", target="sandbox", ref="aria:Submit", request={"kind": "click"})

// 4. Wait for confirmation
browser(
  action="act",
  target="sandbox",
  ref="aria:Thank you",
  request={"kind": "wait", "timeMs": 2000}
)
```

### Recipe 3: Login to a Service (User Browser)

```json
// Requires you to be present at the machine — uses your actual browser session
browser(action="navigate", target="host", url="https://github.com/login")

browser(action="act", target="host", ref="id:login_field", request={"kind": "fill", "text": "myuser"})
browser(action="act", target="host", ref="id:password",    request={"kind": "fill", "text": "mypassword"})
browser(action="act", target="host", ref="css:[type=submit]", request={"kind": "click"})
```

### Recipe 4: Monitor Price / Availability

```json
// Navigate and wait for price to update
browser(action="navigate", target="sandbox", url="https://example.com/product/123")

browser(
  action="act",
  target="sandbox",
  ref="css:.price",
  request={"kind": "wait", "timeMs": 10000}
)

// Capture screenshot
browser(action="screenshot", target="sandbox")

// Evaluate for price text
browser(
  action="act",
  target="sandbox",
  request={
    "kind": "evaluate",
    "fn": "() => document.querySelector('.price').innerText"
  }
)
```

### Recipe 5: Multi-Tab Workflow

```json
// Open new tab
browser(action="navigate", target="sandbox", url="https://mail.google.com")

// Switch tabs
browser(action="act", target="sandbox", request={"kind": "press", "key": "Control+Tab"})

// Close current tab
browser(action="act", target="sandbox", request={"kind": "press", "key": "Control+W"})
```

### Recipe 6: Scroll and Load Lazy Content

```json
// Scroll by a pixel amount
browser(
  action="act",
  target="sandbox",
  request={
    "kind": "evaluate",
    "fn": "() => window.scrollBy(0, 800)"
  }
)

// Scroll to bottom (infinite scroll pages)
browser(
  action="act",
  target="sandbox",
  request={
    "kind": "evaluate",
    "fn": "() => window.scrollTo(0, document.body.scrollHeight)"
  }
)
```

### Recipe 7: Extract Table Data

```json
browser(action="navigate", target="sandbox", url="https://example.com/sales-report")

browser(
  action="act",
  target="sandbox",
  ref="css:table",
  request={"kind": "wait", "timeMs": 2000}
)

browser(
  action="act",
  target="sandbox",
  request={
    "kind": "evaluate",
    "fn": "() => Array.from(document.querySelectorAll('table tr')).map(row => Array.from(row.querySelectorAll('td')).map(cell => cell.innerText))"
  }
)
```

### Recipe 8: Download a File

```json
browser(action="navigate", target="sandbox", url="https://example.com/export.csv")

browser(
  action="act",
  target="sandbox",
  request={
    "kind": "evaluate",
    "fn": "() => { const link = document.querySelector('a[href$=\".csv\"]'); return link ? link.href : null; }"
  }
)
```

## Action Reference

| Action | What It Does |
|--------|-------------|
| `snapshot` | Get structured page DOM |
| `screenshot` | Capture page as PNG/JPEG |
| `navigate` | Open a URL |
| `act` | Click, type, press, hover, select, wait, evaluate |
| `pdf` | Generate PDF of the page |
| `console` | Read browser console logs |
| `open` | Open a new tab |
| `close` | Close current tab |

## act `kind` Reference

| Kind | Parameters |
|------|-----------|
| `click` | — |
| `type` | `text` |
| `fill` | `text` |
| `press` | `key` (e.g. "Enter", "Escape", "Control+Tab") |
| `hover` | — |
| `select` | `values` (array) |
| `wait` | `timeMs` |
| `evaluate` | `fn` (JavaScript string) |
| `drag` | `startRef`, `endRef` |
| `resize` | `width`, `height` |
| `close` | — |

## Anti-Patterns

- **Don't click before the page loads** — always `navigate` then wait for `loadState="networkidle"` or an explicit element wait
- **Don't use hard pixel waits** — prefer waiting for a specific element or `networkidle` state
- **Don't scrape without rate limiting** — add `timeMs` waits between actions to avoid IP blocks
- **Don't use `profile="user"` for automated workflows** — it's meant for attended use; automated flows should use the sandbox browser
- **Don't use xpath unless nothing else works** — xpath selectors break easily when the page changes

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Target closed" error | Browser timed out — navigate again |
| Element not found | Page may be JS-rendered — add `loadState="networkidle"` or explicit wait |
| Click missed the button | Use `ref="aria:Button Text"` instead of CSS — more robust |
| Stale element reference | Element was replaced by a DOM update — re-snapshot and retry |
| Form submits twice | Wait for navigation after submit before continuing |
| Screenshot is blank | Page still loading — add `loadState="networkidle"` |
| `profile="user"` not working | The logged-in browser must already be running; start it manually first |

## See Also

- `webhook-automation` skill — combining browser-extracted data with outgoing webhooks
- `rss-aggregator` skill — using browser scraping as a fallback when feeds aren't available
- `cron-scheduler` skill — scheduling browser-based monitoring tasks
