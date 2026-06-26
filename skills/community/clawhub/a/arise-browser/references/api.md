# AriseBrowser API Reference

Base URL: `http://localhost:16473`

## Health

### GET /health
Returns server status.

Response:
```json
{"status": "ok", "connected": true, "version": "0.2.0"}
```

## Navigation

### POST /navigate
Navigate to a URL.

Body:
```json
{"url": "https://example.com", "newTab": false, "tabId": "tab-001", "timeout": 15000}
```

Response:
```json
{"message": "Navigated to https://example.com", "url": "https://example.com"}
```

## Snapshot

### GET /snapshot
Get accessibility tree snapshot.

Query params:
- `tabId`: snapshot a specific tab without switching the global current tab
- `format`: `yaml` (default), `json`, `compact`, `text`
- `diff`: `true`/`false` — return only changes since last snapshot
- `viewportLimit`: `true`/`false` — limit to visible viewport

Response (yaml):
```json
{"snapshot": "- Page Snapshot\n```yaml\n...\n```", "format": "yaml"}
```

Response (json):
```json
{"nodes": [{"ref": "e0", "role": "link", "name": "Home"}], "url": "...", "title": "...", "count": 42}
```

## Actions

### POST /action
Execute a single browser action.

Body (AriseBrowser native):
```json
{"type": "click", "ref": "e5", "tabId": "tab-001", "owner": "agent-1"}
```

Body (Pinchtab-compatible):
```json
{"kind": "click", "ref": "e5"}
```

Supported kinds: `click`, `type`, `fill`, `press`, `hover`, `scroll`, `select`, `focus`

### POST /actions
Execute multiple actions sequentially.

Body:
```json
{"actions": [{"type": "click", "ref": "e5", "tabId": "tab-001"}], "owner": "agent-1", "stopOnError": true}
```

## Content

### GET /text
Extract page text content.
Query params: `tabId` (optional)

### GET /screenshot
Get JPEG screenshot.

Query params:
- `tabId`: specific tab (optional)
- `quality`: 1-100 (default 75)
- `raw`: `true` returns raw JPEG bytes

### GET /pdf
Export page as PDF.
Query params: `tabId` (optional)

### POST /evaluate
Execute JavaScript in page context.

Body:
```json
{"expression": "document.title", "tabId": "tab-001", "owner": "agent-1"}
```

## Tabs

### GET /tabs
List all open tabs.

### POST /tab
Create, close, or switch tabs.

Body:
```json
{"action": "create", "url": "https://example.com"}
{"action": "close", "tabId": "tab-001"}
{"action": "switch", "tabId": "tab-002"}
```

### POST /tab/lock
Lock a tab for exclusive use.
Locked write routes return `423 Locked` unless the same `owner` is supplied.

Body:
```json
{"tabId": "tab-001", "owner": "agent-1", "ttlMs": 60000}
```

### POST /tab/unlock
Release a tab lock.

Body:
```json
{"tabId": "tab-001", "owner": "agent-1"}
```

## Cookies

### GET /cookies
Get all cookies.

### POST /cookies
Set cookies.

Body:
```json
{"cookies": [{"name": "session", "value": "abc123", "url": "https://example.com"}]}
```

## Recording

### POST /recording/start
Start behavior recording.

Response:
```json
{"recordingId": "session_20260303T180000"}
```

### POST /recording/stop
Stop recording and get operations.

Body:
```json
{"recordingId": "session_20260303T180000"}
```

### GET /recording/status
Check recording status.

Query params:
- `recordingId`: specific recording (optional)

### POST /recording/export
Export recording as Learn protocol format.
Works for active recordings and recently stopped recordings retained in memory.

Body:
```json
{"recordingId": "session_20260303T180000", "task": "Search for AI products"}
```

Response:
```json
{
  "type": "browser_workflow",
  "task": "Search for AI products",
  "success": true,
  "domain": "producthunt.com",
  "steps": [
    {"url": "https://producthunt.com", "action": "navigate"},
    {"url": "https://producthunt.com", "action": "click", "target": "Search"},
    {"url": "https://producthunt.com", "action": "type", "target": "e12", "value": "AI"}
  ],
  "metadata": {
    "duration_ms": 15000,
    "page_count": 3,
    "recorded_at": "2026-03-03T18:00:00Z"
  }
}
```
