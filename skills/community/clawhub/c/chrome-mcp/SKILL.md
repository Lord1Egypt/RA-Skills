---
name: chrome-mcp
description: |
  通过 Chrome DevTools MCP 控制本机 Chrome 浏览器（已登录的真实会话）。
  适用场景：
  - 浏览、阅读任意网页内容
  - 操作 X (Twitter)：浏览 feed、发推文、转帖、点赞、删帖
  - 操作任何需要登录的网站（保留已有登录状态）
  - 截图、读取页面结构、执行 JS
  - "帮我看看 X 上有什么新消息"
  - "帮我发一条推文"
  - "打开 xxx 网站帮我..."
metadata:
  openclaw:
    emoji: "🌐"
---

# Chrome MCP — 浏览器控制 Skill

通过 Chrome DevTools MCP 直接连接已运行的 Chrome，操控真实已登录的浏览器会话。

## 前提条件

Chrome 必须开启远程调试：打开 `chrome://inspect/#remote-debugging` 并启用开关。

## 工具优先级

优先使用 **Chrome DevTools MCP 工具**（`chrome__*`），效率最高：
- 无需截图即可读取页面结构（节省 ~90% token）
- 直接操作 DOM 元素，稳定可靠
- 连接已登录的 Chrome 会话

如果 MCP 工具不可用，回退到 `~/.claude/skills/chrome-cdp/scripts/cdp.mjs`。

## Chrome DevTools MCP 核心工具

```
chrome__navigate          导航到 URL，等待页面加载完成
chrome__screenshot        截图（仅在需要视觉确认时使用）
chrome__get_accessibility_tree  获取页面结构（首选，比截图高效 10x）
chrome__click             点击元素（CSS 选择器）
chrome__type              在当前焦点输入文字
chrome__evaluate          执行 JavaScript
chrome__wait_for_element  等待元素出现
```

## X (Twitter) 操作指南

### 浏览 Feed

```
1. chrome__navigate → https://x.com/home
2. chrome__get_accessibility_tree → 读取推文列表
3. 如需滚动加载更多：chrome__evaluate → window.scrollBy(0, 800)
4. 重复步骤 2-3 直到获取足够内容
```

### 发推文

```
1. chrome__navigate → https://x.com/home
2. chrome__click → [data-testid="tweetTextarea_0"]
3. chrome__type → 推文内容
4. chrome__click → [data-testid="tweetButtonInline"]
```

### 删除推文/取消转帖

删除自己的推文：
```
1. 定位到推文，chrome__click → [data-testid="caret"]（三点菜单）
2. chrome__wait_for_element → [role="menuitem"]
3. chrome__click → 第一个 menuitem（"删除"）
4. chrome__click → [role="alertdialog"] [role="button"]（确认）
```

取消转帖：
```
1. chrome__click → [data-testid="unretweet"]
2. chrome__click → [data-testid="unretweetConfirm"]
```

### 转帖 / 点赞

```
转帖: chrome__click → [data-testid="retweet"] 然后 [data-testid="retweetConfirm"]
点赞: chrome__click → [data-testid="like"]
```

## 通用操作技巧

- **优先用 `get_accessibility_tree` 而非截图**：结构清晰，消耗 token 极少
- **等待加载**：操作后如需等待，用 `wait_for_element` 而非 `sleep`
- **长页面**：通过 `evaluate` 执行 `window.scrollBy` 加载更多内容
- **跨域 iframe 输入**：用 `type` 而非 `evaluate`（JS eval 在跨域 iframe 中无法访问）
