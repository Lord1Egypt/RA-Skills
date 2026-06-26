# XiaoIce Video Tool Migration Plan

## 1. Objective

Build a new standalone project at `/home/yirongbest/xiaoice-video-tool` by extracting the existing XiaoIce video generation capability from the current codebase with the lowest possible development effort.

The first version targets:

- standalone local development
- self-hosted packaging
- MCP stdio integration for agent products
- no SaaS, no multi-tenant design, no control plane

## 2. Project Scope

The new project will contain two runtime parts:

- `video-task-service`
  - creates video tasks
  - stores task state in SQLite
  - submits requests to XiaoIce provider
  - receives provider callbacks
  - exposes task status query APIs
- `mcp-server`
  - exposes a single MCP tool: `xiaoice_video_produce`
  - calls `video-task-service` over local HTTP
  - serves as the main integration surface for OpenClaw, Claude Code, Cursor, and Cline

Out of scope for v1:

- OpenClaw-specific plugin as the primary delivery model
- SaaS hosting
- tenant isolation
- billing or quota platform
- web console
- OAuth

## 3. Source of Truth

The main source files to migrate from the current repository are:

- `/home/yirongbest/claw-xiaoice/services/video-task-service/server.js`
- `/home/yirongbest/claw-xiaoice/services/video-task-service/cli.js`
- `/home/yirongbest/claw-xiaoice/start-video-service.sh`
- `/home/yirongbest/claw-xiaoice/update-video-callback.sh`
- `/home/yirongbest/claw-xiaoice/start-ngrok.sh`
- `/home/yirongbest/claw-xiaoice/video-ngrok-status.sh`
- `/home/yirongbest/claw-xiaoice/__tests__/video-service.test.js`
- `/home/yirongbest/claw-xiaoice/__tests__/video-orchestrator-plugin.test.js`

Provider contract reference:

- XiaoIce OpenAPI `POST /openapi/aivideo/create`

## 4. New Repository Layout

Planned structure:

```text
/home/yirongbest/xiaoice-video-tool
  README.md
  CHANGELOG.md
  .env.example
  package.json
  Dockerfile
  docker-compose.yml
  docs/
    00-migration-plan.md
    01-architecture.md
    02-provider-api-mapping.md
    03-mcp-integration.md
    04-deployment.md
    05-progress.md
    06-decisions.md
  src/
    service/
    mcp/
    shared/
  scripts/
  tests/
```

## 5. Configuration Model

### 5.1 User-facing configuration

The user-facing configuration inputs for v1 are:

- `apiKey`
- `vhbizmode`

Mapping rule:

- `vhbizmode` is mapped internally to provider field `vhBizId`

### 5.2 Internal runtime configuration

The project also requires these runtime settings:

- `VIDEO_TASK_SERVICE_PORT`
- `VIDEO_SERVICE_INTERNAL_TOKEN`
- `VIDEO_SERVICE_ADMIN_TOKEN`
- `VIDEO_SERVICE_CALLBACK_TOKEN`
- `VIDEO_CALLBACK_PUBLIC_BASE_URL`
- `XIAOICE_VIDEO_STATE_DIR`
- `XIAOICE_VIDEO_SERVICE_BASE_URL`

### 5.3 Provider field mapping

Provider request mapping for `POST /openapi/aivideo/create`:

- `prompt` -> `topic`
- `vhbizmode` -> `vhBizId`
- service-generated callback URL -> `callbackUrl`
- `options.title` -> `title`
- `options.content` -> `content`
- `options.materialList` -> `materialList`
- `options.ttsConf` -> `ttsConf`
- `options.aigcWatermark` -> `aigcWatermark`

## 6. MCP Tool Design

The MCP server exposes one tool only:

- `xiaoice_video_produce`

Parameters:

- `action`: `create | get`
- `prompt`: required for `create`
- `taskId`: required for `get`
- `sessionId`: optional
- `traceId`: optional
- `options`: optional object for advanced provider fields

Design choice:

- keep v1 schema minimal
- expose only common fields directly
- pass advanced provider-specific fields through `options`

## 7. Required Refactors

The following refactors are mandatory during migration:

1. Remove hard-coded `.openclaw` path dependencies from scripts.
2. Replace repository-relative state defaults with explicit configuration-first paths.
3. Remove weak production default tokens.
4. Ensure the project can run from any directory.
5. Align documentation with actual service endpoints:
   - use `/v1/tasks`
   - keep one tool only: `xiaoice_video_produce`
6. Align provider payload generation with the provider contract.

## 8. Delivery Strategy

### 8.1 v1 delivery

Primary delivery mode:

- local/self-hosted package
- MCP stdio server

Primary client targets:

- OpenClaw
- Claude Code
- Cursor
- Cline

Codex support is deferred to a later phase if remote MCP transport is required.

### 8.2 OpenClaw compatibility

The new project does not treat the OpenClaw plugin as the main entry point.

OpenClaw should connect through its existing MCP integration layer instead of requiring a dedicated new video plugin in v1.

## 9. Documentation Plan

The project must maintain these documents:

- `README.md`
  - quick start
  - environment setup
  - MCP usage
  - troubleshooting entry points
- `docs/01-architecture.md`
  - service flow
  - callback flow
  - MCP integration flow
- `docs/02-provider-api-mapping.md`
  - XiaoIce OpenAPI field mapping
  - examples
  - result and error code notes
- `docs/03-mcp-integration.md`
  - MCP tool schema
  - client configuration examples
- `docs/04-deployment.md`
  - local run
  - Docker run
  - callback exposure and ngrok usage
- `docs/05-progress.md`
  - date
  - completed work
  - blockers
  - next actions
- `docs/06-decisions.md`
  - decision
  - rationale
  - date
  - owner

## 10. Execution Phases

### Phase 1: Repository bootstrap

- create new repository structure
- initialize Git
- add base documents
- add package metadata

### Phase 2: Service extraction

- move and adapt `video-task-service`
- decouple paths and state locations
- preserve current API surface

### Phase 3: MCP server

- add stdio MCP server
- expose `xiaoice_video_produce`
- connect MCP server to local HTTP service

### Phase 4: Packaging and docs

- add Docker artifacts
- add `.env.example`
- add client integration examples
- finalize progress and decision records

### Phase 5: Verification

- service tests
- MCP integration tests
- local smoke test
- callback flow validation

## 11. Test and Acceptance Criteria

The migration is complete when all of the following are true:

- service health endpoint works
- task creation returns `submitted`
- task query returns correct terminal states
- callback updates `videoUrl` correctly
- MCP `create` works
- MCP `get` works
- user can configure `apiKey`
- user can configure `vhbizmode`
- `vhbizmode` is correctly mapped to `vhBizId`
- documentation is present and usable

## 12. Risks

Main implementation risks:

- callback public URL is still easy to misconfigure
- old scripts contain machine-specific paths
- historical tests and docs are not fully aligned with implementation
- the configuration name `vhbizmode` is user-facing but differs from provider field `vhBizId`, so mapping must be documented clearly

## 13. Estimated Effort

Estimated MVP effort:

- repository and docs: 0.5 to 1 day
- service extraction: 1.5 to 2 days
- MCP server: 1 to 2 days
- packaging and client examples: 0.5 to 1 day
- verification: 1 to 2 days

Total:

- 4.5 to 8 developer days
