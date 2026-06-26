# Overview / Auth / Scoping

## What is confirmed
- CoPaw exposes API under `/api/*`.
- Current deployment may put **nginx Basic Auth** in front of CoPaw.
- CoPaw also has optional internal auth (`Bearer`) when `COPAW_AUTH_ENABLED=true`.
- Many routes are **agent-scoped**:
  - path form: `/api/agents/{agentId}/...`
  - header form: `X-Agent-Id: <agentId>`
  - fallback: active/default agent

## Practical guidance
- For automation, prefer `/api/agents/{agentId}/...`.
- If there is any ambiguity, set agent explicitly and do not rely on implicit default resolution.
- In the current setup, requests may need nginx Basic Auth even if internal Bearer auth is off.

## Relevant API groups
- `/api/chats`
- `/api/console/chat`
- `/api/skills`
- `/api/tools`
- `/api/models`
- `/api/workspace`
- `/api/mcp`
- `/api/cron`
- `/api/agents`

## Interpretation boundary
Confirmed:
- `/api/*` surface exists
- agent-scoped routing exists
- external auth in front of CoPaw is possible

Interpretation:
- for robust integrations, explicit scoping is safer than default-agent behavior
ior
safer than default-agent behavior
