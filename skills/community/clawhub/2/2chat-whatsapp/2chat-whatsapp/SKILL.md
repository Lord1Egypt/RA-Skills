---
name: 2chat-whatsapp
description: Send and receive WhatsApp messages (Web + Business API), SMS, and voice call records through 2Chat. Connects OpenClaw to the official 2Chat remote MCP server so the agent can message contacts, manage WABA templates, read conversations and groups, publish WhatsApp statuses, browse catalogs, and manage contacts. Use whenever the user wants to send a WhatsApp/SMS message, check if a number is on WhatsApp, work with WhatsApp Business templates, or manage 2Chat channels and contacts.
version: 1.0.0
homepage: https://2chat.co
metadata:
  openclaw:
    requires:
      bins: [openclaw]
    network:
      - host: mcp.2chat.io
        reason: Official 2Chat MCP endpoint. All WhatsApp/SMS/contact actions are proxied here. Auth is OAuth 2.1 browser sign-in (PKCE); no API keys are stored by this skill.
    keywords:
      - whatsapp
      - sms
      - 2chat
      - waba
      - messaging
      - mcp
---

# 2Chat — WhatsApp, SMS & Voice for OpenClaw

This skill connects OpenClaw to **2Chat's official remote MCP server**, letting the agent
send and read WhatsApp messages (both WhatsApp Web and the WhatsApp Business API), send SMS,
manage WABA templates, work with contacts, publish WhatsApp statuses, and pull call records —
all through your existing 2Chat account.

- **Server:** `https://mcp.2chat.io/mcp`
- **Transport:** Streamable HTTP
- **Auth:** OAuth 2.1 (browser sign-in with PKCE). **No API key required** — this skill stores no credentials.

## Setup (one time)

Register the remote server with OpenClaw and sign in through the browser:

```bash
openclaw mcp add 2chat \
  --url https://mcp.2chat.io/mcp \
  --transport streamable-http \
  --auth oauth

openclaw mcp login 2chat
```

`openclaw mcp login 2chat` opens the 2Chat sign-in page in your browser and stores the returned
tokens (with automatic refresh). A ready-to-paste config block is also included in
`mcp-server.json` in this skill if you prefer editing `mcp.servers` directly.

Verify it worked:

```bash
openclaw mcp probe 2chat
```

Or just ask the agent: *"List my connected 2Chat WhatsApp channels."*

## When to use this skill

Trigger this skill whenever the user wants to:

- Send a WhatsApp or SMS message, or check whether a number is on WhatsApp.
- Send WhatsApp **Business API** messages with approved templates, or list/sync/price WABA templates.
- Read conversations, group messages, or group participant lists.
- Publish a WhatsApp text/image/video **status** (story).
- Create, search, update, or delete **contacts**.
- Inspect connected channels (WhatsApp Web, WABA, virtual numbers) or pull **call records**.

## Available tools

Once connected, the following 2Chat tools are available to the agent.

**Account** — `get_who_am_i` (authenticated account info), `get_billing_info` (plan limits & usage).

**Messaging — WhatsApp Web** — `send_whatsapp_message` (text/media), `check_if_number_is_on_whatsapp`, `get_whatsapp_messages`.

**Messaging — WhatsApp Business API (WABA)** — `send_waba_message` (template or free-form), `get_waba_templates`, `sync_waba_templates` (pull from Meta), `calculate_waba_template_cost`.

**Messaging — SMS** — `send_sms`.

**Channels — WhatsApp Web** — `get_whatsapp_numbers`, `get_whatsapp_number`, `execute_whatsapp_channel_command` (connect/disconnect).

**Channels — WABA** — `get_waba_numbers`, `get_waba_number`.

**Conversations & Groups** — `list_whatsapp_conversations`, `list_whatsapp_groups`, `list_whatsapp_group_participants`, `get_whatsapp_group_messages`.

**Status (Stories)** — `set_whatsapp_text_status`, `set_whatsapp_image_status`, `set_whatsapp_video_status`.

**Catalog** — `list_whatsapp_catalog_products`.

**Contacts** — `create_contact`, `get_contact`, `list_contacts`, `search_contacts`, `update_contact`, `delete_contact`.

**Calls & Virtual Numbers** — `list_virtual_numbers`, `get_call_history` (CDRs), `get_call_details`, `get_call_price`.

## Usage guidance for the agent

- **Confirm before sending.** Before calling `send_whatsapp_message`, `send_waba_message`, or
  `send_sms`, echo the recipient and the exact message body back to the user for confirmation.
  These actions cost money and reach real people.
- **Verify reachability first** when appropriate: use `check_if_number_is_on_whatsapp` before a
  first-time WhatsApp send.
- **Prefer templates on WABA.** Outside the 24-hour customer service window, WhatsApp Business
  messages must use an approved template — use `get_waba_templates` and, if needed,
  `calculate_waba_template_cost` before sending.
- **Deletions are permanent.** `delete_contact` cannot be undone; confirm the contact UUID first.
- **Pick the right channel.** If the account has multiple connected numbers, list them with
  `get_whatsapp_numbers` / `get_waba_numbers` and confirm which one to send from.

## Notes

- 2Chat account and connected channels are required; connect a WhatsApp number in the 2Chat
  dashboard first (https://2chat.co) if none are listed.
- This skill only adds and calls the remote MCP server. It does not read local files or store
  secrets; all authentication is handled by OpenClaw's OAuth token store.
