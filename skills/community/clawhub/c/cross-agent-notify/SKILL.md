---
name: cross-agent-notify
description: "Standard cross-agent notification and collaboration protocol for OpenClaw multi-agent setups. Use when: (1) one agent needs to delegate a task to another agent, (2) an agent completes work and needs to hand off to another agent, (3) an agent needs to wake up another agent for input or assist, (4) reviewing or auditing cross-agent collaboration consistency. Triggers on phrases like '通知xagent', 'handoff to agent', 'wake up agent x', 'cross-agent协作', '委托任务给其他agent'."
---

# Cross-Agent Notify

## What This Skill Does

Provides the standard cross-agent notification workflow for OpenClaw: how to reliably wake up another agent, delegate tasks, receive results, and trace progress in the Feishu group.

**Core problem solved:** `sessions_send` times out when the target agent's main session is `done`. The `agent:<target>:main` format solves this by activating the agent's persistent session layer regardless of main session state.

## Standard Collaboration Chain

```
任务文件 → inbox 消息 → sessions_send agent:<target>:main → 对方处理 → 结果回写 inbox → 飞书群 trace
```

Four mandatory steps (all four required, in order):

1. **Update task file** — set `communication` fields, `owner`, `status`
2. **Write inbox message** — drop a structured `.txt` file to `shared/inbox/<target_agent>/`
3. **Send wakeup** — `sessions_send` to `agent:<target_agent>:main`
4. **Trace in Feishu group** — post a one-line `@target_agent task TASK-xxx` in `agent:<agent_id>:feishu:group:oc_8efe2b5fdf1ed5939c93f206b5c0e21e`

## Step 1 — Update the Task File

Before sending anything, update the shared task file:

```markdown
owner: target_agent
status: in_progress
communication:
  reply_to_agent: requesting_agent   # always set; never hardcode a name
  submitter_agent: requesting_agent
```

**Rule:** Always set `communication.reply_to_agent`. Never hardcode the requesting agent's name as the reply target.

## Step 2 — Write the Inbox Message

Create a text file at:
```
shared/inbox/<target_agent>/YYYY-MM-DD-HHMM-task-description.txt
```

Minimum required content:
```markdown
# 任务：<task name>
**时间:** YYYY-MM-DD HH:MM GMT+8
**来源:** requesting_agent
**回复给:** target_agent
**任务文件:** shared/tasks/<task-id>.md
---
## 任务内容
<concise description of what is needed>

## 完成后
请将结果回写到任务文件，并将完成状态通知 requesting_agent。
```

## Step 3 — Send the Wakeup

```python
sessions_send(
    sessionKey=None,          # leave blank; target is by agentId
    agentId="<target_agent>"  # e.g. "agent-a", "agent-b"
    message="task TASK-xxx assigned to you, check inbox"
)
```

**Target format:** `agent:<target_agent>:main` — the agent's persistent session layer, works even when the main session is `done`.

**Key finding:** `agent:<target>:main` format successfully activates agents whose main sessions are `done`. This bypasses the `sessions_send timeout` problem.

**Never use** the old Telegram-based group protocol — it is deprecated (2026-04-06).

## Step 4 — Feishu Group Trace

Post a short trace message to the shared Feishu group. Get the stable group session key from the target agent's SKILL.md or team config. Example:

```
@target_agent task TASK-123，已投 agent:target_agent:main，查 inbox
```

Use only the approved one-line templates (see `references/PROTOCOL.md` for full list). Keep it short — the inbox carries full context, not the group message.

**Group session key pattern:**
```
agent:<agent_id>:feishu:group:oc_8efe2b5fdf1ed5939c93f206b5c0e21e
```

## Receiving a Notification

When your inbox is mentioned or `sessions_send` wakes you:

1. Read the inbox message file first
2. Read the linked task file
3. Perform the work
4. Write results back to the task file (`review` field, evidence field)
5. Drop a completion note in the requester's inbox
6. Post a result trace in the Feishu group

**Do not** skip the task file and inbox — they are the source of truth.

## Communication Field Rules

```yaml
communication:
  reply_to_agent: <agent_id>   # mandatory; who to send receipts/results back to
  submitter_agent: <agent_id>   # who initiated the request
```

- `reply_to_agent` must always be set to a named agent ID, never a session ID
- Use `agent:<target>:main` format in `sessions_send`, not session keys
- If `submitter_agent` is missing, fall back to `owner_agent`

## Reference

See `references/PROTOCOL.md` for:
- Full one-line template library (wakeup, assist, handoff, result return, blocked, audit request)
- Feishu group mention validity rules
- Fixed group target and session key pattern
- Deprecated Telegram protocol notice
