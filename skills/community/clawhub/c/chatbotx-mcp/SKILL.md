---
name: chatbotx-mcp
description: Use ChatbotX MCP tools to operate contacts, conversations, flows, broadcasts, sequences, analytics, and workspace automation from agentic IDEs.
version: 1.1.1
homepage: https://github.com/ChatbotXIO/chatbotx-agent/tree/main/skills/chatbotx-mcp
emoji: "🔌"
metadata:
  openclaw:
    primaryEnv: CHATBOTX_API_KEY
    envVars:
      - name: CHATBOTX_API_KEY
        required: true
        description: ChatbotX workspace API key (ChatbotX Settings → Developer → API Keys).
      - name: CHATBOTX_API_URL
        required: true
        description: Base API URL of the ChatbotX instance, e.g. https://app.chatbotx.io/api.
      - name: CHATBOTX_ALLOW_SELF_SIGNED_CERT
        required: false
        description: Set to "true" only for trusted local/self-hosted instances with self-signed TLS.
    install:
      - kind: node
        package: chatbotx-mcp
        bins: [chatbotx-mcp]
---

# ChatbotX MCP

Use the official ChatbotX MCP server to give AI agents tool access to a ChatbotX workspace.
Tools are generated from the connected workspace's OpenAPI spec and filtered by the workspace
token's scopes.

## Setup

Requires Node.js 18 or newer and a ChatbotX workspace token from Settings → Developer → API Keys.

For MCP clients that support stdio servers:

```json
{
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
```

For Claude Code:

```bash
claude mcp add chatbotx \
  -e CHATBOTX_API_KEY=<your-token> \
  -e CHATBOTX_API_URL=https://app.chatbotx.io/api \
  -e CHATBOTX_MCP_TRANSPORT=stdio \
  -s user \
  -- npx -y chatbotx-mcp
```

For a self-hosted or local instance with a trusted self-signed certificate:

```bash
export CHATBOTX_ALLOW_SELF_SIGNED_CERT=true
```

## Workflow

1. Set `CHATBOTX_API_KEY` and `CHATBOTX_API_URL`.
2. Call `capabilities_get` to resolve inboxes, templates, fields, tags, flows, and sequences.
3. Call `token_get` before any write to check the token's permission and scopes.
4. Resolve ids. Most writes take ids, not display names.
5. Use the default tools for common operations.
6. For anything outside the default set, find the tool with `search_tools` and run it with
   `call_tool`.
7. Verify each write with the matching `get`, `list`, or message-history tool.

## Discovery tools

Call these before anything else.

| Tool | Description |
|---|---|
| `capabilities_get` | Discover workspace inboxes, WhatsApp templates, custom/bot fields, tags, AI agents, sequences, and flows. |
| `token_get` | Get the calling token's workspace id, permission (`read_only`/`full`), and scopes. |
| `schemas_flow_spec` | Get the JSON Schema for the flow-spec DSL accepted by flow create/update/publish/validate tools. |

## Default tools

`tools/list` returns a curated default set plus two meta-tools rather than the whole API.

| Tool | Description |
|---|---|
| `search_tools` | Search the full API for a tool outside the default set. Returns name, description, and input schema. |
| `call_tool` | Execute any tool by name, including tools found by `search_tools`. |

Current default categories:

| Category | Tools |
|---|---|
| Capabilities | `capabilities_get`, `schemas_flow_spec`, `token_get` |
| AI Agents | `ai_agents_list`, `ai_agents_create`, `ai_agents_update`, `ai_files_list`, `ai_functions_list` |
| Analytics | `analytics_new_contact_counts_per_day`, `analytics_blocked_contacts_per_day`, `analytics_flow_stats`, `analytics_broadcast_stats`, `analytics_sequence_step_stats` |
| Broadcasts | `broadcasts_list`, `broadcasts_get`, `broadcasts_stop` |
| Contacts | `contacts_create`, `contacts_get`, `contacts_list`, `contacts_list_tags`, `contacts_add_tags_by_name`, `contacts_list_custom_fields`, `contacts_set_custom_field`, `contacts_list_messages`, `contacts_send_message`, `contacts_send_flow`, `contacts_list_sequences`, `contacts_subscribe_sequences` |
| Conversations | `conversations_list`, `conversations_get`, `conversations_assign` |
| Error Logs | `error_logs_list` |
| Flows | `flows_list`, `flows_get`, `flows_create`, `flows_update_draft`, `flows_publish`, `flows_validate` |
| Keywords | `keywords_list` |
| Messages | `messages_list` |
| Sequences | `sequences_list`, `sequences_get`, `sequences_update` |

Everything else is reachable through `search_tools` and `call_tool` when the workspace token is
authorized: deletes, coupons, products, webhooks, saved replies, tag/trigger/inbox/custom-field
management, integrations, workspace members, and other less common operations.

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
2. Prefer read-only tokens for discovery and analytics tasks.
3. For broadcasts, inspect the audience first. Keep drafts and manual review when the task affects
   real customers.
4. For flows, call `schemas_flow_spec` and `flows_validate` before publishing a generated spec.
5. For destructive operations found through `search_tools`, fetch the current resource first and
   verify the exact id.
6. Do not put workspace tokens in prompts, logs, generated docs, or committed config.

## Troubleshooting

- Missing tools: call `token_get` to check scopes and permission, then refresh the MCP client so
  `tools/list` runs again.
- New API not visible: the server refreshes the OpenAPI spec after `CHATBOTX_SPEC_TTL_MS` (default
  5 minutes). Restart the MCP server to force a clean load.
- Auth errors: verify `CHATBOTX_API_KEY` and make sure `CHATBOTX_API_URL` includes the `/api` path
  prefix.
- Local TLS errors: set `CHATBOTX_ALLOW_SELF_SIGNED_CERT=true`, only for trusted local or
  self-hosted instances.
