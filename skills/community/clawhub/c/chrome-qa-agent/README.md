# Chrome QA Agent — 对抗式 UI 测试 Skill

能捕捉 Playwright 抓不到的问题的对抗式测试。它会分析 git diff，只测发生变化的部分，或者探索整个应用来发现 bug。通过 **chrome-devtools MCP** 在真实的本地 Chrome 中运行。

## 安装

需要配置并连接 **chrome-devtools MCP 服务器**（它会驱动一个真实的本地 Chrome）。无需任何额外安装。

当 `mcp__chrome-devtools__*` 工具可用时即说明配置成功（可以试试 `mcp__chrome-devtools__list_pages`）。如果不可用，请添加或启用 `chrome-devtools` MCP 服务器后重试。为避免每次调用工具都要确认，可以在 `settings.json` 的 `permissions.allow` 中放行它们：

```json
{
  "permissions": {
    "allow": [
      "mcp__chrome-devtools"
    ]
  }
}
```

## 快速上手

```
"Test the UI changes in my PR"         → diff 驱动 (工作流 A)
"Explore my app and find bugs"         → 探索式 (工作流 B)
"QA the staging site, group by group"  → 分组顺序测试 (工作流 C)
```

## 工作原理

1. **分析 diff**（或探索应用）来决定测什么
2. **打开真实的本地 Chrome** —— 同一个浏览器既能测 localhost 也能测已部署的 URL，只需改变 URL。使用隔离上下文可获得干净的、未登录状态的运行环境。
3. **尝试搞破坏** —— 对抗式输入、快速点击、纯键盘操作、空状态、XSS
4. **运行确定性检查** —— axe-core、控制台错误、损坏的图片、表单标签
5. **报告结构化结果** —— `STEP_PASS|id|evidence` 或 `STEP_FAIL|id|expected → actual`
6. **生成 HTML 报告** —— 内嵌截图的独立文件，可分享给评审者

## 测试内容

| 类别 | 方式 | Playwright 漏掉的 |
|----------|-----|----------------------|
| 无障碍 | axe-core + 键盘导航 | WCAG 违规、焦点框、屏幕阅读器语义 |
| 视觉质量 | 截图 + Claude 判断 | 布局平衡、排版、间距、空状态 |
| 响应式 | 视口扫描 (375px, 768px, 1440px) | 移动端溢出、触控目标、内容重排 |
| 控制台健康 | 注入 `evaluate_script` | 水合错误、失败的请求、运行时异常 |
| 错误状态 | 导航到空状态/错误状态 | 缺失的空状态、损坏的错误恢复 |
| 对抗式 | XSS、空提交、快速点击、超长输入 | 开发者不会专门写测试的边界情况 |
| 探索式 | 自由导航、尝试搞破坏 | 你想不到要测的 bug |

## 浏览器执行

只有一个本地 Chrome。同一套工具既测 localhost 也测已部署的站点 —— 改变的只有 URL。

- **打开页面** → `mcp__chrome-devtools__navigate_page { type: "url", url }`
- **干净的、未登录的标签页** → `mcp__chrome-devtools__new_page { url, isolatedContext: "ui-test" }`
- **对无障碍树（a11y）做快照** → `mcp__chrome-devtools__take_snapshot`（返回基于 uid 的元素）
- **交互** → `mcp__chrome-devtools__click { uid }`、`mcp__chrome-devtools__fill { uid, value }`、`mcp__chrome-devtools__evaluate_script { function }`
- **截图** → `mcp__chrome-devtools__take_screenshot { filePath: X }`
- **关闭标签页** → `mcp__chrome-devtools__close_page`

**Localhost 与已部署：** 将 URL 指向 `http://localhost:3000` 用于本地开发，或指向 `https://your-app.com` 用于已部署站点 —— 工具用法完全一致。**已部署站点上的鉴权会复用真实 Chrome 配置中已登录的会话** —— 如果你在 Chrome 里已登录，测试也是登录态。要获得可复现的、未登录状态的运行，请在隔离上下文中打开页面（`new_page { isolatedContext: "ui-test" }`）。

**顺序执行，而非并行：** 只有一个共享浏览器，并且 `select_page` 会为整个连接全局设置活动页面。大型任务会被拆分成多个分组以实现上下文隔离，但这些分组是**前后接连**运行的（同一时刻只有一个 agent 占用浏览器），并非并发。

## 项目结构

```
chrome-qa-agent/
├── SKILL.md                              # Skill 定义 —— 工作流、断言协议、预算
├── EXAMPLES.md                           # 9 个带精确命令的实战示例
├── README.md
└── references/
    ├── adversarial-patterns.md           # 对抗式测试模式（表单、模态框、导航、键盘）
    ├── browser-recipes.md                # 可复制粘贴的 chrome-devtools MCP 确定性检查配方
    ├── design-consistency.md             # 设计一致性检查方法论
    ├── design-system.example.md          # 设计系统模板示例（复制为 design-system.md）
    ├── exploratory-testing.md            # agent 驱动的探索式 QA 指南
    ├── parallel-testing.md              # 单一共享浏览器上的分组顺序测试
    ├── report-template.html              # 内嵌截图的 HTML 报告模板
    └── ux-heuristics.md                  # 6 套评估框架（Laws of UX、Nielsen 等）
```

## 理念

传统测试验证的是**意图**。这个 skill 发现的是**盲点**。

没有 YAML 文件，没有生成的测试套件，没有产物。Agent 读取 diff（或探索应用），打开浏览器，尝试搞破坏，然后报告它发现的东西。就像一个对每一条设计原则都了如指掌的人类 QA 测试员。

## 环境要求

- 配置并连接 **chrome-devtools MCP 服务器**（驱动真实的本地 Chrome）—— 通过 `mcp__chrome-devtools__*` 工具确认是否可用。
- 一个正在运行的 Web 应用（localhost 或已部署的 URL）
