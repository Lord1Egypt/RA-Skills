---
name: feishu-progress-heartbeat
homepage: https://github.com/wd041216-bit/openclaw-feishu-progress-heartbeat
description: >
  Use in Feishu when long-running tasks should proactively report progress every
  3 minutes. Pairs heartbeat-driven follow-ups with session status checks so
  active tasks send short status updates with estimated percentages instead of
  staying silent.
---

# Feishu Progress Heartbeat

Use this skill when a Feishu task should continue to feel alive after it has
been spawned or delegated.

## Goal

Turn long-running work into a visible flow:

1. immediate acknowledgement
2. background execution
3. automatic progress heartbeat every 3 minutes while still running
4. final result when finished

## Where it applies

- `main`
- `research`
- `office`
- `slides`
- `council`
- `family`
- `kittypuppy`

## Required behavior

When a heartbeat fires and there are still active tasks in the current Feishu
session:

1. inspect active child tasks with `sessions_list`, `subagents`, or `session_status`
2. infer the most likely current stage for each active task
3. send a short progress update back to the same Feishu conversation
4. include an estimated percentage for each task
5. if a task looks stalled, failed, or has shown no meaningful movement for two heartbeat cycles, send a blocker update instead of another generic progress line

If there is no active task, no meaningful state change, or no useful update,
reply `HEARTBEAT_OK`.

If there is no active child task and no fresh continuation branch was launched,
do not emit a fake progress update just to sound alive.

Do not expose internal session inspection details, raw tool payloads, or
command objects in a heartbeat reply. Only send the user-facing status line.

## Percentage mapping

Use short stage labels and one estimated percentage:

- `已接单` -> `5%`
- `排队中` -> `10%`
- `搜索中` / `收集资料中` -> `25%`
- `整理中` / `分析中` -> `55%`
- `生成文件中` / `写作中` / `制作 PPT 中` -> `80%`
- `等待外部工具` -> `60%`
- `疑似卡住` / `长时间无进展` -> `65%`
- `收尾中` / `准备回复` -> `95%`
- `已完成` -> `100%`
- `执行失败` -> `0%`

These numbers are estimates. Say so naturally when helpful, but do not over-explain.

## Reply format

Prefer Feishu-friendly short lines:

- `进度播报：行业调研 正在整理，约 55%。`
- `进度播报：PPT 生成中，约 80%。`
- `进度播报：#1 行业调研 55%；#2 周报 80%。`
- `阻塞提醒：PPT 导出连续两轮无进展，我正在切换导出路径。`
- `阻塞提醒：调研任务疑似卡住在外部工具，我先回你当前已完成部分。`

If several tasks are running, keep the list compact and readable.

## Guardrails

- Do not send heartbeat updates for tiny tasks that already finished quickly.
- Do not invent exact progress meters; use stage-based estimates.
- Do not spam if nothing meaningful changed.
- If a task is blocked, say what it is waiting on in one short clause.
- Do not repeat the same optimistic progress line forever.
- If the stage is unchanged for two heartbeat cycles, treat it as a stall candidate and surface a blocker or fallback action.
- Do not send meta lines like "我先检查一下当前任务状态". Do the check first, then send the result.
- Do not send a percentage-only progress claim unless there is actual evidence
  that the task is still running or has just been restarted.

## Pairing

Use together with:

- `feishu-parallel-dispatch`
- `feishu-task-status`
- `hierarchical-task-spawn` when one task becomes a task tree
