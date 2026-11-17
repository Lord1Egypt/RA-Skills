---
name: browser-mcp
description: 浏览器能力 MCP 化：@playwright/mcp 与 chrome-devtools-mcp 安装配置、持久 profile 登录态与工具清单
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/browser-mcp/SKILL.md
  url: https://github.com/microsoft/playwright-mcp
  version: 1.0.0
  updated: 2026-10-28
metadata:
  category: 浏览器自动化
  platform: Web
  difficulty: 进阶
---

# 浏览器 MCP 接入（browser-mcp）

> 把浏览器自动化包装成 MCP 工具，给任意 MCP Client / 平台型 Agent 常驻使用：主推 **@playwright/mcp**（微软官方，工具最全），调试向场景叠加 **chrome-devtools-mcp**（网络 / 性能 / 堆快照）。
> 方案选型（为什么选 MCP 而不是 CLI）见 [browser-ops](../browser-ops/SKILL.md)。

## 能力

- 两个官方级浏览器 MCP Server 的安装、多客户端配置与 HTTP 服务化
- 持久 profile / isolated / storage-state 三种会话策略与登录态保持
- 核心工具清单：导航、无障碍快照、点击、表单批量填写、文件上传、截图、JS 执行
- 双 Server 选型：操作自动化 → playwright-mcp；调试诊断 → chrome-devtools-mcp

## 使用方式

在 MCP 客户端（Claude Code / VS Code / Claude Desktop 等）配置：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

```bash
# Claude Code CLI 一行接入
claude mcp add playwright npx @playwright/mcp@latest

# 无显示环境 / 服务化共享：HTTP 模式
npx @playwright/mcp@latest --port 8931   # 客户端配 "url": "http://localhost:8931/mcp"
```

## 工作流（以 @playwright/mcp 为主）

1. **接入**：按上方配置挂载（需 Node 18+）
2. **选会话策略**：
   - 默认持久 profile（macOS 位于 `~/Library/Caches/ms-playwright/mcp-*`）——登录态保留，最接近真人
   - `--user-data-dir <dir>` 自定义 profile 目录；**同一 profile 同时只能一个实例**
   - `--isolated` 内存会话（关浏览器即丢）＋ `--storage-state <file>` 导入 cookie/localStorage
3. **核心工具链**：`browser_navigate` → `browser_snapshot`（无障碍快照，**优先于截图**，ref 定位准且省 token）→ `browser_click` / `browser_type` / `browser_fill_form`（批量表单）/ `browser_file_upload`（上传）→ `browser_take_screenshot` 验证
4. **常用 flags**：`--browser chrome|msedge|firefox|webkit`、`--headless`、`--caps=vision,pdf`、`--cdp-endpoint <ws>` 接管已开浏览器、`--extension` 走浏览器扩展、`--device` / `--mobile` 设备模拟
5. **调试叠加 chrome-devtools-mcp**：`npx chrome-devtools-mcp@latest`（1.12.0+）——`navigate_page` / `take_snapshot` / `evaluate_script` / `list_network_requests` / `performance_analyze_insight` / 堆快照对比。两个 Server 可在同一客户端并存。

## 适用场景

- 平台型 Agent / MCP Client 需要浏览器工具（客户端不便本地跑 Playwright CLI）
- 多任务复用同一登录态的常驻自动化（持久 profile）
- 服务化共享浏览器能力（HTTP 模式），多会话/多客户端接入

## 限制

- MCP 不豁免平台风控：滑块/验证码仍**人工兜底**，不提供反检测与绕过能力
- 同一持久 profile 单实例限制；并行需 `--isolated` 或多 `--user-data-dir`
- 工具列表占客户端上下文；客户端工具过多时按需裁剪 caps
- 不替代 CI 正式 E2E 用例（那是 `software-tester` 的 e2e-testing）
