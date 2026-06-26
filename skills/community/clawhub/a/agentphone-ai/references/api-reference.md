# AgentPhone MCP Tools Reference

Complete reference for all MCP tools available through the AgentPhone server.

---

## Account

### account_overview

Get a complete snapshot of your AgentPhone account: agents, phone numbers, webhook status, and usage limits. Call this first to orient yourself.

**Parameters:** None

---

## Phone Numbers

### list_numbers

List all phone numbers in your account.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | number | no | 20 | Max results (1-100) |

### buy_number

Purchase a new phone number.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `country` | string | no | "US" | 2-letter ISO country code |
| `area_code` | string | no | — | 3-digit area code (US/CA only) |
| `agent_id` | string | no | — | Attach to agent immediately |

### release_number

Release (delete) a phone number. **Irreversible** — the number returns to the carrier pool.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `number_id` | string | yes | Number ID from list_numbers |

---

## Messages

### send_message

Send an outbound SMS (or iMessage where available) from one of your agent's phone numbers.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent to send from |
| `to_number` | string | yes | Destination phone number (E.164) |
| `body` | string | yes | Message text |
| `media_url` | string | no | URL of media to attach (MMS) |
| `number_id` | string | no | Specific number to send from |

### send_reaction

React to a message (e.g., tapback on iMessage).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message_id` | string | yes | Message ID to react to |
| `reaction` | string | yes | Reaction type (e.g., "Liked", "Loved", "Laughed", "Emphasized", "Questioned") |

### get_messages

Get SMS messages for a specific phone number.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `number_id` | string | yes | — | Number ID |
| `limit` | number | no | 50 | Max results (1-200) |

---

## Calls

### list_calls

List recent phone calls across all numbers.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | number | no | 20 | Max results (1-100) |

### list_calls_for_number

List calls for a specific phone number.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `number_id` | string | yes | — | Number ID |
| `limit` | number | no | 20 | Max results (1-100) |

### get_call

Get details and transcript for a specific call.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_id` | string | yes | Call ID |

### make_call

Initiate an outbound phone call (webhook-based). The agent must have a phone number and a webhook configured. For autonomous AI calls, use `make_conversation_call` instead.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |
| `to_number` | string | yes | E.164 format (e.g. +14155551234) |
| `initial_greeting` | string | no | Opening message spoken by the agent |

### make_conversation_call

Place a phone call where the AI holds an autonomous conversation. No webhook required — the built-in LLM handles the full conversation based on the topic.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID (must have a number attached) |
| `to_number` | string | yes | E.164 format |
| `topic` | string | yes | System prompt / conversation topic |
| `initial_greeting` | string | no | Opening message |

### make_web_call

Create a browser-based web call. Returns an access token for the AgentPhone Web SDK. Token expires after 30 seconds.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent to start the web call with |
| `metadata` | object | no | Optional metadata to attach to the call |

### stream_transcript

Stream a call's transcript in real time via Server-Sent Events. Replays existing turns on connect, then streams new turns live. Works for both live and completed calls.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_id` | string | yes | Call ID |

---

## Agents

### list_agents

List all agents with their phone numbers and voice configuration.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | number | no | 20 | Max results (1-100) |

### create_agent

Create a new agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Agent name |
| `description` | string | no | Agent description |
| `voice_mode` | "webhook" \| "hosted" | no | Call handling mode |
| `system_prompt` | string | no | System prompt (required for hosted mode) |
| `begin_message` | string | no | Auto-greeting when call connects |
| `voice` | string | no | Voice ID (use list_voices to see options) |

### get_agent

Get details for a specific agent including phone numbers and voice config.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |

### update_agent

Update an agent's configuration. Only provided fields are updated.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |
| `name` | string | no | New name |
| `description` | string | no | New description |
| `voice_mode` | "webhook" \| "hosted" | no | Call handling mode |
| `system_prompt` | string | no | System prompt |
| `begin_message` | string | no | Auto-greeting |
| `voice` | string | no | Voice ID |

### delete_agent

Delete an agent. Phone numbers attached to it are kept but unassigned. **Cannot be undone.**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |

### attach_number

Attach a phone number to an agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |
| `number_id` | string | yes | Number ID |

### detach_number

Detach a phone number from an agent. The number remains active and can be re-attached to any agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |
| `number_id` | string | yes | Number ID |

### list_voices

List available voices for agents. Use the `voice_id` when calling `create_agent` or `update_agent`.

**Parameters:** None

---

## Conversations

### list_conversations

List SMS conversations across all numbers. Each conversation is a thread between your number and an external contact.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | number | no | 20 | Max results (1-100) |

### get_conversation

Get a specific SMS conversation with message history.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `conversation_id` | string | yes | — | Conversation ID |
| `message_limit` | number | no | 50 | Max messages (1-100) |

### update_conversation

Update conversation metadata. Store custom context for AI agents (customer info, order IDs, session state). Metadata is included in webhook payloads as `conversationState`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `conversation_id` | string | yes | Conversation ID |
| `metadata` | object | no | Arbitrary JSON metadata |

---

## Contacts

### list_contacts

List all contacts in your account. Supports search by name or phone number.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | number | no | 50 | Max results (1-200) |
| `offset` | number | no | 0 | Pagination offset |
| `search` | string | no | — | Search by name or phone number |

### create_contact

Create a new contact. Phone number is normalized to E.164. Returns 409 if a contact with this phone number already exists.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phone_number` | string | yes | E.164 format phone number |
| `name` | string | yes | Contact name |
| `email` | string | no | Email address |
| `notes` | string | no | Free-text notes |

### get_contact

Get a specific contact by ID.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `contact_id` | string | yes | Contact ID |

### update_contact

Update a contact's fields. Only provided fields are updated.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `contact_id` | string | yes | Contact ID |
| `phone_number` | string | no | New phone number (E.164) |
| `name` | string | no | New name |
| `email` | string | no | New email |
| `notes` | string | no | New notes |

### delete_contact

Delete a contact. **Cannot be undone.**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `contact_id` | string | yes | Contact ID |

---

## Usage

### get_usage

Get account usage statistics: plan limits, phone number quotas, message/call volume, and webhook delivery stats.

**Parameters:** None

---

## Webhooks (Project-Level)

These manage the default webhook that receives events for all agents (unless overridden by an agent-specific webhook).

### get_webhook

Get the project-level webhook endpoint.

**Parameters:** None

### set_webhook

Set the project-level webhook URL.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Publicly accessible HTTPS URL |
| `context_limit` | number | no | Recent messages to include (0-50) |

### delete_webhook

Remove the project-level webhook. Agents with their own webhook are not affected.

**Parameters:** None

---

## Webhooks (Per-Agent)

These manage webhooks for individual agents. When set, the agent's events go here instead of the project-level webhook.

### get_agent_webhook

Get the webhook configured for a specific agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |

### set_agent_webhook

Set a webhook URL for a specific agent. Events will be delivered here instead of the project-level webhook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |
| `url` | string | yes | Publicly accessible HTTPS URL |
| `context_limit` | number | no | Recent messages to include (0-50) |

### delete_agent_webhook

Remove the webhook for a specific agent. Events fall back to the project-level webhook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | yes | Agent ID |
