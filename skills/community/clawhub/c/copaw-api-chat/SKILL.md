---
name: copaw-api-chat
description: "Communicate with a CoPaw instance through its HTTP API. Use when: (1) you need to inspect available CoPaw agents or chats, (2) create a chat or session and send a message via API, (3) understand CoPaw auth, scoping, or SSE behavior before integration work, (4) build wrappers, automations, or skills on top of CoPaw API."
---

# CoPaw API Chat

Use this skill to work with **CoPaw over HTTP API**, not through the web UI.

## When to use
- You need to talk to a local CoPaw instance programmatically.
- You need the correct sequence: **create chat/session → send message → read SSE**.
- You need to understand agent scoping, auth layers, or related API groups before building automation.

## Workflow
1. Read `references/overview-auth-scoping.md` first.
2. If the task is about chatting with CoPaw, then read `references/chats-console-sse.md`.
3. If the task touches agent/model/skill/tool management, read `references/agents-models-skills-tools.md`.
4. If the task touches workspace, MCP, or cron, read `references/workspace-mcp-cron.md`.
5. If you need ready-to-run examples, read `references/practical-recipes.md`.

## Minimal practical path
1. Confirm agent id (`default` unless proven otherwise).
2. Create a chat with `POST /api/chats`.
3. Reuse the returned `session_id/user_id/channel` context.
4. Send the message with `POST /api/agents/{agentId}/console/chat`.
5. Read the response as **SSE**.

## Important rules
- Do not assume stateless request/response. CoPaw is **chat/session-centric**.
- Distinguish confirmed API behavior from interpretation.
- Prefer agent-scoped routes (`/api/agents/{agentId}/...`) or set `X-Agent-Id` explicitly.
- In the current deployment, auth may be provided by **nginx Basic Auth** even if internal CoPaw auth is off.
- Treat `/api/workspace` and some `/api/agents/*/files/*` surfaces as dangerous/admin-level APIs.

## References
- `references/overview-auth-scoping.md` — API surface, auth, scoping, priorities
- `references/chats-console-sse.md` — chat lifecycle, session context, SSE mechanics
- `references/agents-models-skills-tools.md` — management surfaces around agents/models/skills/tools
- `references/workspace-mcp-cron.md` — workspace, MCP, cron boundaries and risks
- `references/practical-recipes.md` — short request examples and file structure examples

## Output expectations
When using this skill, answer with:
- the minimal correct endpoint sequence,
- the required payload shape,
- auth/scoping caveats,
- and only the API groups relevant to the task.
