---
name: amplitude-analytics
description: Analyze product events, cohorts, releases, dashboards, and experiment insights via the Amplitude Analytics API. Use this skill when users want to query event analytics, manage cohorts, track releases, or analyze user behavior data.
---

# Amplitude

![Amplitude](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/amplitude.png)

Access Amplitude via the Analytics API with managed API key authentication. Analyze product events, cohorts, releases, dashboards, and experiment data from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=amplitude-analytics) for hosted connection flows and credentials so you do not need to configure Amplitude API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Amplitude |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Amplitude |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Amplitude      │
│   (User Chat)   │     │   (API Key)  │     │   Analytics API  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Amplitude  │                       │
          │                       │  4. Secure Proxy       │
          │                       │  5. API Requests │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Amplitude│
    │  File    │           │ Auth     │           │ Dashboard│
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Amplitude again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Amplitude tools
clawlink_list_tools --integration amplitude

# Search for a specific tool
clawlink_search_tools --query "event" --integration amplitude
```

## Authentication

All Amplitude tool calls are authenticated automatically by ClawLink using the user's connected Amplitude API credentials.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every Amplitude API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=amplitude and connect Amplitude.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `amplitude` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration amplitude
```

**Response:** Returns the live tool catalog for Amplitude.

### Reconnect

If Amplitude tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=amplitude
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration amplitude`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Amplitude is connected.
2. Call `clawlink_list_tools --integration amplitude` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `amplitude`.
5. If no Amplitude tools appear, direct the user to https://claw-link.dev/dashboard?add=amplitude.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List events → Get segmentation → Show results    │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
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

## Tool Reference

### Events & Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `amplitude_list_events` | List all event types with recent statistics | Read |
| `amplitude_get_event_segmentation` | Get event metrics over time with grouping | Read |
| `amplitude_get_funnel_data` | Get funnel analysis showing user conversion | Read |
| `amplitude_get_retention` | Get user retention analysis by cohort | Read |
| `amplitude_get_revenue_ltv` | Get revenue LTV metrics | Read |

### Users & Activity

| Tool | Description | Mode |
|------|-------------|------|
| `amplitude_find_user` | Search for users by canonical identifier | Read |
| `amplitude_get_user_activity` | Get a user's profile and event stream | Read |
| `amplitude_get_active_users` | Get active/new user counts for a date range | Read |
| `amplitude_get_realtime_active_users` | Get real-time active users count | Read |
| `amplitude_get_user_composition` | Get user breakdown by property | Read |

### Cohorts

| Tool | Description | Mode |
|------|-------------|------|
| `amplitude_list_cohorts` | List all discoverable cohorts | Read |
| `amplitude_get_cohort` | Get a cohort by ID and initiate download | Read |
| `amplitude_check_cohort_status` | Check cohort export request status | Read |
| `amplitude_download_cohort_file` | Download cohort file after completion | Read |
| `amplitude_upload_cohort` | Upload or update a cohort | Write |

### Annotations & Releases

| Tool | Description | Mode |
|------|-------------|------|
| `amplitude_list_annotations` | List chart annotations with filtering | Read |
| `amplitude_create_annotation` | Create a chart annotation | Write |
| `amplitude_create_release` | Document a product release | Write |
| `amplitude_delete_annotation` | Delete a chart annotation | Write |

### Sessions & Engagement

| Tool | Description | Mode |
|------|-------------|------|
| `amplitude_get_session_average` | Get average session length | Read |
| `amplitude_get_session_length` | Get session length distribution | Read |
| `amplitude_get_sessions_per_user` | Get average sessions per user | Read |

### User Management

| Tool | Description | Mode |
|------|-------------|------|
| `amplitude_identify` | Update user properties | Write |
| `amplitude_delete_users` | Submit user deletion requests (GDPR/CCPA) | Write |
| `amplitude_map_user` | Map/merge user identities | Write |

## Code Examples

### Get active users

```bash
clawlink_call_tool --tool "amplitude_get_active_users" \
  --params '{
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "unit": "day"
  }'
```

### Get event segmentation

```bash
clawlink_call_tool --tool "amplitude_get_event_segmentation" \
  --params '{
    "event": "page_view",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "interval": "day"
  }'
```

### List cohorts

```bash
clawlink_call_tool --tool "amplitude_list_cohorts" \
  --params '{}'
```

### Create an annotation

```bash
clawlink_call_tool --tool "amplitude_create_annotation" \
  --params '{
    "label": "Feature Launch",
    "date": "2025-01-15",
    "category": "release"
  }'
```

## Security & Permissions

- Access is scoped to the connected Amplitude project's data.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting users, annotations) are marked as high-impact and must be confirmed.
- GDPR/CCPA deletion requests are irreversible once submitted.
- Cohort uploads and user mapping affect downstream analytics segmentation.

## Notes

- Some analytics queries may return large datasets; use pagination and filtering to limit results.
- Event data may have a delay before appearing in queries (typically minutes to hours).
- Cohort downloads are asynchronous; poll the status before downloading.
- For EU data residency, ensure the project is configured accordingly.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration amplitude`. |
| Missing connection | Amplitude is not connected. Direct the user to https://claw-link.dev/dashboard?add=amplitude. |
| `Invalid API key` | The Amplitude API key is invalid or expired. Reconnect the integration. |
| `Project not found` | The project ID does not exist or is inaccessible. |
| `Cohort not ready` | Cohort export is still processing. Poll with `check_cohort_status`. |
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

1. Ensure the integration slug is exactly `amplitude`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Amplitude Analytics API](https://amplitude.com/docs/apis)
- [Amplitude API Reference](https://developers.amplitude.com/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=amplitude-analytics
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=amplitude-analytics)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
