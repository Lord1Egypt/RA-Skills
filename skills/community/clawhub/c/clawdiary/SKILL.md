---
slug: clawdiary-guardian
name: ClawDiary Guardian
version: 1.1.9
tags: [security, audit, guard, mcp]
license: MIT-0
metadata:
  openclaw:
    requires:
      env: [CLAWDIARY_API_KEY]
    redaction_regex_and_truncation: true
    approved_by_human: true
---

# ClawDiary Guardian

An OpenClaw skill for integrating with ClawDiary - a cloud-based audit diary and high-risk operation interception gateway for AI Agents.

## How to Get an API Key (Registration)

To use this guardian skill, you need a ClawDiary API Key.

1. **Visit ClawDiary:** Go to the official site at [clawdiary.org](https://clawdiary.org).
2. **Register & Subscribe:** Choose a plan and follow the registration process.
3. **Get API Key:** Once registered, you will be provided with your unique `CLAWDIARY_API_KEY`.

Alternatively, if you prefer to self-host your own instance, check out the [ClawDiary setup documentation](https://github.com/jetywolf/claw-diary).

## Setup In OpenClaw

Configure your agent with the `CLAWDIARY_API_KEY` obtained from the step above. Note that all `/v1/*` endpoints require authentication via the `Authorization: Bearer <API_KEY>` header.

## Features & Usage

### 1. Active Guard (Approval Gate)
**Endpoint:** `POST https://api.clawdiary.org/v1/guard`
**When to use:** **BEFORE** executing any high-risk, destructive, or outbound action (such as executing bash, file deletions, sending emails).
**Behavior:**
Call this endpoint and wait for the response. Red-light actions will block the HTTP response until a human approves via Telegram. Only proceed with the action if the response returns `approved: true`.

Example Request:
```json
{
  "agent_id": "openclaw",
  "action_type": "execute_bash",
  "command": "rm -rf /tmp/data",
  "params": { "cwd": "/home/user" },
  "thought": "Cleaning up temporary files"
}
```

### 2. Passive Audit (Logging)
**Endpoint:** `POST https://api.clawdiary.org/v1/audit`
**When to use:** **AFTER** an action completes.
**Behavior:**
Report the action, cost, and payload. This helps the human operator review usage asynchronously.

Example Request:
```json
{
  "agent_id": "openclaw",
  "session_id": "sess-001",
  "action_type": "tool_call",
  "cost": 0.003,
  "payload": { "tool": "search_web", "query": "weather in London" }
}
```

### 3. Shared Diary
**Endpoints:** `POST https://api.clawdiary.org/v1/diary` (write), `GET https://api.clawdiary.org/v1/diary?owner_id=...` (list)
**When to use:** To keep a shared diary across multiple devices (lobsters) for one owner. This allows agents to sync status updates and context.

Example Write Request:
```json
{
  "owner_id": "alice",
  "lobster_id": "office-mac",
  "content": "Finished API integration today. All good."
}
```

## MCP Support
ClawDiary provides an MCP descriptor at `GET https://api.clawdiary.org/mcp.json`. Importing this to an MCP client automatically registers the `request_human_approval` tool handling the active guard.
