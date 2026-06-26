# MCP Tools Reference

## Endpoint

```
POST https://dev.ideasprite.com/mcp
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
```

## Authentication

Token is stored in `D:\workspace\demo\elastolink\.env` as `ELASTOLINK_TOKEN`.

## Initialize (Required First)

```bash
curl -X POST https://dev.ideasprite.com/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0.0"}}}'
```

**Important:** Extract `mcp-session-id` from response headers. Use this session ID in all subsequent requests via header `mcp-session-id: <session-id>`.

## Available Tools

### 1. status — 设备状态

检查设备连接状态。

**Arguments:** none

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "status",
    "arguments": {}
  }
}
```

---

### 2. lists — 会议列表

列出所有历史会议。

**Arguments:** none

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "lists",
    "arguments": {}
  }
}
```

**Response:** Returns array of meetings with `meeting_id` and titles.

---

### 3. detail — 会议内容

通过会议 ID 查看会议详细内容。

**Arguments:**
| Name | Type | Required |
|------|------|----------|
| `meeting_id` | string | ✓ |

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "detail",
    "arguments": {
      "meeting_id": "<meeting-id>"
    }
  }
}
```

---

### 4. markdown — 会议 Markdown 原文

通过会议 ID 获取会议输出文档的 Markdown 格式。

**Arguments:**
| Name | Type | Required |
|------|------|----------|
| `meeting_id` | string | ✓ |

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "markdown",
    "arguments": {
      "meeting_id": "<meeting-id>"
    }
  }
}
```

---

### 5. office — 会议 Office 文档

通过会议 ID 下载 Office 格式（Word/Excel/PPT）的输出文档。

**Arguments:**
| Name | Type | Required |
|------|------|----------|
| `meeting_id` | string | ✓ |

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "office",
    "arguments": {
      "meeting_id": "<meeting-id>"
    }
  }
}
```

**Response:** Returns a result object with document URLs or base64-encoded content.

---

## Common Workflow

1. **Initialize** → get session ID
2. **lists** → get meeting list, pick meeting_id
3. **detail/markdown/office** → get meeting content
4. Present results to user

## Notes

- Session ID expires after some time; re-initialize if tools call returns "Missing session ID"
- All responses are JSON-RPC 2.0 format
- Server: Elastolink MCP Server v1.26.0
