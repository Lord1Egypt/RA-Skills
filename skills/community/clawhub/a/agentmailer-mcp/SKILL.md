---
name: agentmailer-mcp
description: Connect to AgentMailer's hosted MCP server, complete human-approved OAuth, or troubleshoot authentication in Claude Code, Codex, Cursor, and other MCP clients.
---

# AgentMailer MCP

Use the universal Streamable HTTP endpoint:

`https://api.agentmailer.ai/mcp`

Prefer the client's native remote-MCP configuration so it can discover OAuth from AgentMailer's protected-resource metadata. Do not ask the user to paste OAuth tokens into prompts, source files, or shell history.

## Connect

Choose the shortest path for the active client:

- Claude Code: run `claude mcp add --transport http agentmailer https://api.agentmailer.ai/mcp`, then `claude mcp login agentmailer`.
- Codex: run `codex mcp add agentmailer --url https://api.agentmailer.ai/mcp`, then `codex mcp login agentmailer`.
- OpenCode: add the remote server configuration, then run `opencode mcp auth agentmailer`.
- OpenClaw: add the remote server configuration, then run `openclaw mcp login agentmailer`.
- Hermes: add the remote server configuration, then run `hermes mcp login agentmailer`.
- Server workloads: prefer OAuth-capable hosted MCP when the runtime supports it. For direct REST access, follow `https://api.agentmailer.ai/auth.md` exactly.
- Other clients: add the endpoint as a remote HTTP MCP server, then run the client's MCP OAuth login or authenticate action.

Every first-time signup requires human approval. After authorization:

1. Call `auth_me` and require a trusted identity with `inboxes:create` before creating an identity inbox. Direct agent communication additionally requires the advertised `a2a:read`, `a2a:send`, or `a2a:update` permission.
2. Call `list_inboxes` as a low-risk functional check.
3. If no existing inbox fits, call `create_inbox` with a stable idempotency key and an optional lowercase username.
4. Verify the returned address ends in `@agentmailer.ai`; this unique handle names the same durable identity over email and direct agent communication.

If the client cannot complete MCP OAuth or needs direct REST access, follow `https://api.agentmailer.ai/auth.md` exactly. Do not invent or partially reproduce its signup and token procedure.

Do not call `create_inbox` with an unverified credential. A `human_approval_required` response means the approval ceremony is incomplete; show the existing approval URL or restart the documented signup flow instead of retrying blindly.

## Diagnose

Read [references/troubleshooting.md](references/troubleshooting.md) when connection, OAuth, or permission checks fail. Preserve the distinction between:

- transport failure;
- OAuth discovery or callback failure;
- authenticated but insufficient permissions;
- a successful connection with no inboxes yet.

Never claim the connection works until an authenticated tool call succeeds.

## Examples

Use the [human-approved signup example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-human-approved-signup) to understand the approval boundary, then the [quickstart](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-quickstart) or [CLI workflows](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/cli) for a low-risk authenticated check. Browse the [complete examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples) for application-specific integrations.
