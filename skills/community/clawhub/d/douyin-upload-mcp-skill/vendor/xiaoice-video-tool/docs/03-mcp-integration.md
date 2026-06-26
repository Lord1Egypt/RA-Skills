# MCP Integration (v1 Draft)

## 1. Scope

This document defines v1 MCP integration for XiaoIce video generation.

Design constraints:

- stdio transport only
- one tool only: `xiaoice_video_produce`
- MCP server delegates to local `video-task-service` HTTP API

Current implementation status (Phase 4 entry):

- implemented under `src/mcp/server.js` + `src/mcp/tool.js` + `src/mcp/cli.js`
- local run entry: `npm run mcp`
- tested for tool-level mapping and stdio protocol request handling
- entered shared client extraction for MCP + OpenClaw adapter reuse
- entered public field hard cut: `vhBizId` as the only external field name

## 2. Tool Contract

Tool name: `xiaoice_video_produce`

Input:

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["create", "get"]
    },
    "prompt": {
      "type": "string"
    },
    "taskId": {
      "type": "string"
    },
    "sessionId": {
      "type": "string"
    },
    "traceId": {
      "type": "string"
    },
    "options": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "required": ["action"]
}
```

Validation rules:

- `action=create` requires `prompt`
- `action=get` requires `taskId`

## 3. MCP <-> Service Mapping

- `action=create` -> `POST /v1/tasks`
- `action=get` -> `GET /v1/tasks/:taskId`

Internal auth:

- MCP server sends `VIDEO_SERVICE_INTERNAL_TOKEN` to task service.
- MCP server depends only on the public HTTP task-service contract; it does not reach into provider-facing internals.

Current Phase 2 assumptions frozen by tests:

- create returns `202` with `data.taskId` and `data.status=submitted`
- get returns the normalized task record (`taskId`, `providerTaskId`, `status`, `videoUrl`, `errorMessage`, timestamps, trace/session ids)
- service maps canonical `vhBizId` directly into provider `vhBizId`
- callback auth and admin config stay service-owned and out of MCP scope

## 4. Tool Result Shape (Normalized)

Common result:

```json
{
  "ok": true,
  "action": "create",
  "task": {
    "taskId": "task_xxx",
    "status": "submitted",
    "videoUrl": null
  }
}
```

Error result:

```json
{
  "ok": false,
  "action": "create",
  "error": {
    "code": "PROVIDER_SUBMIT_FAILED",
    "message": "provider returned non-success"
  }
}
```

## 5. Client Configuration Examples

### 5.1 Generic MCP stdio client

Command target:

- executable: `node`
- args: `["src/mcp/cli.js"]` (current repository entrypoint)

Required env:

- `XIAOICE_VIDEO_SERVICE_BASE_URL`
- `VIDEO_SERVICE_INTERNAL_TOKEN`

### 5.2 OpenClaw / Claude Code / Cursor / Cline

All clients can connect through the same MCP stdio server.

Phase 4 status:

- OpenClaw-native thin plugin work has entered implementation.
- MCP and OpenClaw adapters are expected to share the same service client boundary (`plugin -> shared client -> service`).
- OpenClaw plugin runtime identity is `one-click-video`.

## 6. Smoke Test Scenarios

- create task via MCP returns `submitted`
- get task via MCP returns latest status
- missing required fields returns validation error
- task service unavailable returns structured MCP error

## 7. Iteration Backlog

- finalize exact MCP SDK schema metadata
- add per-client config snippets once runtime entrypoints are fixed
- add integration test fixture for `create -> get` end-to-end flow through MCP stdio
