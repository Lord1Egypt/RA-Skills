---
name: coralos
description: End-to-end Coral Cloud workflow — discover registry remote agents, compose and launch a session of agents, then monitor and close it.
---

# Coral

Use this skill to run a complete Coral Cloud session: discover available agents, build and submit a session payload, then monitor and close it.

## Phase 1 — Discover (Registry)

Identify the agent you want to run before composing a session payload.

**Fast commands:**
- `bash scripts/list_registry_agents.sh`
- `bash scripts/inspect_registry_agent.sh <source> <agent_name> <version>`

**Live endpoints:**
- List: `GET https://api.coralcloud.ai/api/v1/registry`
- Inspect: `GET https://api.coralcloud.ai/api/v1/registry/{source}/{agentName}/{version}`

Before moving on, record:
- `source`
- `agentName`
- `version`
- notable option requirements and constraints

If you see `{"message":"Not found"}`, compare the URL to the current [Coral Cloud API guide](https://docs.coralos.ai/cloud/using-api).

---

## Phase 2 — Create Session

Build and submit a `POST /api/v1/local/session` payload using the agent identified in Phase 1.

**Fast commands:**
- `bash scripts/create_session.sh examples/payloads/echo-session.json`
- `bash scripts/create_session_from_simple.sh examples/payloads/simple/echo-session.json`

**Payload notes:**
- Payload shape is strict — start from `examples/payloads/echo-session.json` or expand from `examples/payloads/simple/` using `scripts/build_coral_session_payload.py`.
- Required fields: `agentGraphRequest`, `namespaceProvider`, `execution`.
- Optional: session `annotations`, `extendedEndReport`.
- Custom tool/webhook flows are experimental until callback host policy is confirmed in your environment.

**Success criteria:**
- Non-error API response
- Real `sessionId` in the response

---

## Phase 3 — Manage Session

Monitor progress and clean up after the session is running.

**Fast command:**
- `bash scripts/get_session_state.sh <namespace> <session_id>`

**Live endpoint:**
- State: `GET /api/v1/local/session/{namespace}/{sessionId}`
- Verify list and delete routes against your environment before automating cleanup loops.

**Lifecycle checklist:**
- Session exists
- Agents connect and begin execution
- Output appears in Coral Cloud thread when requested
- Session is closed when no longer needed

**Success criteria:**
- Real state payload for the target session
- Evidence of agent progress and/or thread activity
