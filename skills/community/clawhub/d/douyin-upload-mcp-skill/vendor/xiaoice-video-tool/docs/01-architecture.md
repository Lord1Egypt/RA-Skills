# XiaoIce Video Tool Architecture (v1 Draft)

## 1. Scope

This document defines the v1 architecture for the standalone XiaoIce video tool described in `docs/00-migration-plan.md`.

In scope:

- local/self-hosted deployment
- one HTTP service for task lifecycle
- one MCP stdio server for agent integration

Out of scope:

- multi-tenant control plane
- billing/quota platform
- web console
- OAuth

## 2. Runtime Components

| Component | Responsibility | Interface |
| --- | --- | --- |
| `video-task-service` | Create/query tasks, persist state, call provider, receive callback | HTTP (`/health`, `/v1/tasks`, callback endpoint) |
| `mcp-server` | Expose tool `xiaoice_video_produce`; translate MCP calls to local HTTP | MCP stdio + internal HTTP client |
| `SQLite` | Persist task state and callback updates | Local file DB |
| `XiaoIce Provider` | Process video generation request and send callback | `POST /openapi/aivideo/create` + provider callback |

## 3. Service API Surface (v1)

Base path: `/v1`

| Endpoint | Auth | Contract |
| --- | --- | --- |
| `GET /health` | none | readiness/liveness check |
| `POST /v1/tasks` | `X-Internal-Token` | create a task row, queue provider submission, return `202` with `submitted` status |
| `GET /v1/tasks/:taskId` | `X-Internal-Token` | query current normalized task state |
| `POST /v1/callbacks/provider` | `X-Callback-Token` or `?token=` | receive provider callback and update terminal state |
| `PUT /v1/admin/config` | `X-Admin-Token` | update runtime provider config used by future submissions |

## 4. Canonical Task Model

Externally visible task fields:

- `taskId` (internal stable id)
- `providerTaskId` (if provider returns one)
- `status` (`submitted | processing | succeeded | failed | timeout`)
- `videoUrl` (nullable, set when terminal success)
- `errorMessage` (nullable)
- `createdAt`
- `updatedAt`
- `finishedAt` (nullable)
- `sessionId` (nullable)
- `traceId` (nullable)

## 5. State Transitions

```text
submitted -> processing -> succeeded
submitted -> processing -> failed
submitted -> processing -> timeout
submitted -> failed
```

Rules:

- `POST /v1/tasks` returns `202` with `submitted` before provider submission completes.
- Provider submission runs asynchronously after the initial task row is stored.
- Callback is the source of truth for terminal state and `videoUrl`.
- Query-time timeout materialization may convert stale `submitted` or `processing` tasks into `timeout`.
- Unknown provider status must be normalized to a safe internal state (`processing` or `failed`) with logs.

## 6. Core Flows

### 6.1 Create Task Flow

1. Client (or MCP server) calls `POST /v1/tasks`.
2. Service validates input and writes an initial task row with `submitted` status.
3. Service enqueues async provider submission work.
4. Service returns `202` with the internal `taskId`.
5. Background submission stores the provider task id and transitions the task to `processing` or `failed`.

### 6.2 Callback Update Flow

1. Provider calls callback URL with auth token.
2. Service validates token and task binding.
3. Service normalizes provider result/state.
4. Service updates task row (`status`, `videoUrl`, error fields).

### 6.3 MCP Query Flow

1. MCP client calls tool `xiaoice_video_produce` with `action=get`.
2. MCP server calls `GET /v1/tasks/:taskId`.
3. MCP returns normalized task status to client.

## 7. Security Boundaries

- `VIDEO_SERVICE_INTERNAL_TOKEN`: required between MCP server and task service.
- `VIDEO_SERVICE_CALLBACK_TOKEN`: required for provider callback endpoint.
- `VIDEO_SERVICE_ADMIN_TOKEN`: required for runtime config updates via `/v1/admin/config`.
- Secrets are configuration-only; no hard-coded default production token.

## 8. Observability (v1 Minimum)

- structured logs with `traceId`, `taskId`, `providerTaskId`
- health endpoint for process checks
- explicit error logs on mapping failure, callback auth failure, provider non-2xx

## 9. Iteration Backlog

- lock final callback payload schema from real provider samples
- decide idempotency strategy for repeated callbacks
- add retry/dead-letter policy for transient provider failures
- add sequence diagram once implementation stabilizes
