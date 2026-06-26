# Browser Automation — API Reference / API 参考

> **[English](#english)** | **[中文](#中文)**

---

<a id="english"></a>

## English

> Shared reference documentation. Skills link here for detailed tool information.

### Calling Convention

You do NOT call browser tools directly. You call `browser_subagent` with these parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `TaskName` | ✅ | Human-readable title, e.g., "Navigate to URL" |
| `Task` | ✅ | Detailed instructions for the subagent |
| `TaskSummary` | ✅ | 1-2 sentence summary for UI display |
| `RecordingName` | ✅ | Filename for WebP recording (max 3 words, lowercase_underscores) |
| `MediaPaths` | ❌ | Up to 3 image/video paths to provide as context |
| `ReusedSubagentId` | ❌ | Resume from a previous subagent's context |

### Available Browser Tools (inside browser_subagent)

#### Navigation

| Tool | Description |
|------|-------------|
| `open_browser_url` | Navigate to a URL |

#### Observation

| Tool | Returns | Description |
|------|---------|-------------|
| `capture_browser_screenshot` | PNG file path | Visual snapshot of the current viewport |
| `browser_get_dom` | DOM tree (text) | Full DOM with element attributes and coordinates |
| `read_browser_page` | Markdown text | Page content converted to readable markdown |
| `browser_list_network_requests` | Request list | All HTTP requests with methods, URLs, status codes |
| `capture_browser_console_logs` | Log entries | JavaScript console output (errors, warnings, info) |

#### Interaction

| Tool | Parameters | Description |
|------|------------|-------------|
| `click_browser_pixel` | `x`, `y` | Click at pixel coordinates |
| `browser_press_key` | key name | Press a keyboard key (Enter, Tab, Escape, etc.) |
| `browser_scroll` | `direction`, `amount` | Scroll the page (up/down/left/right) |
| `browser_drag_pixel_to_pixel` | start/end coords | Drag from one point to another |

#### Window Control

| Tool | Parameters | Description |
|------|------------|-------------|
| `browser_resize_window` | `width`, `height` | Resize the browser viewport |

### Essential Patterns

#### Pattern 1: Observe → Act → Verify
1. **Observe**: `capture_browser_screenshot` + `browser_get_dom`
2. **Act**: `click_browser_pixel` / `browser_press_key` / `browser_scroll`
3. **Verify**: `capture_browser_screenshot` (confirm the action worked)

#### Pattern 2: Coordinate-Based Interaction
The browser uses **pixel coordinates** for clicking, not CSS selectors.
1. Use `browser_get_dom` to find the element
2. The DOM response includes position/coordinate information
3. Click at the element's coordinates using `click_browser_pixel`

#### Pattern 3: Reuse Subagent Context
For multi-step workflows on the same page:
1. First call: save the returned `SubagentId`
2. Subsequent calls: pass `ReusedSubagentId` to continue from the same browser state

#### Pattern 4: Screenshot Verification
After every subagent call:
1. Look for screenshot file paths in the response
2. Use `view_file` on the screenshot to verify what actually happened
3. **Never trust subagent claims without verification**

### Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `open_browser_url` failed | Browser issue | Ask user how to proceed |
| Element not found in DOM | Page not loaded / wrong page | Wait and retry, or navigate first |
| Click didn't work | Wrong coordinates | Re-read DOM, recalculate coordinates |
| Page blank after navigation | JavaScript-heavy SPA | Wait longer for rendering |

### Limitations

- Cannot handle native OS dialogs (file pickers, print dialogs)
- Cannot interact with browser chrome (address bar, settings)
- Cannot handle HTTP auth popups natively
- Maximum 3 media files can be passed as context
- RecordingName is limited to 3 words

---

<a id="中文"></a>

## 中文

> 共享参考文档。各 Skill 通过链接引用此处的详细工具说明。

### 调用约定

你**不能直接调用**浏览器工具。你需要通过 `browser_subagent` 间接调用，参数如下：

| 参数 | 必需 | 说明 |
|------|------|------|
| `TaskName` | ✅ | 可读标题，如 "Navigate to URL" |
| `Task` | ✅ | 给 subagent 的详细指令 |
| `TaskSummary` | ✅ | 1-2 句简要描述，用于 UI 显示 |
| `RecordingName` | ✅ | WebP 录制文件名（最多3个词，小写下划线） |
| `MediaPaths` | ❌ | 最多 3 个图片/视频路径作为上下文 |
| `ReusedSubagentId` | ❌ | 从之前的 subagent 上下文继续执行 |

### 可用浏览器工具（browser_subagent 内部）

#### 导航

| 工具 | 说明 |
|------|------|
| `open_browser_url` | 导航到指定 URL |

#### 观察

| 工具 | 返回值 | 说明 |
|------|--------|------|
| `capture_browser_screenshot` | PNG 文件路径 | 当前视口的视觉快照 |
| `browser_get_dom` | DOM 树（文本） | 完整 DOM 结构，含元素属性和坐标 |
| `read_browser_page` | Markdown 文本 | 页面内容转换为可读 Markdown |
| `browser_list_network_requests` | 请求列表 | 所有 HTTP 请求（方法、URL、状态码） |
| `capture_browser_console_logs` | 日志条目 | JavaScript 控制台输出（错误、警告、信息） |

#### 交互

| 工具 | 参数 | 说明 |
|------|------|------|
| `click_browser_pixel` | `x`, `y` | 在像素坐标处点击 |
| `browser_press_key` | 键名 | 按键盘键（Enter、Tab、Escape 等） |
| `browser_scroll` | `direction`, `amount` | 滚动页面（上/下/左/右） |
| `browser_drag_pixel_to_pixel` | 起/终坐标 | 从一个点拖拽到另一个点 |

#### 窗口控制

| 工具 | 参数 | 说明 |
|------|------|------|
| `browser_resize_window` | `width`, `height` | 调整浏览器视口大小 |

### 核心模式

#### 模式一：观察 → 行动 → 验证
1. **观察**：`capture_browser_screenshot` + `browser_get_dom`
2. **行动**：`click_browser_pixel` / `browser_press_key` / `browser_scroll`
3. **验证**：`capture_browser_screenshot`（确认操作成功）

#### 模式二：基于坐标的交互
浏览器使用**像素坐标**进行点击，而非 CSS 选择器。
1. 用 `browser_get_dom` 找到元素
2. DOM 响应中包含位置/坐标信息
3. 用 `click_browser_pixel` 在元素坐标处点击

#### 模式三：复用 Subagent 上下文
用于同一页面上的多步操作：
1. 第一次调用：保存返回的 `SubagentId`
2. 后续调用：传入 `ReusedSubagentId` 以继续同一浏览器状态

#### 模式四：截图验证
每次 subagent 调用后：
1. 在响应中查找截图文件路径
2. 用 `view_file` 查看截图验证实际结果
3. **永远不要不经验证就相信 subagent 的声明**

### 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `open_browser_url` 失败 | 浏览器问题 | 询问用户如何处理 |
| DOM 中找不到元素 | 页面未加载/错误页面 | 等待重试，或先导航 |
| 点击无效 | 坐标错误 | 重新读取 DOM，重新计算坐标 |
| 导航后页面空白 | JavaScript 重型 SPA | 等待更长时间让页面渲染 |

### 限制

- 无法处理原生系统对话框（文件选择器、打印对话框）
- 无法操作浏览器自身（地址栏、设置页面）
- 无法原生处理 HTTP 认证弹窗
- 最多传递 3 个媒体文件作为上下文
- RecordingName 限制最多 3 个词
