# Project Memory / 项目记忆工作流

## Role / 角色

This module preserves project context so the user or another AI can resume work accurately.

本模块保存项目上下文，让用户或下一任 AI 可以准确恢复工作。

## Core Files / 核心文件

```text
Docs/PROJECT.md
Docs/TARGET.md
Docs/STATUS.md
Docs/COMPLETED.md
Docs/PENDING.md
Docs/NEXT_ACTIONS.md
Docs/HANDOFF.md
Docs/CONFIG.md
Docs/archive/YYYY-MM.md
```

## Workflow / 工作流程

### Start Work / 开工

Read existing project files. If none exist, create the minimum project memory set.

读取现有项目文件。如不存在，创建最小项目记忆文件组。

### Checkpoint / 中段检查

Update current status, decisions, blockers, and next actions.

更新当前状态、已做决策、阻碍和下一步。

### Wrap Up / 收工

Summarize completed work, pending work, risks, next actions, and handoff notes.

总结已完成、待办、风险、下一步和交接信息。

### Handoff / 交接

Create a compact, actionable handoff note for the next AI or human.

为下一任 AI 或人员创建简洁可执行的交接说明。

## Legacy Migration / 旧版迁移

If legacy Daily Workflow files exist, migrate by mapping:

如果发现旧版 Daily Workflow 文件，按以下方式迁移：

```text
PROJECT_TARGET.md  -> TARGET.md
PROJECT_STATUS.md  -> STATUS.md
COMPLETED_JOBS.md  -> COMPLETED.md
PENDING_JOBS.md    -> PENDING.md
NEXT_STEPS.md      -> NEXT_ACTIONS.md
SCHEDULE.md        -> NEXT_ACTIONS.md or compatibility alias
```

Do not delete old files automatically.

不要自动删除旧文件。
