---
name: feishu-task-control
homepage: https://docs.openclaw.ai/commands
description: >
  Use in Feishu chats when the user wants to inspect, stop, or clean up
  background tasks spawned from the current chat. Uses subagents and session
  tools to list running tasks, stop one specific task, or stop all active tasks.
---

# Feishu Task Control

Use this skill when the user wants to stop a task, cancel a background job, or
see which tasks are still running in the current Feishu chat.

## Goal

Give the user clear control over spawned background tasks.

## Built-In Commands

OpenClaw already supports these slash commands in the requester chat:

- `/subagents list` to list active child tasks
- `/subagents kill <id|#|all>` to stop one child task or all child tasks
- `/subagents info <id|#>` to inspect one task
- `/stop` to stop the current requester run and all active spawned child tasks

## Natural-Language Handling

If the user says things like:

- `结束这个任务`
- `停掉第2个任务`
- `取消那个调研`
- `把所有后台任务停掉`
- `现在有哪些任务在跑`
- `第2个任务现在到多少了`
- `给我看看每个任务的进度`

Then translate that into the right task-control action.

If the user instead says `继续`, `再试一试`, or something that clearly means
"resume the unfinished thing", do not force a task-control flow unless the
conversation is truly about stopping/inspecting tasks. First check whether the
previous request itself is unfinished.

## Workflow

### 1. Find active tasks

Use `subagents` or `sessions_list` to inspect the active child tasks for the
current requester session.

### 2. Resolve the target

Resolve the user's target in this order:

1. exact numeric id or list index
2. exact label
3. fuzzy match on the task summary
4. if still ambiguous, show the active task list and ask the user which one

### 3. Stop the right scope

- One specific child task -> `subagents kill <id>`
- All child tasks in this requester chat -> `subagents kill all`
- Entire current run plus children -> `/stop`

## Response Style

Keep Feishu replies short and explicit.

Never expose internal tool payloads, raw JSON, session ids, command objects,
or "I will now call X" narration in the user-facing reply. Perform the check or
kill action first, then answer only with the human-readable result.

If the user says `再试一试`, `继续`, or similar, do not reply with a checklist of
what you plan to inspect. Inspect it silently and reply with the actual task
status or the actual blocker.

Examples:

- `已停掉任务 #2：行业调研。`
- `已结束当前聊天里全部后台任务。`
- `当前在跑 3 个任务：#1 周报，#2 行业调研，#3 PPT 生成。`
- `当前在跑 3 个任务：#1 周报 75%，#2 行业调研 30%，#3 PPT 85%。`
- `现在有两个任务都叫“调研”，请告诉我是 #2 还是 #4。`

## Safety

- Never kill tasks from another unrelated chat unless the current tool
  visibility explicitly allows that and the user clearly asked for it
- If no matching task exists, say so directly
- If the kill fails, report the failure plainly
