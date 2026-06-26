---
name: clickup-tasks
description: Manage ClickUp tasks, lists, spaces, folders, comments, goals, and workspace data via the ClickUp API. Use this skill when users want to create tasks, manage project workflows, track goals, or automate ClickUp workspace operations from chat.
---

# ClickUp

![ClickUp](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/clickup.svg)

Access ClickUp via the ClickUp API with managed API key authentication. Manage tasks, lists, spaces, folders, comments, goals, and workspace data from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickup-tasks) for hosted connection flows and credentials so you do not need to configure ClickUp API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect ClickUp |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect ClickUp |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    ClickUp API    │
│   (User Chat)   │     │   (API Key)  │     │   (Tasks)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │3. Connect ClickUp   │                       │
          │                       │  4. Secure Proxy │
          │                       │  5. API Requests        │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ ClickUp │
    │  File    │           │ Auth     │           │ Workspace│
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for ClickUp again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List ClickUp tools
clawlink_list_tools --integration clickup

# Search for a specific tool
clawlink_search_tools --query "task" --integration clickup
```

## Authentication

All ClickUp tool calls are authenticated automatically by ClawLink using the user's connected ClickUp API credentials.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every ClickUp API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=clickup and connect ClickUp.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `clickup` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration clickup
```

**Response:** Returns the live tool catalog for ClickUp.

### Reconnect

If ClickUp tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=clickup
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration clickup`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm ClickUp is connected.
2. Call `clawlink_list_tools --integration clickup` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `clickup`.
5. If no ClickUp tools appear, direct the user to https://claw-link.dev/dashboard?add=clickup.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List tasks → Get details → Show results            │
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

### Spaces, Folders& Lists

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_get_spaces` | List all spaces in a workspace | Read |
| `clickup_get_space` | Get space details | Read |
| `clickup_create_space` | Create a new space | Write |
| `clickup_delete_space` | Delete a space | Write |
| `clickup_get_folders` | List folders in a space | Read |
| `clickup_create_folder` | Create a folder | Write |
| `clickup_get_lists` | List lists in a folder | Read |
| `clickup_create_list` | Create a list | Write |

### Tasks

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_get_tasks` | List tasks in a list | Read |
| `clickup_get_task` | Get task details by ID | Read |
| `clickup_create_task` | Create a new task | Write |
| `clickup_update_task` | Update a task | Write |
| `clickup_delete_task` | Delete a task | Write |
| `clickup_get_filtered_team_tasks` | Get filtered tasks from workspace | Read |

### Comments& Collaboration

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_get_task_comments` | Get comments on a task | Read |
| `clickup_create_task_comment` | Add a comment to a task | Write |
| `clickup_create_threaded_comment` | Create a threaded reply | Write |
| `clickup_delete_comment` | Delete a comment | Write |

### Goals& Key Results

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_get_goals` | List goals in workspace | Read |
| `clickup_get_goal` | Get goal details | Read |
| `clickup_create_goal` | Create a new goal | Write |
| `clickup_delete_goal` | Delete a goal | Write |
| `clickup_create_key_result` | Create a key result for a goal | Write |

### Views& Templates

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_get_list_views` | List views for a list | Read |
| `clickup_create_list_view` | Create a view | Write |
| `clickup_get_task_templates` | Get task templates | Read |
| `clickup_create_task_from_template` | Create task from template | Write |

### Tags, Dependencies& Custom Fields

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_add_tag_to_task` | Add a tag to a task | Write |
| `clickup_add_dependency` | Add task dependency | Write |
| `clickup_get_accessible_custom_fields` | Get custom fields for a list | Read |

### Chat (Messages)

| Tool | Description | Mode |
|------|-------------|------|
| `clickup_get_chat_messages` | Get messages from a chat channel | Read |
| `clickup_create_chat_message` | Send a chat message | Write |
| `clickup_create_direct_message_channel` | Create a DM channel | Write |

## Code Examples

### List tasks in a list

```bash
clawlink_call_tool --tool "clickup_get_tasks" \
  --params '{
    "list_id": "123456"
  }'
```

### Create a task

```bash
clawlink_call_tool --tool "clickup_create_task" \
  --params '{
    "name": "New Feature Implementation",
    "list_id": "123456",
    "priority": 3,
    "due_date": 1705310400000
  }'
```

### Get task details

```bash
clawlink_call_tool --tool "clickup_get_task" \
  --params '{
    "task_id": "ABC123"
  }'
```

### Add a comment

```bash
clawlink_call_tool --tool "clickup_create_task_comment" \
  --params '{
    "task_id": "ABC123",
    "comment_text": "This is blocked by the upstream dependency"
  }'
```

## Security & Permissions

- Access is scoped to the connected ClickUp account's workspace permissions.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting tasks, spaces, folders, lists) are marked as high-impact and must be confirmed.
- Guest access is only available on ClickUp Enterprise plans.
- Bulk operations affect multiple records; confirm before executing.

## Notes

- ClickUp task IDs may be standard or custom; use `custom_task_ids=true` and provide `team_id` when using custom IDs.
- Some operations require specific ClickApps to be enabled (e.g., "Tasks in Multiple Lists").
- Time tracking data is available when the Time Tracking ClickApp is enabled.
- Nested subtasks have limitations on which list they can belong to.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration clickup`. |
| Missing connection | ClickUp is not connected. Direct the user to https://claw-link.dev/dashboard?add=clickup. |
| `Task not found` | The task ID does not exist or is not accessible. |
| `List not found` | The list ID does not exist or is not accessible. |
| `forbidden` | No permission to perform this action. Check workspace permissions. |
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

1. Ensure the integration slug is exactly `clickup`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [ClickUp API Documentation](https://clickup.com/api)
- [ClickUp API Reference](https://clickup.com/api/docs)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickup-tasks
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickup-tasks)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
