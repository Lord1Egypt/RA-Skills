---
type: API Reference
title: "Camoufox Default Browser — Complete API Reference"
version: 1.1.0
---

# Camoufox Default Browser — API Reference

HTTP API server for Camoufox browser automation (Firefox fork with anti-detection fingerprints). Server listens on port **9377** by default (configurable via `PORT` env var) and accepts all requests as JSON.

## Authentication

Most endpoints require an `Authorization: Bearer <CAMOUFOX_API_KEY>` header. Cookie import operations (`camofox_import_cookies`) are particularly sensitive — always validate API key before accepting cookie-file uploads. Unauthenticated requests to protected endpoints return `401 Unauthorized`.

## Response Format

All successful responses follow this envelope:

```json
{
  "status": "ok",
  "data": { ... },
  "timestamp": "2026-07-30T13:00:00+07:00"
}
```

Error responses use this envelope:

```json
{
  "status": "error",
  "code": "TOOL_ERROR",
  "message": "Human-readable error description",
  "details": { ... }
}
```

---

## Health & Info Endpoints

### GET /health

Checks whether the Camoufox server process and browser engine are alive.

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"healthy"` or `"degraded"` |
| `browserRunning` | boolean | Whether the browser process is active |
| `tabCount` | integer | Number of open tabs |
| `uptime` | integer | Server uptime in seconds |

**Example response:**

```json
{
  "status": "ok",
  "data": {
    "status": "healthy",
    "browserRunning": true,
    "tabCount": 2,
    "uptime": 3600
  }
}
```

### GET /info

Returns server version, platform, and environment details.

```json
{
  "status": "ok",
  "data": {
    "version": "1.1.0",
    "engine": "Camoufox Firefox ESR",
    "platform": "linux-x64",
    "nodeVersion": "v24.18.0",
    "port": 9377
  }
}
```

---

## Tool Endpoints

Every `camofox_*` tool maps to a `POST /tool/<tool_name>` endpoint. The body matches the tool parameters exactly. All endpoints require a valid `tabId` unless noted otherwise.

### 1. POST /tool/camofox_create_tab

Creates a new browser tab with isolated fingerprint context. The browser engine launches lazily on first call if not already running.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | No | Initial URL to navigate to. Defaults to blank page if omitted. |

**Returns:** `tabId` string

**Example request:**

```json
{ "url": "https://example.com" }
```

**Response:**

```json
{
  "status": "ok",
  "data": {
    "tabId": "cf-tab-a1b2c3d4"
  }
}
```

**Errors:**
- `500 InternalServerError` — Browser binary not found (`CAMOUFOX_EXECUTABLE` unset or invalid path)
- `500 InternalServerError` — Browser launch failed (missing system libraries, OOM)

---

### 2. POST /tool/camofox_snapshot

Captures the accessibility tree of the current page plus an optional base64 screenshot. Element refs follow the pattern `e1`, `e2`, `e3` etc., which can then be used with `camofox_click` and `camofox_type`. Large pages may be paginated with `hasMore=true` and a `nextOffset` value.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Tab identifier from `create_tab` |
| `offset` | integer | No | Character offset for paginated snapshots. Use `nextOffset` from prior truncated response. |

**Returns:** Accessibility tree text, element refs, and screenshot metadata.

**Example request:**

```json
{ "tabId": "cf-tab-a1b2c3d4", "offset": 0 }
```

**Response:**

```json
{
  "status": "ok",
  "data": {
    "text": "[root] Page\n  [link] Home (e1)\n  [textbox] Search (e2)\n  [button] Submit (e3)",
    "hasMore": false,
    "screenshot": "iVBORw0KGgoAAAANSUhEUg..."
  }
}
```

**Errors:**
- `400 BadRequest` — Missing `tabId`
- `404 NotFound` — Tab does not exist or was closed
- `500 InternalServerError` — Snapshot capture failed

---

### 3. POST /tool/camofox_click

Clicks an element identified by ref (`e1`) or CSS selector within a tab.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Target tab identifier |
| `ref` | string | No* | Element ref from snapshot (e.g., `"e3"`). Either `ref` or `selector` required. |
| `selector` | string | No* | CSS selector alternative to `ref`. |

**Returns:** Success confirmation object.

**Example request (by ref):**

```json
{ "tabId": "cf-tab-a1b2c3d4", "ref": "e3" }
```

**Example request (by selector):**

```json
{ "tabId": "cf-tab-a1b2c3d4", "selector": "#submit-button" }
```

**Response:**

```json
{ "status": "ok", "data": { "clicked": "e3" } }
```

**Errors:**
- `400 BadRequest` — Neither `ref` nor `selector` provided
- `404 NotFound` — Ref/selector not found in the current DOM
- `404 NotFound` — Tab ID is invalid or closed

---

### 4. POST /tool/camofox_type

Types text into a form field identified by ref or CSS selector. Optional `pressEnter` flag submits the form.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Target tab identifier |
| `text` | string | Yes | Text to type |
| `ref` | string | No* | Element ref from snapshot (e.g., `"e2"`). Either `ref` or `selector` required. |
| `selector` | string | No* | CSS selector alternative to `ref`. |
| `pressEnter` | boolean | No | Press Enter key after typing. Default `false`. |

**Returns:** Confirmation with typed character count.

**Example request:**

```json
{ "tabId": "cf-tab-a1b2c3d4", "text": "hello world", "ref": "e2", "pressEnter": true }
```

**Response:**

```json
{ "status": "ok", "data": { "typed": "hello world", "chars": 11, "enterPressed": true } }
```

**Errors:**
- `400 BadRequest` — Empty `text` provided
- `404 NotFound` — Target element not found
- `500 InternalServerError` — Keyboard injection failed

---

### 5. POST /tool/camofox_navigate

Navigates the tab to a URL or executes a built-in search macro. Macros automatically construct the appropriate search query URL and wait for results to load.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Target tab identifier |
| `url` | string | No* | Direct URL to navigate to. Either `url` or `macro` required. |
| `macro` | enum | No* | Built-in search macro. One of: `@google_search`, `@youtube_search`, `@amazon_search`, `@reddit_search`, `@wikipedia_search`, `@twitter_search`, `@yelp_search`, `@spotify_search`, `@netflix_search`, `@linkedin_search`, `@instagram_search`, `@tiktok_search`, `@twitch_search`. |
| `query` | string | Conditional | Search query string when using a `macro`. Ignored if `url` is provided. |

**Returns:** Navigation confirmation with final URL.

**Example request (direct URL):**

```json
{ "tabId": "cf-tab-a1b2c3d4", "url": "https://www.google.com" }
```

**Example request (search macro):**

```json
{ "tabId": "cf-tab-a1b2c3d4", "macro": "@google_search", "query": "Camoufox browser docs" }
```

**Response:**

```json
{
  "status": "ok",
  "data": {
    "finalUrl": "https://www.google.com/search?q=Camoufox+browser+docs",
    "statusCode": 200
  }
}
```

**Errors:**
- `400 BadRequest` — Neither `url` nor `macro` provided
- `400 BadRequest` — Invalid macro name
- `400 BadRequest` — Macro specified but `query` is empty
- `404 NotFound` — Tab ID is invalid or closed
- `500 InternalServerError` — Network error or navigation timeout

---

### 6. POST /tool/camofox_scroll

Scrolls the page in a cardinal direction by a specified pixel amount.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Target tab identifier |
| `direction` | enum | Yes | Scroll direction: `up`, `down`, `left`, `right` |
| `amount` | number | No | Pixels to scroll. Defaults to viewport height (vertical) or width (horizontal) if omitted. |

**Returns:** New scroll position confirmation.

**Example request:**

```json
{ "tabId": "cf-tab-a1b2c3d4", "direction": "down", "amount": 500 }
```

**Response:**

```json
{ "status": "ok", "data": { "direction": "down", "amount": 500 } }
```

**Errors:**
- `400 BadRequest` — Invalid `direction` value
- `404 NotFound` — Tab does not exist

---

### 7. POST /tool/camofox_screenshot

Captures a screenshot of the current page state. Returns a base64-encoded PNG image embedded in the response body. Useful for visual verification before handing results back to the parent agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Target tab identifier |

**Returns:** Base64-encoded PNG screenshot data.

**Example request:**

```json
{ "tabId": "cf-tab-a1b2c3d4" }
```

**Response:**

```json
{
  "status": "ok",
  "data": {
    "screenshot": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQUJBAACX...",
    "format": "png",
    "width": 1920,
    "height": 1080
  }
}
```

**Errors:**
- `400 BadRequest` — Missing `tabId`
- `404 NotFound` — Tab does not exist
- `500 InternalServerError` — Screenshot capture failed

---

### 8. POST /tool/camofox_close_tab

Closes a specific tab and frees its resources. After closing, the `tabId` becomes invalid for subsequent operations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Tab identifier to close |

**Returns:** Closure confirmation.

**Example request:**

```json
{ "tabId": "cf-tab-a1b2c3d4" }
```

**Response:**

```json
{ "status": "ok", "data": { "closed": "cf-tab-a1b2c3d4" } }
```

**Errors:**
- `400 BadRequest` — Missing `tabId`
- `404 NotFound` — Tab already closed or never existed

---

### 9. POST /tool/camofox_evaluate

Executes JavaScript directly in the page context of a given tab. Returns the evaluated result serialized as JSON. Ideal for reading page state, injecting scripts, calling web app APIs, or checking for framework-specific globals (e.g., `window.__REACT_DEVTOOLS_GLOBAL_HOOK__`).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tabId` | string | Yes | Target tab identifier |
| `expression` | string | Yes | JavaScript expression to evaluate in page context. Should be a valid JS expression that returns a value. |

**Returns:** Serialized evaluation result.

**Example request (framework detection):**

```json
{ "tabId": "cf-tab-a1b2c3d4", "expression": "window.__REACT_DEVTOOLS_GLOBAL_HOOK__ !== undefined" }
```

**Example request (DOM read):**

```json
{ "tabId": "cf-tab-a1b2c3d4", "expression": "document.title" }
```

**Response:**

```json
{ "status": "ok", "data": { "result": true } }
```

**Errors:**
- `400 BadRequest` — Missing `tabId` or `expression`
- `500 InternalServerError` — JS execution threw an exception (returned in `details.exception`)
- `404 NotFound` — Tab does not exist

---

### 10. POST /tool/camofox_list_tabs

Lists all currently open tabs across sessions. Returns each tab's ID, URL, title, and creation time. Essential for session management and resource auditing.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| _(none)_ | — | — | This endpoint takes no parameters. |

**Returns:** Array of tab objects.

**Example request:**

```json
{}
```

**Response:**

```json
{
  "status": "ok",
  "data": [
    {
      "tabId": "cf-tab-a1b2c3d4",
      "url": "https://example.com",
      "title": "Example Domain",
      "createdAt": "2026-07-30T12:00:00+07:00"
    },
    {
      "tabId": "cf-tab-e5f6a7b8",
      "url": "about:blank",
      "title": "",
      "createdAt": "2026-07-30T13:05:00+07:00"
    }
  ]
}
```

**Errors:**
- `500 InternalServerError` — Browser process not responding

---

### 11. POST /tool/camofox_import_cookies

Imports cookies from a Netscape-format cookie file into the active Camoufox user session. Used for authenticated browsing without interactive login. The file must contain at least one cookie record per line in Netscape format. Optionally filter by domain suffix.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cookiesPath` | string | Yes | Absolute path to Netscape-format `cookies.txt` file. |
| `domainSuffix` | string | No | Only import cookies whose domain ends with this suffix (e.g., `.linkedin.com`). Leaves all cookies imported if omitted. |

**Returns:** Import summary with total and filtered counts.

**Example request (full import):**

```json
{ "cookiesPath": "/tmp/linkedin-cookies.txt" }
```

**Example request (filtered import):**

```json
{ "cookiesPath": "/tmp/cookies.txt", "domainSuffix": ".linkedin.com" }
```

**Response:**

```json
{
  "status": "ok",
  "data": {
    "imported": 47,
    "filtered": 0,
    "totalLines": 47
  }
}
```

**Errors:**
- `400 BadRequest` — Missing `cookiesPath`
- `400 BadRequest` — File not found at `cookiesPath`
- `400 BadRequest` — Invalid Netscape format detected
- `401 Unauthorized` — `CAMOUFOX_API_KEY` missing or invalid
- `500 InternalServerError` — Import operation failed (permission denied, corrupted file)

---

## Error Codes Reference

| HTTP Code | Tool Error Code | Meaning | Action |
|-----------|----------------|---------|--------|
| `200` | `ok` | Success | Proceed normally |
| `400` | `BAD_REQUEST` | Missing or invalid parameter | Check required fields and value constraints |
| `401` | `UNAUTHORIZED` | Invalid or missing API key | Provide valid `CAMOUFOX_API_KEY` |
| `404` | `NOT_FOUND` | Tab ID doesn't exist or is closed | Call `camofox_list_tabs` to verify active tabs, or create a new one |
| `429` | `RATE_LIMITED` | Too many requests | Back off and retry with exponential delay |
| `500` | `INTERNAL_SERVER_ERROR` | Browser crashed, binary missing, or OOM | Check `CAMOUFOX_EXECUTABLE`, install missing libs, restart server |

---

## Environment Variables Summary

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `CAMOUFOX_EXECUTABLE` | **Yes** | — | Path to Camoufox binary |
| `CAMOUFOX_API_KEY` | No | — | API key for auth (protects import_cookies) |
| `CAMOFOX_CRASH_REPORT_ENABLED` | No | `true` | Enable anonymized crash telemetry |
| `PORT` | No | `9377` | HTTP server listen port |
| `DISPLAY` | Conditional | `:0` | X11 display (required outside WSL/container) |
| `XDG_RUNTIME_DIR` | Conditional | — | D-Bus socket dir (required in containers) |

---

## Resource Management

- **Idle memory:** ~40 MB (browser process, zero tabs)
- **Active memory:** ~200 MB per tab
- **Auto-shutdown:** Browser shuts down after configurable idle timeout (default 5 min)
- **Crash telemetry:** Anonymized only — no page content, cookies, or IPs. Opt out with `CAMOFOX_CRASH_REPORT_ENABLED=false`
- **Session isolation:** Separate cookies/storage per user session

---

## Common Patterns

### Full Automation Flow

```
1. Create tab              → camofox_create_tab(url="...")     // gets tabId
2. Read page structure     → camofox_snapshot(tabId)           // get e1, e2, e3 refs
3. Interact                → camofox_click(tabId, ref="e3")    // click button
4. Fill form               → camofox_type(tabId, text="val", ref="e2", pressEnter=true)
5. Navigate                → camofox_navigate(tabId, url="...")
6. Verify                  → camofox_screenshot(tabId)         // visual proof
7. Cleanup                 → camofox_close_tab(tabId)          // free resources
```

### Authenticated Browsing Flow

```
1. Start tab               → camofox_create_tab()
2. Import cookies          → camofox_import_cookies(pluginsPath="/tmp/cookies.txt")
3. Navigate to site        → camofox_navigate(tabId, url="https://target.com")
4. Snapshot + interact     → camofox_snapshot(tabId)
5. Close                   → camofox_close_tab(tabId)
```

### Framework Detection

```
evaluate(tabId, "window.__REACT_DEVTOOLS_GLOBAL_HOOK__ !== undefined")  // React
evaluate(tabId, "window.__NEXT_DATA__ !== undefined")                    // Next.js
evaluate(tabId, "angular")                                              // Angular
```
