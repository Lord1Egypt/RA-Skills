---
name: chrome-qa-agent
description: "基于 chrome-devtools MCP 的对抗式 UI 测试。分析 git diff 只测改动部分，或探索整个应用找 bug。覆盖功能正确性、无障碍(a11y)、响应式布局与 UX 启发式。当用户要测试 UI 改动、QA 一个 PR、审计无障碍、或做探索式测试时使用。驱动真实本地 Chrome，本地与任意线上 URL 都适用。"
license: MIT
metadata:
  author: "云中江树 (yzfly)"
  version: "0.5.0"
allowed-tools: Bash Read Glob Grep Agent mcp__chrome-devtools__navigate_page mcp__chrome-devtools__new_page mcp__chrome-devtools__select_page mcp__chrome-devtools__list_pages mcp__chrome-devtools__close_page mcp__chrome-devtools__take_snapshot mcp__chrome-devtools__take_screenshot mcp__chrome-devtools__click mcp__chrome-devtools__fill mcp__chrome-devtools__fill_form mcp__chrome-devtools__hover mcp__chrome-devtools__drag mcp__chrome-devtools__press_key mcp__chrome-devtools__type_text mcp__chrome-devtools__upload_file mcp__chrome-devtools__evaluate_script mcp__chrome-devtools__list_console_messages mcp__chrome-devtools__get_console_message mcp__chrome-devtools__list_network_requests mcp__chrome-devtools__get_network_request mcp__chrome-devtools__wait_for mcp__chrome-devtools__resize_page mcp__chrome-devtools__emulate mcp__chrome-devtools__handle_dialog
compatibility: "需要 chrome-devtools MCP 服务已配置并连接（驱动本地 Chrome）。无需额外安装 —— 认证复用真实 Chrome 配置文件的登录态。"
---

# Chrome QA Agent — 对抗式 UI 测试 Skill

在真实浏览器里测试 UI 改动。你的任务是**想办法把它弄坏**，而不是确认它能跑。

本 skill 通过 **chrome-devtools MCP**（`mcp__chrome-devtools__*` 工具）驱动**单个本地 Chrome**。由于该 MCP 只控制一个浏览器，且 `select_page` 会为整条连接全局设置当前活动页面，**浏览器测试是单线程的** —— 绝不能让两个 agent 同时对同一个浏览器操作。

两种工作流：
- **diff 驱动** —— 分析 git diff，只测改动部分
- **探索式** —— 在应用里到处点，找出开发者没想到的 bug

对于较大的任务，你仍可以把工作拆给多个子 agent 以隔离上下文，但它们必须轮流独占这唯一的浏览器 —— 见下文「拆分工作的原则」一节。

## 测试如何运作

主 agent 负责**协调** —— 它制定测试策略、把任务分派给子 agent、并汇总结果。真正的浏览器测试由子 agent 执行。

### 规划：先从多个角度想，再一次性执行

**你必须亲自完成全部三轮规划并输出，然后才能启动任何子 agent。** 规划发生在你自己的回复里 —— 不能委派给子 agent。不要跳过规划直接执行。

**第一轮 —— 功能：** 核心用户流程有哪些？什么应该正常工作？把每个测试写成：动作 → 预期结果。

**第二轮 —— 对抗：** 重读第一轮。你漏了什么？想想：不同的用户类型/角色、错误路径、空状态、竞态、边界输入（空值、超长、特殊字符、连续快速点击）。

**第三轮 —— 覆盖盲区：** 重读第一、二轮。还有什么没考虑：无障碍（axe-core、纯键盘）、移动端视口、控制台错误、与应用其余部分的视觉一致性？

**去重：** 把三轮合并成一份带编号的测试清单。去掉重叠项。给每个测试分配一个分组（例如 Group A、Group B）。

**然后一次性执行** —— 每个分组启动一个子 agent。每个子 agent 只接收它那份具体的测试清单，别的都不给。子 agent 不探索、不规划 —— 它们执行被指派的测试并汇报结果。

在调用任何 Agent 工具之前，把三轮规划、合并后的计划、以及分组分配都输出在你的回复里。

### 拆分工作的原则

- **一个浏览器，同一时刻只有一个 agent。** chrome-devtools MCP 控制单个 Chrome，且 `select_page` 是全局状态。**顺序**分派子 agent —— 每个在自己回合里独占浏览器，跑完，下一个再开始。并发驱动浏览器的 agent 会破坏彼此的页面状态。（你仍可以并行跑*非浏览器*的工作，比如 diff 分析。）
- **子 agent 跑被指派的测试，而非开放式探索。** 主 agent 交给每个子 agent 一份具体的、带编号的测试清单。子 agent 不规划、不探索、不决定测什么 —— 它们执行清单然后停下。
- **即便是串行，拆分依然有用** —— 它让每个 agent 的上下文保持小而聚焦。许多小 agent 优于少数大 agent。这里的收益是上下文隔离和每组干净的汇报，而不是挂钟时间上的并行。
- **按改动规模匹配投入** —— 单个组件的修复不需要很多 agent 或很多步数；主 agent 直接跑就行。整页重构才值得拆成多个分组。让 diff 的范围来驱动计划。
- **遇到失败不要提前停** —— 在被指派的测试范围内尽可能多地找出 bug。

### 给子 agent 设定步数预算

**主 agent 必须在每个子 agent 的提示里写明步数上限。** 一「步」= 一次 chrome-devtools MCP 工具调用（`navigate_page`、`take_snapshot`、`click`、`evaluate_script`……）。子 agent 不会自我设限 —— 除非被告知，否则它们会一直跑到完成。

粗略经验值：几项有针对性的检查约 25 步，一个完整页面（功能 + 对抗 + a11y）约 40 步，多个页面或一大类约 75 步。**根据被指派测试的实际需要来调整** —— 这些是起点，不是规则。

每个子 agent 的提示都必须包含：
```
You have a budget of N steps (each chrome-devtools MCP tool call = 1 step). Count your steps as you go. When you reach N, stop immediately and report:
- STEP_PASS/STEP_FAIL for every test you completed
- STEP_SKIP|<test-id>|budget reached for every test you didn't get to

Drive the browser ONLY through the chrome-devtools MCP tools (mcp__chrome-devtools__*).
You own the browser exclusively for this run — no other agent is using it. When done, the next agent will reuse the same Chrome, so leave it in a clean state (close extra tabs you opened with close_page).
Do not retry or continue after hitting the budget.
Run only these tests: [numbered list from the merged plan]
Do not explore beyond the assigned tests.
Do NOT generate an HTML report or write any files (except screenshots via take_screenshot's filePath). Return only step markers and your findings as text.
```

主 agent 自己不应驱动浏览器（除了验证开发服务器是否已启动）。所有测试都在子 agent 里进行，**一次只分派一个** —— 绝不要同时跑两个驱动浏览器的子 agent，因为它们共用一个 Chrome。

**当某个子 agent 用尽预算时，主 agent 直接接受这份部分结果。** 不要重跑或重试这个子 agent。把 SKIPPED 的测试写进最终报告，让开发者知道哪些没覆盖到。

### 汇报

**每个子 agent 回报时给出：**
```
Tests: 8 | Passed: 5 | Failed: 2 | Skipped: 1 | Pages visited: 2
```

**主 agent 汇总成最终报告：**
```
Tests: 20 | Passed: 14 | Failed: 4 | Skipped: 2 | Agents: 3 | Pass rate: 70%
```

不要汇报「用了多少步」 —— MCP 工具调用次数是实现细节，对评审者来说不是有意义的指标。

## 测试理念

**你是一名对抗式测试者。** 你的目标是找出 bug，而不是证明正确性。

- **想办法弄坏你测的每个功能。** 别只检查「按钮在不在？」 —— 快速点它两下、提交空表单、粘贴 500 个字符、流程中途按 Escape。
- **测开发者没想到的地方。** 空状态、错误恢复、纯键盘导航、移动端溢出。
- **每条断言都必须基于证据。** 对比前后快照。按 ref 检查具体元素。没有来自无障碍树或确定性检查的实在证据，绝不报 PASS。
- **失败要报到足以复现的程度。** 包含确切的动作、你的预期、实际得到的结果，以及一条修复建议。

## 断言协议

每个测试步骤都必须产出一条结构化的断言。不要写「看起来不错」这种自由文本。

### 步骤标记

每个测试步骤，恰好发出一个标记：

```
STEP_PASS|<step-id>|<evidence>
```
或
```
STEP_FAIL|<step-id>|<expected> → <actual>|<screenshot-path>
```

- `step-id`：简短标识，如 `homepage-cta`、`form-validation-error`、`modal-cancel`
- `evidence`：你观察到的、能证明此步通过的东西（元素 uid、文本内容、URL、`evaluate_script` 结果）
- `expected → actual`：你的预期 vs 实际得到的
- `screenshot-path`：保存的截图路径（仅失败时 —— 见下文「失败截图」）

### 失败截图

**每条 STEP_FAIL 都必须配一张截图**，好让开发者直观看到哪里出了问题。

当某个测试步骤失败时，立即截图，直接写入以 step-id 命名的路径：

```
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/<step-id>.png" }
```

`take_screenshot` 直接写文件 —— 不需要再单独移动/复制。要截取单个元素而非视口，传它的 `uid`；要截整个可滚动页面，传 `fullPage: true`。

每次测试运行开始时，创建一次截图目录：

```bash
mkdir -p .context/ui-test-screenshots
```

**规则：**
- 文件名 = step-id（例如 `double-submit.png`、`axe-audit.png`、`modal-focus-trap.png`）
- 存到 `.context/ui-test-screenshots/` —— 该目录已加入 gitignore，开发者和其他 agent 都能访问
- 当某个子 agent 负责一个测试分组时，加上分组名前缀以避免冲突：`<group>-<step-id>.png`（例如 `signup-double-submit.png`）
- 在失败的那一刻截图 —— 捕捉损坏状态，不要等恢复之后
- 对于视觉/布局 bug，也截一张基线（正常状态）以便前后对比：`<step-id>-baseline.png`

### 如何验证（按严谨程度排序）

1. **确定性检查**（最强） —— `evaluate_script` 返回可 JSON 序列化的数据供你检视。例如：axe-core 违规计数、`document.title`、表单字段值、控制台错误数组、元素数量。
2. **快照元素匹配** —— 在 `take_snapshot` 返回的无障碍树里存在某个具有特定角色和文本的元素。每个元素都有一个 `uid`（例如 `uid=12 button "Save"`）。元素要么在树里，要么不在。
3. **前后对比** —— 动作前快照，执行动作，动作后快照。验证树按预期发生了变化（元素出现、消失、文本改变）。
4. **截图 + 视觉判断**（最弱） —— 仅用于无障碍树无法捕捉的纯视觉属性（颜色、间距、布局）。务必说明你具体在评估什么。

### 前后对比模式

这是核心的验证循环。每次交互都用它：

```
# 1. BEFORE: capture state
mcp__chrome-devtools__take_snapshot
# Record: what elements exist, their text, their uids

# 2. ACT: perform the interaction (uid comes from the snapshot above)
mcp__chrome-devtools__click { uid: "12" }

# 3. AFTER: capture new state
mcp__chrome-devtools__take_snapshot
# Compare: what changed? What appeared? What disappeared?

# 4. ASSERT: emit marker based on comparison
# If dialog appeared: STEP_PASS|modal-open|dialog "Confirm" appeared at uid=20
# If nothing changed:
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/modal-open.png" }
# STEP_FAIL|modal-open|expected dialog to appear → snapshot unchanged|.context/ui-test-screenshots/modal-open.png
```

> **uid 不稳定。** 每次 `take_snapshot` 都可能给元素重新编号。永远基于**最近一次**快照里的 uid 来操作；任何导航、点击或 DOM 变化之后，使用 uid 前都要重新快照。你也可以把 uid 作为 `args` 传给 `evaluate_script`，对特定元素进行操作。

## 安装配置

本 skill 需要 **chrome-devtools MCP 服务**已配置并连接 —— 它驱动真实的本地 Chrome。无需任何额外安装。

确认工具可用：你应该能调用 `mcp__chrome-devtools__list_pages`。如果 MCP 未连接，告诉用户去添加/启用 `chrome-devtools` MCP 服务后重试。

### 避免权限疲劳

本 skill 会发起大量 MCP 工具调用（快照、点击、eval）。为免逐个批准，在 `.claude/settings.json`（项目级）或 `~/.claude/settings.json`（用户级）里放行 chrome-devtools 工具：

```json
{
  "permissions": {
    "allow": [
      "mcp__chrome-devtools"
    ]
  }
}
```

## 模式选择

只有一个浏览器 —— 你本地的 Chrome。同一套工具既测 localhost 也测线上站点；区别只在 URL。

| 目标 | 怎么做 | 认证 |
|--------|-----|------|
| `localhost` / `127.0.0.1` | `navigate_page { type: "url", url: "http://localhost:3000" }` | 本地开发无需认证 |
| 线上 / 预发布站点 | `navigate_page { type: "url", url: "https://staging.your-app.com" }` | 复用真实 Chrome 配置文件的登录会话 —— 如果你在 Chrome 里已登录，那这里也登录了 |

**隔离：** 默认情况下 MCP 会附着到用户的 Chrome（带着它的 cookie/登录态）。当你需要一个干净的、未登录的浏览器来做可复现的运行时，在隔离上下文里打开页面：

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000", isolatedContext: "ui-test" }
```

同一个 `isolatedContext` 里的页面共享 cookie/存储；换一个上下文名 = 一个全新会话。当测试需要已有的登录/状态时，用用户的默认上下文；要做无干扰的可复现性测试时，用隔离上下文。

## 工作流 A：diff 驱动测试

### 阶段 1：分析 diff

```bash
git diff --name-only HEAD~1          # or: git diff --name-only / git diff --name-only main...HEAD
git diff HEAD~1 -- <file>            # read actual changes
```

给改动的文件分类：

| 文件模式 | UI 影响 | 测什么 |
|-------------|-----------|--------|
| `*.tsx`, `*.jsx`, `*.vue`, `*.svelte` | 组件 | 渲染、交互、状态、边界情况 |
| `pages/**`, `app/**`, `src/routes/**` | 路由/页面 | 导航、页面加载、内容、404 处理 |
| `*.css`, `*.scss`, `*.module.css` | 样式 | 视觉外观（截图）、响应式 |
| `*form*`, `*input*`, `*field*` | 表单 | 校验、提交、空输入、超长输入、特殊字符 |
| `*modal*`, `*dialog*`, `*dropdown*` | 交互 | 打开/关闭、escape、焦点陷阱、取消 vs 确认 |
| `*nav*`, `*menu*`, `*header*` | 导航 | 链接、激活态、路由、键盘导航 |
| 仅非 UI 文件 | 无 | 跳过 —— 报告「无需 UI 测试」 |

### 阶段 2：把文件映射到 URL

检测框架：`cat package.json | grep -E '"(next|react|vue|nuxt|svelte|@sveltejs|angular|vite)"'`

| 框架 | 默认端口 | 文件 → URL 模式 |
|-----------|-------------|-----|
| Next.js App Router | 3000 | `app/dashboard/page.tsx` → `/dashboard` |
| Next.js Pages Router | 3000 | `pages/about.tsx` → `/about` |
| Vite | 5173 | 查路由配置 |
| Nuxt | 3000 | `pages/index.vue` → `/` |
| SvelteKit | 5173 | `src/routes/+page.svelte` → `/` |
| Angular | 4200 | 查路由模块 |

### 阶段 3：确保跑的是对的代码

测试前，确认开发服务器提供的是 diff 里的代码 —— 而不是某个过时的分支。

**如果测的是某个 PR 或特定分支：**
```bash
# Check what branch is currently checked out
git branch --show-current

# If it's not the PR branch, switch to it
git fetch origin <branch> && git checkout <branch>

# Install deps — the lockfile may differ between branches
yarn install  # or npm install / pnpm install
```

如果开发服务器之前是在另一个分支上跑的，checkout 之后要重启它。

**找出正在运行的开发服务器：**
```bash
for port in 3000 3001 5173 4200 8080 8000 5000; do
  s=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port" 2>/dev/null)
  if [ "$s" != "000" ]; then echo "Dev server on port $port (HTTP $s)"; fi
done
```

如果什么都没找到：让用户启动他们的开发服务器。

**验证它确实能渲染：**
执行 `navigate_page` + `take_snapshot` 后，检查无障碍树里是否含有真实的页面内容（导航、标题、可交互元素） —— 而不只是一个错误浮层或空 body。Next.js 开发服务器可能返回 HTTP 200，却展示一个全屏的构建错误对话框。如果快照为空或被错误对话框占满，说明服务器坏了 —— 先修构建再测试。同时尽早调用 `list_console_messages { types: ["error"] }` —— 一个能渲染却往控制台狂刷错误的页面，本身就已经在失败了。

### 阶段 4：生成测试计划

对每个改动区域，**正常路径与对抗测试都要规划**：

```
Test Plan (based on git diff)
=============================
Changed: src/components/SignupForm.tsx (added email validation)

1. [happy] Valid email submits successfully
   URL: http://localhost:3000/signup
   Steps: fill valid email → submit → verify success message appears

2. [adversarial] Invalid email shows error
   Steps: fill "not-an-email" → submit → verify error message appears

3. [adversarial] Empty form submission
   Steps: click submit without filling anything → verify error, no crash

4. [adversarial] XSS in email field
   Steps: fill "<script>alert(1)</script>" → submit → verify sanitized/rejected

5. [adversarial] Rapid double-submit
   Steps: click submit twice quickly → verify no duplicate submission

6. [adversarial] Keyboard-only flow
   Steps: Tab to email → type → Tab to submit → Enter → verify success
```

### 阶段 5：执行测试

```bash
mkdir -p .context/ui-test-screenshots
```
```
# Open the app (localhost or deployed). Use an isolated context for a clean run.
mcp__chrome-devtools__new_page { url: "http://localhost:3000", isolatedContext: "ui-test" }
```

每个测试都遵循**前后对比模式**：

```
# Navigate
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/path" }
mcp__chrome-devtools__wait_for { text: "<text that proves the page is ready>" }   # optional

# BEFORE snapshot
mcp__chrome-devtools__take_snapshot
# Note the current state: elements, uids, text

# ACT (uids come from the snapshot above)
mcp__chrome-devtools__click { uid: "<uid>" }
# or: mcp__chrome-devtools__fill { uid: "<uid>", value: "..." }
# or: mcp__chrome-devtools__fill_form { ... }      # several fields at once
# or: mcp__chrome-devtools__type_text { text: "..." }
# or: mcp__chrome-devtools__press_key { key: "Enter" }

# AFTER snapshot
mcp__chrome-devtools__take_snapshot
# Compare against BEFORE: what changed?

# ASSERT with marker
# STEP_PASS|step-id|evidence  OR  STEP_FAIL|step-id|expected → actual
```

### 阶段 6：汇报结果

```
## UI Test Results

### STEP_PASS|valid-email-submit|status "Thanks!" appeared at uid=42 after submit
- URL: http://localhost:3000/signup
- Before: form with email input uid=3, submit button uid=7
- Action: filled "user@test.com", clicked uid=7
- After: form replaced by status element with "Thanks! We'll be in touch."

### STEP_FAIL|double-submit|expected single submission → form submitted twice|.context/ui-test-screenshots/double-submit.png
- URL: http://localhost:3000/signup
- Before: form with submit button uid=7
- Action: clicked uid=7 twice rapidly
- After: two success toasts appeared, suggesting duplicate submission
- Screenshot: .context/ui-test-screenshots/double-submit.png
- Suggestion: disable submit button after first click, or debounce the handler

---
**Summary: 4/6 passed, 2 failed**
Failed: double-submit, xss-sanitization

Screenshots saved to `.context/ui-test-screenshots/` — open any failed step's screenshot to see the broken state.
```

测试完成后，用 `mcp__chrome-devtools__close_page` 关掉你打开的额外标签页，让下一个 agent 接手一个干净的浏览器。不要关掉用户自己的其他标签页。

### 阶段 7：生成 HTML 报告

产出文本报告之后，生成一份独立的 HTML 报告，让评审者可以在浏览器里打开。报告把截图内联嵌入（base64），因此作为单文件即可工作 —— 无外部依赖。

**为什么：** 文本报告适合 agent 对话，但评审者（PM、设计师、其他工程师）想要一个可打开、可浏览、可分享的视觉产物。内联截图让失败一目了然。

#### 怎么生成

1. 读取 HTML 模板 [references/report-template.html](references/report-template.html)
2. 用真实测试数据替换模板里的占位符来构建报告：

| 占位符 | 取值 |
|-------------|-------|
| `{{TITLE}}` | `<title>` 标签的报告标题（例如 "UI Test: PR #1234 — OAuth Settings"） |
| `{{TITLE_HTML}}` | 可见 `<h1>` 的报告标题。若有 PR URL，把 PR 引用用 `<a>` 标签包起来使其可点击（例如 `UI Test: <a href="https://github.com/org/repo/pull/1234">PR #1234</a> — OAuth Settings`）。若无 URL，则用与 `{{TITLE}}` 相同的纯文本。 |
| `{{META}}` | 一行上下文：日期、应用 URL、用户、分支 |
| `{{TOTAL_TESTS}}` | STEP_PASS + STEP_FAIL 总数 |
| `{{AGENT_COUNT}}` | 参与运行的子 agent 数量 |
| `{{PASS_COUNT}}` | STEP_PASS 数量 |
| `{{FAIL_COUNT}}` | STEP_FAIL 数量 |
| `{{PASS_RATE}}` | 整数百分比（例如 "92"） |
| `{{RATE_CLASS}}` | `good`（≥90%）、`warn`（70–89%）、`bad`（<70%） |
| `{{FAILURES_SECTION}}` | 失败测试卡片的 HTML（见下文） |
| `{{PASSES_SECTION}}` | 通过测试卡片的 HTML（见下文） |

3. 为每条测试结果生成一个 `<details>` 卡片。失败的测试应**默认展开**，让评审者立刻看到：

```html
<!-- Failed test card (open by default) -->
<div class="section">
  <h2>Failures <span class="count">{{FAIL_COUNT}}</span></h2>
  <details class="test-card fail" open>
    <summary>
      <span class="badge fail">FAIL</span>
      <span class="step-id">step-id-here</span>
      <span class="evidence">expected → actual</span>
    </summary>
    <div class="body">
      <dl>
        <dt>URL</dt><dd>http://localhost:3000/path</dd>
        <dt>Action</dt><dd>What was done</dd>
        <dt>Expected</dt><dd>What should have happened</dd>
        <dt>Actual</dt><dd>What happened instead</dd>
      </dl>
      <div class="suggestion">Fix: description of suggested fix</div>
      <div class="screenshot">
        <img src="data:image/png;base64,..." alt="Screenshot of failure">
        <div class="caption">step-id.png — captured at moment of failure</div>
      </div>
    </div>
  </details>
</div>

<!-- Passed test card (collapsed by default) -->
<div class="section">
  <h2>Passed <span class="count">{{PASS_COUNT}}</span></h2>
  <details class="test-card pass">
    <summary>
      <span class="badge pass">PASS</span>
      <span class="step-id">step-id-here</span>
      <span class="evidence">evidence summary</span>
    </summary>
    <div class="body">
      <dl>
        <dt>URL</dt><dd>http://localhost:3000/path</dd>
        <dt>Evidence</dt><dd>What was observed</dd>
      </dl>
    </div>
  </details>
</div>
```

4. **把截图以 base64 嵌入**，使 HTML 完全自包含：

```bash
# Convert screenshot to base64 data URI
base64 -i .context/ui-test-screenshots/step-id.png | tr -d '\n'
# Use as: src="data:image/png;base64,<output>"
```

读取每个在 STEP_FAIL 标记里引用的截图文件，做 base64 编码，并作为 `<img src="data:image/png;base64,...">` 嵌入对应的测试卡片。对于 STEP_PASS，仅当显式截过图时才嵌入（例如基线截图）。

5. 把最终 HTML 写到 `.context/ui-test-report.html`：

```bash
# Write the generated HTML
cat > .context/ui-test-report.html << 'REPORT_EOF'
<!DOCTYPE html>
...generated report...
REPORT_EOF

# Open it for the reviewer
open .context/ui-test-report.html  # macOS
# xdg-open .context/ui-test-report.html  # Linux
```

6. 告诉用户：`Report saved to .context/ui-test-report.html`，并主动提出帮他打开。

**规则：**
- 失败区放在通过区之前 —— 评审者最先关心的是哪里坏了
- 失败卡片默认 `open`；通过卡片默认折叠
- 每个 STEP_FAIL 卡片都必须嵌入一张截图 —— 如果截图文件缺失，在卡片里注明
- 如果提供了修复建议，在每个失败卡片里包含该建议/修复
- 报告必须能离线工作 —— 无 CDN 链接、无外部资源
- 把 HTML 控制在 5MB 以内 —— 如果截图把它撑超了，降低图片质量，或对通过项跳过基线截图

## 对抗式测试模式

把这些应用到你测的每个可交互元素上。完整的模式库（表单、模态框、导航、错误状态、键盘无障碍）见 [references/adversarial-patterns.md](references/adversarial-patterns.md)。

## 确定性检查

这些产出结构化数据，而非主观判断。把它们当作最强形式的断言来用。

| 检查 | 能抓到什么 | 断言 |
|-------|----------------|------|
| axe-core | WCAG 违规 | `violations.length === 0` |
| 控制台错误 | 运行时异常、失败的请求 | 空的错误数组 |
| 损坏图片 | 缺失/加载失败的图片 | 没有 `naturalWidth === 0` 的图片 |
| 表单标签 | 没有可访问标签的输入框 | 每个输入都 `hasLabel: true` |

确切的 `evaluate_script` 配方见 [references/browser-recipes.md](references/browser-recipes.md)。

## 工作流 B：探索式测试

没有 diff，没有计划 —— 就打开应用，想办法把它弄坏。当用户说「测我的应用」「找 bug」「QA 一下这个站点」时用它。

### 方法

1. **摸清应用** —— 读 `package.json` 检测框架，然后打开根 URL 并快照，看看里面有什么
2. **遍历一切** —— 点遍导航链接，访问每个能到达的页面，记下存在什么
3. **测你发现的东西** —— 对每个页面，应用下面的对抗式模式（表单、模态框、导航、键盘、错误状态）
4. **跑确定性检查** —— 对每个页面跑 axe-core、控制台错误、损坏图片、表单标签
5. **汇报发现** —— 用 STEP_PASS/STEP_FAIL 标记，失败项附上复现步骤

不必追求系统化的覆盖。就像一个用户那样探索，但带着把东西弄坏的意图。agent 擅长这个 —— 放手让它去逛。

### 探索式运行的技巧

- 从首页开始，然后自然地顺着导航走
- 试试 404 页（`/does-not-exist`） —— 是自定义的还是默认的？
- 找空状态（没有数据的页面）
- 先用垃圾输入再用有效输入测表单
- 在每个页面检查移动端视口（375px） —— 会溢出吗？用 `resize_page { width: 375, height: 812 }` 或 `emulate` 套用设备预设
- 如果应用有认证，在真实 Chrome（默认上下文）里登录一次，会话就会延续 —— 无需 cookie-sync

## 工作流 C：分组顺序测试

chrome-devtools MCP 驱动**一个** Chrome，所以测试分组不能并发跑 —— `select_page` 是全局的，并行 agent 会破坏彼此的状态。取而代之，把一个大任务拆成多个分组以**隔离上下文**，并**接连**运行：分派一个子 agent，让它跑完并汇报，再分派下一个。每个分组可以独占自己的标签页（`new_page`），主 agent 在最后汇总结果。

当你要测很多页面或类别、又想要每组干净的汇报且不撑爆单个 agent 的上下文时，用它。

完整工作流见 [references/parallel-testing.md](references/parallel-testing.md)：分组拆分、顺序分派 agent、标签页/页面管理、以及结果汇总。

## 设计一致性

检查改动后的 UI 在视觉上是否与应用其余部分相符。做视觉或设计检查时，读 [references/design-consistency.md](references/design-consistency.md)。

## 测试类别

| 类别 | 怎么做 | 断言类型 |
|----------|-----|---------|
| 无障碍 | axe-core + 键盘导航 | 确定性（违规计数） |
| 视觉质量 | 截图 + 启发式评估 | 视觉判断（最弱 —— 注明具体细节） |
| 响应式 | 视口扫描 + 截图 | 视觉 + 确定性（溢出检查） |
| 控制台健康 | 控制台捕获 eval | 确定性（错误计数） |
| UX 启发式 | 快照 + Laws of UX + Nielsen 原则 | 结构化判断（引用具体启发式） |
| 错误状态 | 导航到空状态/错误状态 | 前后对比 |
| 数据展示 | 对表格/仪表盘做快照 | 元素匹配（列数、格式化） |
| 设计一致性 | 截基线图 + 改动页对比 | 视觉判断（引用具体属性） |
| 探索式 | 自由导航 + 对抗式测试 | 前后对比 + 判断 |

参考指南（按需加载）：
- **对抗式模式** —— [references/adversarial-patterns.md](references/adversarial-patterns.md) —— 测试表单、模态框、导航或键盘 a11y 时加载
- **浏览器配方** —— [references/browser-recipes.md](references/browser-recipes.md) —— 跑确定性检查（axe-core、控制台、图片、表单标签）时加载
- **探索式测试** —— [references/exploratory-testing.md](references/exploratory-testing.md) —— 用于工作流 B（无 diff，开放探索）
- **UX 启发式** —— [references/ux-heuristics.md](references/ux-heuristics.md) —— 评估 UX 质量或引用具体启发式时加载
- **设计系统** —— [references/design-system.example.md](references/design-system.example.md) —— 供用户自行定制的模板
- **设计一致性** —— [references/design-consistency.md](references/design-consistency.md) —— 做视觉一致性检查时加载
- **分组顺序测试** —— [references/parallel-testing.md](references/parallel-testing.md) —— 用于工作流 C（在一个浏览器上接连跑分组）
- **报告模板** —— [references/report-template.html](references/report-template.html) —— 阶段 7 生成报告用的 HTML 模板

带确切命令的实战示例见 [EXAMPLES.md](EXAMPLES.md)，如果你想看断言协议的实际运行效果。

## 最佳实践

1. **保持对抗** —— 想办法弄坏，别只确认它能跑
2. **每条断言都要有证据** —— 快照 uid、`evaluate_script` 结果，或前后 diff
3. **每次交互都做前后对比** —— 快照、动作、快照、对比
4. **使用 uid 前先重新快照** —— uid 每次快照都会变；永远基于最新的那次操作
5. **每个失败都截图** —— STEP_FAIL 时立即 `take_screenshot { filePath: ... }`，保存到 `.context/ui-test-screenshots/<step-id>.png`
6. **先做确定性检查** —— axe-core、控制台错误、表单标签先于视觉判断
7. **可复现的运行用隔离上下文** —— `new_page { isolatedContext: "ui-test" }`；仅当需要已有登录/状态时才用默认上下文
8. **一个浏览器，同一时刻一个 agent** —— 顺序分派测试分组子 agent，完成后关掉额外标签页（`close_page`）
9. **失败要带复现步骤汇报** —— 动作、预期、实际、截图路径、建议

## 故障排查

- **没有页面 / 工具不可用**：调用 `list_pages`；如果它报错，说明 chrome-devtools MCP 未连接 —— 让用户启用它。如果没有页面，用 `new_page { url }`。
- **开发服务器无响应**：`curl http://localhost:<port>` —— 让用户启动它
- **`evaluate_script` 与 `await`**：传一个 `async () => { ... }` 函数 —— `evaluate_script` 会 await 返回的 promise。结果必须可 JSON 序列化。
- **元素 uid 找不到 / 已失效**：重新 `take_snapshot` —— uid 在每次快照及任何 DOM 变化后都会重新编号
- **空白快照**：快照前先 `wait_for { text: "..." }`（或重新导航）；页面可能还没渲染完
- **SPA 深链接 404**：先导航到 `/`，再点进去
- **认证失败**：在真实 Chrome（默认上下文）里手动登录 —— MCP 会复用那个会话。如果你打开了 `isolatedContext`，它按设计是未登录状态；去掉隔离上下文即可继承登录态。
- **焦点在错误的标签页**：`list_pages` 然后 `select_page { pageId }` —— 记住这是全局的，所以同一时刻只应有一个 agent 驱动浏览器
- **对话框阻塞**：用 `handle_dialog` 处理原生对话框，或给 `evaluate_script` 传 `dialogAction` / 给 `navigate_page` 传 `handleBeforeUnload`
