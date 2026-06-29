# brower-opener + webapp-testing + opencode 集成指南

## 概述

本技能包（brower-opener）负责**启动带远程调试端口的 Chrome 浏览器并复用 cookie**，配合 `webapp-testing` 技能编写 Playwright 测试脚本，在 opencode 环境下实现完整的自动化测试工作流。

## 三个组件的关系

```
brower-opener (本技能)
  └─ 启动 Chrome (端口 9222, 复用主 profile cookie)
      └─ webapp-testing (AI 技能)
          └─ 指导 AI 编写 connect_over_cdp 脚本
              └─ opencode (运行环境)
                  └─ 自动加载 AGENTS.md 中的测试规则
```

| 组件 | 职责 | 来源 |
|------|------|------|
| **brower-opener** | 启动 Chrome，复用 cookie，开放 9222 端口 | 本项目 `.opencode/skills/web-testing-cookie/` |
| **webapp-testing** | 指导 AI 写 Playwright 测试脚本的模式和最佳实践 | 全局 skill (`~/.agents/skills/webapp-testing/`) |
| **opencode** | 运行环境，自动加载 AGENTS.md 规则 | CLI 工具 |

## 配合使用流程

### 1. 启动浏览器（brower-opener）

```bash
cd .opencode/skills/web-testing-cookie && python scripts/launcher.py --mode reuse
```

- `--mode reuse`：复用主 profile cookie（默认）
- `--mode independent`：无痕模式，不保留会话

启动后 Chrome 会在 `http://127.0.0.1:9222` 开放远程调试端口。

### 2. 验证状态（可选）

```bash
cd .opencode/skills/web-testing-cookie && python scripts/health.py
```

### 3. 编写测试脚本（webapp-testing）

要求 AI 按以下模式编写 Playwright 脚本：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 连接 brower-opener 已启动的浏览器
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]   # 复用 cookie
    page = context.new_page()       # 新标签页

    # 监控控制台
    page.on("console", lambda msg: print(msg) if msg.type == "error" else None)

    # 监控 API
    page.on("response", lambda res: ... if "/api/proxy/" in res.url else None)

    page.goto("http://localhost:3000/web/lbx-amt/xxx", wait_until="networkidle")
    # ... 测试逻辑
```

### 4. 关键约定

| 规则 | 说明 |
|------|------|
| **禁止** `chromium.launch()` | 不得自行启动浏览器，必须连接已有实例 |
| **必须** `contexts[0]` | 使用第一个已有上下文以复用 cookie |
| **必须** `connect_over_cdp` | 通过 CDP 协议连接 9222 端口 |
| **必须** `networkidle` | 等待页面完全加载后再操作 |

## opencode 集成

### AGENTS.md 配置

在项目根目录的 `AGENTS.md` 中配置以下规则，opencode 每次对话时自动加载：

```markdown
## 自动化测试规范

### 测试脚本生成时机

每次**新建或修改页面文件**（`pages/` 下任何 `.vue` 文件）时，AI **必须同步生成**对应的 Playwright 测试脚本，与业务代码一同提交。

### 浏览器复用规范

1. 测试脚本**禁止**使用 `chromium.launch()`
2. 必须通过 `connect_over_cdp("http://localhost:9222")` 连接已启动的 Chrome
3. 必须使用 `browser.contexts[0]` 复用 cookie
4. 浏览器启动由 `brower-opener` 负责

### 测试脚本规范

| 要求 | 说明 |
|------|------|
| 存放路径 | `tests/e2e/{页面路径对应目录}/{页面名}_test.py` |
| 命名规则 | 页面名 + `_test.py` 后缀 |
| 必须覆盖 | API 接口监控、控制台错误检测、关键交互操作 |
| 报告 | `tests/reports/{页面名}_report.md`（Markdown 格式） |

### 测试执行流程

AI 收到"测试 xxx 页面"指令时：
1. 若 Chrome 未在 9222 端口运行 → 执行 brower-opener 启动（复用 cookie）
2. 运行 `tests/e2e/` 下对应的测试脚本
3. 输出 Markdown 报告到 `tests/reports/`
4. 若测试失败，分析原因并给出修复建议
```

### 提示词模板

让 AI 执行测试时，你可以直接说：

> **"先复用 cookie 启动浏览器，然后用 Playwright 测试 [xxx 页面]，覆盖 API 监控、控制台错误检测和关键交互，输出 Markdown 报告"**

AI 会自动执行：
1. 调用 `brower-opener` 启动 Chrome（若未启动）
2. 读取或生成 `tests/e2e/` 下的测试脚本
3. 运行脚本并输出 `tests/reports/` 下的 Markdown 报告

## 目录结构约定

```
项目根目录/
├── .opencode/
│   └── skills/
│       └── web-testing-cookie/    ← 本技能（brower-opener）
│           ├── README.md           ← 本文件
│           ├── SKILL.md
│           └── scripts/
│               ├── launcher.py
│               └── health.py
├── tests/
│   ├── e2e/                       ← 测试脚本（目录结构与 pages/ 一一对应）
│   │   └── goods-plan/
│   │       └── transference/
│   │           ├── simulation_test.py
│   │           └── warzone_test.py
│   └── reports/                   ← 测试报告（Markdown 格式，不提交）
│       ├── simulation_report.md
│       └── warzone_report.md
└── AGENTS.md                      ← opencode 配置文件（加载测试规则）
```

## 常见问题

### Q: 浏览器启动后页面空白？
运行 `python scripts/health.py` 检查 9222 端口是否正常响应。

### Q: cookie 没有复用？
确认使用的是 `--mode reuse` 模式，且脚本中用的是 `browser.contexts[0]` 而非 `browser.new_context()`。

### Q: 脚本中该用哪些等待策略？
- 导航后：`wait_until="networkidle"`
- 动态内容：`wait_for_selector()` 或 `wait_for_timeout(2000)`
- Element Plus 弹窗：`wait_for_timeout(500)` 等待动画

### Q: webapp-testing 的 launch_chrome_debug.py 还要用吗？
**不用**。brower-opener 已负责启动浏览器，webapp-testing 只需用它提供的脚本模式和最佳实践来编写测试代码即可。
