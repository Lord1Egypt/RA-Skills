---
name: claude-code-team-scaffold
description: "Initialize a multi-agent AI development framework for a project on Claude Code. Creates .claude/ structure with settings.json hooks (6 lifecycle events), subagent definitions, slash commands, and the planning-with-files project skill. Sets up spec-flow landing directory and a 2-tier memory system (project + global). Use when starting a new project and wanting to set up a structured AI-assisted development workflow with code quality gates, CLAUDE.md-style synchronization discipline, and task execution pipeline. Trigger phrases: 初始化项目AI框架(Claude Code), scaffold AI framework for Claude Code, init Claude Code team, 搭建Claude Code开发框架, setup Claude Code agent workflow."
user-invocable: true
---

# Claude Code Team Scaffold

为新项目搭建完整的 Claude Code AI 辅助开发框架。把 Claude Code 从一个对话 agent 变成一个有组织、有纪律的虚拟开发团队。

## 核心理念

```
需求文档 → 设计规格 → 任务分解 → Subagent 分发执行 → 自动化保障（hooks + CLAUDE.md）
```

通过以下四层保障 AI 执行质量：

- **文件化的约束**（根 `CLAUDE.md`）— 自动加载到上下文的全局规则
- **自动化的保障**（`.claude/settings.json` hooks）— 6 个生命周期事件：上下文注入、质量门禁、降级策略
- **持久化的记忆**（`~/.claude/memory/` + `.claude/memory/`）— 弥补 AI 的上下文遗忘，自动积累教训
- **结构化的任务**（`.spec-flow/` + `tasks.md`）— 确保需求到代码的可追溯性

### 运行时生命周期

```
SessionStart ──→ PreToolUse ──→ PostToolUse ──→ SubagentStart ──→ SubagentStop ──→ Stop
     │                │               │               │                │            │
  记忆注入         路径门控       编辑追踪       审计记录       质量验证门禁     完成度检查
  日志清理         applyTo注入    新目录提醒                       降级策略        同步纪律
```

### 同步纪律（同原 AGENTS.md 全生命周期保障）

```
SessionStart → 初始化门控(.claude/.runtime/gate.json) + 编辑追踪(.claude/.runtime/edits.json)
      │
PreToolUse  → 写代码前必须先读过模块的 CLAUDE.md（门控）
      │        create_file 到无 CLAUDE.md 的新模块目录 → 阻断
      │
PostToolUse → 记录 read_file CLAUDE.md → 打开门控
      │        追踪代码 + CLAUDE.md 编辑到 .claude/.runtime/edits.json
      │        create_file 到无 CLAUDE.md 的新目录 → 软提醒
      │
Stop        → 比对 .claude/.runtime/edits.json：代码改了但 CLAUDE.md 没改 → 阻断
```

### 学习闭环

```
失败 → 自动记录(lessons-learned.md) → 统计分析(趋势) → 注入新会话 → 预防重犯
```

## 前提条件

此 skill 假设以下全局 skill 已安装：

- **spec-flow** — 需求拆解工作流（proposal → requirements → design → tasks）
- **superpowers** — 用于开发纪律

## ⚠️ 交互规则

使用**分阶段确认**工作流。每个阶段完成后等待用户确认再继续。

---

## Phase 1: 采集项目信息

向用户提出以下问题（用 AskUserQuestion）：

### 必填信息

1. **项目名称**：用于 spec-flow 目录名和 CLAUDE.md 标题（如 `CMC-ARD系统`）
2. **项目简述**：一句话描述项目做什么
3. **后端技术栈**：Python/FastAPI+Tortoise · Python/FastAPI+SQLAlchemy · Python/Django · Node.js/Express · Go/Gin · Java/Spring · 无
4. **前端技术栈**：React+TS+Antd · React+TS+MUI · Vue3+TS · Next.js · 无
5. **数据库**：Azure SQL · PostgreSQL · MySQL · SQLite · MongoDB · 无
6. **需要哪些 Agent 角色**（多选）：后端 / 前端 / AI工程师 / 测试 / 需求分析 / 架构师（只读）

### 可选信息

7. **认证方式**：SSO JWT / 自建 / 无
8. **CI/CD**：Docker Compose / GitHub Actions / Azure DevOps / 无
9. **表前缀**：数据库表名前缀
10. **代码检查工具**：ruff / eslint / 其他

### Phase 1 完成后

输出采集摘要，等用户确认。

---

## Phase 2: 生成 Hooks 配置与脚本

向目标项目 `.claude/settings.json` 写入 hooks 配置（6 个事件），并把所有 hook 脚本复制到 `.claude/hooks/scripts/`。

### 2.1 settings.json hooks 结构

事件名：SessionStart, PreToolUse, PostToolUse, SubagentStart, SubagentStop, Stop

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "node .claude/hooks/scripts/session-start.js" }] }
    ],
    "PreToolUse": [
      { "matcher": "Edit|Write|MultiEdit", "hooks": [{ "type": "command", "command": "node .claude/hooks/scripts/pre-tool-use.js" }] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write|MultiEdit", "hooks": [{ "type": "command", "command": "node .claude/hooks/scripts/post-tool-use.js" }] }
    ],
    "SubagentStart": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "node .claude/hooks/scripts/subagent-start.js" }] }
    ],
    "SubagentStop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "node .claude/hooks/scripts/subagent-stop.js" }] }
    ],
    "Stop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "node .claude/hooks/scripts/agent-stop.js" }] }
    ]
  }
}
```

### 2.2 脚本清单（从 `templates/hooks/` 复制到项目的 `.claude/hooks/scripts/`）

- `paths.js` — 路径解析
- `session-log.js` — 审计日志
- `session-start.js` — SessionStart 处理
- `pre-tool-use.js` — PreToolUse 处理
- `post-tool-use.js` — PostToolUse 处理
- `subagent-start.js` — SubagentStart 处理
- `subagent-stop.js` — SubagentStop 处理（质量门禁）
- `agent-stop.js` — Stop 处理（同步检查）

### 2.3 applyTo 指令模板

从 `templates/instructions/` 复制到项目的 `.claude/instructions/`：

- `planning-with-files.md` — applyTo: `docs/sessions/**/*`, `.spec-flow/**/*`
- `testing.md` — applyTo: `tests/**/*`, `**/*test*`, `**/*.test.*`
- `spec-flow-run-task.md` — applyTo: `.spec-flow/**/*`（占位符 `{{PROJECT_SLUG}}` 需替换）

每个文件含 YAML frontmatter 形如 `applyTo: "**/*.py"`，由 PreToolUse hook 解析并按路径匹配注入 `additionalContext`。

---

## Phase 3: 生成 CLAUDE.md（根项目约束）

将 `templates/TEMPLATE-CLAUDE.md` 复制到目标项目根，替换占位符：
- `{{PROJECT_NAME}}` · `{{PROJECT_DESCRIPTION}}` · `{{PROJECT_SLUG}}`
- 根据技术栈生成架构说明、配置管理、构建运行命令
- 注入安全合规、代码质量、测试策略、Agent 分配规则

---

## Phase 4: 生成 Subagent 定义

根据 Phase 1 选择的 Agent 角色，从 `templates/agents/` 复制对应文件到 `.claude/agents/`，替换占位符。

每个 subagent 的 frontmatter 形如：

```yaml
---
name: backend-developer
description: "后端开发专家。实现 API 端点、ORM 模型、Schema、业务服务层、后台任务。"
tools: Read, Edit, Glob, Grep, Bash, Task, TodoWrite
model: sonnet
---
```

---

## Phase 5: 生成 Slash Command

从 `templates/commands/run-task.md` 复制到 `.claude/commands/run-task.md`。frontmatter 必含：

```yaml
---
description: "..."
argument-hint: "Task ID, e.g. T-008"
---
```

命令体内用 `$ARGUMENTS` 接收任务 ID。

---

## Phase 6: 初始化 Spec-Flow 落地目录

创建空目录 `.spec-flow/active/{{PROJECT_SLUG}}/`。不创建 proposal.md 等文件——由 spec-flow skill 在执行时生成。

---

## Phase 7: 初始化双层记忆

### 项目级（在仓库内，跟随 git）

```
.claude/memory/
├── code-style.md              # 空模板，使用中积累代码风格约定
└── execution-discipline.md    # 空模板，使用中积累执行教训
```

### 全局级（用户家目录，跨项目）

```
~/.claude/memory/
├── agent-principles.md        # Agent 行为原则
└── hooks-config.md            # Claude Code hooks 配置笔记
```

`~/.claude/CLAUDE.md` 已存在则追加 hook 章节，否则创建。

---

## Phase 8: 输出检查清单

打印已创建文件清单与下一步指引（spec-flow 拆需求 → /run-task T-001 执行 → SubagentStop 自动验证）。

---

## 与原版关键差异

1. **AGENTS.md → CLAUDE.md**：根约束文件用 CLAUDE.md（Claude Code 原生、自动加载）
2. **Hook 配置位置**：`.github/hooks/*.json` → `.claude/settings.json` 单一文件
3. **Hook 脚本接口**：字段名 `tool_input` 而非 `tool_args`；阻断用 JSON `{"decision":"block"}` 而非 exit 2
4. **Agent 工具列表**：`[read, edit, search, execute, agent, todo]` → `Read, Edit, Glob, Grep, Bash, Task, TodoWrite`
5. **Prompt → Slash Command**：`.github/prompts/*.prompt.md` → `.claude/commands/*.md`（`$ARGUMENTS` 接收参数）
6. **applyTo 指令注入**：从 frontmatter 字段 → PreToolUse hook 路径匹配 + `additionalContext` 输出
7. **记忆双层**：项目 `.claude/memory/`（git 追踪） + 全局 `~/.claude/memory/` + `~/.claude/CLAUDE.md`