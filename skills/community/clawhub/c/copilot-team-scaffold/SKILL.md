---
name: copilot-team-scaffold
description: "Initialize a multi-agent AI development framework for any project. Creates .github/ structure with agents, hooks, instructions, prompts, and planning-with-files skill. Sets up spec-flow landing directory and memory templates. Use when starting a new project and wanting to set up a structured AI-assisted development workflow with specialized agents, automated lint hooks, file-based planning, and task execution pipeline. Trigger phrases: 初始化项目AI框架, scaffold AI framework, init copilot team, 搭建AI开发框架, setup agent workflow, 初始化开发框架."
user-invocable: true
---

# Copilot Team Scaffold

为新项目搭建完整的 AI 辅助开发框架。把 Copilot 从代码补全工具变成一个有组织、有纪律的虚拟开发团队。

## 核心理念

```
需求文档 → 设计规格 → 任务分解 → Agent 分发执行 → 自动化保障（hooks + instructions）
```

通过以下四层保障 AI 执行质量：

- **文件化的约束**（AGENTS.md）— 明确每个角色的职责和规范
- **自动化的保障**（hooks）— 覆盖 6 个生命周期事件：上下文注入、质量门禁、降级策略
- **持久化的记忆**（memories + sessions + lessons）— 弥补 AI 的上下文遗忘，自动积累教训
- **结构化的任务**（spec-flow + tasks.md）— 确保需求到代码的可追溯性

### 运行时生命周期

```
SessionStart ──→ PreToolUse ──→ PostToolUse ──→ SubagentStart ──→ SubagentStop ──→ Stop
     │                │               │               │                │            │
  计划恢复         计划上下文       更新提醒       审计记录       质量验证门禁     完成度检查
  教训注入         AGENTS门控      编辑追踪                       降级策略        AGENTS同步检查
  趋势分析         新模块阻断      新目录提醒                                     会话摘要
  门控/追踪初始化
```

### AGENTS.md 全生命周期保障

```
SessionStart → 初始化门控(.agents-gate) + 编辑追踪(.code-edits)
      │
PreToolUse  → 写代码前必须先读过 AGENTS.md（门控）
      │        create_file 到无 AGENTS.md 的模块目录 → 阻断
      │
PostToolUse → 记录 read_file AGENTS.md → 打开门控
      │        追踪代码 + AGENTS.md 编辑到 .code-edits
      │        create_file 到无 AGENTS.md 的目录 → 软提醒
      │
Stop        → 比对 .code-edits：代码改了但 AGENTS.md 没改 → 阻断
```

### 学习闭环

```
失败 → 自动记录(lessons-learned.md) → 统计分析(趋势) → 注入新会话 → 预防重犯
```

## 前提条件

此 skill 假设以下全局 skill 已安装：

- **spec-flow** — 需求拆解工作流（proposal → requirements → design → tasks）
- **planning-with-files** — 会话级文件计划（可选，将作为项目级 skill 生成）

## ⚠️ 交互规则

使用**分阶段确认**工作流。每个阶段完成后等待用户确认再继续。

---

## Phase 1: 采集项目信息

向用户提出以下问题（使用 vscode_askQuestions 或对话形式）：

### 必填信息

1. **项目名称**：用于 spec-flow 目录名和 AGENTS.md 标题（如 `CMC-ARD系统`）
2. **项目简述**：一句话描述项目做什么
3. **后端技术栈**（选择一项）：
   - Python / FastAPI + Tortoise ORM
   - Python / FastAPI + SQLAlchemy
   - Python / Django
   - Node.js / Express
   - Go / Gin
   - Java / Spring Boot
   - 无后端
4. **前端技术栈**（选择一项）：
   - React + TypeScript + Ant Design
   - React + TypeScript + MUI
   - Vue 3 + TypeScript
   - Next.js
   - 无前端
5. **数据库**（选择一项）：
   - Azure SQL Server
   - PostgreSQL
   - MySQL
   - SQLite
   - MongoDB
   - 无数据库
6. **需要哪些 Agent 角色**（多选，建议全选相关的）：
   - 后端开发Agent
   - 前端开发Agent
   - AI工程师Agent
   - 测试工程师Agent
   - 需求分析工程师Agent
   - 架构师Agent（只读不写代码）

### 可选信息

7. **认证方式**：SSO JWT / 自建用户系统 / 无认证
8. **CI/CD**：Docker Compose / GitHub Actions / Azure DevOps / 无
9. **表前缀**：数据库表名前缀（如 `custom_ardqc_`）
10. **代码检查工具**：ruff（Python）/ eslint（TS）/ 其他

### Phase 1 完成后

输出采集到的配置摘要，等待用户确认：

```
📋 **项目信息采集完成**

- 项目名：{{PROJECT_NAME}}
- 后端：{{BACKEND_STACK}}
- 前端：{{FRONTEND_STACK}}
- 数据库：{{DATABASE}}
- Agent 角色：{{AGENT_LIST}}

✅ 确认无误后说 "继续" 开始生成文件
✏️ 有修改请直接说
```

---

## Phase 2: 生成静态文件

以下文件**直接从 `templates/` 目录复制**，无需定制：

### 2.1 Hooks（自动化钩子）

从 `templates/hooks/` 复制到项目的 `.github/hooks/`：

```
.github/hooks/
├── planning-with-files.json          # 全生命周期 hook 配置（6 个事件）
├── post-tool-lint.json               # 自动 lint hook 配置
├── post-tool-lint.js                 # lint 执行脚本
└── scripts/
    ├── planning-paths.js             # 路径解析共享模块
    ├── session-log.js                # 审计日志共享模块
    ├── session-start.js              # SessionStart: 恢复上下文 + 教训注入 + 趋势分析 + 门控初始化
    ├── pre-tool-use.js               # PreToolUse: AGENTS.md 门控 + 新模块阻断 + 计划注入
    ├── post-tool-use.js              # PostToolUse: AGENTS.md 追踪 + 编辑记录 + 新目录提醒
    ├── subagent-start.js             # SubagentStart: 审计记录
    ├── subagent-stop.js              # SubagentStop: 质量验证门禁 + 降级策略
    └── agent-stop.js                 # Stop: AGENTS.md 同步检查 + 完成度检查 + 会话摘要
```

**planning-with-files.json** 覆盖 6 个生命周期事件：
- `SessionStart`(15s) — 计划恢复 + 教训注入 + 趋势分析 + 日志清理 + AGENTS.md 门控/编辑追踪初始化
- `PreToolUse`(15s) — AGENTS.md 门控（写代码前须先读 AGENTS.md）+ 新模块目录 AGENTS.md 强制创建 + 计划上下文注入
- `PostToolUse`(15s) — AGENTS.md 门控追踪 + 代码编辑追踪 + 新目录 AGENTS.md 提醒 + 计划更新提醒
- `SubagentStart`(10s) — 审计记录 Agent 启动
- `SubagentStop`(120s) — **核心门禁**：ruff + pyright + tsc + 关联测试 + 降级策略
- `Stop`(10s) — **AGENTS.md 同步检查**（代码改了但 AGENTS.md 没更新 → 阻断）+ 任务完成度检查 + 会话摘要

**SubagentStop 验证门禁** 详解：
1. `git diff` 获取变更文件列表
2. Python 文件 → `ruff check` + `pyright`
3. TypeScript 文件 → `tsc --noEmit`
4. 自动映射关联测试文件并运行（pytest / vitest）
5. 验证失败 → block 让 agent 继续修复
6. 连续失败 3 次 → 降级到人工，不再 block（防止死循环）
7. 每次失败自动追加到 `lessons-learned.md`

**session-log.js** 共享模块：
- `appendLog(sessionId, event, details)` — 结构化日志追加
- `cleanupLogs()` — 自动清理过期日志（>30天 / >100个）+ 过期重试计数器（>1天）
- 日志文件格式：`.github/session-logs/YYYY-MM-DD_<sid8>.md`

### 2.2 planning-with-files Skill（项目级）

从 `templates/skills/planning-with-files/` 复制到 `.github/skills/planning-with-files/`：

```
.github/skills/planning-with-files/
├── SKILL.md                          # Skill 定义
├── templates/
│   ├── task_plan.md
│   ├── findings.md
│   └── progress.md
└── scripts/
    └── session-catchup.py
```

### 2.3 Sessions 工作区

从 `templates/docs/` 复制：

```
docs/sessions/README.md               # 会话目录说明
```

---

## Phase 3: 生成动态文件

以下文件需要根据 Phase 1 采集的信息**动态生成**。

### 3.1 根 AGENTS.md

创建 `AGENTS.md`，结构如下（用采集到的信息填充）：

```markdown
# {{PROJECT_NAME}} — Project Guidelines

> 根目录 AGENTS.md — 全局规则，适用于所有模块。
> 子模块细节见各目录下的 `AGENTS.md`。

## 项目概述
{{PROJECT_DESCRIPTION}}

## 架构
{{根据技术栈生成架构图}}

## 安全合规
- 禁止硬编码敏感信息
- 日志脱敏
- 输入验证
- .env 不入库

## 配置管理
{{根据技术栈生成配置说明}}

## 代码质量
- 类型安全
- 异步编程
- 错误处理
- 结构化日志
- 代码简洁性

## 数据库
{{如有数据库，生成表前缀和数据隔离规则}}

## 测试策略
| 模式 | 适用场景 |
|------|----------|
| TDD | 纯逻辑、边界条件多 |
| 边写边测 | REST 端点 |
| 实现后补 | AI 输出/UI 交互 |

## Agent 分配规则
{{根据选择的 Agent 角色生成分配表}}

## Agent 执行约定
1. 执行前：读取目标模块的 AGENTS.md
2. 执行中：遵守安全合规与代码质量要求
3. 联合开发：读取相关模块 AGENTS.md，确保接口兼容
4. 自动分发：根据任务类型通过 runSubagent 分发给对应 Agent
5. 跨模块感知：识别所有受影响模块，分别调度对应 Agent

## 模块 AGENTS.md 规则
- 每个模块开发前须先创建该模块的 AGENTS.md
- 必须包含：模块功能、技术栈、接口定义、数据模型、注意事项
- 功能变更后同步更新

## 构建与运行
{{根据技术栈生成命令}}
```

### 3.2 Agent 定义文件

为每个选择的 Agent 在 `.github/agents/` 下创建 `.agent.md`。

**Agent 文件基本结构**（以后端开发Agent为例）：

```markdown
---
description: "后端开发Agent。Use when implementing backend API endpoints, routes, ORM models, schemas, business services, or any backend code. Triggers: 后端开发, backend, API开发, 服务端, {{BACKEND_FRAMEWORK}}, ORM, schema, service, 数据库"
name: "后端开发Agent"
tools: [read, edit, search, execute, agent, todo]
---

你是 {{PROJECT_NAME}} 的**后端开发专家**。

## 角色定位
你负责所有后端代码的开发，包括 API 端点、ORM 模型、Schema、业务服务层、后台任务。

## 技术栈
{{根据后端技术栈填充}}

## 执行前准备
1. 阅读 `.spec-flow/active/{{PROJECT_SLUG}}/design.md` 中的相关章节
2. 阅读目标模块的 `AGENTS.md` 文件
3. 检查依赖任务是否已完成
4. 创建新模块时，必须先创建该模块的 `AGENTS.md`

## 约束
- 遵守根目录 AGENTS.md 的安全合规和代码质量要求
- 所有 API 必须 async/await
- 使用结构化日志
- 类型安全
```

**各角色要点**：

| Agent | 文件名 | 关键特征 |
|-------|--------|----------|
| 后端开发Agent | `backend-developer.agent.md` | 负责 API/ORM/Service/Task |
| 前端开发Agent | `frontend-developer.agent.md` | 负责组件/Hooks/状态管理/i18n |
| AI工程师Agent | `ai-engineer.agent.md` | 负责 LLM/文档解析/规则引擎 |
| 测试工程师Agent | `test-engineer.agent.md` | 负责 pytest/vitest/覆盖率 |
| 需求分析工程师Agent | `requirements-analyst.agent.md` | 负责文档/手册/需求追踪 |
| 架构师Agent | `architect.agent.md` | 只读不写代码，负责设计评审 |

### 3.3 Instructions（指令约束）

在 `.github/instructions/` 下生成：

#### 3.3.1 通用 Instructions（直接复制）

- `planning-with-files.instructions.md` — 从 `templates/instructions/` 复制
- `testing.instructions.md` — 从 `templates/instructions/` 复制
- `spec-flow-run-task.instructions.md` — 从 `templates/instructions/` 复制（需替换 `{{PROJECT_SLUG}}`）

#### 3.3.2 技术栈 Instructions（动态生成）

**如果有后端**，生成 `backend-*.instructions.md`，包含：
- 该后端框架的异步模式约束
- ORM 使用规范
- 日志框架约束
- lint 工具和配置

**如果有前端**，生成 `frontend-*.instructions.md`，包含：
- 组件规范
- i18n 规则
- 状态管理约束
- UI 框架使用规范

### 3.4 run-task.prompt.md

在 `.github/prompts/` 下生成：

```markdown
---
description: "Execute a task from tasks.md by task ID (e.g. T-008)."
agent: "agent"
argument-hint: "Task ID, e.g. T-008"
---
Execute the following task from the project task list.

## Steps

1. Read the task list: [tasks.md](.spec-flow/active/{{PROJECT_SLUG}}/tasks.md)
2. Find the task matching `{{ input }}` — extract its description, dependencies, status, complexity, and assigned Agent
3. **Dependency check**: If any dependency task is not ✅ Done, stop and report which are blocking
4. **Read module AGENTS.md**: Read the `AGENTS.md` file(s) for the target module(s)
5. **Execute**: Implement the task following the constraints in [AGENTS.md](AGENTS.md)
6. **Test**: If the task's test mode is TDD or 边写边测, write/update tests
7. **Verify**: Run the relevant test suite and confirm passing
8. **Report**: Summarize what was done, files changed, and any follow-up needed
```

---

## Phase 4: 初始化 Spec-Flow 落地目录

创建 spec-flow 的项目落地目录：

```
.spec-flow/active/{{PROJECT_SLUG}}/
```

**不要**在这里创建 proposal.md / requirements.md 等文件 — 那些由 spec-flow skill 在实际执行时生成。只创建空目录。

---

## Phase 5: 初始化数据层与记忆模板

### 5.1 教训知识库

从 `templates/lessons-learned.md` 复制到 `.github/lessons-learned.md`。此文件由 SubagentStop hook 自动写入验证失败记录，SessionStart hook 自动读取注入。

### 5.2 审计日志目录

创建 `.github/session-logs/` 目录（空），并在项目 `.gitignore` 中添加：

```
# Copilot session logs (auto-generated, not tracked)
.github/session-logs/
```

### 5.3 记忆模板

提示用户手动或通过 memory tool 创建以下仓库级记忆文件：

```
/memories/repo/code-style.md      — 代码风格备忘（空模板，使用中积累）
/memories/repo/execution-discipline.md — 执行纪律备忘（空模板，犯错后记录）
```

内容建议：

**code-style.md**:
```markdown
# 代码风格备忘

<!-- 使用过程中积累的代码风格约定 -->
```

**execution-discipline.md**:
```markdown
# 执行纪律备忘

## 任务执行 Checklist（每个任务必须）

1. 完整读取 tasks.md §0 — 开发约束、Agent规则、执行约定
2. 必须通过 runSubagent 派发给指定 Agent 执行
3. 模块开发前先创建该模块的 AGENTS.md
4. 执行前准备 — 读 AGENTS.md → 了解模块结构 → 检查依赖完成
5. 安全合规 — 禁止硬编码密码、日志脱敏、输入验证
6. 代码质量 — 类型提示、async/await、错误处理、结构化日志
7. 测试策略 — 按任务指定的测试模式执行

## 教训

<!-- 犯错后在此记录，避免重复 -->
```

### 5.4 全局用户记忆（首次使用框架时初始化）

通过 `memory` tool **检查并创建**以下全局记忆文件。这些文件跨项目持久化，每次会话自动加载到上下文中。**如果已存在则跳过**（`memory create` 对已有文件会失败，这是预期行为）。

#### `/memories/agent-principles.md` — Agent 行为原则

```markdown
# Agent 行为原则（跨项目通用）

## 独立技术判断
- 用户提问 ≠ 要求修改；先独立分析对错，再给结论
- 推理基于技术事实，不基于"用户暗示了方向"

## 先讨论后动手
- 收到功能修改/新增请求时，**不要直接改代码**，先给出修改方案与用户讨论
- 用户明确确认方案后才可开始写代码

## 约束优先
- 执行任务前先读项目约束文件（AGENTS.md、instructions/），不因任务简单就跳过
- 安全合规不可跳过：禁止硬编码敏感信息、日志脱敏、输入验证

## 待办状态即时更新（严格执行）
- 每完成一个 todo，**立即调用 manage_todo_list 标记 completed**，再做下一个
- 禁止批量完成后一次性更新——上下文压缩会吞掉未持久化的状态
- 节奏：mark in-progress → 执行 → mark completed → 下一个 mark in-progress

## 分析→分发→执行
- 多模块任务先全面分析，再按职责分派给对应 Agent（runSubagent），不由主 Agent 直接写任务代码
- 模块开发前先读取/创建该模块的 AGENTS.md；功能变更后同步更新
- ⚠️ **AGENTS.md 同步是硬约束**：每次修改代码后，必须在同一轮操作中更新涉及模块的 AGENTS.md，不得遗留到用户提醒后再补
```

#### `/memories/copilot-hooks.md` — Hooks 配置笔记

```markdown
# Copilot Chat Hooks 配置笔记

- 文档：https://code.visualstudio.com/docs/copilot/customization/hooks
- 配置位置：`.github/hooks/*.json`（项目级）、`~/.copilot/hooks/`（全局级）
- 事件名必须 PascalCase：SessionStart, PreToolUse, PostToolUse, Stop, SubagentStart, SubagentStop
- 需同时设 `command`（默认）+ `windows`（Windows 覆盖）；`bash` 仅映射 osx/linux

## Windows 环境
- bash.exe 在 RemoteApp 下会弹控制台窗口 → 已全部迁移到 Node.js 脚本
- hook 脚本用 `.js` + `node` 执行，子进程加 `windowsHide: true`
```

> **执行逻辑**：对每个文件先用 `memory view` 检查是否存在，不存在才用 `memory create` 创建。已有文件保持不动，不覆盖用户积累的个性化内容。

---

## Phase 6: 输出检查清单

全部文件生成后，输出最终清单：

```
✅ **AI 开发框架初始化完成**

### 已创建文件

**Hooks（自动化保障 — 6 个生命周期事件）:**
- .github/hooks/planning-with-files.json（6 事件配置）
- .github/hooks/post-tool-lint.json + post-tool-lint.js
- .github/hooks/scripts/ (8 个脚本：planning-paths, session-log, session-start, pre-tool-use, post-tool-use, subagent-start, subagent-stop, agent-stop)

**Skills（技能包）:**
- .github/skills/planning-with-files/ (SKILL.md + templates + scripts)

**Agents（专职角色）:**
- .github/agents/ ({{N}} 个 Agent 定义文件)

**Instructions（约束注入）:**
- .github/instructions/ ({{N}} 个指令文件)

**Prompts（快捷入口）:**
- .github/prompts/run-task.prompt.md

**数据层（学习闭环）:**
- .github/lessons-learned.md（教训知识库，SubagentStop 自动写入）
- .github/session-logs/（审计日志目录，已加入 .gitignore）

**记忆文件（3 层记忆体系）:**
- /memories/agent-principles.md（全局 — Agent 行为原则，首次创建）
- /memories/copilot-hooks.md（全局 — Hooks 配置笔记，首次创建）
- /memories/repo/code-style.md（仓库级 — 代码风格备忘）
- /memories/repo/execution-discipline.md（仓库级 — 执行纪律备忘）

**项目文档:**
- AGENTS.md（根级约束）
- docs/sessions/README.md

**Spec-Flow 落地目录:**
- .spec-flow/active/{{PROJECT_SLUG}}/

### 运行时保障一览

| 事件 | 脚本 | 功能 |
|------|------|------|
| SessionStart | session-start.js | 计划恢复 + 趋势分析 + 教训注入 + 日志清理 + 门控初始化 |
| PreToolUse | pre-tool-use.js | AGENTS.md 门控 + 新模块阻断 + 计划注入 |
| PostToolUse | post-tool-use.js | AGENTS.md 追踪 + 编辑记录 + 新目录提醒 + 计划更新提醒 |
| SubagentStart | subagent-start.js | 审计记录 Agent 启动 |
| SubagentStop | subagent-stop.js | 质量门禁 + 降级策略 + 教训记录 |
| Stop | agent-stop.js | AGENTS.md 同步检查 + 完成度检查 + 会话摘要 |

### 下一步

1. 🔧 根据项目实际需求完善 `AGENTS.md` 中的架构图和配置说明
2. 📝 说 **"spec-flow"** 或 **"spec mode"** 开始拆解需求
3. 🚀 需求拆解完成后，说 **/run-task T-001** 开始执行第一个任务
4. 📊 SubagentStop 会自动验证代码质量，lessons-learned.md 自动积累经验
```

---

## 静态文件内容参考

以下文件内容存放在 `templates/` 目录中，scaffold 执行时直接复制到目标项目。详见各模板文件。

### post-tool-lint.js 适配说明

模板中的 lint 脚本支持 Python（ruff）和 TypeScript（eslint）。如果项目使用其他语言/lint 工具，在 Phase 2 复制后需要修改 `post-tool-lint.js` 中的扩展名判断和工具调用。

### planning-paths.js 配置

默认 `PLANNING_ROOT = 'docs/sessions'`。如果项目需要不同的会话目录，可通过环境变量 `PLANNING_WITH_FILES_ROOT` 覆盖。

### spec-flow-run-task.instructions.md 路径

模板中使用 `{{PROJECT_SLUG}}` 占位符，需替换为实际的 spec-flow 目录名。例如 `.spec-flow/active/CMC-ARD系统/tasks.md`。
