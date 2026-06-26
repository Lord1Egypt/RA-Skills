# Coze-Power API Reference

## Overview

Base URL: `http://localhost:8899` (replace with your public URL)

Authentication: `X-API-Key` header

All responses are JSON.

---

## `GET /health`

Health check endpoint (no auth required).

### Response

```json
{
  "status": "ok",
  "version": "1.0.0",
  "tools": ["web-search", "read-file", "write-file", "list-dir", "run-command", "system-info", "clipboard-read", "clipboard-write", "notify"]
}
```

---

## `POST /tools/web-search`

Search the web. Uses DuckDuckGo, no API key required.

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | ✅ | — | Search query |
| `count` | integer | ❌ | 5 | Number of results (1-10) |

### Response

```json
{
  "success": true,
  "query": "2026 AI trends",
  "results": [
    {
      "title": "2026年AI行业趋势分析",
      "url": "https://example.com/article",
      "snippet": "2026年AI Agent将进入规模化部署阶段..."
    }
  ]
}
```

---

## `POST /tools/read-file`

Read a file from the local filesystem.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | ✅ | File path (absolute or relative) |

### Response

```json
{
  "success": true,
  "path": "/home/user/notes.txt",
  "content": "文件内容...",
  "size": 1024
}
```

### Errors

- `Access denied: path is not in allowed paths` — path outside `allowed_paths`
- `File not found` — file doesn't exist
- `File too large` — exceeds `max_file_size_kb`

---

## `POST /tools/write-file`

Write content to a file. Creates parent directories automatically.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | ✅ | File path |
| `content` | string | ✅ | Content to write |

### Response

```json
{
  "success": true,
  "path": "/home/user/output.md",
  "size": 256
}
```

---

## `POST /tools/list-dir`

List files and directories.

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `path` | string | ❌ | `.` | Directory path |

### Response

```json
{
  "success": true,
  "path": "/home/user",
  "count": 3,
  "items": [
    {
      "name": "Documents",
      "type": "dir",
      "size": 4096,
      "modified": "2026-06-05T12:00:00"
    },
    {
      "name": "notes.txt",
      "type": "file",
      "size": 1024,
      "modified": "2026-06-05T10:30:00"
    }
  ]
}
```

---

## `POST /tools/run-command`

Execute a shell command. Only whitelisted commands allowed.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string | ✅ | Shell command string |

### Response

```json
{
  "success": true,
  "stdout": "command output...",
  "stderr": "",
  "return_code": 0
}
```

### Errors

- `Command 'xxx' not allowed` — command not in whitelist
- `Command timed out` — execution > 30 seconds

---

## `GET /tools/system-info`

Get system information.

### Response

```json
{
  "success": true,
  "os": "Linux 6.6.1",
  "hostname": "my-machine",
  "architecture": "x86_64",
  "cpu_count": 16,
  "disk_total_gb": 512.0,
  "disk_free_gb": 167.4,
  "disk_used_pct": 67.3,
  "python_version": "3.11.4",
  "current_time": "2026-06-05T12:00:00"
}
```

---

## `POST /tools/clipboard-read`

Read current clipboard content.

### Response

```json
{
  "success": true,
  "content": "clipboard text..."
}
```

### Note

Requires `pyperclip` library (`pip install pyperclip`) or `xclip` on Linux.

---

## `POST /tools/clipboard-write`

Write text to clipboard.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | ✅ | Text to copy |

### Response

```json
{
  "success": true,
  "size": 42
}
```

---

## `POST /tools/notify`

Send a desktop notification.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | ✅ | Notification title |
| `message` | string | ✅ | Notification body |

### Response

```json
{
  "success": true,
  "title": "Reminder",
  "message": "Meeting at 10 AM"
}
```

### Platform support

| Platform | Method |
|----------|--------|
| Linux | `notify-send` (libnotify) |
| macOS | `osascript` |
| Windows | `MessageBoxW` |

---

## Error Format

All errors follow this format:

```json
{
  "success": false,
  "error": "Error description"
}
```

HTTP status codes:
- `200` — Success (even for tool errors, the HTTP call itself succeeded)
- `400` — Bad request (invalid JSON, missing params)
- `401` — Unauthorized (bad API key)
- `404` — Not found
- `500` — Internal server error

## CORS

All endpoints support CORS for browser-based Coze clients:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, X-API-Key`
