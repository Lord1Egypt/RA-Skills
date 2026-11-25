---
name: chatbotx-mcp
description: "Use the ChatbotX MCP server's tools to operate a ChatbotX workspace (contacts, conversations, flows, broadcasts, sequences, pipelines, analytics, automation) from MCP-capable agents and IDEs. Use when the ChatbotX MCP server is connected and the user asks to read or change ChatbotX workspace data, or needs help signing in, choosing a workspace, or approving a CONFIRMATION_REQUIRED action."
version: 1.2.3
homepage: https://github.com/ChatbotXIO/chatbotx-agent/tree/main/skills/chatbotx-mcp
emoji: "🔌"
metadata:
  openclaw:
    envVars:
      - name: CHATBOTX_API_KEY
        required: false
        description: Workspace API key (Settings → Developer → API Keys). Only for the local stdio server; the hosted server signs in with OAuth.
      - name: CHATBOTX_API_URL
        required: false
        description: API URL including /api, only for the local stdio server. Defaults to https://app.chatbotx.io/api.
      - name: CHATBOTX_ALLOW_SELF_SIGNED_CERT
        required: false
        description: Set to "true" only for trusted local/self-hosted instances with self-signed TLS.
---

# ChatbotX MCP

Use the official ChatbotX MCP server to give AI agents tool access to a ChatbotX workspace.
Tools are generated from the workspace's OpenAPI spec and filtered by the token's scopes.

## Setup

### Hosted server with OAuth (recommended)

| Transport | URL |
|---|---|
| Streamable HTTP | `https://app.chatbotx.io/mcp/messages` |
| SSE (legacy clients, ChatGPT connectors) | `https://app.chatbotx.io/mcp/sse` |

No API key and no local Node.js. On first connect the client opens a browser:

1. Sign in to ChatbotX.
2. Pick the workspace on the consent screen. Only workspace owners and super admins can authorize.
3. Every token the client gets acts on that one workspace. To switch workspaces, disconnect the
   server in the client and connect again.

Some clients need a login step after adding the server: Claude Code `/mcp`, Codex
`codex mcp login chatbotx`, Gemini CLI `/mcp auth chatbotx`, OpenCode `opencode mcp auth chatbotx`.

Claude Code:

```bash
claude mcp add chatbotx -t http -s user https://app.chatbotx.io/mcp/messages
```

Cursor and most JSON-configured clients (Windsurf names the key `serverUrl`; VS Code uses
`"servers"` with `"type": "http"`):

```json
{ "mcpServers": { "chatbotx": { "url": "https://app.chatbotx.io/mcp/messages" } } }
```

### Local stdio server with an API key (self-hosted, CI, headless)

Requires Node.js 24 or newer and a workspace API key from Settings → Developer → API Keys.

```json
{
  "mcpServers": {
    "chatbotx": {
      "command": "npx",
      "args": ["-y", "chatbotx-mcp"],
      "env": {
        "CHATBOTX_API_KEY": "your_workspace_token",
        "CHATBOTX_API_URL": "https://app.chatbotx.io/api",
        "CHATBOTX_MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

For a self-hosted instance, point `CHATBOTX_API_URL` at it (including `/api`). For a trusted
self-signed certificate, also set `CHATBOTX_ALLOW_SELF_SIGNED_CERT=true`.

## Workflow

1. Call `token_get` to confirm which workspace you are connected to, the permission, and scopes.
2. Call `capabilities_get` to resolve inboxes, templates, fields, tags, flows, and sequences.
3. Resolve ids. Most writes take ids, not display names. When a name matches more than one row,
   ask the user which one; do not pick the first.
4. Use the default tools for common operations. For anything else, find the tool with
   `search_tools` (an English "action + resource" query) and run it with `call_tool`. The
   [Claude connection](#claude-connection) has no `search_tools` or `call_tool`.
5. When a write returns `CONFIRMATION_REQUIRED`, follow [Confirmation](#confirmation).
6. Verify each write with the matching `get`, `list`, or message-history tool.

## Confirmation

Mutating tools return `CONFIRMATION_REQUIRED` instead of acting. The response carries the policy,
the proposed arguments, and the current state when it could be read (`currentStateUnavailable`
explains when it could not).

1. Show the user the proposed action and the current state.
2. Wait for explicit approval.
3. Repeat the same call with the same arguments plus `_confirm: true`.

Never add `_confirm: true` on the first attempt or without approval. `_confirm` is a guardrail,
not an authorization boundary: the token's real permissions still apply.

## Discovery tools

Call these before anything else.

| Tool | Description |
|---|---|
| `capabilities_get` | Discover workspace inboxes, templates, fields, tags, AI agents, sequences, and flows. Pass the target channel before authoring a channel-bound FlowSpec to get its supported blocks and limits. |
| `token_get` | Get the calling token's workspace id, permission (`read_only`/`full`), and scopes. |
| `schemas_flow_spec` | Get the JSON Schema for the flow-spec DSL accepted by flow create/update/publish/validate tools. |

## Default tools

`tools/list` returns a curated default set plus three meta-tools rather than the whole API.

| Tool | Description |
|---|---|
| `search_tools` | Search the full API for a tool outside the default set. Returns name, description, and input schema. Queries must be English. |
| `call_tool` | Execute any tool by name, including tools found by `search_tools`. Pass fields at the top level, not nested under a body object. |
| `get_guide` | Read an operational guide for approvals, flows, inbox handover, contacts, or pipelines. |

Current default categories:

| Category | Tools |
|---|---|
| Capabilities | `capabilities_get`, `schemas_flow_spec`, `token_get` |
| AI Agents | `ai_agents_list`, `ai_agents_create`, `ai_agents_update`, `ai_files_list`, `ai_functions_list` |
| Analytics | `analytics_new_contact_counts_per_day`, `analytics_blocked_contacts_per_day`, `analytics_flow_stats`, `analytics_broadcast_stats`, `analytics_sequence_step_stats` |
| Broadcasts | `broadcasts_list`, `broadcasts_get`, `broadcasts_stop` |
| Connections | `connections_create`, `connection_providers_list`, `connect_sessions_get` |
| Contacts | `contacts_create`, `contacts_get`, `contacts_list`, `contacts_list_tags`, `contacts_add_tags_by_name`, `contacts_list_custom_fields`, `contacts_set_custom_field`, `contacts_list_messages`, `contacts_send_message`, `contacts_send_flow`, `contacts_list_sequences`, `contacts_subscribe_sequences` |
| Conversations | `conversations_list`, `conversations_get`, `conversations_assign` |
| Error Logs | `error_logs_list` |
| Flows | `flows_list`, `flows_get`, `flows_create`, `flows_update_draft`, `flows_publish`, `flows_validate` |
| Keywords | `keywords_list` |
| Messages | `messages_list` |
| Mini Apps | `mini_apps_list`, `mini_apps_create` |
| Pipelines | `pipelines_list`, `pipelines_list_items`, `pipelines_create_item`, `pipelines_move_item` |
| Posts | `post_analytics_summary` |
| Sequences | `sequences_list`, `sequences_get`, `sequences_update` |

Everything else is reachable through `search_tools` and `call_tool` when the token is authorized:
deletes, coupons, products, webhooks, saved replies, tag/trigger/inbox/custom-field management,
connection lifecycle (disconnect, reconnect, verify), workspace members, and other less common
operations.

## Claude connection

The ChatbotX plugin and connector for Claude (claude.ai, Claude Desktop, Cowork, Claude Code)
connect to `https://app.chatbotx.io/mcp/claude`, a fixed tool set for that directory:

- Every default tool above except the three Connections tools, plus `get_guide`.
- No `search_tools` or `call_tool`. An operation outside the list (deletes, coupons, products,
  webhooks, workspace members, connecting channels) is not available on this connection. Use the
  `chatbotx` CLI or the ChatbotX app for it, and tell the user so instead of looking for a
  workaround.
- Every tool that changes data is marked destructive, so Claude asks before each one. The
  `CONFIRMATION_REQUIRED` step still applies after that.

## Scope and read-only behavior

- A token missing a scope does not see that scope's tools in `tools/list`.
- A `read_only` token only sees read-only default tools.
- `capabilities_get` and `token_get` are always visible so the agent can discover what it can do.
- `search_tools` can find tools that are not in `tools/list`, but the API still returns `403` when
  the token is not authorized.
- If token introspection hits a transient network failure, filtering may fail open in `tools/list`.
  The API call still enforces the real permissions.

## Safety rules

1. Do not send a contact message, conversation message, flow, sequence, or broadcast until the
   target contact, audience, and inbox have been resolved to exact ids.
2. To reply in a known conversation, use the conversation's message tool with its id; do not
   replace it with a contact-level send. Keep the selected inbox and channel.
3. For broadcasts, inspect the audience first. Keep drafts and manual review when the task affects
   real customers.
4. For flows, call `schemas_flow_spec` and `flows_validate` before publishing a generated spec.
   A draft-only request never publishes or sends.
5. For destructive operations found through `search_tools`, fetch the current resource first and
   verify the exact id.
6. When a tool returns a URL, `nextAction`, or `awaiting_selection` (OAuth or channel connection),
   show it to the user and wait for them to finish before reading the connection state.
7. `connections_create` with `provider: "api"` returns a one-time `secret.token`. Tell the user to
   store it; it cannot be retrieved again.
8. Never report success after `isError`, `403`, `404`, `422`, or a business failure. Distinguish
   created, queued, accepted, and delivered.
9. Do not put workspace tokens in prompts, logs, generated docs, or committed config.

## Troubleshooting

- `401` or "needs auth" on the hosted server: run the client's login step again (see Setup).
- Wrong workspace: `token_get` shows the bound workspace. Disconnect and reconnect to pick another.
- Authorization refused: only workspace owners and super admins can grant access.
- Missing tools: call `token_get` to check scopes and permission, then refresh the MCP client so
  `tools/list` runs again.
- New API not visible: the server refreshes the OpenAPI spec every 5 minutes.
- stdio auth errors: verify `CHATBOTX_API_KEY` and that `CHATBOTX_API_URL` includes `/api`.
- stdio TLS errors: set `CHATBOTX_ALLOW_SELF_SIGNED_CERT=true`, only for trusted local or
  self-hosted instances.
