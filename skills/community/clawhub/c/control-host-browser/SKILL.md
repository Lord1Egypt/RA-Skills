---
name: control-host-browser
description: >
  Control the host machine's Chrome browser to open specific URLs in new tabs.
  Use when: User explicitly asks to "open a link", "show me this page", or "search for X in browser" on the host machine.
  NOT for: Internal agent browsing tasks or headless scraping.
version: 1.0.0
---

# Host Browser Controller

## 功能定义
此技能用于控制宿主机（用户物理机）上的 Chrome 浏览器。它通过 Chrome DevTools Protocol (CDP) 创建新标签页并导航至指定 URL，让用户能在本地屏幕上查看网页内容。

## 触发场景
- 用户说：“在浏览器里打开这个链接”。
- 用户说：“帮我搜索一下‘AI 发展趋势’”。
- 用户希望查看某个文档或网页的可视化效果。

## 执行步骤 (SOP)
1. **参数准备**：
   - 确认目标 URL。如果是搜索请求，先构造 Google/Bing 搜索链接。
   - 确认 Profile 名称（默认为 `main`，对应宿主机上的特定用户配置）。
2. **创建标签页**：
   - 调用 `control_host_browser.sh` 脚本。
   - 传入 `profile` 参数（通常为 `main`）。
   - 脚本会通过 CDP 接口在宿主机 Chrome 中创建一个新 Tab，并返回 `targetId`。
3. **导航页面**：
   - 使用返回的 `targetId`，通过 CDP WebSocket 发送 `Page.navigate` 指令。
   - 传入目标 URL。
4. **确认状态**：
   - 等待页面加载事件（`Page.loadEventFired`）。
   - 向用户反馈：“已在您的浏览器中打开 [标题/URL]”。

## 参数说明
- **profile**: 浏览器配置文件标识。
  - `main`: 主配置文件（默认）。
- **url**: 需要打开的完整 URL（包含 `https://`）。

## 输出格式
- 成功：返回 "Tab created with ID: [ID], navigating to [URL]"。
- 失败：返回具体的 CDP 错误信息（如 "Connection refused", "Invalid URL"）。

## 限制说明
- 仅支持 HTTP/HTTPS 协议。
- 依赖于宿主机 Chrome 浏览器已开启远程调试端口（默认 18800）。
- 无法直接操作页面内的 DOM（如点击按钮），仅负责打开页面。

Usage:
```bash
./control_host_browser.sh <profile> <url>
```
Where profile is main
