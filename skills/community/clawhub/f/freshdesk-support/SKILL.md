---
name: freshdesk-support
description: Manage Freshdesk tickets, notes, watchers, conversations, and support workflows via the Freshdesk API. Use this skill when users want to search and inspect tickets, add notes and replies, manage ticket watchers and access, or coordinate customer-support workflows in Freshdesk.
---

# Freshdesk

![Freshdesk](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/freshdesk.svg)

Access Freshdesk via the Freshdesk API with API key authentication. Manage tickets, notes, watchers, conversations, and support workflows.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshdesk-support) for hosted connection flows and credentials so you do not need to configure Freshdesk API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Freshdesk |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Freshdesk |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Freshdesk API  │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Freshdesk │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Freshdesk│
   │  File    │           │ Auth     │           │ Tickets  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Freshdesk again."

## Quick Start

```bash
# List all tickets
clawlink_call_tool --tool "freshdesk_list_tickets" --params '{}'

# Get a specific ticket
clawlink_call_tool --tool "freshdesk_get_ticket" --params '{"ticket_id": 12345}'

# Add a note to a ticket
clawlink_call_tool --tool "freshdesk_add_note_to_ticket" --params '{"ticket_id": 12345, "body": "Internal note content", "private": true}'
```

## Authentication

All Freshdesk tool calls are authenticated automatically by ClawLink using the user's connected Freshdesk account.

**No API key is required in chat.** ClawLink stores credentials securely and injects them into every Freshdesk API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=freshdesk and connect Freshdesk.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `freshdesk` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration freshdesk
```

**Response:** Returns the live tool catalog for Freshdesk.

### Reconnect

If Freshdesk tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=freshdesk
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration freshdesk`

## Security & Permissions

- Access is scoped to tickets, conversations, and resources accessible to the connected Freshdesk account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting tickets, closing without resolution) are marked as high-impact and must be confirmed.
- Ticket access depends on agent permissions and ticket visibility settings.

## Tool Reference

### Tickets

| Tool | Description | Mode |
|------|-------------|------|
| `freshdesk_list_tickets` | List tickets with filtering options (status, priority, type) | Read |
| `freshdesk_get_ticket` | Get ticket details including description, requester, and assignments | Read |
| `freshdesk_create_ticket` | Create a new support ticket | Write |
| `freshdesk_update_ticket` | Update ticket fields (status, priority, assignee, etc.) | Write |
| `freshdesk_delete_ticket` | Delete a ticket permanently | Write |
| `freshdesk_add_note_to_ticket` | Add a private or public note to a ticket | Write |
| `freshdesk_reply_ticket` | Reply to a ticket conversation | Write |
| `freshdesk_add_watcher` | Add the authenticated user as a ticket watcher | Write |
| `freshdesk_bulk_unwatch_tickets` | Remove watcher status from multiple tickets | Write |

### Conversations

| Tool | Description | Mode |
|------|-------------|------|
| `freshdesk_list_ticket_conversations` | Get all conversations on a ticket (notes, replies, forwards) | Read |

### Agents & Users

| Tool | Description | Mode |
|------|-------------|------|
| `freshdesk_list_agents` | List all agents in the Freshdesk account | Read |
| `freshdesk_get_agent` | Get details for a specific agent | Read |
| `freshdesk_list_groups` | List all support groups | Read |
| `freshdesk_add_ticket_user_access` | Grant agent access to a specific ticket | Write |

### Companies

| Tool | Description | Mode |
|------|-------------|------|
| `freshdesk_list_companies` | List all companies in the account | Read |
| `freshdesk_get_company` | Get details for a specific company | Read |

## Code Examples

### List open tickets

```bash
clawlink_call_tool --tool "freshdesk_list_tickets" \
  --params '{
    "filter": "open"
  }'
```

### Add a private note to a ticket

```bash
clawlink_call_tool --tool "freshdesk_add_note_to_ticket" \
  --params '{
    "ticket_id": 12345,
    "body": "Customer called back. Issue resolved via phone call. Closing ticket.",
    "private": true
  }'
```

### Reply to a ticket

```bash
clawlink_call_tool --tool "freshdesk_reply_ticket" \
  --params '{
    "ticket_id": 12345,
    "body": "Thank you for reaching out. Our team is investigating this issue and will update you within 24 hours.",
    "incoming": false
  }'
```

### Update ticket priority

```bash
clawlink_call_tool --tool "freshdesk_update_ticket" \
  --params '{
    "ticket_id": 12345,
    "priority": 4,
    "status": 2
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Freshdesk is connected.
2. Call `clawlink_list_tools --integration freshdesk` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `freshdesk`.
5. If no Freshdesk tools appear, direct the user to https://claw-link.dev/dashboard?add=freshdesk.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List tickets → Get ticket → Show details          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview note → User approves      │
│           → Execute add note                                 │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Ticket IDs are required for all ticket-specific operations. Use `freshdesk_list_tickets` to find ticket IDs.
- Notes can be public (visible to customers) or private (agent-only). Always confirm which is intended.
- Replies sent via `freshdesk_reply_ticket` are always public and visible to the customer.
- Watcher functionality follows the authenticated user automatically — no need to specify user ID.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration freshdesk`. |
| Missing connection | Freshdesk is not connected. Direct the user to https://claw-link.dev/dashboard?add=freshdesk. |
| `404 Not Found` | Ticket or resource does not exist. Verify the ticket ID. |
| `403 Forbidden` | Insufficient permissions. Agent may not have access to this ticket. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `freshdesk`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Freshdesk API Documentation](https://developers.freshdesk.com/api/)
- [Freshdesk Ticket API](https://developers.freshdesk.com/api/#tickets)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshdesk-support)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Freshservice IT](https://clawhub.ai/hith3sh/freshservice-it) — For IT service management
- [Zendesk](https://clawhub.ai/hith3sh/zendesk) — For alternative support ticketing

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshdesk-support)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)