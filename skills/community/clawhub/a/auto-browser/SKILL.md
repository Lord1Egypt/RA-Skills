---
name: auto-browser
description: 通过 Chrome Debug 模式（CDP）自动化操作真实浏览器——导航、点击、填表、提取数据、截图、执行多步流程。当用户说"帮我在网页上操作"、"打开浏览器"、"帮我点"、"帮我填"、"帮我抓取"、"帮我截图"、"auto-browser"时使用。
---

# auto-browser

你的浏览器遥控器。导航、点击、填表、抓数据、截图——说一句话就行。

## 使用方式

```
/auto-browser 打开 GitHub 看看我的 notifications
/auto-browser 去 Amazon 搜索 mechanical keyboard 截图前三个结果
/auto-browser 登录后台，把订单列表导出来
/auto-browser 帮我在这个页面点「下一步」然后填写地址表单
```

自然语言描述意图即可，不需要写代码。

## 必须使用 playwright-cdp 工具集

所有浏览器操作使用 **`user-playwright-cdp`** 的工具（连接真实 Chrome，保留登录态）。

- ✅ 用：`user-playwright-cdp` 的 `browser_navigate`、`browser_snapshot`、`browser_click` 等
- ❌ 禁止：`cursor-ide-browser` 的同名工具（沙盒浏览器，无登录态）

---

## 核心工作流

### 0. 确保 Chrome Debug 在线

```bash
curl -s http://127.0.0.1:9222/json/version
```

- ✅ 有响应 → 继续
- ❌ 无响应 → 直接启动，不问用户：

```bash
nohup /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome_debug_profile" \
  > /tmp/chrome_debug.log 2>&1 &
```

等 2 秒后重新 curl 确认。

### 1. 感知：snapshot 先行

**每次操作前**都先 `browser_snapshot`，获取页面无障碍树。这是你的「眼睛」。

- 用 snapshot 中的 `ref` 来定位元素
- 不确定页面状态时，先 snapshot 再决定下一步

### 2. 行动：选择合适的操作

根据用户意图选择操作，可自由组合：

| 意图 | 工具 | 说明 |
|------|------|------|
| 打开网页 | `browser_navigate` | 推断 URL，直接导航 |
| 后退 | `browser_navigate_back` | |
| 点击按钮/链接 | `browser_click` | 用 snapshot 的 ref |
| 填写输入框 | `browser_type`（追加）/ `browser_fill_form`（清空后填） | |
| 选择下拉框 | `browser_select_option` | |
| 上传文件 | `browser_file_upload` | 需绝对路径 |
| 按键 | `browser_press_key` | Enter、Escape、Tab 等 |
| 悬停 | `browser_hover` | 展开菜单、tooltip |
| 拖拽 | `browser_drag` | startRef → endRef |
| 处理弹窗 | `browser_handle_dialog` | alert/confirm/prompt |
| 等待加载 | `browser_wait_for` | 等时间或等文本出现/消失 |
| 执行 JS | `browser_evaluate` | 页面没有暴露 UI 时的后备手段 |
| 管理标签页 | `browser_tabs` | list/new/close/select |
| 调整窗口 | `browser_resize` | 测试响应式布局 |

### 3. 确认：截图反馈

操作完成后 `browser_take_screenshot` 截图给用户确认结果。

---

## 操作原则

### URL 推断

根据用户描述直接推断 URL 并导航，不要反问：

- 「打开 Google」→ `https://www.google.com`
- 「去 GitHub」→ `https://github.com`
- 「看看 V2EX」→ `https://www.v2ex.com`
- 模糊描述 → 用常识判断，导航后截图确认

只有完全无法推断时才问。

### 多步操作

复杂任务拆成步骤，每步遵循：**snapshot → 操作 → 等待 → snapshot 确认**。

```
示例：「登录后台导出订单」
1. navigate 到登录页 → snapshot
2. 如果已登录跳过，否则填写账号密码 → click 登录
3. wait_for 页面加载 → snapshot
4. click 导航到订单页 → snapshot
5. click 导出按钮 → 截图确认
```

### 等待策略

页面变化后（导航、点击、提交），用短间隔等待 + snapshot 确认：

```
browser_wait_for time=2 → snapshot → 检查是否就绪
→ 没好？再 wait_for time=2 → snapshot
```

不要一次等太久。2-3 秒一轮，最多重试 3 次。

### 数据提取

需要从页面抓取数据时：

1. `browser_snapshot` 获取页面结构
2. 从无障碍树中提取所需信息
3. 信息不够时用 `browser_evaluate` 执行 JS 提取
4. 结果太长写入文件，回复给摘要 + 路径

### 表单填写

填表场景遵循 auto-fill 的规则：

- 语义匹配字段，不要求精确
- 不确定的字段列出来问用户
- 密码类字段填前确认
- 多字段优先用 `browser_fill_form` 批量填写
- 填完截图确认

---

## 安全边界

| 操作 | Agent 直接做 | 需用户确认 |
|------|-------------|-----------|
| 导航、浏览、截图 | ✅ | |
| 点击普通按钮/链接 | ✅ | |
| 填写非敏感字段 | ✅ | |
| 读取/提取页面数据 | ✅ | |
| 填写密码 | | ✅ |
| 点击「提交」「付款」「删除」 | | ✅（除非用户明确说"帮我提交"） |
| 发送消息/邮件 | | ✅ |
| 关闭标签页 | | ✅（除非用户要求） |

**原则：只读操作自由做，写入/不可逆操作先确认。**

---

## 错误处理

| 问题 | 处理 |
|------|------|
| 元素找不到 | 重新 snapshot，ref 可能变了 |
| 页面加载慢 | `browser_wait_for` 等待，不要盲目重试 |
| 弹窗阻断 | `browser_handle_dialog` 处理 |
| 需要登录 | 告诉用户，等用户手动登录后继续 |
| 验证码/人机验证 | 截图告知用户，等用户处理 |
| JS 报错 | `browser_console_messages` 查看错误日志 |

---

## 环境配置（首次）

如果 `~/.cursor/mcp.json` 里没有 `playwright-cdp` 配置，添加：

```json
"playwright-cdp": {
  "command": "npx",
  "args": ["-y", "@playwright/mcp@latest", "--cdp-endpoint", "http://127.0.0.1:9222"]
}
```

添加后提示用户重载 MCP（Cursor 设置 → MCP → Reload）。
