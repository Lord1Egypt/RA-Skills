# OpenClaw Thin Plugin Plan (Phase 4)

## 0. Status

- Date: 2026-03-13
- Status: approved plan
- Scope: optional enhancement after Phase 3 MCP baseline

This plan does not change the v1 baseline:

- v1 remains runnable with `video-task-service` + `mcp-server` only
- OpenClaw thin plugin remains an optional adapter layer

## 1. Objective

Build an OpenClaw-native thin plugin that exposes exactly one tool:

- `xiaoice_video_produce`

and unify the public contract on `vhBizId` only.

## 2. Locked Decisions

The following decisions are fixed for Phase 4:

- plugin path must be `plugin -> shared client -> video-task-service`
- plugin must not call MCP as an internal transport hop
- OpenClaw plugin identity should use `one-click-video`
- `vhBizId` is the only public field name going forward
- `vhbizmode` is removed from public request, response, config, env, docs, and tests

## 3. Design Boundary

The adapter must stay thin.

It must not:

- build provider payloads
- handle callback workflows
- own SQLite state
- reimplement status transitions
- introduce provider-facing configuration

It must:

- register one native OpenClaw tool
- validate create/get input shape
- call `video-task-service` through a shared HTTP client
- map service responses into OpenClaw tool result shape

## 4. Dependency Direction

Allowed:

- OpenClaw thin plugin -> shared client -> `video-task-service`

Explicitly not allowed:

- OpenClaw thin plugin -> MCP server -> `video-task-service`

Reason:

- extra hop without user-facing value
- duplicated failure surface
- harder debugging
- likely behavior drift between MCP and plugin

## 5. Public Contract

Tool contract must stay aligned with MCP and service after the field cleanup.

Supported tool fields:

- `action`: `create | get`
- `prompt`: required for `create`
- `taskId`: required for `get`
- `sessionId`: optional
- `traceId`: optional
- `vhBizId`: optional
- `options`: optional object

Removed public aliases:

- `vhbizmode`

Config keys remain transport-only:

- `serviceBaseUrl`
- `internalToken`
- `requestTimeoutMs`

Provider-facing settings stay service-owned:

- `apiKey`
- callback settings
- provider auth header/scheme
- provider default business id

## 6. Historical Plugin Identity

The plugin should use the `one-click-video` runtime identity consistently across code, config, and docs.

Use:

- plugin id: `one-click-video`
- OpenClaw config lookup path: `plugins.entries['one-click-video']`

Do not keep:

- old inline HTTP transport implementation
- old weak default token behavior
- old contract names such as `vhbizmode`

## 7. Repository Placement

```text
xiaoice-video-tool/
  adapters/
    openclaw-plugin/
      index.js
      openclaw.plugin.json
      package.json
      README.md
      __tests__/
```

## 8. Shared Client Prerequisite

Before plugin implementation, extract service transport logic to:

- `src/shared/video-service-client.js`

Required API:

- `createTask(params, config)`
- `getTask(taskId, config)`

`config` must include:

- `serviceBaseUrl`
- `internalToken`
- `requestTimeoutMs`
- `fetch` override for tests

This module becomes the single transport layer used by:

- `src/mcp/tool.js`
- `adapters/openclaw-plugin/index.js`

## 9. Phase 4 Milestones

### M1: Shared Client Extraction

- add `src/shared/video-service-client.js`
- move MCP HTTP request logic into the shared client
- add timeout support through `AbortController`
- keep MCP behavior and tests green

### M2: `vhBizId` Hard Cut

- remove `vhbizmode` from service request parsing and admin config handling
- remove `vhbizmode` from MCP tool schema and validation
- rename canonical runtime config/env docs to `VIDEO_PROVIDER_VH_BIZ_ID`
- return validation error if callers still send `vhbizmode`

### M3: OpenClaw Plugin Skeleton

- add `adapters/openclaw-plugin/index.js`
- add `adapters/openclaw-plugin/openclaw.plugin.json`
- add `adapters/openclaw-plugin/package.json`
- set OpenClaw plugin id to `one-click-video`

### M4: Native Tool Wiring

- register only `xiaoice_video_produce`
- validate `create/get` arguments
- call shared client
- return OpenClaw result shape: `content[]` + `isError`

### M5: Docs + Tests

- add plugin README with install/config examples
- add OpenClaw config snippet
- add focused adapter tests only
- update existing docs to reflect plugin availability and `vhBizId` hard cut

## 10. Test Scope

Shared client tests:

- `createTask` request mapping
- `getTask` request mapping
- timeout handling
- 4xx/5xx/network error normalization
- invalid service response handling

Service and MCP regression tests:

- `vhBizId` accepted in create/config flows
- `vhbizmode` rejected with validation error
- provider payload still uses `vhBizId`
- MCP tool schema exposes only `vhBizId`

OpenClaw plugin tests:

- registers exactly one tool named `xiaoice_video_produce`
- reads config from `one-click-video`
- create/get map correctly through shared client
- validation errors return `isError: true`
- upstream/network failures return `isError: true`

Do not add duplicate tests for:

- callback state transitions
- provider callback parsing
- SQLite persistence behavior already covered by service tests

## 11. Documentation Sync Required

When Phase 4 lands, update:

- `docs/03-mcp-integration.md`
- `docs/04-deployment.md`
- `docs/05-progress.md`
- `docs/06-decisions.md`
- `README.md`

All examples and field tables must use:

- `vhBizId`

All old examples using:

- `vhbizmode`

must be removed rather than kept as compatibility aliases.

## 12. Acceptance Criteria

Phase 4 is complete when:

- OpenClaw can use native tool `xiaoice_video_produce`
- plugin depends only on shared client + service API
- plugin runtime identity is `one-click-video`
- service, MCP, plugin, docs, and tests all use `vhBizId` only
- `vhbizmode` is rejected instead of silently accepted
- adapter and regression tests pass
- operator docs for OpenClaw setup are published

## 13. Risks and Mitigations

- Risk: copy-paste from legacy plugin reintroduces transport drift.
  Mitigation: shared client first, plugin second.

- Risk: public field rename creates hidden breakage in old callers.
  Mitigation: hard-cut all tests/docs together and make rejection explicit.

- Risk: plugin accepts provider-facing config and blurs ownership.
  Mitigation: keep plugin config schema limited to transport fields only.

- Risk: MCP and OpenClaw adapters diverge in validation behavior.
  Mitigation: route both through shared validation/client code where possible.
