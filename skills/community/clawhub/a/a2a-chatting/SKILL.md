---
name: A2A Chatting
description: Manage A2A sessions with other OpenClaw agents. Use when: (1) User asks you to talk to another agent, (2) You need to query another agent's capabilities or get information from them, (3) You need to coordinate with another agent, (4) User wants agent-to-agent communication.
version: 0.4.0
---

# A2A Chatting

Manage sessions with other OpenClaw agents. **Messaging is done via the built-in `sessions_send` tool**, not via the CLI. This CLI only handles session lifecycle (create, list, view, delete).

## Message Format (Required)

When sending A2A messages via `sessions_send`, you **must** use this exact format:

```
[From: <name>] [fromAgentId: <agentId>] [reply-to: <sourceSession>] <message>
```

**For notifications (no reply needed):**
```
[From: <name>] [fromAgentId: <agentId>] [DO NOT REPLY] <message>
```

**Example — ask Anna to do something:**
```
[From: Lewis] [fromAgentId: echi-ceo] [reply-to: <your sessionId>] 早上好，请更新本周销售报告。
```

**Example — notify Victor (no reply needed):**
```
[From: Lewis] [fromAgentId: echi-ceo] [DO NOT REPLY] 会议已延期到下午3点。
```

**Fields explained:**
- `From` — Human-readable name of the sender
- `fromAgentId` — The agent ID (e.g. `echi-ceo`, `echitech-sales-manager-victor`)
- `reply-to` — Your own `sourceSession` (so the receiver knows where to route replies)
- `DO NOT REPLY` — Use when no response is needed (fire-and-forget)

## Prerequisites

Configure the OpenClaw directory:
```bash
a2a-chatting.sh config <openclaw_dir>
# Example: a2a-chatting.sh config /Users/roco/.openclaw
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `config <path> [--force]` | Configure OpenClaw directory |
| `get-agents` | List all available agents with their IDs |
| `new-session <agent_id> <topic>` | Create a new A2A session with an agent |
| `list-sessions` | List all A2A sessions |
| `get-session <session_id>` | Show session info |
| `delete-session <session_id>` | Delete a session |

## Workflow

### Step 1: Create a Session
```bash
# Use the CLI to create a session with the target agent
a2a-chatting.sh new-session <agent_id> "Discuss project structure"
# Returns: Session ID (e.g. 30d53db1-d1fd-41d8-a7f3-8373aa58a840)
```

### Step 2: Send Message (via sessions_send)
```bash
# Use sessions_send tool with the format above:
sessions_send(
  sessionKey: "<target agent session>",
  message: "[From: Lewis] [fromAgentId: echi-ceo] [reply-to: <sourceSession>] 早上好，请更新本周销售报告。"
)
```

### Step 3: Receive Reply
The receiver's reply automatically routes back to your session via `sessions_send` source tracking.

## Tips

- **Session Reuse**: Reuse existing sessions for ongoing conversations — agents maintain context
- **Topic Naming**: Use descriptive topics so you can find sessions later with `list-sessions`
- **Format Strictly**: Always use the `[From: ...]` format — it identifies you in multi-agent conversations
- **reply-to vs DO NOT REPLY**: Only use `reply-to` when you need a response. Use `DO NOT REPLY` for notifications.

## Examples

### Create session with Anna
```bash
a2a-chatting.sh new-session echitech-marketing-manager-anna "Marketing sync"
# → Session ID: db4aaf45-dd47-4766-87d0-0c2f690e8797
```

### Send a task request
```
sessions_send(
  sessionKey: "agent:echitech-marketing-manager-anna:main",
  message: "[From: Lewis] [fromAgentId: echi-ceo] [reply-to: <sourceSession>] 请更新本周营销计划。"
)
```

### Send a notification (no reply)
```
sessions_send(
  sessionKey: "agent:echitech-sales-manager-victor:main",
  message: "[From: Lewis] [fromAgentId: echi-ceo] [DO NOT REPLY] 今晚8点有全员会议，请准时参加。"
)
```

## Storage

Session index: `<openclaw_dir>/a2a-sessions/sessions.jsonl`
