# Chrome DevTools Protocol (CDP) 参考

## 协议概述

Chrome DevTools Protocol 是 Chrome 浏览器提供的调试协议，允许外部工具控制浏览器行为。

## 核心端点

### HTTP 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/json/list` | GET | 获取所有可调试页面 |
| `/json/new?url=` | GET | 创建新标签页 |
| `/json/close/` | GET | 关闭标签页 |

### WebSocket 端点

```
ws://127.0.0.1:{PORT}/devtools/page/{PAGE_ID}
```

## 常用 CDP 命令

### Page.enable

启用 Page domain，用于监听页面事件。

```json
{ "id": 1, "method": "Page.enable" }
```

### Runtime.evaluate

执行 JavaScript 并获取结果。

```json
{
  "id": 2,
  "method": "Runtime.evaluate",
  "params": {
    "expression": "document.documentElement.outerHTML",
    "returnByValue": true
  }
}
```

### Network.enable / Network.getResponseBody

启用网络监控和获取响应体。

## 响应格式

### 成功响应

```json
{
  "id": 1,
  "result": {
    "result": {
      "type": "string",
      "value": "<html>...</html>"
    }
  }
}
```

### 错误响应

```json
{
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

## 协议版本

CDP 协议有多个版本，每个 Chrome 版本可能支持不同的协议域。

- 查看协议版本：`http://127.0.0.1:{PORT}/json/version`
- 查看协议域支持：`http://127.0.0.1:{PORT}/json/protocol`

## 调试技巧

### 1. 获取页面列表

```bash
curl http://127.0.0.1:9222/json/list
```

返回：
```json
[
  {
    "id": "page-id",
    "url": "https://chatgpt.com/share/xxx",
    "title": "对话标题",
    "type": "page"
  }
]
```

### 2. 创建新标签页

```bash
curl "http://127.0.0.1:9222/json/new?https://chatgpt.com/share/xxx"
```

### 3. 实时监听消息

使用 Chrome DevTools 可以实时查看 CDP 消息：

1. 打开 `chrome://inspect`
2. 点击目标页面的 "inspect"
3. 在 DevTools 中查看 Console/Network

## 安全注意事项

1. **CSP 限制**：CDP 是浏览器内部协议，不受页面 CSP 限制
2. **调试端口**：不要在公共网络暴露调试端口
3. **会话复用**：复用已有 Chrome 会话可绕过登录态

## 参考链接

- [官方文档](https://chromedevtools.github.io/devtools-protocol/)
- [Protocol Viewer](https://chromium.googlesource.com/chromium/src/+/master/third_party/devtools-frontend/src/front_end/protocol.json)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)