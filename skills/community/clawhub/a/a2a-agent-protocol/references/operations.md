# A2A Protocol Operations Reference

> Reference: https://a2a-protocol.org/latest/specification/ Section 3

All operations are JSON-RPC 2.0 over HTTP POST to the agent's A2A endpoint.
Base URL pattern: `https://<agent-host>/a2a/`

---

## Core Operations

### tasks/send — Send Message

**Purpose:** Submit a new task to a remote agent.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "params": {
    "taskId": "string (optional — server generates if omitted)",
    "sessionId": "string (optional)",
    "contextId": "string (optional)",
    "message": {
      "role": "user | agent",
      "parts": [{ "kind": "text", "text": "..." }]
    },
    "configuration": {
      "stream": false,
      "pushNotificationConfig": null
    }
  },
  "id": 1
}
```

**Response (sync):**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "task": { ... Task object with status=completed ... },
    "artifacts": [ ... ]
  }
}
```

**Response (async — task requires time):**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "task": { "taskId": "abc123", "status": { "state": "submitted" } }
  }
}
```

---

### tasks/sendSubscribe — Send Streaming Message

**Purpose:** Submit a task and receive real-time SSE stream of status/artifact updates.

**Request:** Same as `tasks/send` with `configuration.stream: true`

**Response:** SSE stream of events:
```
event: task_status_update
data: { "kind": "TaskStatusUpdateEvent", "taskId": "abc123", "status": { "state": "working" }, "final": false }

event: task_artifact_update
data: { "kind": "TaskArtifactUpdateEvent", "taskId": "abc123", "artifact": { ... }, "final": false }

event: task_status_update
data: { "kind": "TaskStatusUpdateEvent", "taskId": "abc123", "status": { "state": "completed" }, "final": true }
```

---

### tasks/get — Get Task

**Purpose:** Retrieve the current state of a task by ID.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/get",
  "params": { "taskId": "string (required)" },
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "task": {
      "taskId": "abc123",
      "status": { "state": "completed", "timestamp": "..." },
      "artifacts": [ ... ],
      "messages": [ ... ]
    }
  }
}
```

---

### tasks/list — List Tasks

**Purpose:** List tasks, optionally filtered by session or context.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/list",
  "params": {
    "sessionId": "string (optional)",
    "contextId": "string (optional)",
    "pageSize": 10,
    "continuationToken": "string (optional)"
  },
  "id": 3
}
```

---

### tasks/cancel — Cancel Task

**Purpose:** Cancel a running task.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/cancel",
  "params": { "taskId": "string (required)" },
  "id": 4
}
```

---

### tasks/subscribe — Subscribe to Task Updates

**Purpose:** Subscribe to push notifications for a task (webhook or SSE delivery).

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tasks/subscribe",
  "params": {
    "taskId": "string (required)",
    "pushConfig": {
      "pushProviderName": "string",
      "pushProviderUrl": "https://...",
      "authentication": { "kind": "apiKey", "credentials": "..." },
      "payload": { "secret": "..." }
    }
  },
  "id": 5
}
```

---

### tasks/push — Receive Push Notification (webhook endpoint)

**Purpose:** Incoming push notification webhook (agent implements this endpoint).

```
POST /a2a/tasks/push
Content-Type: application/a2a+json

{
  "taskId": "abc123",
  "result": { ... },
  "pushNotificationConfigId": "string"
}
```

---

### pushNotificationConfig/create — Create Push Config

### pushNotificationConfig/get — Get Push Config

### pushNotificationConfig/list — List Push Configs

### pushNotificationConfig/delete — Delete Push Config

### agent/getExtendedAgentCard — Get Authenticated Extended Agent Card

---

## Operation Semantics

### Idempotency

- `tasks/send` is idempotent if `taskId` is supplied by the client (same `taskId` = same task)
- Without a client-supplied `taskId`, the server generates a unique one

### Capability Validation

Before sending, client should verify:
1. Target agent supports the required operation (check AgentCard)
2. Authentication requirements are met
3. Streaming preference is supported (if streamingRequested)

### Error Handling

Standard JSON-RPC 2.0 error codes:

| Code | Meaning |
|------|---------|
| `-32700` | Parse error — malformed JSON |
| `-32600` | Invalid request |
| `-32603` | Internal error |
| Agent-specific codes in `data` object |

### Multi-Turn Threads

| Field | Purpose |
|-------|---------|
| `sessionId` | Groups all messages in a single conversation session |
| `contextId` | Threads related sessions into a broader context |
| `contextId` + `sessionId` together enable multi-turn cross-agent conversations |

---

## URL Patterns (HTTP+JSON binding)

| Operation | Method | Path |
|-----------|--------|------|
| `tasks/send` | POST | `/a2a/tasks/send` |
| `tasks/sendSubscribe` | POST | `/a2a/tasks/sendSubscribe` |
| `tasks/get` | POST | `/a2a/tasks/get` |
| `tasks/list` | POST | `/a2a/tasks/list` |
| `tasks/cancel` | POST | `/a2a/tasks/cancel` |
| `tasks/subscribe` | POST | `/a2a/tasks/subscribe` |
| `tasks/push` | POST | `/a2a/tasks/push` |
| AgentCard | GET | `/.well-known/agent.json` |
| Extended AgentCard | GET | `/a2a/agent/extendedCard` |