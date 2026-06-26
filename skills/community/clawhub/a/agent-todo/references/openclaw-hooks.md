# OpenClaw Hooks Integration Guide

This document describes how to integrate `agent-todo` with OpenClaw hooks as an execution queue.

## Hook Scripts

`agent-todo` provides two hook scripts:

- `hooks/post_reply.sh` — convert reply commitments into executable tasks
- `hooks/heartbeat.sh` — claim the next task during heartbeat

## Installation

### 1. Copy hooks into your OpenClaw hooks directory

```bash
mkdir -p ~/.openclaw/hooks/agent-todo
cp -r ./hooks/* ~/.openclaw/hooks/agent-todo/
```

### 2. Enable hooks

If your OpenClaw setup supports a hooks enable command:

```bash
openclaw hooks enable agent-todo
```

Or configure manually:

```toml
[hooks.agent-todo]
enabled = true
path = "~/.openclaw/hooks/agent-todo"
```

## Heartbeat Integration

Add this to `HEARTBEAT.md`:

```bash
bash /path/to/agent-todo/script.sh run-pending --claim
```

Expected behavior:

- no task → `HEARTBEAT_OK`
- task found → `EXECUTE_NOW` brief is printed
- the agent should then do the task immediately
- success → mark with `done`
- blocked → mark with `block`

## Reply Hook Integration

When a reply contains a clear commitment such as “我来处理” or “我会补上”, `post_reply.sh` turns it into a structured queue item.

The generated task includes:

- `task_type`
- `source`
- `next_action`
- `success_criteria`
- inferred deadline when obvious words like 今天 / 明天 / 这周 appear

## HEARTBEAT.md Pattern

```markdown
## Agent execution queue
bash /path/to/agent-todo/script.sh run-pending --claim
```

## Cron Integration (Alternative)

```bash
# Try to claim one task every hour during work hours
0 9-18 * * * cd /path/to/agent-todo && bash ./script.sh run-pending --claim
```

## OpenClaw Cron Integration

```json
{
  "name": "agent-todo-run-pending",
  "schedule": { "kind": "cron", "expr": "0 * * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run: cd /path/to/agent-todo && bash ./script.sh run-pending --claim"
  },
  "sessionTarget": "isolated"
}
```
