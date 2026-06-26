# Event model and steering

Claude Managed Agents is event-driven.

## Main user event types

- `user.message`
- `user.interrupt`
- `user.tool_confirmation`
- `user.custom_tool_result`

## Main agent and session events to watch

- `agent.message`
- `agent.tool_use`
- `agent.tool_result`
- `agent.mcp_tool_use`
- `agent.mcp_tool_result`
- `agent.custom_tool_use`
- `session.status_running`
- `session.status_idle`
- `session.error`
- `session.status_terminated`

## Basic send and stream loop

1. create session
2. send `user.message`
3. stream events
4. stop on `session.status_idle` or `session.error`

## Interrupt and redirect

If the agent is going sideways:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --interrupt \
  --message "Stop the audit. Focus only on the failing auth middleware."
```

This sends two events in one request:

- `user.interrupt`
- `user.message`

## Tool confirmation flow

When a tool policy is `ask`, the session may go idle waiting on approval.

Recommended flow:

1. inspect recent events
2. find the pending `agent.tool_use` or `agent.mcp_tool_use` ID
3. send an allow or deny confirmation

Allow example:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --confirm-tool-use-id tool_evt_123 \
  --confirm-result allow
```

Deny example:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --confirm-tool-use-id tool_evt_123 \
  --confirm-result deny \
  --deny-message "Do not modify files yet. Only inspect and report."
```

## Custom tool flow

When the agent calls one of your custom tools, it emits `agent.custom_tool_use` and the session goes idle.

Your job:

1. capture the `agent.custom_tool_use` event ID
2. execute the real tool in your own system
3. send back `user.custom_tool_result`

Success example:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --custom-tool-use-id custom_evt_123 \
  --custom-tool-text '{"ok":true,"temperature_f":72}'
```

Error example:

```bash
python3 ~/.openclaw/skills/claude-managed-agents/scripts/managed_agents.py \
  session send \
  --session-id sess_123 \
  --custom-tool-use-id custom_evt_123 \
  --custom-tool-text '{"ok":false,"error":"weather API timeout"}' \
  --custom-tool-is-error
```

## Streaming advice

The helper's stream command supports:

- `--until-idle`
- `--stop-on-error`
- `--jsonl`
- `--history-dedupe`

Use `--history-dedupe` when reconnecting to an already active session and you want to avoid replaying event IDs you already fetched from history.

## Operator interpretation tips

- `session.status_running` means work is in flight
- `session.status_idle` means the turn is done or waiting on you
- `session.error` includes retry status hints
- `session.status_terminated` means the session hit a terminal condition and is dead

If you need the exact pending action, read recent events instead of guessing from the session summary.
