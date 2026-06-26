---
name: feishu-parallel-dispatch
homepage: https://docs.openclaw.ai/session-tool
description: >
  Use in Feishu chats when the assistant should stay responsive while longer
  work continues in the background. Creates one spawned sub-agent task per
  substantial user prompt, keeps the foreground session short, and lets each
  child task report back independently when finished.
---

# Feishu Parallel Dispatch

Use this skill when working in Feishu and the user may send another prompt
before the current task is done.

Pair it with `feishu-progress-heartbeat` or the equivalent heartbeat pattern so
long-running child tasks can send automatic progress updates about every 3
minutes while they are still active.

## Goal

Keep the main Feishu chat responsive.

Do not let one long task occupy the foreground session when the work can be
offloaded to a spawned sub-agent.

## Core Rule

For any substantial Feishu request, prefer:

1. quick acknowledgement in the current chat
2. immediate `sessions_spawn`
3. end the current turn
4. let the child task announce its own result later

For substantial tasks, staying in the foreground without a spawned child is a
failure mode, not an acceptable fallback.

This keeps the foreground session free so the next user prompt can create its
own child task instead of waiting behind the previous one.

## When To Spawn

Spawn a child task when the request is likely to need any of these:

- web search or verification
- file creation or document generation
- multiple tool calls
- coding or debugging
- multi-step planning
- anything likely to take more than about 5-10 seconds
- any task where the user asked for periodic progress updates
- any task where the user expects the work to continue until fully complete

Do not spawn for tiny answers that can be completed immediately.

## One Prompt, One Child

Treat each substantial user prompt as its own work item.

- If task A is still running and the user sends task B, spawn another child
  task for B.
- Do not wait for A to finish before starting B.
- Do not merge unrelated prompts into one child task unless the user clearly
  asked for one combined deliverable.

## Agent Choice

Pick the child agent with the clearest fit:

- `research`: current facts, comparisons, source-backed analysis
- `office`: team planning, meeting outputs, shared project coordination
- `slides`: personal planning, solo execution, personal review work
- `family`: family-shared tasks only
- `kittypuppy`: couple-shared tasks only
- `council`: explicit multi-agent discussion
- current agent: when the task belongs to the same specialist context

## Foreground Reply Pattern

Use short Feishu-friendly acknowledgement text, for example:

- `已接单，正在开一个独立任务处理，完成后我会直接回到这个会话。`
- `这个任务我先异步跑起来，你可以继续发下一个，我会分别回报。`
- `开始处理，这条我会交给独立子任务执行，做好后直接汇报结果。`

After this acknowledgement, spawn and stop. Do not stay in the foreground
session doing the heavy work.

If the spawn fails, retry once immediately with a narrower label or a more
obvious specialist. If it still fails, tell the user plainly that the
background handoff failed and what fallback path you are taking.

Do not narrate the spawn mechanics, raw action payloads, or internal command
objects to the user.

## Completion Behavior

Each child task should report back independently when it finishes.

- Do not wait for all child tasks to finish before replying
- Do not bundle unrelated task results into one final message
- If a child task fails, report the failure for that task only
- If a child task keeps running, let it produce short 3-minute progress updates with estimated percentages instead of going silent
- If a child task disappears before the user-visible deliverable is complete,
  spawn one bounded continuation child and keep going instead of silently
  dropping the work

## Progress Queries

If the user asks:

- `还在吗`
- `哪些任务在跑`
- `第几个做完了`
- `这个是不是卡住了`

Then:

1. use `sessions_list` with tree visibility to find active child sessions
2. use `session_status` if needed
3. reply with a short per-task status list

Do not answer with a plan like "我先检查一下". Perform the status inspection
first and reply only with the result.

If the inspection shows no active child but the last explicit request is still
unfinished, immediately recreate a bounded continuation child for the missing
next step before replying.

## Labeling

When spawning, use a short `label` so later status replies are readable.

Good labels:

- `行业调研`
- `项目周报`
- `旅行计划`
- `情侣清单`
- `PPT 生成`

If helpful, choose labels that make progress checks easier to read later.
Prefer short noun phrases over vague labels like `任务` or `处理中`.

## Boundaries

- This is a dispatch pattern, not an excuse to over-spawn
- Keep one child per meaningful user request, not one child per tiny sub-step
- Do not spawn from a spawned sub-agent
- If the user explicitly wants one synchronous answer, honor that
- For long Feishu work, never let the task exist only as a foreground promise;
  there must be an active child task or a clear blocker already surfaced
