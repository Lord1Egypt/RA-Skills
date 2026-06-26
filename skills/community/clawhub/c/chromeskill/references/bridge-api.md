# Bridge API Reference — Chrome AI Action

Complete reference for all actions available via the CAA bridge HTTP API (64+ actions).

**Base URL**: `http://127.0.0.1:9876/`

---

## Core Request Format

```json
{"type": "action", "action": "<ACTION>", "params": {...}, "requestId": "optional-id"}
```

### Batch Format

```json
{"type": "batch", "actions": [
  {"action": "<ACTION>", "params": {...}},
  {"action": "<ACTION>", "params": {...}}
]}
```

---

## Navigation

### `navigate`
Navigate to a URL. Chinese characters in query params MUST be pre-encoded.

```json
{"action": "navigate", "params": {"url": "https://www.baidu.com/s?wd=%E5%A6%BB%E5%AD%90", "waitUntil": "load", "timeout": 30000}}
```

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `url` | string | Yes | — | Full URL (non-ASCII auto-encoded, but query values should be pre-encoded) |
| `waitUntil` | string | No | `"load"` | `"load"`, `"domcontentloaded"`, `"networkidle0"`, `"none"` |
| `timeout` | number | No | `30000` | Navigation timeout in ms |

**Response**: `{url, title}`

### `getUrl` / `getTitle`
Get current URL or page title. No params.

### `goBack` / `goForward` / `reload`
Browser history navigation. No params.

---

## Page Content

### `getText` / `getHtml`
```json
{"action": "getText", "params": {"selector": ".content"}}
{"action": "getHtml", "params": {"selector": "#main"}}
```
`selector` is optional (omit for full page).

### `getLinks` / `getImages` / `getHeadings` / `getMetaTags`
No params. Returns arrays of all matching elements.

### `getFormFields`
Returns all form inputs with: tag, type, name, id, placeholder, value, disabled, required, label.

### `getFocusableElements`
Returns all interactive elements with: tag, id, type, name, placeholder, value, text, rect.

---

## Element Interaction

### `click`
```json
{"action": "click", "params": {"selector": "#submit-btn", "timeout": 5000}}
```
| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `selector` | string | Yes | — | CSS selector |
| `timeout` | number | No | `5000` | Wait for element timeout |

### `type`
```json
{"action": "type", "params": {"selector": "input[name=q]", "value": "search text", "clear": true, "delay": 0}}
```
`clear` defaults to `true` (clear before typing). `delay` is ms between keystrokes.

### `pressKey`
```json
{"action": "pressKey", "params": {"key": "Enter", "ctrl": false, "alt": false, "shift": false, "meta": false}}
```
Supported keys: `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`, `Home`, `End`, `PageUp`, `PageDown`, `Space`, `\n` (Enter), `\t` (Tab).

### `scroll` / `scrollIntoView`
```json
{"action": "scroll", "params": {"x": 0, "y": 500, "behavior": "smooth"}}
{"action": "scrollIntoView", "params": {"selector": "#footer", "behavior": "instant", "block": "center"}}
```

### `focus` / `hover` / `select`
```json
{"action": "focus", "params": {"selector": "#input"}}
{"action": "hover", "params": {"selector": "#menu"}}
{"action": "select", "params": {"selector": "select[name=country]", "value": "CN"}}
```

### `findElement`
Find element by text content. Returns first match.
```json
{"action": "findElement", "params": {"text": "Submit", "tagName": "button"}}
```

---

## Data Extraction

### `getValue` / `getAttribute` / `getAttributeAll` / `getBoundingBox`
```json
{"action": "getValue", "params": {"selector": "#email"}}
{"action": "getAttribute", "params": {"selector": "img", "name": "src"}}
{"action": "getAttributeAll", "params": {"selector": "#el"}}
{"action": "getBoundingBox", "params": {"selector": "#main"}}
```

### `getCookies`
No params. Returns all cookies.

### `getPerformanceMetrics`
No params. Returns timing and navigation entries.

### `getSelectedValue` / `getSelectOptions`
```json
{"action": "getSelectedValue", "params": {"selector": "select[name=country]"}}
{"action": "getSelectOptions", "params": {"selector": "select[name=country]"}}
```

---

## JavaScript Execution

### `evaluate`
```json
{"action": "evaluate", "params": {"code": "document.querySelector('h1').textContent"}}
```
JS runs in page context, has access to DOM. Return values must be JSON-serializable.

### `injectScript` / `injectCSS`
```json
{"action": "injectScript", "params": {"code": "console.log('injected')"}}
{"action": "injectCSS", "params": {"css": "body { background: red; }"}}
```

---

## Screenshot & Export

### `screenshot`
```json
{"action": "screenshot", "params": {"format": "png", "quality": 80, "fullPage": false}}
```
| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `format` | string | No | `"png"` | `"png"` or `"jpeg"` |
| `quality` | number | No | `80` | JPEG quality (1-100) |
| `fullPage` | boolean | No | `false` | Capture full scrollable page |

**Response**: `{screenshot: "data:image/png;base64,..."}`

### `getPdf`
```json
{"action": "getPdf", "params": {"format": "A4"}}
```
Returns PDF as base64 data URI.

---

## Tab Management

| Action | Params | Description |
|---|---|---|
| `listTabs` | — | List all tabs: `{tabId, url, title}[]` |
| `newTab` | `{url?}` | Open new tab (optional URL) |
| `closeTab` | `{tabId}` | Close tab by ID |
| `switchTab` | `{tabId}` | Switch to tab (brings to front) |
| `getCurrentTab` | — | Get active tab: `{tabId, url, title}` |

---

## Waiting

### `waitForElement`
```json
{"action": "waitForElement", "params": {"selector": ".loaded", "timeout": 10000, "state": "visible"}}
```
`state`: `"attached"` (default), `"visible"`, `"hidden"`.

### `waitForTimeout`
```json
{"action": "waitForTimeout", "params": {"ms": 2000}}
```

### `waitForNavigation`
```json
{"action": "waitForNavigation", "params": {"timeout": 30000}}
```

---

## Cookie Management

### `setCookie`
```json
{"action": "setCookie", "params": {"name": "token", "value": "abc123", "domain": ".example.com", "path": "/"}}
```

### `deleteCookie`
```json
{"action": "deleteCookie", "params": {"name": "token"}}
```

---

## Network Interception

### `blockUrls` / `unblockUrls`
```json
{"action": "blockUrls", "params": {"patterns": ["analytics.com", "tracking.js"]}}
{"action": "unblockUrls", "params": {"patterns": ["analytics.com"]}}
```
If `patterns` is omitted for `unblockUrls`, all blocks are cleared.

### `mockResponse`
```json
{"action": "mockResponse", "params": {"urlPattern": "/api/data", "statusCode": 200, "contentType": "application/json", "body": "{\"ok\":true}"}}
```

### `getNetworkRequests` / `clearNetworkRequests`
No params for get. Returns: `{url, method, headers, resourceType, timestamp}`.

---

## Storage

### `getLocalStorage`
```json
{"action": "getLocalStorage", "params": {"key": "token"}}
```
Omit `key` to get all items.

### `setLocalStorage` / `removeLocalStorage`
```json
{"action": "setLocalStorage", "params": {"key": "theme", "value": "dark"}}
{"action": "removeLocalStorage", "params": {"key": "theme"}}
```

### `clearLocalStorage`
No params.

---

## File Operations

### `uploadFile`
```json
{"action": "uploadFile", "params": {"selector": "input[type=file]", "filePath": "C:\\path\\to\\file.pdf"}}
```

### `setInputFiles`
```json
{"action": "setInputFiles", "params": {"selector": "input[type=file]", "files": ["C:\\a.pdf", "C:\\b.pdf"]}}
```

### `downloadFile`
```json
{"action": "downloadFile", "params": {"url": "https://example.com/file.pdf", "destination": "C:\\downloads\\file.pdf"}}
```

---

## Viewport

### `getViewport`
No params. Returns `{width, height}`.

### `setViewport`
```json
{"action": "setViewport", "params": {"width": 1920, "height": 1080}}
```

---

## Console Logs

### `getConsoleLogs`
No params. Returns captured page console logs: `{type, text, timestamp}`.

### `clearConsoleLogs`
No params. Clears captured logs.

---

## Accessibility

### `getAccessibilityTree`
```json
{"action": "getAccessibilityTree", "params": {}}
```
Returns the full accessibility tree via CDP.

---

## Utility

| Action | Params | Response |
|---|---|---|
| `ping` | — | `{pong, cdpConnected, cdpPort, bridgePort}` |
| `highlight` | `{selector, color?}` | Highlights element with colored outline |
| `dispatchEvent` | `{selector, event, options?}` | Dispatches custom DOM event |
| `getBrowserInfo` | — | `{browser, cdpPort, platform, node}` |

---

## Generic Action Fallback

If an action name doesn't match built-in handlers, the bridge calls a custom handler on the page:

```javascript
window.__aiActionHandlers = window.__aiActionHandlers || {};
window.__aiActionHandlers['myCustomAction'] = function(params) {
  return { done: true };
};
```

## Error Codes

| Code | Description |
|---|---|
| `CDP_NOT_CONNECTED` | Chrome not running with `--remote-debugging-port=9222` (auto-retry) |
| `ACTION_ERROR` | Action execution error |
| `INVALID_REQUEST` | Missing required fields |
| `PARSE_ERROR` | Invalid JSON body (HTTP 400) |
