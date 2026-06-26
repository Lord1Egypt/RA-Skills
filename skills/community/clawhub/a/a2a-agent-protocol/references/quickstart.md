# A2A Quickstart — Full End-to-End Example

> This document walks through a complete A2A interaction from discovery to task completion.
> All JSON-RPC requests and responses are shown in full — copy and adapt directly.

---

## Scenario

- **Server Agent**: `data-agent` — receives a data extraction task, outputs structured JSON
- **Client Agent**: `orchestrator` — discovers `data-agent`, sends a task, retrieves results

Both agents are A2A-compliant. The client does not know the server's internal implementation.

---

## Step 1: Server Agent publishes its AgentCard

The server agent serves `/.well-known/agent.json`:

```bash
# Server: GET https://data-agent.example.com/.well-known/agent.json
```

```json
{
  "name": "data-agent",
  "description": "Specialized in extracting financial metrics from raw CSV and JSON data sources",
  "version": "1.0",
  "provider": {
    "organization": "Acme Corp",
    "url": "https://acme.example.com"
  },
  "capabilities": {
    "streaming": "SUPPORTED",
    "pushNotifications": "NOT_SUPPORTED",
    "agentPrivilege": false,
    "signedAgentCard": false,
    "dataStreamingSupported": true,
    "supportsAuthenticatedExtendedAgentCard": false
  },
  "skills": [
    {
      "id": "csv-extraction",
      "name": "CSV Financial Extraction",
      "description": "Extracts revenue, EBITDA, and net income from CSV files",
      "tags": ["finance", "csv", "extraction"],
      "examples": ["Extract revenue from Q3_2025.csv"]
    }
  ],
  "authentication": {
    "schemes": ["httpBearer"],
    "credentials": "required"
  },
  "defaultInputModes": ["text", "json", "csv"],
  "defaultOutputModes": ["json"],
  "endpoint": "https://data-agent.example.com/a2a/"
}
```

---

## Step 2: Client discovers the server's AgentCard

```bash
GET https://data-agent.example.com/.well-known/agent.json
```

Client reads the AgentCard and confirms:
- `capabilities.streaming = SUPPORTED` ✓ (we want streaming)
- `authentication.schemes = ["httpBearer"]` → need a Bearer token
- `skills[0].id = "csv-extraction"` matches the task

---

## Step 3: Client sends a task (streaming)

Client constructs and sends a streaming task:

```bash
POST https://data-agent.example.com/a2a/tasks/sendSubscribe
Content-Type: application/a2a+json
Authorization: Bearer eyJhbGciOiJSUzI1NiJ9...
```

```json
{
  "jsonrpc": "2.0",
  "method": "tasks/sendSubscribe",
  "params": {
    "taskId": "task-abc-123",
    "sessionId": "session-xyz-456",
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "data",
          "data": {
            "instruction": "Extract revenue and EBITDA from Q3_2025.csv",
            "fileUrl": "https://storage.acme.example.com/data/Q3_2025.csv"
          }
        }
      ]
    },
    "configuration": {
      "stream": true
    }
  },
  "id": 1
}
```

---

## Step 4: Server responds with streaming SSE events

```
event: task_status_update
data: {"kind":"TaskStatusUpdateEvent","taskId":"task-abc-123","status":{"state":"submitted","message":"Task received","timestamp":"2026-05-14T07:00:01Z"},"final":false}

event: task_status_update
data: {"kind":"TaskStatusUpdateEvent","taskId":"task-abc-123","status":{"state":"working","message":"Fetching file","timestamp":"2026-05-14T07:00:02Z"},"final":false}

event: task_artifact_update
data: {"kind":"TaskArtifactUpdateEvent","taskId":"task-abc-123","artifact":{"artifactId":"art-001","name":"partial-extract","parts":[{"kind":"data","data":{"status":"parsing","rows_processed":42}}]},"final":false}

event: task_status_update
data: {"kind":"TaskStatusUpdateEvent","taskId":"task-abc-123","status":{"state":"completed","message":"Extraction complete","timestamp":"2026-05-14T07:00:05Z"},"final":true}
```

Client accumulates events, then extracts the final result.

---

## Step 5: Client extracts the final artifact

From the completed task (via `tasks/get` if polling instead of streaming):

```json
{
  "task": {
    "taskId": "task-abc-123",
    "sessionId": "session-xyz-456",
    "status": {
      "state": "completed",
      "message": "Extraction complete",
      "timestamp": "2026-05-14T07:00:05Z"
    },
    "artifacts": [
      {
        "artifactId": "art-001",
        "name": "Q3-2025-financials",
        "description": "Extracted financial metrics from Q3_2025.csv",
        "parts": [
          {
            "kind": "data",
            "data": {
              "revenue": 4523000,
              "ebitda": 1234000,
              "net_income": 891000,
              "currency": "USD",
              "source_file": "Q3_2025.csv",
              "rows_processed": 847
            }
          }
        ]
      }
    ]
  }
}
```

Client returns `artifacts[0].parts[0].data` to the user — structured output, not the raw task object.

---

## Error Handling Example

### Version Negotiation Failure

```json
// Client sends (declares A2A version):
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "params": {
    "message": { "role": "user", "parts": [{"kind": "text", "text": "do stuff"}] }
  },
  "id": 1,
  "a2aVersion": "0.9"   // ← old version
}
```

```json
// Server responds:
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32001,
    "message": "Version negotiation failed",
    "data": {
      "supportedVersions": ["1.0"],
      "requestedVersion": "0.9"
    }
  }
}
```

Client retries with `a2aVersion: "1.0"`.

---

## MCP + A2A Combined Scenario

```
User ──→ Orchestrator Agent (A2A Client)
              │
              ├── MCP: calls search_tool → gets raw CSV URL
              │
              └── A2A: sends task to data-agent
                        │ (with CSV URL in message.data)
                        ▼
                   data-agent
                        │ (extracts, computes)
                        ▼
                   returns artifacts[].parts[].data
                        │
                        ▼
              Orchestrator ──→ MCP: calls report_tool → generates PDF
```

In this flow:
- **MCP** connects the orchestrator to tools and storage
- **A2A** connects the orchestrator to the specialized data-agent
- Both protocols coexist — they solve different problems