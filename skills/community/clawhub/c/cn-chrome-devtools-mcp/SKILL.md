---
name: chrome-devtools-mcp
description: Chrome DevTools MCP 服务器，让 AI 编码助手（Claude Code、Cursor、Copilot）直接控制和调试真实 Chrome 浏览器，实现截图、性能分析、网络请求检查、控制台调试和自动化操作
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npx
    emoji: 🔧
    homepage: https://github.com/ChromeDevTools/chrome-devtools-mcp
---

# chrome-devtools-mcp — AI 浏览器调试与自动化 MCP 工具

chrome-devtools-mcp 是 Google Chrome DevTools 团队官方出品的 MCP 服务器，通过 Model Context Protocol 让 AI 编码助手获得完整的 Chrome DevTools 能力。它使用 Puppeteer 实现可靠的浏览器自动化，内置等待机制确保操作结果正确。支持 Claude Code、Cursor、VS Code Copilot、Codex 等主流 AI 工具，是 AI 驱动前端调试和 Web 自动化的首选方案。

## 核心使用场景

- **前端 Bug 调试**：AI 直接打开页面、查看控制台报错（含源码映射的堆栈追踪）、检查网络请求
- **性能分析**：录制页面性能 Trace、提取可操作的优化建议，结合真实用户数据（CrUX）
- **截图与视觉验证**：AI 截图当前页面状态，辅助 UI 回归测试和 Bug 复现
- **Web 自动化测试**：AI 填写表单、点击按钮、导航页面，可靠等待操作完成
- **接入已有 Chrome 实例**：连接 DevTools 远程调试端口，调试任意 Chrome 标签页

## AI 辅助使用流程

1. **安装配置** — AI 在 Claude Code 中执行一行命令完成 MCP 服务器安装
2. **连接浏览器** — 服务器自动启动 Chrome，或连接指定的 DevTools 远程端口
3. **导航目标页面** — AI 通过 MCP 工具导航到待调试的 URL
4. **执行调试操作** — AI 截图、检查控制台、分析网络请求、录制性能 Trace
5. **自动化交互** — AI 自动化点击/填写/滚动等用户操作
6. **分析结果** — AI 基于 DevTools 数据给出优化建议或 Bug 定位

## 关键章节导航

- [安装指南](guides/01-installation.md) — Claude Code / VS Code / Cursor 多种安装方式
- [快速开始](guides/02-quickstart.md) — 调试工作流、截图、性能分析、网络检查
- [高级用法](guides/03-advanced-usage.md) — 连接已有浏览器、Slim 模式、隐私配置
- [故障排查](troubleshooting.md) — 浏览器连接失败、超时、权限问题

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 通过 `claude mcp add` 或 `/plugin install` 完成 MCP 服务器安装
- ✅ 导航到任意 URL 并等待页面加载完成
- ✅ 截图当前页面状态（支持全页面 / 视口截图）
- ✅ 读取浏览器控制台消息（含源码映射的完整堆栈追踪）
- ✅ 检查网络请求（URL / 状态码 / 响应头 / 响应体）
- ✅ 录制性能 Trace 并提取关键性能指标
- ✅ 执行点击、填写表单、键盘输入等自动化操作
- ✅ 执行任意 JavaScript 代码并获取返回值

## 核心功能

- ✅ **截图** — 全页面或视口截图，辅助视觉 Bug 复现
- ✅ **控制台检查** — 读取 log/warn/error 消息，含源码映射堆栈
- ✅ **网络分析** — 拦截和检查所有 HTTP/HTTPS 请求
- ✅ **性能分析** — 录制 DevTools Trace，结合 CrUX 真实用户数据
- ✅ **浏览器自动化** — 基于 Puppeteer 的可靠点击/填写/导航
- ✅ **JavaScript 执行** — 在页面上下文中执行任意 JS
- ✅ **Slim 模式** — 精简工具集，适合基础浏览任务
- ✅ **无头模式** — `--headless` 支持 CI 环境
- ✅ **远程连接** — 连接已有 Chrome DevTools 远程调试端口
- ✅ **多 AI 工具** — Claude Code / Cursor / VS Code / Copilot / Codex

## 快速安装示例

```bash
# Claude Code CLI 安装（推荐）
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest

# Claude Code 插件安装（含 Skills）
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
/plugin install chrome-devtools-mcp

# VS Code CLI 安装
code --add-mcp '{"name":"chrome-devtools","command":"npx","args":["-y","chrome-devtools-mcp"]}'
```

**MCP 配置（手动添加到 settings.json）：**
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## 安装要求

| 依赖 | 版本要求 |
|------|---------|
| Node.js | >= 20.19（最新 LTS 维护版） |
| Chrome | 当前稳定版或更新 |
| npm | 任意版本 |

## 项目链接

- GitHub：https://github.com/ChromeDevTools/chrome-devtools-mcp
- 工具参考：https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
- Slim 工具参考：https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md
- 故障排查：https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md
