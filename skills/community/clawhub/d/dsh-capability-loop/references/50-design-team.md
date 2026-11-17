# 50 · 设计生产能力与团队协作

> 目标：UI 设计达到**生产级/企业级**（不是「能看就行」），并让设计力随任务累积；团队能力**边界清晰、可自动路由、可评审**。
> 设计能力由 skill `ui-design-production` 承载（本文件负责路由、角色与门禁）；**出稿前的现有系统判断见 `55-design-intake.md`（硬门）**。

## 0. 设计前置硬门（先做，不做不出稿）

1. 跑 `scripts/product-context.ps1 -Project <工程>` 拿到技术栈/组件库/主题线索；
2. 按 `55-design-intake.md` 填 `templates/design-context.md`（框架与组件库、主题 token 实测值、布局骨架、数据规范、状态、3 个样本页、设计稿来源、差异清单）；
3. `loop-gate.ps1` 的 design 类别默认检查 `design-context*.md`，缺失 → FAIL；
4. 设计稿必须**在现有体系上扩展**：与现有组件库/主题冲突处写「为什么不用现有方案 + 影响面」。

## 1. `ui-design-production`（设计任务必须加载）

- **触发**：设计/重新设计/改版页面或界面、出设计稿、UI 评审、视觉验收；纯后端/数据/文档任务不加载。description 压到 ≤200 字符（源环境 83 字符）。
- **8 步工作流**：brief → IA → design token → 组件状态 → 响应式 → 无障碍 → 性能预算 → 视觉 QA。
- **design token 必须给数值**：间距 4/8/12/16/24/32/48、字号 12/14/16/20/28/36、圆角 4/8/12、动效 120/180/240ms、对比度 ≥4.5:1、触控 ≥44px、CLS <0.1。
- **组件 8 态**：default/hover/active/focus/disabled/loading/empty/error（数据面另加 3 态）。
- **ToB 覆盖档**（4/3/8）与能源/电网数据密集场景（数字精度/单位/时区/危险操作二次确认）。
- **旧 skill 处理**：`design-taste-frontend`（无触发限定、任何前端任务都可能自动加载）移入 `skills-disabled/`，避免双触发。

## 2. 评审 rubric（`design-review-rubric.md`，同 skill 目录）

- 8 维加权 100 分（布局/层级/一致性/状态完备/可访问性/响应式/性能/品牌契合）；
- **V1–V12 一票否决**：对比度不足、键盘/focus 不可达、375 破损、状态缺失、假数据、控制台错误、规范崩坏、严重 AI 味、触控 <44px、布局抖动/CLS、危险操作无确认、评审流程无效；
- 问题分 P0/P1/P2；**无证据维度最高 2 分**；**禁止自审自过**；评审必须由非实现者给出，Lead 终门基于评审记录。

## 3. 视觉 QA（沙箱限制下的现实方案）

**先跑探测，再动手**：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill>\scripts\visual-qa-check.ps1" -OutDir "<工作区>\.tmp\visual-qa"
# exit 0 = A 路径可用；exit 2 = 权限受限（必须显式提示用户选 A/B/C）；exit 1 = Chrome 缺失/参数错误
```

**沙箱与权限（2026-11-13 实测更新）**：普通 `workspace-write` 下 agent-browser 拉起 Chrome 会因 **crashpad `OpenProcess` 被拒** 失败（`exit -36863`，无 DevTools 端口）；这是**进程/权限限制**，不是「浏览器永远不可用」。`danger-full-access`（或用户终端）下 Chrome 可正常渲染：**Chrome headless `--screenshot` 实测出图且像素正确**（1280×720，背景/标题色与页面一致）。agent-browser 在放宽权限后能启动并保存截图，但 `open` 命令在本机会挂起（CLI/守护进程行为），需后台运行 + 超时终止，不建议作为主路径。

可行路径（推荐顺序）：
- **A 全权限会话 + Chrome headless 截图**：`chrome.exe --headless=new --disable-gpu --user-data-dir=<临时> --window-size=... --screenshot=<png> <url>`；实测可渲染，批量 375/768/1440 × 明/暗 最省事；需会话为 danger-full-access。`visual-qa-check.ps1` 就是这条路径的探针。
- **B 用户终端截图 + `read_image` 评审**（最稳）：请用户在自己的浏览器打开页面，把 375/768/1024/1440 × 明/暗 截图放进 `design-qa/<task>/`。
- **C 手动截图 + 标注「未实测」** + 补测方式。

**权限不足时必须显式提示用户（不得静默继续）**：`visual-qa-check.ps1` 返回 exit 2 时，用下面话术（`ask_user_question` 或直接问）：

```text
浏览器视觉验收当前不可用（A 路径受限：普通沙箱下 Chrome crashpad 被拒，属权限/进程限制）。
请选一种：
  A) 切到 danger-full-access 会话，我重跑探测并自动截图；
  B) 你在自己浏览器截 375/768/1024/1440 × 明/暗，放到 design-qa/<task>/，我来评审；
  C) 本次无法截图 → 交付物标「未实测（浏览器权限不足）」+ 原因 + 补测方式，不计 PASS。
```

探测脚本会留下 HTML/PNG 作为证据（`<工作区>\.tmp\visual-qa\`）；不能实测的项必须写进交付物；不得用「应该没问题」代替截图。

## 4. 团队角色与评审门

| 角色 | 职责 | 禁止 |
|---|---|---|
| Lead | 拆任务、派活、验收、收口 | 不亲自实现被委派的产物 |
| Designer（设计负责人） | brief / IA / 设计 token / 视觉方向 | 不实现代码 |
| Engineer | 实现与还原，产出证据（截图/测试） | 不给自己打分 |
| Reviewer | 按 rubric 独立评审（G1 设计门 + G2 实现门） | **不得审自己写的东西** |
| 需求评审员 | 按 8 维 + 一票否决评审需求/方案 | 不改需求、不写方案、不实现 |
| QA | 按测试工作流独立执行、取证 | 不修改实现、禁止假绿 |

- 评审门：**G1 设计门**（brief/token/状态/无障碍过 rubric）→ **G2 实现门**（还原度/截图/测试）→ **G3 交付门**（Lead 终门 + 门禁脚本）；任一 PASS 必须来自没写过该产物的人。
- 派活：`team_task_create`（写清 subject/description/`write_scopes`/`blocked_by`），执行者 `claim → 干 → complete`；**写范围互斥**，同一路径同一时间只有一个 owner。
- 团队规模：默认 2–3 人；超过 4 人必须有明确收益说明；小任务（单文件、≤30 分钟、无新组件/新页面）**不 spawn 团队**。

## 5. 自动路由（写进 `AGENTS.md`，DSH 自动加载）

| 用户说 | 行为 |
|---|---|
| 设计/重新设计/改版/出页面 | **必加载** `ui-design-production`；小改 Lead 直接做 + pre-flight 自检；中/大改 spawn Designer→Engineer→Reviewer→QA |
| 需求评审/方案评审/立项 | 走 `30-requirement.md` + `requirement-review.md`，spawn 需求评审员（不得自审） |
| 自动化测试/回归/e2e | 走 `40-testing.md` + 测试工作流，spawn QA（先建台账，双门禁） |
| 写代码/交接实现 | 走 skill `feature-handoff`（见 `60-handoff.md`） |
| 小改/改文案/看代码 | **不组队**，直接做（避免为小任务付团队成本） |

**诚实边界**：DSH 没有「配置级路由/hook」，上述是 `AGENTS.md`（自动注入）+ skill description + `memory/rules.md` 三道软约束；不会自动生成团队，也无常驻 Reviewer/QA。要更硬：会话开头显式要求「按团队流程做 + 最后给 gate-check 结果」，或在会话内预 spawn 角色（跨会话不保留）。

## 6. TeamHarness 结论（不要重复踩）

- TeamHarness MCP（`~/.dsh/teamharness-mcp/server.py`）是 **QwenPaw/CoPaw 平台客户端**：`api_base` 默认 `http://127.0.0.1:8088`，该端口实测 CLOSED；DSH profile 未注册 `dsh-mcp-client` → 8 个 TeamHarness skill 当前**没有工具可用**。
- 「用 TeamHarness 替代原生 Team，设计 skill 就不会无触发限定」**因果不成立**：skill 触发只由 frontmatter description 决定，与团队后端无关。
- 结论：**不替换原生 Team**；需要跨房间协作时再评估 MCP 注册（成本高、需后端与密钥）。

## 7. 设计任务完成前

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "upgrade\team\gate-check.ps1" -TaskDir "<任务目录>" -Kind design
```
要求：brief/IA/token/组件/a11y/perf 产物齐全 + 非实现者评审记录（含得分或 V1–V12 否决项）+ 截图或「未实测」标注。GATE FAIL 不得 claim 完成。
