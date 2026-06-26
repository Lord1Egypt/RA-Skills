---
name: cdp-bridge
version: 1.0.0
description: "CDP Bridge MCP 浏览器控制：通过浏览器插件远程控制真实浏览器。适用于已安装 CDP Bridge 插件的浏览器，可获取标签页、扫描页面、执行JS、截图、导航、读取Cookie等操作。当用户说要控制浏览器、操作真实浏览器、读取网页内容、执行浏览器操作时调用本skill。"
metadata:
  requires:
    bins: ["powershell"]
  config:
    mcpUrl: "http://127.0.0.1:8000/mcp"
    wsPort: 18765
---

# CDP Bridge MCP 浏览器控制

> **前置条件：** 浏览器已安装 CDP Bridge 插件，且 MCP 服务已启动。

## 快速判断

- 用户说"控制浏览器"、"操作真实浏览器"、"读取网页" → 调用本 skill
- 用户说"用CDP"、"连接浏览器插件" → 调用本 skill
- 用户要操作**已登录的真实浏览器会话** → 调用本 skill

## 架构原理

```
┌────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
│   OpenClaw     │ ←── │  CDP Bridge MCP      │ ←── │  浏览器插件        │
│   (调用skill)  │ HTTP│  服务端              │ WS  │  (tmwd_cdp_bridge)│
│                │     │ 127.0.0.1:8000/mcp   │     │ 127.0.0.1:18765   │
└────────────────┘     └──────────────────────┘     └───────────────────┘
```

**关键端口：**
- `8000/mcp`：HTTP MCP 端点（Agent 调用）
- `18765`：WebSocket 端点（浏览器插件连接）

## Agent 执行流程

1. **检查服务状态** → 调用 `cdp-bridge/scripts/check-service.ps1`
2. **初始化 MCP 会话** → 获取 session-id
3. **选择工具** → 根据用户意图选择对应工具
4. **调用工具** → 通过 HTTP POST 调用 MCP

## 可用工具

| 工具 | 功能 | 参数 |
|------|------|------|
| `browser_get_tabs` | 获取所有标签页列表 | 无 |
| `browser_scan` | 扫描页面内容 | `tabs_only`, `switch_tab_id`, `text_only` |
| `browser_execute_js` | 执行 JavaScript | `script`, `switch_tab_id`, `no_monitor` |
| `browser_switch_tab` | 切换活动标签页 | `tab_id` |
| `browser_navigate` | 跳转到 URL | `url` |
| `browser_screenshot` | 截图 | `tab_id` |
| `browser_cookies` | 读取 Cookie | `url` |
| `browser_wait` | 等待条件 | `condition_js`, `timeout`, `interval` |
| `browser_batch` | 批量执行 CDP 命令 | `commands`, `tab_id`, `timeout` |

## 意图 → 工具索引

| 意图 | 工具 | 示例参数 |
|------|------|----------|
| 查看有哪些标签页 | `browser_get_tabs` | 无参数 |
| 读取页面内容 | `browser_scan` | `{"text_only": true}` |
| 执行 JS / 点击按钮 | `browser_execute_js` | `{"script": "document.querySelector('button').click()"}` |
| 切换到某个标签页 | `browser_switch_tab` | `{"tab_id": "123456"}` |
| 打开新网址 | `browser_navigate` | `{"url": "https://example.com"}` |
| 截图 | `browser_screenshot` | 无参数或 `{"tab_id": "xxx"}` |
| 读取 Cookie | `browser_cookies` | 无参数或 `{"url": "https://xxx.com"}` |
| 等待元素出现 | `browser_wait` | `{"condition_js": "document.querySelector('.result')", "timeout": 10}` |

## 调用方式

本 skill 通过 PowerShell 调用 MCP HTTP API：

```powershell
# 1. 初始化会话
$headers = @{
    "Accept" = "application/json, text/event-stream"
    "Content-Type" = "application/json"
}
$body = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $body
$sessionId = $response.Headers["mcp-session-id"]

# 2. 调用工具
$headers["mcp-session-id"] = $sessionId
$body = '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"browser_get_tabs","arguments":{}}}'
$response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/mcp' -Method POST -Headers $headers -Body $body
```

## 核心规则

1. **每次调用必须带上 session-id** — 初始化后获取的 session-id 需要在后续所有请求的 header 中传递
2. **先获取标签页，再操作** — 操作前先 `browser_get_tabs` 确认目标 tab_id
3. **避免操作 DevTools 端点页面** — URL 为 `127.0.0.1:9222/json` 的标签页可能有其他调试器附加，会报错
4. **扫描页面用 text_only 节省 token** — 大页面建议 `text_only: true`
5. **截图返回 base64 PNG** — 结果是图片数据，需要时可以保存或展示

## 常见错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Missing session ID` | 未传递 session-id header | 初始化后保存 session-id，后续请求带上 |
| `Another debugger is already attached` | 目标标签页已有其他调试器 | 切换到其他标签页操作 |
| `ERR_CONNECTION_REFUSED` | MCP 服务未启动 | 启动 CDP Bridge MCP 服务 |
| `Tool execution failed` | 参数错误或页面不支持 | 检查参数，尝试简化操作 |

## 启动 MCP 服务

如果 MCP 服务未启动，执行：

```powershell
$env:Path = "C:\Users\Administrator\.local\bin;$env:Path"
$env:UV_HTTP_TIMEOUT = "600"
Start-Process -NoNewWindow -FilePath "uvx" -ArgumentList "cdp-bridge@latest","--transport","streamable-http","--port","8000","--ws-port","18765"
```

## 参考文档

- [cdp-bridge-api.md](references/cdp-bridge-api.md) — MCP API 调用详解
- [cdp-bridge-tools.md](references/cdp-bridge-tools.md) — 各工具详细参数和返回格式
- [cdp-bridge-examples.md](references/cdp-bridge-examples.md) — 完整操作示例

## 插件安装指引

插件文件位于：`cdp-bridge-tutorial/extension/tmwd_cdp_bridge/`

安装步骤：
1. 打开浏览器扩展页面（Chrome: `chrome://extensions/`，Edge: `edge://extensions/`）
2. 开启「开发者模式」
3. 点击「加载已解压的扩展程序」
4. 选择 `tmwd_cdp_bridge` 文件夹
5. 配置 Bridge Host = `127.0.0.1`，Port = `18765`