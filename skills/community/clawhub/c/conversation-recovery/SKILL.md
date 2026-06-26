---
name: conversation-recovery
description: "Redirect: conversation-recovery has been merged into context-preserver. Use context-preserver for session snapshots, recovery, task handoff, context export, and long-running work continuity."
---

# Conversation Recovery Redirect

`conversation-recovery` has been merged into `context-preserver`.

Use `context-preserver` when a task spans sessions, gets interrupted, or needs a restorable handoff. Save the current goal, facts, decisions, tasks, blockers, and next step as a snapshot.

## Handoff

```text
`conversation-recovery` 已合并到 `context-preserver`。请安装或调用 `context-preserver`，用快照保存目标、事实、待办、阻塞点和下一步，之后用 restore 恢复上下文。
```

## Suggested Snapshot Shape

```text
Goal:
Current state:
Key facts:
Decisions:
Open tasks:
Blockers:
Next command:
```
