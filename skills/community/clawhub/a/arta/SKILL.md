---
name: arta
version: 0.3.0
title: ARTA — Agentic Real-Time Awareness
description: In-memory awareness layer for agents to track their own activity within a single process. Provides queryable awareness of what an agent is doing in other sessions. Note: Cross-process/cross-instance sharing requires a shared backend (future enhancement).
metadata: {"openclaw":{"emoji":"🧩","category":"awareness","tags":["awareness","self-awareness","session","identity"]}}
---

# ARTA — Agentic Real-Time Awareness

**In-memory self-awareness for agents.**

⚠️ **Current Limitation:** This version provides awareness within a single agent process. True cross-instance/cross-agent awareness would require a shared backend (Redis, database, or OpenClaw global API) — not yet implemented.

---

## What is ARTA?

ARTA gives agents **awareness** of their own activity across sessions within a single process.

Without ARTA:
- Agent is fragmented across sessions
- Each session is isolated
- Can't answer: "What am I doing in other sessions?"

With ARTA:
- Tracks own sessions
- Queryable state
- Can say: "I'm also talking to you in another session"

---

## Core Concepts

### 1. Agent Instance

A single session of an agent.

```json
{
  "instanceId": "session-abc123",
  "agent": "my-agent",
  "channel": "telegram:CHAT_ID",
  "human": "USER_NAME",
  "task": "discussing ARTA",
  "status": "active"
}
```

### 2. Awareness Graph

The state of agent instances:

```json
{
  "agents": {
    "my-agent": {
      "instances": [
        {
          "instanceId": "session-1",
          "channel": "telegram:CHAT_ID_1",
          "task": "discussing ARTA",
          "status": "active"
        },
        {
          "instanceId": "session-2",
          "channel": "discord:CHANNEL_ID",
          "task": "code review",
          "status": "active"
        }
      ]
    }
  }
}
```

### 3. Context Broker

The queryable API:
- "What am I doing elsewhere?"
- "What is in channel X?"
- "Who is the human talking to?"

---

## What ARTA Reads from OpenClaw

When running within OpenClaw, ARTA can access:

| Data | Example | Purpose |
|------|---------|---------|
| Channel type | `telegram`, `discord` | Identify channel |
| Chat ID | `123456789` | Unique channel identifier |
| Sender name | `john_smith` | Human identifier |
| Session ID | `session-abc` | Unique session identifier |

**Note:** ARTA reads metadata only — not message content, not credentials, not bot tokens.

---

## Configuration

### Option 1: Auto-Configure from OpenClaw

```javascript
// Auto-detect from OpenClaw context
const channel = process.env.OPENCLAW_CHANNEL || 'unknown';
const chatId = process.env.OPENCLAW_CHAT_ID || 'unknown';
const human = process.env.OPENCLAW_SENDER_NAME || 'unknown';

const channelId = `${channel}:${chatId}`;
```

### Option 2: Environment Variables

```bash
# Optional - ARTA will auto-detect from OpenClaw if not set
export ARTA_AGENT_NAME="your-agent-name"
export ARTA_CHANNEL_TYPE="telegram"
export ARTA_CHAT_ID="123456789"
export ARTA_HUMAN_NAME="human-name"
```

### Bot Tokens

**ARTA does NOT require bot tokens.** The skill works with metadata (channel IDs, user names) only. If you see references to bot tokens in documentation, they are for reference — not required.

---

## Protocol

### Register

```javascript
arta.register({
  instanceId: "session-abc",
  channel: "telegram:CHAT_ID",
  human: "USER_NAME",
  task: "initial task"
});
```

### Update

```javascript
arta.update({
  instanceId: "session-abc",
  task: "new task",
  status: "active"
});
```

### Query

```javascript
const otherInstances = arta.queryOtherThan("session-abc");
```

### Leave

```javascript
arta.leave({
  instanceId: "session-abc"
});
```

---

## Implementation

```javascript
class ARTA {
  constructor(agentName) {
    this.agentName = agentName;
    this.instances = new Map();
  }

  register({ instanceId, channel, human, task = 'idle' }) {
    this.instances.set(instanceId, {
      instanceId,
      channel,
      human,
      task,
      status: 'active',
      started: Date.now(),
      lastHeartbeat: Date.now()
    });
  }

  update({ instanceId, task, status = 'active' }) {
    const instance = this.instances.get(instanceId);
    if (instance) {
      instance.task = task;
      instance.status = status;
      instance.lastHeartbeat = Date.now();
    }
  }

  leave({ instanceId }) {
    this.instances.delete(instanceId);
  }

  query() {
    return Array.from(this.instances.values());
  }

  queryOtherThan(instanceId) {
    return this.query().filter(i => i.instanceId !== instanceId);
  }

  queryByChannel(channel) {
    return this.query().filter(i => i.channel === channel);
  }

  queryByHuman(human) {
    return this.query().filter(i => i.human === human);
  }
}
```

---

## Integration with IBT

```javascript
// In IBT Observe phase
const otherTasks = arta.queryOtherThan(currentSessionId);
if (otherTasks.length > 0) {
  // Agent is active in other sessions
}
```

---

## Security & Privacy

### What ARTA Reads (from OpenClaw context):
- Channel type and ID (metadata)
- Human name from sender
- Agent name from config

### What ARTA Stores (in-memory only):
- Session ID
- Channel identifier
- Human name
- Task description
- Status

### What ARTA NEVER Does:
- ❌ Reads bot tokens or credentials
- ❌ Stores credentials
- ❌ Exfiltrates data
- ❌ Makes external network calls
- ❌ Persists data to disk
- ❌ Logs message content
- ❌ Shares data with other agents

---

## Install

```bash
clawhub install arta
```

---

## Version

0.3.0 — Clarified in-memory only limitation, removed bot token requirements, specified metadata-only access
