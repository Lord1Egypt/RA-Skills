# AWP Built-in Tools Reference

AWP-compliant runtimes SHOULD provide the following built-in tools. All tools use the `namespace.action` naming convention and return the standard AWP tool result format.

## Standard Tool Result Format

Every tool MUST return:

```json
{
  "ok": true,
  "status": 200,
  "data": { ... },
  "error": null,
  "log": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `ok` | boolean | Whether the call succeeded |
| `status` | integer | HTTP-like status code (200, 400, 404, 500) |
| `data` | any | Result payload (tool-specific) |
| `error` | string or null | Error message if `ok` is false |
| `log` | string or null | Execution log for debugging |

---

## Web Tools

### `web.search`

Search the web for information.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | -- | Search query (1-500 chars) |
| `max_results` | integer | No | 10 | Maximum results (1-100) |
| `language` | string | No | "en" | Language filter (ISO 639-1) |

### `http.request`

Make an arbitrary HTTP request.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | Yes | -- | Target URL |
| `method` | string | No | "GET" | HTTP method |
| `headers` | object | No | {} | HTTP headers |
| `body` | string | No | null | Request body |
| `timeout` | integer | No | 30 | Timeout in seconds |

---

## File Tools

### `file.read`

Read file contents from disk.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | -- | File path |
| `encoding` | string | No | "utf-8" | File encoding |

### `file.write`

Write content to a file.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | -- | File path |
| `content` | string | Yes | -- | Content to write |
| `mode` | string | No | "overwrite" | "overwrite" or "append" |

### `file.list`

List files in a directory.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | -- | Directory path |
| `pattern` | string | No | "*" | Glob pattern |
| `recursive` | boolean | No | false | Include subdirectories |

---

## Shell Tools

### `shell.execute`

Execute a shell command in a sandboxed environment.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `command` | string | Yes | -- | Command to execute |
| `timeout` | integer | No | 30 | Timeout in seconds |
| `cwd` | string | No | null | Working directory |

---

## Agent Communication Tools

### `agent.send_message`

Send a message to another agent via the message bus.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `to` | string | Yes | -- | Target agent ID or "*" for broadcast |
| `content` | any | Yes | -- | Message content |
| `channel` | string | No | "direct" | Channel name |
| `type` | string | No | "event" | Message type (request/response/event) |

### `agent.list_messages`

List messages received from other agents.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `from_agent` | string | No | null | Filter by sender |
| `channel` | string | No | null | Filter by channel |
| `limit` | integer | No | 50 | Maximum messages to return |

---

## Memory Tools

### `memory.write`

Write to daily log or long-term memory (MEMORY.md).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content` | string | Yes | -- | Content to write |
| `target` | string | No | "daily" | "daily" or "long_term" |

### `memory.search`

Keyword search across all memory files.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | -- | Search query |
| `max_results` | integer | No | 10 | Maximum results |
| `date_range` | string | No | null | Date filter (e.g., "2026-03-01:2026-03-23") |

### `memory.read`

Read MEMORY.md, daily log, or list available dates.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target` | string | No | "long_term" | "long_term", "daily", or "dates" |
| `date` | string | No | null | Specific date for daily log (YYYY-MM-DD) |

### `memory.curate`

Trigger LLM-based curation: extract stable facts from daily logs into MEMORY.md.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `days` | integer | No | 7 | Number of recent days to curate |
| `model` | string | No | null | Override curation model |

---

## Arithmetic Tools

### `arithmetic.add` / `arithmetic.subtract` / `arithmetic.multiply` / `arithmetic.divide`

Basic arithmetic operations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number | Yes | First operand |
| `b` | number | Yes | Second operand |

---

## Reserved Namespaces

The following namespaces are reserved for built-in tools. Custom tools MUST NOT use these namespaces (R15):

`web`, `http`, `file`, `shell`, `agent`, `memory`, `arithmetic`, `numpy`, `matplot`, `pandas`, `doc`, `sklearn`
