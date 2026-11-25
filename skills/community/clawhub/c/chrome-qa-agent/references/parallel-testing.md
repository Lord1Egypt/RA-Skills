# 分组顺序测试

把一个大的测试任务拆分成若干分组（Group A、B、C……），并**一个接一个、一次一组地**运行它们——派出一个分组的子 agent，等它完成并汇报，再派出下一个。这是 SKILL 中的 **Workflow C**。

这里的收益在于**上下文隔离和干净的分组报告**，而不是挂钟时间上的速度。许多个小而专注的 agent 胜过少数几个庞大的 agent，即便它们是串行运行的。

### 为什么是顺序，而非并行

chrome-devtools MCP 驱动的是**一个共享的 Chrome**，并且 `select_page` 为整个 MCP 连接**全局地**设置活动页面。如果两个驱动浏览器的 agent 同时运行，它们就会争抢同一个浏览器：一个 agent 的 `select_page` / `navigate_page` 会悄无声息地改变另一个 agent 正在对其做断言的页面，从而破坏两次运行。

所以**绝不要让两个驱动浏览器的 agent 并发运行。** 每个分组的 agent 在它的回合里独占浏览器，完成并汇报，然后下一个才开始。

（非浏览器的工作——读取 diff、分析文件、起草计划——没有共享的浏览器状态，*可以*并行化。只有驱动浏览器这件事必须串行。）

### 何时拆分成分组，何时直接运行

| 场景 | 做法 |
|----------|----------|
| 页面/路由很多，或有若干个不同类别（表单、a11y、响应式） | **拆分成分组** — 每个分组一个子 agent，依次派出 |
| 单个组件的修复，寥寥几项检查 | **直接运行** — 由主 agent（或一个子 agent）来做；无需拆分 |
| 同一个流程中的各个步骤（填表单 → 提交 → 检查结果） | **始终顺序进行** — 各步骤相互依赖；把它们放在一个分组里 |

一个分组内部的测试始终顺序运行。各分组之间也是顺序运行——拆分是为了上下文的整洁，而非为了并发。

### 阶段 1：按区域对测试分组

在生成测试计划（Workflow A）或确定要测的页面（Workflow B）之后，把合并后的编号测试列表按区域拆分成若干分组。每个分组成为一个子 agent 的任务。

```
Test Groups (from diff-driven test plan)
========================================
Group A (signup)    → /signup form validation (happy + adversarial)
Group B (dashboard) → /dashboard empty state + data display
Group C (a11y)      → /settings accessibility audit (axe-core + keyboard)
```

每个分组还会获得一个唯一的 `isolatedContext` 名称（使用分组名），这样它的标签页就能从一个干净、可复现的会话开始。

### 阶段 2：一次派出一个子 agent

使用 Agent 工具，**每个分组用一次，并在启动下一个之前等待每一个完成。** 不要把多个 Agent 调用放进同一条消息里——那会让它们并发运行，从而破坏共享的浏览器。

派出顺序：Group A → 等待汇报 → Group B → 等待汇报 → Group C。

每个子 agent 的 prompt 都应当告诉它：
1. 用 `new_page` 在其分组的隔离上下文中打开自己的标签页。
2. 运行分配给它的测试（在这一回合里它独占浏览器）。
3. 对每一次失败截图，文件名以分组名为前缀。
4. 在结束前用 `close_page` 关闭自己的标签页，给下一个分组留下一个干净的浏览器。

```
Agent — Group A (dispatch first; wait for it to report before dispatching Group B):
  "Run signup form tests. You own the single shared Chrome exclusively for this run —
   no other agent is using it right now.

   Open your tab:
     mcp__chrome-devtools__new_page { url: "<localhost URL>", isolatedContext: "signup" }

   Run these tests: [numbered list from the merged plan].
   Drive the browser ONLY through chrome-devtools MCP tools (mcp__chrome-devtools__*).
   Follow the before/after assertion protocol (take_snapshot → act → take_snapshot → assert).

   On any STEP_FAIL, immediately screenshot, prefixing the file with the group name:
     mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/signup-<step-id>.png" }

   Return structured STEP_PASS / STEP_FAIL markers (include screenshot path for failures),
   plus a one-line tally: Tests | Passed | Failed | Skipped | Pages visited.

   Before finishing, close every tab you opened:
     mcp__chrome-devtools__close_page { ... }
   Leave the browser clean — the next group's agent reuses the same Chrome."

Agent — Group B (dispatch only AFTER Group A has reported): same shape,
  isolatedContext: "dashboard", screenshots prefixed "dashboard-".

Agent — Group C (dispatch only AFTER Group B has reported): same shape,
  isolatedContext: "a11y", screenshots prefixed "a11y-".
```

**分组派发的关键规则：**
- **同一时刻只有一个驱动浏览器的 agent。** 在派出下一个之前，等待每个分组的汇报。共享的 Chrome 和全局的 `select_page` 使并发变得不安全。
- 每个 agent 通过 `new_page { url, isolatedContext: "<group>" }` 打开自己的标签页——一个新的上下文名称会给出一个干净、已登出的会话。仅当某个测试需要既有的 Chrome 登录/状态时，才复用默认上下文。
- 每个 agent 在结束前用 `close_page` 关闭自己的标签页，这样下一个分组就能继承一个干净的浏览器。不要杀掉用户的其他标签页。
- 把完整的测试步骤和断言协议传给每个 agent——它们没有 skill 的上下文。
- 告诉每个 agent 把失败截图保存到 `.context/ui-test-screenshots/` 下，采用命名约定 `<group>-<step-id>.png`，以避免分组之间的冲突。
- 在每个 prompt 中包含一个明确的步骤预算（参见 SKILL 中的"Giving sub-agents a step budget"）。

### 阶段 3：跨分组合并结果

每个分组汇报后，收集它的 STEP_PASS / STEP_FAIL 标记。一旦所有分组都完成，合并成一份报告：

```
## UI Test Results (Grouped Sequential Run)

### Group A: signup
STEP_PASS|valid-email|heading "Welcome!" appeared after submit
STEP_PASS|empty-submit|validation error shown for empty form
STEP_FAIL|double-submit|expected single submission → two success toasts appeared|.context/ui-test-screenshots/signup-double-submit.png

### Group B: dashboard
STEP_PASS|empty-state|"No items yet" message with CTA displayed
STEP_PASS|data-display|table rendered 5 rows with correct columns

### Group C: a11y
STEP_FAIL|axe-audit|expected 0 violations → 2 critical: color-contrast, missing-label|.context/ui-test-screenshots/a11y-axe-audit.png
STEP_PASS|keyboard-nav|all 12 elements reachable via Tab

---
Tests: 7 | Passed: 5 | Failed: 2 | Skipped: 0 | Agents: 3 | Pass rate: 71%
Failed: double-submit (Group A), axe-audit (Group C)

Screenshots: `.context/ui-test-screenshots/`
- signup-double-submit.png — duplicate toast after rapid submit
- a11y-axe-audit.png — page showing color contrast and missing label violations
```

使用与 skill 其余部分相同的合并格式：`Tests | Passed | Failed | Skipped | Agents | Pass rate`。

### 需要认证的页面

无需额外设置——没有 cookie 同步，没有云端或远程浏览器，没有代理。chrome-devtools MCP 挂接到真实的本地 Chrome，因此它已登录的会话本就可用。要测试需要认证的页面，在 Chrome（默认上下文）里登录一次；每个需要该登录态的分组都应在**默认上下文**中打开它的标签页（省略 `isolatedContext`），以便继承该会话。仅当需要干净、已登出的可复现性时，才使用具名的 `isolatedContext`。

### 清理

每个分组的 agent 在结束前关闭自己的标签页（`close_page`）。如果在最后一个分组之后还有任何遗留，主 agent 可以收尾：

```
mcp__chrome-devtools__list_pages
mcp__chrome-devtools__close_page { ... }   # close any leftover test tabs
```

不要关闭用户自己的标签页——只关闭这次测试运行打开的那些。
