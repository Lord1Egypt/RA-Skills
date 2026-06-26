---
name: box-files
description: Manage Box files, folders, collaborations, shared links, metadata, and enterprise content workflows via the Box API. Use this skill when users want to browse enterprise content, manage file sharing, automate document workflows, or coordinate Box Sign signature requests.
---

# Box

![Box](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/box.svg?v=2)

Access Box via the Box API with managed OAuth authentication. Browse files, inspect metadata, manage sharing and collaboration, and coordinate file workflows from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=box-files) for hosted connection flows and credentials so you do not need to configure Box API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Box |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Box |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│     Box API        │
│   (User Chat)   │     │   (OAuth)    │     │   (Files) │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Box      │                       │
          │                       │  4. Secure Token      │
          │                       │  5. Proxy Requests    │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  Box     │
    │  File    │           │ Auth     │           │ Web App │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Box again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Box tools
clawlink_list_tools --integration box

# Search for a specific tool
clawlink_search_tools --query "file" --integration box
```

## Authentication

All Box tool calls are authenticated automatically by ClawLink using the user's connected Box account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Box API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=box and connect Box.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `box` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration box
```

**Response:** Returns the live tool catalog for Box.

### Reconnect

If Box tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=box
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration box`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Box is connected.
2. Call `clawlink_list_tools --integration box` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `box`.
5. If no Box tools appear, direct the user to https://claw-link.dev/dashboard?add=box.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List files → Get metadata → Show results │
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

### Files& Folders

| Tool | Description | Mode |
|------|-------------|------|
| `box_list_folder` | List items in a folder | Read |
| `box_get_file` | Get file metadata and details | Read |
| `box_create_folder` | Create a new folder | Write |
| `box_upload_file` | Upload a file to Box | Write |
| `box_copy_file` | Copy a file to another folder | Write |
| `box_move_file` | Move a file to another folder | Write |
| `box_delete_file` | Permanently delete a file | Write |
| `box_download_file` | Download a file from Box | Read |

### Sharing & Collaborations

| Tool | Description | Mode |
|------|-------------|------|
| `box_create_collaboration` | Add a collaborator to a file or folder | Write |
| `box_delete_collaboration` | Remove a collaborator | Write |
| `box_add_shared_link_to_file` | Add a shared link to a file | Write |
| `box_add_shared_link_to_folder` | Add a shared link to a folder | Write |
| `box_get_file_collaborators` | List collaborators on a file | Read |

### Metadata& Templates

| Tool | Description | Mode |
|------|-------------|------|
| `box_create_metadata_template` | Create a metadata template | Write |
| `box_create_metadata_instance_on_file` | Apply metadata to a file | Write |
| `box_create_metadata_instance_on_folder` | Apply metadata to a folder | Write |
| `box_get_metadata_template` | Get metadata template details | Read |

### Box Sign (Signature Requests)

| Tool | Description | Mode |
|------|-------------|------|
| `box_create_box_sign_request` | Create a signature request | Write |
| `box_cancel_box_sign_request` | Cancel a pending signature request | Write |
| `box_get_sign_request` | Get signature request status | Read |

### Users& Groups

| Tool | Description | Mode |
|------|-------------|------|
| `box_list_users` | List enterprise users | Read |
| `box_create_user` | Create a new managed user | Write |
| `box_create_group` | Create a new group | Write |
| `box_add_user_to_group` | Add a user to a group | Write |

### Retention & Legal Hold

| Tool | Description | Mode |
|------|-------------|------|
| `box_create_retention_policy` | Create a retention policy | Write |
| `box_assign_retention_policy` | Assign a retention policy | Write |
| `box_create_legal_hold_policy` | Create a legal hold policy | Write |
| `box_assign_legal_hold_policy` | Assign a legal hold policy | Write |

### AI (Box AI Studio)

| Tool | Description | Mode |
|------|-------------|------|
| `box_ask_question` | Ask questions about Box files using AI | Read |
| `box_create_ai_agent` | Create a custom AI agent | Write |

## Code Examples

### List folder items

```bash
clawlink_call_tool --tool "box_list_folder" \
  --params '{
    "folder_id": "0",
    "limit": 20
  }'
```

### Get file metadata

```bash
clawlink_call_tool --tool "box_get_file" \
  --params '{
    "file_id": "123456789"
  }'
```

### Create a folder

```bash
clawlink_call_tool --tool "box_create_folder" \
  --params '{
    "name": "New Project Folder",
    "parent_folder_id": "0"
  }'
```

### Create a collaboration

```bash
clawlink_call_tool --tool "box_create_collaboration" \
  --params '{
    "item": {
      "type": "file",
      "id": "123456789"
    },
    "accessible_by": {
      "type": "user",
      "email": "collaborator@example.com"
    },
    "role": "viewer"
  }'
```

## Security & Permissions

- Access is scoped to the connected Box account's permissions and enterprise policies.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting files, folders, users) are marked as high-impact and must be confirmed.
- Collaboration changes affect external user access; confirm before adding or removing collaborators.
- Legal hold and retention policy operations require appropriate admin permissions.

## Notes

- Folder ID "0" refers to the root (All Files) folder.
- File IDs and folder IDs are distinct namespaces in Box.
- Shared links can be configured with different access levels (open, company, collaborators).
- Some enterprise features (classifications, legal hold, retention) require specific Box plans.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration box`. |
| Missing connection | Box is not connected. Direct the user to https://claw-link.dev/dashboard?add=box. |
| `ItemNotFound` | File or folder does not exist. Check the ID. |
| `Conflict` | A file or folder with that name already exists in the target location. |
| `AccessDenied` | No permission to access this resource. Verify account permissions. |
| `Write rejected` | User did not confirm a write action. Always confirm before executing writes. |

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

1. Ensure the integration slug is exactly `box`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Box Developer Documentation](https://developer.box.com/)
- [Box API Reference](https://developer.box.com/reference/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=box-files
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=box-files)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
