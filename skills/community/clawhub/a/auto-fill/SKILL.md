---
name: auto-fill
description: 通过 Chrome Debug 模式（CDP）读取当前页面的表单结构并自动填写。由用户显式调用（/auto-fill），不自动触发。用户负责导航和点击，Agent 负责识别字段、填写内容、截图确认。
---

# auto-fill

帮你填表。你来点击导航，我来识别字段和填写内容。

## 使用方式

```
/auto-fill 公司名: ACME, 邮箱: foo@bar.com, 备注: 测试订单
```

数据格式自由，键值对 / 自然语言描述都行，我来匹配字段。

## 重要：必须使用 playwright-cdp 工具集

所有浏览器操作必须使用 **`playwright-cdp` 的工具**（连接真实 Chrome），不要使用 `cursor-ide-browser` 的内置浏览器工具。

- ✅ 用：`playwright-cdp` 提供的 `browser_navigate`、`browser_snapshot`、`browser_fill` 等
- ❌ 禁止：`cursor-ide-browser` 的同名工具（沙盒浏览器，没有登录态）

---

## 工作流程

### 第一步：检查 Chrome debug 是否在线

```bash
curl -s http://127.0.0.1:9222/json/version
```

- ✅ 有响应 → 继续
- ❌ 无响应 → **直接用 Shell 启动 Chrome**，不要让用户手动跑命令

**直接执行（后台启动）：**
```bash
nohup /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome_debug_profile" \
  > /tmp/chrome_debug.log 2>&1 &
```

等 2 秒后重新 curl 确认启动成功，再继续。

### 第二步：导航到目标页面

根据用户的描述推断目标 URL，**直接 `browser_navigate` 过去，不要问用户要链接**。

- 「打开 Google」→ `https://www.google.com`
- 「去 Wise 注册」→ `https://wise.com/register`
- 「打开 Creem」→ `https://creem.io`
- 模糊描述 → 用常识判断最合理的 URL，导航后截图确认

只有完全无法推断时，才问用户要链接。

### 第三步：读取页面结构

```
browser_snapshot
```

获取无障碍树，识别所有可填写字段（input、textarea、select 等）。

### 第四步：匹配字段

把用户提供的数据与页面字段对应：

- 字段名/placeholder/label → 语义匹配，不要求精确
- **不确定的字段：列出来问用户，不要乱填**
- 没有对应数据的字段：跳过，保持原值

### 第五步：填写

使用 `browser_fill` 逐字段填入。

**规则：**
- 密码类字段：填前确认
- 下拉框（select）：用 `browser_select_option`
- 文件上传：用 `browser_upload_file`，需用户确认路径

### 第六步：截图确认

```
browser_take_screenshot
```

展示填写结果，明确告知：**「填完了，请你来点提交」**。

---

## 边界规则

| 操作 | Agent 做 | 用户做 |
|------|---------|--------|
| 识别表单字段 | ✅ | |
| 填写内容 | ✅ | |
| 截图确认 | ✅ | |
| 点击导航 / 翻页 | | ✅ |
| 点击提交按钮 | 除非明确说「帮我提交」 | ✅ 默认 |
| 处理弹窗 / 验证码 | | ✅ |

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
