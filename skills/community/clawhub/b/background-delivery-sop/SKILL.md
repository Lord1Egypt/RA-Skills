---
name: background-delivery-sop
description: Standardize how agents handle tasks that run in the background, via sub-agents, or via ACP sessions, so completed work is always proactively delivered back to the user. Use when creating or improving agent workflows for async/background execution, fixing cases where results finish but are not sent, or teaching another agent how to do receipt → execution → final delivery without making the user chase for updates.
---

# Background Delivery SOP

Use this skill to enforce a simple rule: **if work finishes in the background, the user should not have to ask for the result.**

This skill is for orchestration and delivery discipline, not for the task domain itself.

## Core Rule

Treat every background completion as a **delivery obligation**.

If a task was delegated to:
- a background run,
- a sub-agent,
- an ACP session,
- or any async workflow,

then the parent / main agent must actively close the loop with the user.

## 5-Line SOP

1. **If no tools are needed, answer in the main session.**
2. **If tools are needed, run in background instead of expanding execution in the main session.**
3. **Send exactly one short start acknowledgment.**
4. **When background work completes, proactively deliver the result / progress / blocker.**
5. **Do not wait for the user to ask again unless the completion adds nothing new.**

## Delivery States

When a background task returns, classify it into exactly one of these states and act immediately.

### 1. Final result available
Send the final result now.

Use when:
- the requested work is complete,
- the user can act on the answer immediately,
- no further confirmation is required.

Output pattern:
- concise conclusion,
- essential evidence or summary,
- next step only if useful.

### 2. Partial progress available
Send a progress update now.

Use when:
- work is not fully complete,
- but there is meaningful progress,
- or the user benefits from seeing interim findings.

Output pattern:
- what is done,
- what remains,
- expected next step / ETA if known.

### 3. Blocked
Send the blocker now.

Use when:
- approval is needed,
- input is missing,
- permissions or environment prevent completion,
- or an external dependency failed.

Output pattern:
- what is blocked,
- why,
- exactly what the user needs to provide or approve.

## Required Two-Phase Pattern

Use this fixed pattern for background work:

### Phase 1: Start acknowledgment
Send one short message when the task begins.

Examples:
- "我去后台查，查完主动回你。"
- "我先放后台跑，完成后直接给你结果。"
- "我去处理，完成后我会主动同步。"

Rules:
- send it once,
- keep it short,
- do not repeat synonymous "already working on it" messages.

### Phase 2: Completion delivery
When the background task completes, send exactly one substantive follow-up:
- final result,
- meaningful progress,
- or blocker.

Never leave the task in a state where:
- the start acknowledgment was sent,
- the background run completed,
- but no user-facing delivery followed.

## Completion Event Handling

When a completion event reaches the main agent, default to this interpretation:

> This is not just internal orchestration data. This is pending user delivery.

So the default action is:
- **deliver**, not ignore;
- **summarize**, not dump raw internal logs;
- **close the loop**, not wait for another prompt.

## When `NO_REPLY` Is Allowed

Only allow silence if at least one of these is true:

1. The returned content is materially identical to what the user already received.
2. The user has already received an equivalent final answer.
3. The agent is suppressing a duplicate internal event and will immediately send the proper delivery message.

If none of those are true, do **not** swallow the completion.

## Anti-Patterns

Avoid these failure modes:

- Background task completes, but the agent says nothing.
- Main session treats completion as internal-only and never converts it into a user-facing update.
- Agent waits for "any update?" before sending finished work.
- Agent sends multiple start acknowledgments but no real completion delivery.
- Agent dumps raw internal status instead of a cleaned user-facing answer.

## Quick Decision Tree

### If the user asks a simple question and no tools are needed
Answer directly in the main session.

### If tools or multi-step work are needed
Move execution to background / sub-agent / ACP as appropriate.

### After spawning or delegating
Send one short acknowledgment.

### When the async work finishes
Ask:
- Is there a final result? → deliver it.
- Is there useful progress? → send it.
- Is there a blocker? → explain it.
- Is it only duplicate noise? → silence is allowed.

## Minimal Handoff Template For Other Agents

Use this template when teaching another agent or building a workflow rule:

> If you move work into the background, you own the final delivery. Send one short acknowledgment when work starts. When the background task completes, proactively send either the final result, a meaningful progress update, or a blocker. Do not wait for the user to ask again unless the completion is truly duplicate.

## Success Criteria

This SOP is being followed if:
- users do not need to chase completed work,
- background tasks consistently end with proactive delivery,
- start acknowledgments are short and non-repetitive,
- completion events are converted into clean user-facing updates.

## Adaptive Thinking Profile

Use task-level adaptive thinking instead of trying to hot-switch the main conversation constantly.

Recommended mapping:
- **Normal chat / simple direct answers** → `off`
- **Routine tool tasks / short checks** → `low`
- **Multi-step analysis / complex diagnosis / multi-source research** → `medium`
- **Programming / code changes / engineering debugging / ACP coding harness work** → `high`

Recommended operating pattern:
- keep the **main session** lightweight by default,
- raise thinking mainly in **background runs, sub-agents, or ACP sessions**, not through frequent main-session toggling.

## 中文极简版

适合直接教给中文 agent 的一句话原则：

> 只要任务转入后台、sub-agent 或 ACP 执行，完成后就必须主动把结果发给用户；不要等用户追问。

### 中文 5 行 SOP

1. **不用工具**：主会话直接答。  
2. **需要工具**：默认后台执行。  
3. **启动时**：只发一次简短回执。  
4. **完成后**：主动发结果 / 进度 / 卡点。  
5. **非重复内容**：禁止等用户追问才回复。  

### 中文交付口径

后台任务完成后，主会话必须三选一：
- **有最终结果** → 直接交付结果
- **有阶段进度** → 主动同步进度
- **被阻塞** → 主动说明卡点和所需确认

### 中文反模式

以下都算没按 SOP 执行：
- 后台做完了但不发
- 用户不追问就不回
- 连续发“在处理”但不给结果
- 把完成事件当内部消息吞掉
