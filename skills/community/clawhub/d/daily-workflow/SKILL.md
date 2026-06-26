---
name: daily-workflow
description: "Bilingual EN/ZH project memory workflow for start work, checkpoint, wrap-up, and handoff. Maintains project-local Docs/ notes with target, metadata, status, compressed context, completed work, pending work, next actions, archives, and legacy migration from older Daily Workflow file names."
---

# Daily Workflow / 项目记忆工作流

Version: 3.0.0  
Purpose: keep a project understandable and resumable across work sessions, context resets, and AI-to-AI handoffs.  
Storage: project-local `Docs/` only.
Upgrade note: This is the upgraded version of the previous Chinese and English Daily Workflow editions; going forward, both language editions will be maintained together in this single bilingual package. / 这是此前中文与英文 Daily Workflow 两版的升级版；以后中英文版本会合并在这个双语包里统一维护。

## Core Principle / 核心原则

Write concise, factual project state that a user and the next AI can continue from. Prefer concrete targets, decisions, files, commands, blockers, risks, and next actions over narrative.

记录应当简洁、可验证、可继续执行。优先保存目标、决策、文件路径、命令结果、阻塞、风险和下一步，而不是聊天记录全文。

Do not record secrets, credentials, private customer data, full confidential documents, large logs, or unrelated source excerpts.

## Trigger Phrases / 触发语

Treat these phrases as equivalent triggers:

- Start work / 开工: `开工啦`, `开始工作`, `start work`, `begin work`, `starting work`, `start of day`
- Checkpoint / 中段检查: `中段检查`, `吃饭啦`, `checkpoint`, `lunch check`, `lunch time`, `break time`, `midday check`
- Wrap up / 收工: `收工啦`, `结束工作`, `wrap up`, `end work`, `ending work`, `end of day`
- Handoff / 交接: `交接`, `handoff`, `next AI`, `下一任 AI`
- Reconfigure / 重新配置: `重新配置工作流`, `configure workflow`, `update workflow config`

If the user defines custom triggers in `Docs/CONFIG.md`, honor them.

## Managed Files / 管理文件

Create `Docs/` if missing. Maintain these files:

- `Docs/PROJECT.md`: project metadata, owner, workspace, repository, phase, language, and last checkpoint.
- `Docs/TARGET.md`: project purpose, success criteria, scope, and out-of-scope items. Default read-only after creation unless the user changes the goal.
- `Docs/STATUS.md`: current state, progress, active context, compressed context, latest update history, and known risks.
- `Docs/COMPLETED.md`: completed work log. Append only; never overwrite older entries.
- `Docs/PENDING.md`: current pending work, blockers, and decisions needed. May be rewritten as the current queue while preserving unresolved blockers.
- `Docs/NEXT_ACTIONS.md`: immediate continuation plan and handoff plan. Overwrite each checkpoint/wrap-up with the latest actionable plan.
- `Docs/CONFIG.md`: optional trigger and language preferences.

Compatibility alias:

- `Docs/SCHEDULE.md` is a legacy/current alias for next actions. If it exists, read it. Prefer writing `NEXT_ACTIONS.md` in v3.0.0. If a project already depends on `SCHEDULE.md`, either keep both synchronized or explain the migration before changing.

Optional files:

- `Docs/HANDOFF.md`: create only when the user asks for a standalone handoff file or when the handoff block becomes too long.
- `Docs/archive/YYYY-MM.md`: monthly archive for older status updates.

## Configuration / 配置

Optional configuration is project-local:

```text
Docs/CONFIG.md
```

Default config block:

```json
{
  "version": "3.0.0",
  "startPhrase": "开工啦",
  "checkpointPhrase": "中段检查",
  "lunchPhrase": "吃饭啦",
  "endPhrase": "收工啦",
  "handoffPhrase": "交接",
  "language": "bilingual",
  "primaryNextActionsFile": "NEXT_ACTIONS.md",
  "archiveAfterStatusEntries": 10,
  "firstRun": false
}
```

Create or update config only inside `Docs/`. Do not write global user state.

## Legacy Migration / 旧版迁移

Before creating new files, check for legacy Daily Workflow files.

Legacy English v1 names:

```text
Docs/PROJECT_TARGET.md      -> Docs/TARGET.md
Docs/PROJECT_STATUS.md      -> Docs/STATUS.md
Docs/COMPLETED_JOBS.md      -> Docs/COMPLETED.md
Docs/PENDING_JOBS.md        -> Docs/PENDING.md
Docs/NEXT_STEPS.md          -> Docs/NEXT_ACTIONS.md
.workbuddy/daily-workflow-config.json -> Docs/CONFIG.md
```

Legacy v2/current alias:

```text
Docs/SCHEDULE.md -> Docs/NEXT_ACTIONS.md
```

Migration rules:

1. Read legacy files before creating replacements.
2. If the v3 target file is missing, create it from the legacy content and add `Migrated from: <legacy file>`.
3. If both legacy and v3 files exist, do not overwrite. Summarize the difference and ask the user whether to merge.
4. Never delete legacy files automatically.
5. Never migrate secrets or secret-like fields.
6. Add a migration entry to `STATUS.md` or `Docs/archive/YYYY-MM.md`.

## File Templates / 文件模板

### PROJECT.md

```markdown
# Project Metadata / 项目元数据

- Project ID / 项目编号:
- Project Name / 项目名称:
- Owner / 负责人:
- Workspace / 工作区:
- Repository / 代码仓库:
- Current Phase / 当前阶段:
- Primary Language / 主要语言:
- Risk Level / 风险等级:
- Last Checkpoint / 最近检查点:
- Last Updated / 最近更新:
```

### TARGET.md

```markdown
# Project Target / 项目目标

## Purpose / 目的
[What the project is trying to accomplish.]

## Success Criteria / 成功标准
- [Criterion 1]
- [Criterion 2]

## Scope / 范围
In scope / 范围内:
- [Item]

Out of scope / 范围外:
- [Item]

## Assumptions / 假设
- [Assumption]

## Last Reviewed / 最后确认
[YYYY-MM-DD]
```

If the target is unclear, create a provisional section instead of stopping:

```markdown
## Unconfirmed Target / 待确认目标
[Best-effort summary based on current context. Ask the user to confirm or correct.]
```

### STATUS.md

```markdown
# Project Status / 项目状态

## Current State / 当前状态
[Short factual summary.]

## Progress / 进度
[Percent or milestone-based progress when known.]

## Active Context / 当前上下文
- Files or areas being worked on:
- Important constraints:
- Known risks:

## Compressed Context / 提炼上下文
- User intent / 用户意图:
- Decisions made / 已作决策:
- Current state / 当前状态:
- Completed work / 已完成:
- Pending work / 待处理:
- Blockers / risks / 阻塞与风险:
- Files touched / 涉及文件:
- Commands/tests run / 已运行命令或测试:
- Immediate next action / 下一步立即行动:

## Update History / 更新历史
### [YYYY-MM-DD HH:mm] [start/checkpoint/wrap-up/handoff/migration]
- [What changed]
- [Evidence, command, or file reference when useful]
```

### COMPLETED.md

```markdown
# Completed Jobs / 已完成工作

## [YYYY-MM-DD]
- [Completed item with enough detail for another AI to understand what changed.]
```

### PENDING.md

```markdown
# Pending Jobs / 待办工作

## Immediate / 立即处理
- [ ] [Task, owner/context if known, acceptance condition]

## Later / 稍后处理
- [ ] [Task]

## Blockers and Decisions / 阻塞与待决策
- [Blocker or decision needed]
```

### NEXT_ACTIONS.md

```markdown
# Next Actions / 下一步行动

## Immediate Next Action / 下一步立即行动
1. [Action with file/path/context]
2. [Action]

## Handoff Summary / 交接摘要
- Current state / 当前状态:
- Completed since last checkpoint / 上次检查后完成:
- Pending work / 待处理:
- Blockers / risks / 阻塞与风险:
- Files touched / 涉及文件:
- Commands/tests run / 已运行命令或测试:
- Immediate next action / 下一步立即行动:

## Notes for Next AI / 给下一任 AI 的说明
[Any context the next AI must know before acting.]
```

## Context Compression and Reset / 上下文提炼与清理

At checkpoint, wrap-up, and handoff time, compress the current conversation context before updating workflow files.

Compression means extracting only what is needed to continue work:

- Current user intent and target
- Decisions already made
- Completed work
- Pending work
- Blockers, risks, and assumptions
- Files touched or important paths
- Commands/tests run and outcomes
- Immediate next action

Write this into `Docs/STATUS.md` under the latest update entry and into `Docs/NEXT_ACTIONS.md` for continuation. Do not paste the full conversation transcript.

After saving compressed context, treat the old long working context as cleared for workflow purposes. Continue from `STATUS.md` and `NEXT_ACTIONS.md`.

For checkpoint only, return the compressed context to the current AI in the response so work can continue immediately.

## Start Work Flow / 开工流程

When triggered by start work:

1. Check `Docs/`; create missing managed files from templates.
2. Detect and offer legacy migration when legacy files exist.
3. Check `Docs/CONFIG.md`; honor it if present.
4. Read all managed files and compatible legacy aliases.
5. Summarize target, metadata, current status, recently completed work, pending work, blockers, and immediate next action.
6. If target is missing or unclear, create or preserve an `Unconfirmed Target` section and ask the user to confirm or correct it.
7. Update `STATUS.md` with a start entry.
8. Refresh `NEXT_ACTIONS.md` only if next steps are missing, stale, or contradicted by the user.

## Checkpoint Flow / 中段检查流程

When triggered by checkpoint or lunch check:

1. Compress the current conversation into a concise continuation summary.
2. Append completed items to `COMPLETED.md`.
3. Update `PROJECT.md` last checkpoint and phase if known.
4. Update `STATUS.md` with current state, progress, risks, commands/tests run, and compressed context.
5. Rewrite `PENDING.md` as the current queue while preserving unresolved blockers.
6. Rewrite `NEXT_ACTIONS.md` with the latest continuation and handoff block.
7. Archive older `STATUS.md` entries if the configured threshold is exceeded.
8. Return the compressed context plus the immediate next action.

## Wrap Up Flow / 收工流程

When triggered by wrap up:

1. Compress the current conversation into an end-of-session summary.
2. Append all completed work to `COMPLETED.md`.
3. Update `PROJECT.md` last checkpoint and phase if known.
4. Update `STATUS.md` with final state, commands/tests run, risks, and compressed context.
5. Update `PENDING.md` with unfinished work, blockers, and decisions needed.
6. Update `TARGET.md` only if the goal changed or the user explicitly asks.
7. Rewrite `NEXT_ACTIONS.md` as the main handoff document.
8. Archive older `STATUS.md` entries if needed.
9. Give the user a short wrap-up summary and the immediate next action for the next session.

## Handoff Flow / 交接流程

When triggered by handoff:

1. Read the managed files.
2. Compress the current conversation into a concise handoff summary.
3. Update `PROJECT.md`, `STATUS.md`, and `NEXT_ACTIONS.md`.
4. Include only actionable context: current state, completed work since last checkpoint, pending tasks, blockers and risks, touched files, commands/tests run and outcomes, and immediate next action.
5. Treat previous long context as cleared for workflow purposes.
6. Do not invent results that were not observed.
7. Create `Docs/HANDOFF.md` only if the user asks for a separate handoff artifact.

## Archive Policy / 归档规则

Keep `STATUS.md` readable.

- Keep the latest 5-10 update entries in `STATUS.md`, using `archiveAfterStatusEntries` from config when available.
- Move older update entries to `Docs/archive/YYYY-MM.md`.
- Never delete history.
- Add archive notes with source file, date range, and reason.

## Write Rules / 写入规则

- Use absolute paths when reporting file locations to the user.
- Append to `COMPLETED.md`; do not overwrite it.
- Preserve `STATUS.md` update history unless archiving older entries.
- Preserve unresolved blockers when rewriting `PENDING.md`.
- Overwrite `NEXT_ACTIONS.md` at each checkpoint or wrap-up so the next AI has a single current plan.
- Never delete managed or legacy files automatically.
- Do not edit files outside `Docs/` for this workflow unless the user's broader task requires it.

## Safety Rules / 安全规则

Do not write:

- API keys, tokens, passwords, cookies, private keys, `.env` values, or browser sessions.
- Full private customer records or confidential source text.
- Sensitive security findings beyond concise status summaries.
- Large unrelated logs.

If important context contains sensitive details, summarize safely and refer to the secure source location only when appropriate.

## User Response Style / 用户反馈格式

Keep responses short and useful:

```text
Saved workflow state.
- Updated: PROJECT.md, STATUS.md, NEXT_ACTIONS.md
- Appended: COMPLETED.md
- Pending: 3 items, 1 blocker
- Next: run the failing test and inspect the parser change
```
