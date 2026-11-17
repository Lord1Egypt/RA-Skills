# AI_Health MCP 原始协议示例（手工调试用）

仅在无 MCP 客户端、需要直接用 HTTP 调试时加载本文件。`BASE_URL` 默认 `https://health.geeyo.com`。

## Streamable HTTP

### 1. initialize（新会话）

```bash
curl -s -D - -X POST $BASE_URL/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"my-agent","version":"1.0"}}}'
```

从响应头取 `mcp-session-id`，后续所有请求携带 `-H "mcp-session-id: <SID>"`。
响应体为 SSE 格式（`event: message` + `data: {...}`），解析 `data:` 行即可。

### 2. initialized 通知（初始化后必发）

```bash
curl -s -X POST $BASE_URL/mcp -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" -H "mcp-session-id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

### 3. tools/list 与 tools/call

```bash
# 列工具
-d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# 穴位咨询
-d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"acupoint_consult","arguments":{"message":"前额胀痛，受凉后加重","sessionId":"<clientId>-a1b2c3"}}}'

# 列古籍
-d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"list_reference_books","arguments":{}}}'
```

### 4. 关闭会话

```bash
curl -s -X DELETE $BASE_URL/mcp -H "mcp-session-id: $SID"
```

## 旧版 HTTP+SSE

```bash
# 1. 建立长连接（保持不断开），首个事件为 endpoint：
#    event: endpoint
#    data: /mcp/messages?sessionId=<uuid>
curl -N $BASE_URL/mcp/sse

# 2. 向 endpoint POST JSON-RPC（响应 202，实际结果从 SSE 流返回）
curl -s -X POST "$BASE_URL/mcp/messages?sessionId=<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"my-agent","version":"1.0"}}}'
```

## 工具返回格式

所有工具返回 `content[0].text` 内嵌 JSON 字符串，需二次 `JSON.parse`。例：

```json
{"reply":"...","isFinal":false,"sessionId":"xxx","followupCount":1,"maxFollowup":3}
```
