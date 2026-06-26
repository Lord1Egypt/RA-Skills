---
name: AI Browser
slug: ai-browser
version: 1.0.0
homepage: https://github.com/openclaw/ai-browser
description: "通过 WebSocket 控制真实浏览器，实现导航、点击、输入、截图、DOM 获取等完整自动化操作。特点：真正的浏览器内核 (Chromium)、WebSocket 实时控制、支持无头/有头模式、自动重连机制。"
changelog: "初始版本 - 完整浏览器控制功能"
metadata: {"clawdbot":{"emoji":"🌐","os":["linux","darwin","win32"]}}
---

# AI Browser Skill 🌐

通过 WebSocket 控制真实浏览器，实现导航、点击、输入、截图、DOM 获取等自动化操作。

## 特点

- ✅ 真正的浏览器内核 (Chromium)
- ✅ WebSocket 实时控制
- ✅ 支持无头/有头模式
- ✅ 简单的标签页管理
- ✅ 自动重连机制

## 启动方法

```bash
# 1. 安装依赖
npm install

# 2. 启动服务
npm start

# 服务将运行在 ws://localhost:18790
```

## WebSocket 协议

### 连接

连接到 `ws://localhost:18790`

### 消息格式

发送 JSON:

```json
{
  "id": "请求 ID (可选)",
  "action": "动作名称",
  "params": { ... }
}
```

### 支持的动作

| 动作 | 参数 | 说明 |
|------|------|------|
| `navigate` | `{ url: "https://..." }` | 导航到指定 URL |
| `snapshot` | `{}` | 获取当前页面简化 DOM 结构 |
| `screenshot` | `{ fullPage: false }` | 截图 (返回 base64) |
| `click` | `{ selector: "button" }` | 点击元素 |
| `type` | `{ selector: "input", text: "hello", delay: 50 }` | 输入文本 |
| `evaluate` | `{ script: "document.title" }` | 执行 JS 脚本 |
| `status` | `{}` | 获取浏览器状态 |

### 响应格式

```json
{
  "id": "请求 ID",
  "success": true,
  "result": { ... }
}
```

## 使用示例 (Python)

```python
import websocket
import json

ws = websocket.create_connection("ws://localhost:18790")

# 导航
ws.send(json.dumps({"action": "navigate", "params": {"url": "https://fanqie.baidu.com"}}))
print(ws.recv())

# 截图
ws.send(json.dumps({"action": "screenshot", "params": {}}))
resp = json.loads(ws.recv())
with open("screen.png", "wb") as f:
    f.write(base64.b64decode(resp["result"]["image"]))

ws.close()
```

## 注意事项

- 首次启动会自动下载 Chromium (约 100MB)
- 默认端口 18790，可通过 `AI_BROWSER_PORT` 环境变量修改
- 无头模式设为 `false`，可以看到浏览器界面（方便调试）

## 使用场景

- 网页自动化测试
- 数据抓取
- 截图采集
- 表单自动填写
- 网站监控