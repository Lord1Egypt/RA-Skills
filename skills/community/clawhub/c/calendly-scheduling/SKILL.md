---
name: calendly-scheduling
description: Manage Calendly events, invitees, scheduling links, webhooks, and availability via the Calendly API. Use this skill when users want to list events, check invitees, create scheduling links, manage webhooks, or handle event cancellations.
---

# Calendly

![Calendly](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/calendly.svg?v=2)

Work with Calendly from chat — manage events, invitees, scheduling links, webhooks, and availability via the Calendly API with OAuth authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=calendly-scheduling) for hosted connection flows and credentials so you do not need to configure Calendly API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Calendly |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Calendly |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Calendly API    │
│   (User Chat)   │     │   (OAuth)    │     │ (Events/Scheduling)│
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Calendly  │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Calendly │
   │  File    │           │ Auth     │           │ Scheduling│
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Calendly again."

## Quick Start

```bash
# List scheduled events
clawlink_call_tool --tool "calendly_list_scheduled_events" --params '{"user": "https://api.calendly.com/users/USER_UUID"}'

# List event types
clawlink_call_tool --tool "calendly_list_event_types" --params '{"user": "https://api.calendly.com/users/USER_UUID"}'

# Get event invitees
clawlink_call_tool --tool "calendly_list_event_invitees" --params '{"event": "https://api.calendly.com/scheduled_events/EVENT_UUID"}'
```

## Authentication

All Calendly tool calls are authenticated automatically by ClawLink using the user's connected Calendly account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Calendly API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=calendly and connect Calendly.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `calendly` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration calendly
```

**Response:** Returns the live tool catalog for Calendly.

### Reconnect

If Calendly tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=calendly
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration calendly`

## Security& Permissions

- Access is scoped to the connected Calendly account's events and resources.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (cancel event, delete invitee data, remove organization membership) are marked as high-impact and must be confirmed.

## Tool Reference

### Scheduled Events

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_list_scheduled_events` | List scheduled events for a user or organization | Read |
| `calendly_get_event` | Get a specific event by UUID | Read |
| `calendly_cancel_scheduled_event` | Permanently cancel a scheduled event (sends notifications) | Write |
| `calendly_list_event_invitees` | List invitees for a specific event | Read |
| `calendly_get_event_invitee` | Get a specific invitee's details | Read |
| `calendly_invitee_no_show` | Mark an invitee as a no-show | Write |

### Event Types

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_list_event_types` | List all event types for a user or organization | Read |
| `calendly_get_event_type` | Get a specific event type by UUID | Read |
| `calendly_create_event_type` | Create a new one-on-one event type | Write |
| `calendly_update_event_type` | Update an existing event type | Write |
| `calendly_list_event_type_memberships` | List hosts for an event type | Read |
| `calendly_get_event_type_availability` | Get availability rules for an event type | Read |
| `calendly_list_event_type_available_times` | Get available time slots for an event type | Read |

### Scheduling Links

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_create_scheduling_link` | Create a reusable scheduling link with max bookings | Write |
| `calendly_create_single_use_scheduling_link` | Create a one-time scheduling link | Write |
| `calendly_create_share` | Create a shareable link with event type overrides | Write |

### Users & Organizations

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_get_user` | Get user details | Read |
| `calendly_get_organization` | Get organization details | Read |
| `calendly_list_organization_memberships` | List organization members | Read |
| `calendly_list_user_busy_times` | Get user's busy time intervals | Read |
| `calendly_list_user_availability_schedules` | List user's availability schedules | Read |
| `calendly_get_user_availability_schedule` | Get a specific availability schedule | Read |
| `calendly_organization_invitation` | Invite a user to an organization | Write |
| `calendly_revoke_user_s_organization_invitation` | Revoke a pending invitation | Write |
| `calendly_remove_user_from_organization` | Remove a user from an organization | Write |

### Routing Forms

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_list_routing_forms` | List routing forms for an organization | Read |
| `calendly_get_routing_form` | Get a specific routing form | Read |
| `calendly_get_routing_form_submission` | Get a routing form submission | Read |

### Groups

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_list_groups` | List groups in an organization | Read |
| `calendly_get_group` | Get a specific group | Read |
| `calendly_list_group_relationships` | List user's group memberships and roles | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_list_webhook_subscriptions` | List webhook subscriptions for an organization | Read |
| `calendly_get_webhook_subscription` | Get a specific webhook subscription | Read |
| `calendly_create_webhooks` | Create a webhook subscription | Write |
| `calendly_delete_webhook_subscription` | Delete a webhook subscription | Write |
| `calendly_get_sample_webhook_data` | Get sample webhook payload for testing | Read |

### Activity & Data

| Tool | Description | Mode |
|------|-------------|------|
| `calendly_list_activity_log_entries` | List activity log entries (Enterprise only) | Read |
| `calendly_delete_invitee_data` | Delete invitee data for GDPR compliance (Enterprise) | Write |
| `calendly_delete_scheduled_event_data` | Delete scheduled event data in a time range (Enterprise) | Write |

## Code Examples

### List upcoming events

```bash
clawlink_call_tool --tool "calendly_list_scheduled_events" \
  --params '{
    "user": "https://api.calendly.com/users/YOUR_USER_UUID",
    "status": "active",
    "count": 20
  }'
```

### Create a scheduling link

```bash
clawlink_call_tool --tool "calendly_create_scheduling_link" \
  --params '{
    "owner": "https://api.calendly.com/users/YOUR_USER_UUID",
    "max_event_count": 5,
    "applies_to": "events"
  }'
```

### Cancel a scheduled event

```bash
clawlink_call_tool --tool "calendly_cancel_scheduled_event" \
  --params '{
    "event": "https://api.calendly.com/scheduled_events/EVENT_UUID",
    "reason": "Rescheduled by organizer"
  }'
```

### Create a webhook subscription

```bash
clawlink_call_tool --tool "calendly_create_webhooks" \
  --params '{
    "organization": "https://api.calendly.com/organizations/YOUR_ORG_UUID",
    "scope": "organization",
    "callback_url": "https://your-server.com/webhooks/calendly",
    "events": ["invitee.created", "invitee.canceled"]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Calendly is connected.
2. Call `clawlink_list_tools --integration calendly` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `calendly`.
5. If no Calendly tools appear, direct the user to https://claw-link.dev/dashboard?add=calendly.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → call                              │
│                                                             │
│  Example: List events → Get event details → Show results    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call         │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Event UUIDs are in URL format (e.g., `https://api.calendly.com/scheduled_events/UUID`).
- Organization scope webhooks trigger for all events in the org; user/group scopes are more targeted.
- Single-use scheduling links expire after one booking.
- Invite data deletion is asynchronous and may take up to one week (Enterprise).
- Event data deletion may take up to 7 days to complete (Enterprise).
- Organization owners cannot be removed from their own organization.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration calendly`. |
| Missing connection | Calendly is not connected. Direct the user to https://claw-link.dev/dashboard?add=calendly. |
| `not_found` | Event, user, or resource does not exist. Check the UUID. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
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

1. Ensure the integration slug is exactly `calendly`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Calendly API Documentation](https://developer.calendly.com/)
- [Calendly Events API](https://developer.calendly.com/api-docs/evedefaultapi/scheduled-events)
- [Calendly Webhooks](https://developer.calendly.com/api-docs/webhook-subscriptions)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=calendly-scheduling
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Calendar](https://clawhub.ai/hith3sh/google-calendar-scheduling) — For Google Calendar operations
- [Zoom](https://clawhub.ai/hith3sh/zoom-meetings) — For Zoom meeting management
- [Microsoft Outlook](https://clawhub.ai/hith3sh/outlook-mail) — For Outlook calendar and mail

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=calendly-scheduling)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
