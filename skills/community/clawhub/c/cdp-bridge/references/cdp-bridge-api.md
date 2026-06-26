# CDP Bridge MCP API 调用详解

## MCP 协议基础

CDP Bridge MCP 使用 streamable-http 模式，支持 JSON-RPC 2.0 协议。

### 请求格式

```json
{
    "jsonrpc": "2.0",
    "id": <number>,
    "method": "<method_name>",
    "params": { ... }
}
```

### 响应格式（SSE）

```
event: message
data: {"jsonrpc":"2.0","id":<id>,"result":{...}}
```

## 初始化流程

### 1. 发送 initialize 请求

```powershell
$headers = @{
    "Accept" = "application/json, text/event-stream"
    "Content-Type" = "application/json"
}
$body = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $body
```

### 2. 获取 session-id

```powershell
$sessionId = $response.Headers["mcp-session-id"]
# 示例: cb34dcb93ebb4a02a96960a53755c56d
```

### 3. 后续请求带上 session-id

```powershell
$headers["mcp-session-id"] = $sessionId
```

## 工具调用

### tools/list

列出所有可用工具：

```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}
```

返回 9 个工具：browser_get_tabs, browser_scan, browser_execute_js, browser_switch_tab, browser_navigate, browser_screenshot, browser_cookies, browser_wait, browser_batch

### tools/call

调用具体工具：

```json
{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "browser_get_tabs",
        "arguments": {}
    }
}
```

## 错误处理

### 常见错误码

| 错误码 | 含义 |
|--------|------|
| -32600 | Bad Request（缺少 session-id） |
| -32601 | Method not found |
| -32602 | Invalid params |

### 错误响应格式

```json
{
    "jsonrpc": "2.0",
    "id": "server-error",
    "error": {
        "code": -32600,
        "message": "Missing session ID"
    }
}
```

## 完整调用示例

```powershell
# 1. 初始化
$headers = @{
    "Accept" = "application/json, text/event-stream"
    "Content-Type" = "application/json"
}
$initBody = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
$initResponse = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $initBody -TimeoutSec 10
$sessionId = $initResponse.Headers["mcp-session-id"]

# 2. 调用工具
$headers["mcp-session-id"] = $sessionId
$toolBody = '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"browser_get_tabs","arguments":{}}}'
$toolResponse = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $toolBody -TimeoutSec 30

# 3. 解析结果
$content = $toolResponse.Content
# SSE 格式: event: message\ndata: {...}
$jsonLine = ($content -split "\n" | Where-Object { $_ -match "^data: " })[0].Substring(6)
$result = $jsonLine | ConvertFrom-Json
$result.result.content[0].text | ConvertFrom-Json
```

## 服务状态检查

```powershell
# 检查 MCP 服务是否运行
try {
    Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -TimeoutSec 5 -ErrorAction Stop
} catch {
    # 服务未启动，需要启动服务
}
```