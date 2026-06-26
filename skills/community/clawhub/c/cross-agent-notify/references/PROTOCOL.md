# Cross-Agent Notification Protocol — Full Reference

Last updated: 2026-04-06

## Purpose

- Feishu group is the primary agent-to-agent public trace and coordination channel.
- Feishu private chat remains the primary user-to-agent private channel.
- **Main session + task file + inbox is the real execution chain.**

## Fixed Group Target

- Shared Feishu group label: `oc_8efe2b5fdf1ed5939c93f206b5c0e21e`
- Stable per-agent group session key pattern: `agent:<agent_id>:feishu:group:oc_8efe2b5fdf1ed5939c93f206b5c0e21e`
- Use this only for short public trace messages — not for full task delivery.

## Standard Collaboration Chain

```
任务文件 → inbox → agent:<target_agent>:main → 处理 → 结果回写 inbox → 飞书群 trace
```

**Execution always targets:** `agent:<target_agent>:main` — the persistent session layer, works even when main session is `done`.

**Feishu `@target_agent`** is only a short public trace, not the sole delivery path.

## One-line Summary

> Feishu group leaves trace, `agent:<target>:main` takes the work, task file and inbox carry context.

## Step-by-Step Workflow

### Step 1 — Update Task File

Before sending, update the shared task file:

```markdown
owner: target_agent
status: in_progress
communication:
  reply_to_agent: requesting_agent
  submitter_agent: requesting_agent
```

### Step 2 — Write Inbox Message

Drop a structured file to `shared/inbox/<target_agent>/YYYY-MM-DD-HHMM-task-description.txt`:

```markdown
# 任务：<task name>
**时间:** YYYY-MM-DD HH:MM GMT+8
**来源:** requesting_agent
**回复给:** target_agent
**任务文件:** shared/tasks/<task-id>.md
---
## 任务内容
<concise description>

## 完成后
请将结果回写到任务文件，并将完成状态通知 requesting_agent。
```

### Step 3 — sessions_send Wakeup

```python
sessions_send(
    agentId="<target_agent>"  # e.g. "agent-a", "agent-b"
    message="task TASK-xxx assigned to you, check inbox"
)
```

**Critical finding:** `agent:<target>:main` format successfully wakes agents even when their main session is `done`. This solves the `sessions_send timeout` problem that occurs with session-key-based targeting.

### Step 4 — Feishu Group Trace

Post a one-line trace to `agent:<your_agent_id>:feishu:group:oc_8efe2b5fdf1ed5939c93f206b5c0e21e`:

```
@target_agent task TASK-123，已投 agent:target_agent:main，查 inbox
```

## Feishu One-Line Templates

### Wakeup / Delegate
```
@target_agent task TASK-123，已投 agent:target_agent:main，查 inbox
```

### Assist
```
@target_agent task TASK-123，协助处理，查 inbox
```

### Need Input
```
@target_agent task TASK-123，补充输入，查 inbox
```

### Handoff
```
@target_agent task TASK-123，交接给你，查 inbox
```

### Result Return
```
@target_agent task TASK-123，结果已回，查 inbox
```

### Blocked
```
@target_agent task TASK-123，当前阻塞，查 inbox
```

### Audit Request
```
@<auditor_agent> task TASK-123，提审，查 inbox
```

### Audit Result
```
@target_agent task TASK-123，审计结果已回，查 inbox
```

## Feishu Reply Templates

### Receipt
```
收到，查 inbox
```

### Done
```
已处理，结果已回 inbox
```

### Blocked
```
已查看，当前阻塞，细节见 inbox
```

## Mention Validity Rules

Treat the message as a valid wakeup if **any one** of the following is true:
1. Feishu message body contains a real mention tag
2. Message metadata contains `was_mentioned: true`
3. System annotation says the mention targets the current agent

If any of the above is true, the agent **must not** treat the message as unaddressed.

## Group Rules

- If you were not explicitly mentioned, do not reply in the group
- Keep group messages short and operational
- Do not put full business context in the group
- Do not treat a group wakeup as the only evidence
- Do not treat a group `@` as the real execution target
- If you need to publish a trace yourself, send to your own stable group session key:
  `agent:<your_agent_id>:feishu:group:oc_8efe2b5fdf1ed5939c93f206b5c0e21e`

## Deprecated: Telegram Group Protocol

**Status:** DEPRECATED as of 2026-04-06

The Telegram-based agent group collaboration protocol (`TELEGRAM-AGENT-GROUP-PROTOCOL`) is no longer in use. Do not use Telegram as a collaboration channel between agents.

## Key Discoveries

1. **`agent:<target>:main` format works when main session is `done`** — The persistent session layer (`main`) activates agents regardless of main session state, solving `sessions_send timeout` failures.

2. **Always set `communication.reply_to_agent`** — Prevents hardcoded reply targets that break when agents change or sessions reset.

3. **Inbox is the source of truth, Feishu is the trace** — Full context lives in task files and inbox; Feishu only carries short operational signals.

4. **Task file is mandatory for all cross-agent work** — No task file means no audit trail, no accountability, no review chain.
