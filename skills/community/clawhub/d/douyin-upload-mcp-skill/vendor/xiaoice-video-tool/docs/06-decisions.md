# Architecture Decisions (ADR-lite)

This file records key migration decisions for traceability.

Status values:

- `accepted`
- `superseded`
- `proposed`

Current state snapshot (2026-03-13, Phase 4 entry):

- D-008 is `accepted` and defines `vhBizId` as the only public field name.
- D-006 remains `superseded` for historical traceability only.

## D-001 Standalone Local/Self-Hosted v1

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: deliver v1 as standalone local/self-hosted package only.
- Rationale: lowest-effort extraction path from current codebase.
- Consequences: no SaaS control plane, no tenant isolation, no billing in v1.

## D-002 Two-Runtime Split (`video-task-service` + `mcp-server`)

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: separate HTTP task service from MCP stdio server.
- Rationale: clear boundary between business workflow and agent integration.
- Consequences: requires internal auth and explicit service base URL config.

## D-003 Single MCP Tool in v1

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: expose only `xiaoice_video_produce`.
- Rationale: keep schema and integration surface minimal.
- Consequences: advanced provider fields pass through `options`.

## D-004 Stable Internal API Contract

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: standardize service API on `/v1/tasks` (+ callback endpoint).
- Rationale: reduce ambiguity and keep docs/implementation aligned.
- Consequences: all clients and tests must target `/v1/tasks`.

## D-005 Configuration-First Runtime Paths and Tokens

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: remove hard-coded `.openclaw` assumptions and weak default tokens.
- Rationale: project must run from any directory with explicit config.
- Consequences: deployment must provide complete env vars before startup.

## D-006 Provider Mapping Alias (legacy alias -> `vhBizId`)

- Date: 2026-03-13
- Status: superseded
- Owner: migration team
- Decision: keep a legacy user input alias while mapping internally to provider `vhBizId`.
- Rationale: preserve user-facing simplicity without leaking provider naming.
- Consequences: superseded by D-008; this alias must not remain part of the long-term public contract.

## D-007 Optional OpenClaw Native Thin Plugin (Phase 4)

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: keep MCP as the default integration path, and execute an optional OpenClaw-native thin plugin in Phase 4.
- Rationale: preserve native OpenClaw discoverability without duplicating service business logic.
- Consequences: requires shared service client extraction, plugin identity standardization on `one-click-video`, and strict adapter boundaries (`plugin -> shared client -> service` only).

## D-008 Canonical Public Field Name (`vhBizId`)

- Date: 2026-03-13
- Status: accepted
- Owner: migration team
- Decision: use `vhBizId` as the only public field name across service, MCP, OpenClaw plugin, docs, examples, and runtime configuration.
- Rationale: eliminate alias drift, align directly with provider naming, and remove needless translation from public APIs.
- Consequences: callers using legacy alias fields become incompatible and must migrate; public validation should reject non-canonical field names explicitly; runtime config examples must expose `VIDEO_PROVIDER_VH_BIZ_ID` only.
