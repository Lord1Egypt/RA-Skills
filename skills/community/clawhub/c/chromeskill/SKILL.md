---
name: chrome-ai-action-skill
description: "Browser automation via Chrome AI Action (CAA) bridge. Control Chrome programmatically — navigate, click, type, screenshot, extract content, and more. Uses Puppeteer (CDP) mode. First use auto-installs npm package and starts the bridge. Chrome is auto-launched if not running."
---

# Chrome AI Action — Browser Automation Skill

AI Agent 浏览器自动化技能。通过 Chrome AI Action (CAA) 桥接服务，以 Puppeteer (CDP) 模式编程控制 Chrome 浏览器，支持导航、点击、输入、截图、内容提取、网络拦截、Cookie 管理、PDF 导出等 60+ 操作。

---

## When to Use / 何时使用

| 场景 | 调用 |
|---|---|
| User asks to browse a web page, search, fill forms, extract data | Yes |
| User needs screenshots of a web page | Yes |
| User wants to automate browser interactions | Yes |
| User asks about writing code / debugging (no browser involved) | No |

| 场景 | 调用 |
|---|---|
| 用户需要在浏览器中打开网页、搜索、填写表单、提取数据 | 是 |
| 用户需要网页截图 | 是 |
| 用户希望自动化浏览器操作 | 是 |
| 用户问代码/调试相关（不涉及浏览器） | 否 |

---

## ⚠️ CRITICAL: Chinese URL Encoding

> **IMPORTANT**: When constructing URLs with Chinese characters for the `navigate` action, the agent MUST encode the query string values using `encodeURIComponent`. The bridge automatically encodes non-ASCII characters in the URL path, but query string values must be pre-encoded by the caller.

> **重要说明**: 调用 `navigate` 时，URL 中如果包含中文字符，智能体必须先用 `encodeURIComponent` 对查询参数值进行编码。例如 `wd=妻子的浪漫旅行` 必须写成 `wd=%E5%A6%BB%E5%AD%90%E7%9A%84%E6%B5%AA%E6%BC%AB%E6%97%85%E8%A1%8C`。

### Correct / 正确写法

```json
{"action": "navigate", "params": {"url": "https://www.baidu.com/s?wd=%E5%A6%BB%E5%AD%90%E7%9A%84%E6%B5%AA%E6%BC%AB%E6%97%85%E8%A1%8C"}}
```

### Wrong / 错误写法

```json
{"action": "navigate", "params": {"url": "https://www.baidu.com/s?wd=妻子的浪漫旅行"}}
```

### How to encode in Node.js / 如何在 Node.js 中编码

```javascript
const encoded = encodeURIComponent('妻子的浪漫旅行');
// Result: %E5%A6%BB%E5%AD%90%E7%9A%84%E6%B5%AA%E6%BC%AB%E6%97%85%E8%A1%8C
```

---

## Prerequisites / 前提条件

| Requirement | Check | Auto-resolve |
|---|---|---|
| Chrome / Chromium installed | Detected automatically | No (user must install) |
| Chrome running with CDP | Detected on startup | Yes (auto-launched) |
| Node.js 18+ | `node --version` | No |

| 要求 | 检查方式 | 自动处理 |
|---|---|---|
| 已安装 Chrome / Chromium | 自动检测常用安装路径 | 否（用户需安装） |
| Chrome 以 CDP 模式运行 | 启动时检测 | 是（自动启动） |
| Node.js 18+ | `node --version` | 否 |

---

## Startup Protocol / 启动协议

When loaded for the first time, the agent MUST run the startup script. The script runs the bridge as a **background child process** — the agent does NOT need to manage the process separately.

首次加载时，AI 智能体必须执行以下启动脚本。脚本会自动在后台启动桥接服务，智能体**无需单独管理进程**。

```bash
node <skill_dir>/scripts/startup.js
```

### What it does / 执行流程

1. **Check if bridge is already running**: `GET /health` on port 9876 → skip if OK
2. **Ensure npm package installed**: `npm list -g chrome-ai-action` → installs via `npm install -g chrome-ai-action` if missing
3. **Start the bridge**: `chrome-ai-action --port 9876`, waits for health check
4. **Auto-launch Chrome**: If Chrome not running with CDP, the bridge starts it automatically (cross-platform)

### Environment Variables / 环境变量

| Variable | Default | Description |
|---|---|---|
| `CAA_BRIDGE_PORT` | `9876` | Bridge HTTP server port |
| `CAA_STARTUP_TIMEOUT` | `30000` | Max wait for bridge ready (ms) |
| `CHROME_PATH` | auto-detect | Custom Chrome executable path |
| `CHROME_USER_DATA_DIR` | platform-dependent | Chrome profile directory |

---

## API Protocol / 通信协议

**Endpoint**: `http://127.0.0.1:9876/`

### Endpoints / 接口地址

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check — returns bridge & CDP status |
| `GET` | `/schema` | Full action schema (64+ actions) |
| `POST` | `/` | Execute action(s) |

### Request Format / 请求格式

```json
{"type": "action", "action": "<ACTION>", "params": {...}, "requestId": "optional-id"}
```

### Batch Request / 批量请求

```json
{"type": "batch", "actions": [
  {"action": "navigate", "params": {"url": "https://example.com"}},
  {"action": "getTitle"}
]}
```

### Response Format / 响应格式

```json
{"success": true, "data": {...}, "requestId": "req-1", "timestamp": 1712345678901}
```

### Error Response / 错误响应

```json
{"success": false, "error": {"code": "ACTION_ERROR", "message": "..."}, "requestId": "req-1", "timestamp": 1712345678901}
```

---

## Available Actions (64+) / 可用操作 (64+)

### Navigation / 导航
`navigate`, `goBack`, `goForward`, `reload`, `getUrl`, `getTitle`

### Page Content / 页面内容
`getText`, `getHtml`, `getLinks`, `getImages`, `getHeadings`, `getMetaTags`, `getFormFields`, `getFocusableElements`

### Element Interaction / 元素交互
`click`, `type`, `pressKey`, `scroll`, `scrollIntoView`, `findElement`, `focus`, `hover`, `select`

### Data Extraction / 数据提取
`getValue`, `getAttribute`, `getAttributeAll`, `getBoundingBox`, `getCookies`, `getPerformanceMetrics`, `getSelectedValue`, `getSelectOptions`

### JavaScript / JS 执行
`evaluate`, `injectScript`, `injectCSS`

### Screenshot & Export / 截图与导出
`screenshot` (PNG/JPEG), `getPdf` (A4/Letter)

### Tab Management / 标签页管理
`listTabs`, `newTab`, `closeTab`, `switchTab`, `getCurrentTab`

### Waiting / 等待
`waitForElement`, `waitForTimeout`, `waitForNavigation`

### Cookie Management / Cookie 管理
`setCookie`, `deleteCookie`

### Network Interception / 网络拦截
`blockUrls`, `unblockUrls`, `mockResponse`, `getNetworkRequests`, `clearNetworkRequests`

### Storage / 本地存储
`getLocalStorage`, `setLocalStorage`, `removeLocalStorage`, `clearLocalStorage`

### File Operations / 文件操作
`uploadFile`, `setInputFiles`, `downloadFile`

### Viewport / 视口
`getViewport`, `setViewport`

### Console / 控制台日志
`getConsoleLogs`, `clearConsoleLogs`

### Accessibility / 无障碍
`getAccessibilityTree`

### Utility / 工具
`ping`, `connect`, `disconnect`, `getBrowserInfo`, `highlight`, `dispatchEvent`

---

## Typical Workflow / 典型工作流

1. **Navigate**: `navigate` → go to target URL (encode Chinese in query params)
2. **Wait**: `waitForElement` → wait for key content
3. **Read**: `getText` / `getHtml` / `getLinks` → understand page
4. **Interact**: `click` / `type` / `pressKey` → perform actions
5. **Extract**: `getText` / `screenshot` / `evaluate` → get results
6. **Confirm**: `screenshot` → visually verify

### Example: Search Baidu with Chinese / 百度搜索中文示例

```json
{"type": "batch", "actions": [
  {"action": "navigate", "params": {"url": "https://www.baidu.com/s?wd=%E5%A6%BB%E5%AD%90%E7%9A%84%E6%B5%AA%E6%BC%AB%E6%97%85%E8%A1%8C"}},
  {"action": "waitForTimeout", "params": {"ms": 2000}},
  {"action": "getText"}
]}
```

### Example: Full Login Flow / 登录流程示例

```json
{"type": "batch", "actions": [
  {"action": "navigate", "params": {"url": "https://example.com/login"}},
  {"action": "waitForElement", "params": {"selector": "input[name=username]", "timeout": 10000}},
  {"action": "type", "params": {"selector": "input[name=username]", "value": "myuser"}},
  {"action": "type", "params": {"selector": "input[name=password]", "value": "mypassword"}},
  {"action": "click", "params": {"selector": "button[type=submit]"}},
  {"action": "waitForTimeout", "params": {"ms": 3000}},
  {"action": "getCurrentTab"}
]}
```

---

## Error Handling / 错误处理

| Error Code | Meaning | Resolution |
|---|---|---|
| `CDP_NOT_CONNECTED` | Chrome not running with debug port | Bridge auto-launches Chrome, retries every 3s |
| `ACTION_ERROR` | Action execution failed | Check params, use `getFocusableElements` to find elements first |
| `INVALID_REQUEST` | Malformed request | Check request format |
| `PARSE_ERROR` | JSON parse failure | Send valid JSON |

---

## Discovery Tips / 探测提示

When you don't know what elements are on a page:

1. `getFocusableElements` → all interactive elements (with positions)
2. `getFormFields` → all form inputs with metadata
3. `getLinks` → all links on page
4. `getHeadings` → understand page structure
5. `getText` → all visible text

---

## References / 参考资料

- `references/bridge-api.md` — Complete API reference with all 64+ actions
- `references/setup-guide.md` — Detailed setup and troubleshooting
- `scripts/startup.js` — Startup automation script
