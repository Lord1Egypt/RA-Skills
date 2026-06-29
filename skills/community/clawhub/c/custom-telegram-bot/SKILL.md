---
name: custom-telegram-bot
description: "Custom Telegram Bot: Two-way Telegram messaging through the user's own custom bot token. Use when an agent needs custom telegram bot, build a branded customer support bot on telegram, send business notifications under your own bot identity, receive and respond to inbound customer messages, share photos and documents from your branded bot, get updates, offset, limit through AgentPMT-hosted remote tool calls. Discovery terms: custom telegram bot, build a branded customer support bot on telegram."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/custom-telegram-bot
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/custom-telegram-bot"}}
---
# Custom Telegram Bot

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Build your own branded Telegram bot and connect it to your AI agent for fully customizable two-way communication. Create a bot through Telegram's BotFather, choose your own name and profile picture, define custom commands, then connect it here. Send and receive text messages, share photos and documents, track unread conversations with smart cursors, and create interactive button menus — all under your own brand identity.

## Product Instructions
### Custom Telegram Bot

Two-way messaging through your own Telegram bot connection.

#### Setup

1. Create your Telegram bot
2. Connect the required Telegram credential in AgentPMT
3. Send `/start` to your bot in Telegram
4. Use `get_updates` to read inbound messages and reply

#### Actions

##### `send_message`
Required: `chat_id`, `text`

##### `send_photo`
Required: `chat_id`
Provide one of:
- `photo` (URL, Telegram file_id, or base64)
- `photo_file_id` (AgentPMT File Manager file_id)

##### `send_document`
Required: `chat_id`
Provide one of:
- `document` (URL, Telegram file_id, or base64)
- `document_file_id` (AgentPMT File Manager file_id)

If using base64 `document`, `filename` is required.

##### `get_updates`
Optional:
- `offset`, `limit` (1-100), `timeout` (0-60), `allowed_updates`
- `unread_only`, `cursor_offset`, `mark_as_read`
- `ingest_files_to_manager`, `ingest_max_files`, `ingest_expiration_days`

##### `list_known_chat_ids`
Returns chat IDs seen by this BYO bot within this budget scope.
Use `get_updates` first to discover chats.

#### File Manager Flows

- Send from File Manager: use `photo_file_id` or `document_file_id`
- Save inbound Telegram media: set `ingest_files_to_manager: true` on `get_updates`
- Ingested uploads are returned in `ingested_files` with new File Manager `file_id` values

#### Shared Optional Params (send actions)

`parse_mode`, `caption`, `reply_markup`, `disable_notification`, `protect_content`, `message_thread_id`

## When To Use
- Use this skill for `Custom Telegram Bot` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: custom telegram bot, build a branded customer support bot on telegram, send business notifications under your own bot identity, receive and respond to inbound customer messages, share photos and documents from your branded bot, get updates, offset, limit.
- Supported action names: `get_updates`, `list_known_chat_ids`, `send_document`, `send_message`, `send_photo`.

## Use Cases
- Build a branded customer support bot on Telegram
- Send business notifications under your own bot identity
- Receive and respond to inbound customer messages
- Share photos and documents from your branded bot
- Create interactive menus with inline keyboard buttons
- Run automated conversational workflows
- Collect leads and feedback through your own Telegram bot
- Internal team communication with a custom bot

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `get_updates` (action slug: `get-updates`): Poll incoming updates with persisted cursor and optional media ingestion into File Manager. Price: `2` credits. Parameters: `allowed_updates`, `cursor_offset`, `ingest_expiration_days`, `ingest_files_to_manager`, `ingest_max_files`, `limit`, `mark_as_read`, `offset`, plus 2 more.
- `list_known_chat_ids` (action slug: `list-known-chat-ids`): List known chat IDs discovered by get_updates for this BYO bot scope. Price: `0` credits. Parameters: none.
- `send_document` (action slug: `send-document`): Send a document via URL/file_id/base64 or File Manager file_id. Price: `2` credits. Parameters: `caption`, `chat_id`, `disable_notification`, `document`, `document_file_id`, `filename`, `message_thread_id`, `parse_mode`, plus 1 more.
- `send_message` (action slug: `send-message`): Send a text message to a Telegram user, group, or channel your bot can access. Price: `2` credits. Parameters: `chat_id`, `disable_notification`, `message_thread_id`, `parse_mode`, `protect_content`, `reply_markup`, `text`.
- `send_photo` (action slug: `send-photo`): Send a photo via URL/file_id/base64 or File Manager file_id. Price: `2` credits. Parameters: `caption`, `chat_id`, `disable_notification`, `message_thread_id`, `parse_mode`, `photo`, `photo_file_id`, `protect_content`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "custom-telegram-bot"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "custom-telegram-bot"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "custom-telegram-bot"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "custom-telegram-bot"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "custom-telegram-bot"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "custom-telegram-bot"
  }
}
```

## Call This Tool
Product slug: `custom-telegram-bot`

Marketplace page: https://www.agentpmt.com/marketplace/custom-telegram-bot

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Custom-Telegram-Bot",
    "arguments": {
      "action": "get_updates",
      "allowed_updates": [
        "example allowed update"
      ],
      "cursor_offset": 1,
      "ingest_expiration_days": 7,
      "ingest_files_to_manager": true,
      "ingest_max_files": 10,
      "limit": 100,
      "mark_as_read": true,
      "offset": 1
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "custom-telegram-bot",
  "parameters": {
    "action": "get_updates",
    "allowed_updates": [
      "example allowed update"
    ],
    "cursor_offset": 1,
    "ingest_expiration_days": 7,
    "ingest_files_to_manager": true,
    "ingest_max_files": 10,
    "limit": 100,
    "mark_as_read": true,
    "offset": 1
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_updates` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/custom-telegram-bot
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
