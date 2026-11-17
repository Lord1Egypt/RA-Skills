---
name: "council-blackboard"
description: "Visible OpenClaw–Open WebUI council rooms with typed blackboards and session handovers."
---

# Council blackboard

Use when the user asks OpenClaw and an Open WebUI model to confer, compare approaches, review one another, or form a multi-model council.

## Rules

1. Create a fresh board and Open WebUI room for every new council:
   `python skills/council-blackboard/scripts/council.py room --topic "..." --user-id USER_ID`
2. Give the user the returned `chat_url` immediately. The WebUI room is the visible transcript; the JSON board is the auditable source of truth.
3. Validate before every hop. Read the goal, typed entries, revision, next capability, and unresolved questions.
4. Do one bounded contribution per hop. Never rewrite another writer's entry.
5. Record observations as facts, conclusions as inferences, user choices as user_decisions, and checks as evidence/test_results.
6. The Open WebUI model uses the attached `Council Blackboard` tool to read the board, contribute, and call an isolated OpenClaw council session.
7. A council handover must name the board path, WebUI chat ID/URL, current revision, decisions, unresolved questions, next capability, and receipt locators. Do not dump private memory into the room.
8. The user may join either side at any time. Treat the newest authenticated user contribution as authoritative user context; preserve it as a user decision when it changes scope or constraints.
9. Stop on `needs_user`, a safety boundary, a failed board validation, or exhausted hops.
10. Completion still needs independent verification under the blackboard policy.

## Configuration

The scripts default to `~/.openclaw/workspace` and can be configured through environment variables rather than hard-coded machine paths.

Useful variables include:

- `OPENCLAW_WORKSPACE`
- `OPENWEBUI_BASE_URL`
- `OPENWEBUI_DB`
- `COUNCIL_BLACKBOARD_SCRIPT`
- `COUNCIL_ROOM_SCRIPT`
- `COUNCIL_WEBUI_MODEL`
- `COUNCIL_WEBUI_MODEL_NAME`
- `COUNCIL_OPENCLAW_MODEL`
- `COUNCIL_OPENCLAW_AGENT`
- `COUNCIL_USER_WRITER`

## OpenClaw to WebUI

Create the room before models confer. Use `council.py room`; then work from the returned board. The browser-visible URL is derived from `OPENWEBUI_BASE_URL` and the created chat ID.

## WebUI to OpenClaw

The WebUI model calls `consult_openclaw` with a bounded question and its current position. The tool appends the WebUI contribution, routes the board, invokes a dedicated OpenClaw session key, and returns the OpenClaw reply into the visible WebUI chat.

## Handover

Use `handover` when switching lead model or pausing. Keep it operational and short: outcome, constraints, decisions, evidence, failures, open questions, exact next action.
