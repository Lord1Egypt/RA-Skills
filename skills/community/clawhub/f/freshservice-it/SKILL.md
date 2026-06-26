---
name: freshservice-it
description: Manage Freshservice tickets, requesters, agents, assets, changes, problems, and service catalog data via the Freshservice API. Use this skill when users want to list and inspect tickets, create or update tickets after confirmation, work with requesters, agents, assets, locations, review problems, changes and releases, or browse service catalog items in Freshservice.
---

# Freshservice

![Freshservice](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/freshservice.png)

Access Freshservice via the Freshservice API with API key authentication. Manage tickets, requesters, agents, assets, changes, problems, and service catalog data.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshservice-it) for hosted connection flows and credentials so you do not need to configure Freshservice API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Freshservice |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Freshservice |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Freshservice API │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Freshservice                        │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │Freshservice│
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

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Freshservice again."

## Quick Start

```bash
# List all tickets
clawlink_call_tool --tool "freshservice_list_tickets" --params '{}'

# Get a specific ticket
clawlink_call_tool --tool "freshservice_get_ticket" --params '{"ticket_id": 12345}'

# List requesters
clawlink_call_tool --tool "freshservice_list_requesters" --params '{}'
```

## Authentication

All Freshservice tool calls are authenticated automatically by ClawLink using the user's connected Freshservice account.

**No API key is required in chat.** ClawLink stores credentials securely and injects them into every Freshservice API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=freshservice and connect Freshservice.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `freshservice` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration freshservice
```

**Response:** Returns the live tool catalog for Freshservice.

### Reconnect

If Freshservice tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=freshservice
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration freshservice`

## Security & Permissions

- Access is scoped to tickets, assets, and resources accessible to the connected Freshservice account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting tickets, assets, or releasing changes) are marked as high-impact and must be confirmed.
- IT service management operations depend on agent permissions.

## Tool Reference

### Tickets

| Tool | Description | Mode |
|------|-------------|------|
| `freshservice_list_tickets` | List tickets with filtering and pagination | Read |
| `freshservice_get_ticket` | Get ticket details by ID | Read |
| `freshservice_create_ticket` | Create a new service ticket | Write |
| `freshservice_update_ticket` | Update ticket fields | Write |
| `freshservice_delete_ticket` | Delete a ticket | Write |

### Requesters & Users

| Tool | Description | Mode |
|------|-------------|------|
| `freshservice_list_requesters` | List all requesters in the account | Read |
| `freshservice_get_requester` | Get requester details by ID | Read |
| `freshservice_list_agents` | List all agents | Read |
| `freshservice_get_agent` | Get agent details | Read |

### Assets

| Tool | Description | Mode |
|------|-------------|------|
| `freshservice_list_assets` | List all assets | Read |
| `freshservice_get_asset` | Get asset details | Read |

### Locations

| Tool | Description | Mode |
|------|-------------|------|
| `freshservice_list_locations` | List all locations | Read |

### Problems & Changes

| Tool | Description | Mode |
|------|-------------|------|
| `freshservice_list_problems` | List all problems | Read |
| `freshservice_get_problem` | Get problem details | Read |
| `freshservice_list_changes` | List all changes | Read |
| `freshservice_get_change` | Get change details | Read |

### Service Catalog

| Tool | Description | Mode |
|------|-------------|------|
| `freshservice_list_service_catalog_items` | List service catalog items | Read |
| `freshservice_get_service_catalog_item` | Get catalog item details | Read |

## Code Examples

### List all open tickets

```bash
clawlink_call_tool --tool "freshservice_list_tickets" \
  --params '{
    "filter": "open"
  }'
```

### Create a new ticket

```bash
clawlink_call_tool --tool "freshservice_create_ticket" \
  --params '{
    "subject": "Laptop not working",
    "description": "User reports laptop is not turning on",
    "email": "user@example.com",
    "priority": 2,
    "status": 2
  }'
```

### Get requester details

```bash
clawlink_call_tool --tool "freshservice_get_requester" \
  --params '{
    "requester_id": 12345
  }'
```

### List assets

```bash
clawlink_call_tool --tool "freshservice_list_assets" \
  --params '{}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Freshservice is connected.
2. Call `clawlink_list_tools --integration freshservice` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `freshservice`.
5. If no Freshservice tools appear, direct the user to https://claw-link.dev/dashboard?add=freshservice.

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
│  Example: Describe tool → Preview ticket → User approves    │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Ticket IDs and requester IDs are required for ticket and user-specific operations.
- Freshservice uses different status and priority values than Freshdesk — verify the expected values in the tool schema.
- Service catalog availability depends on the Freshservice plan and configuration.
- Asset management requires appropriate IT admin permissions.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration freshservice`. |
| Missing connection | Freshservice is not connected. Direct the user to https://claw-link.dev/dashboard?add=freshservice. |
| `404 Not Found` | Ticket or resource does not exist. Verify the ID. |
| `403 Forbidden` | Insufficient permissions for the requested operation. |
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

1. Ensure the integration slug is exactly `freshservice`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Freshservice API Documentation](https://api.freshservice.com/)
- [Freshservice Ticket API](https://api.freshservice.com/v2/tickets.html)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshservice-it)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Freshdesk Support](https://clawhub.ai/hith3sh/freshdesk-support) — For customer support ticketing
- [Zendesk](https://clawhub.ai/hith3sh/zendesk) — For alternative ticketing

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=freshservice-it)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)