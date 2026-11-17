# Project Memory Fallback / 项目记忆回退模块

Use this reduced-fidelity module only when `daily-workflow` is unavailable. Preserve enough factual context for the user or another agent to resume accurately.

本模块只在 `daily-workflow` 不可用时使用，保存足够的事实上下文，让用户或下一任 Agent 可以准确恢复工作。

## Ownership / 权威边界

When project governance or a coding loop is active, defer owned fields to that system. Read and summarize existing files, but do not overwrite targets, acceptance evidence, QA decisions, latest verification, stop gates, or loop records.

项目治理或编码循环处于活动状态时，不抢写它们拥有的字段。可以读取和总结现有文件，但不得覆盖目标、验收证据、QA 决定、最近验证、停止门禁或循环记录。

Persist only for an explicit start/resume, checkpoint, wrap-up, or handoff request.

只有用户明确要求开工/恢复、checkpoint、收工或交接时才持久化。

## Minimal Files / 最小文件

Reuse project-owned files. If none exist and persistence is requested, start with:

```text
Docs/STATUS.md
Docs/NEXT_ACTIONS.md
```

Add `PROJECT.md`, `TARGET.md`, `COMPLETED.md`, `PENDING.md`, `HANDOFF.md`, or `CONFIG.md` only when each has a distinct owner and purpose. Do not create `TARGET.md` from an AI guess.

复用项目已有文件。只有在没有权威体系且用户要求持久化时，才从 `STATUS.md` 和 `NEXT_ACTIONS.md` 开始。不要根据 AI 猜测创建 `TARGET.md`。

## Record / 记录内容

- current state and authority / 当前状态与权威
- user intent and decisions / 用户意图与决定
- completed work with evidence / 有证据的已完成工作
- exact commands and final outcomes / 准确命令与最终结果
- not-executed or deferred scenarios / 未执行或延后场景
- dirty worktree notes / 脏工作树说明
- pending work, blockers, risks, and Owner decisions / 待办、阻塞、风险与 Owner 决定
- exactly one immediate next action / 唯一立即下一步

Do not store secrets, full confidential content, large logs, or hidden reasoning. Preserve history; do not delete legacy files automatically.

不得保存密钥、完整机密内容、大段日志或隐藏推理。保留历史，不自动删除旧文件。
