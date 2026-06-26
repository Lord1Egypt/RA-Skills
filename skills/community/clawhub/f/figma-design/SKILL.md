---
name: figma-design
description: Read files, manage comments, extract design tokens, download images, and create webhooks in Figma via the Figma REST API. Use this skill when users want to inspect Figma designs, export assets, manage file comments and reactions, extract design tokens for Tailwind CSS, or set up Figma webhooks for file event notifications.
---

# Figma

![Figma](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/figma.svg?v=2)

Access Figma via the Figma API with OAuth authentication. Read files, manage comments, extract design tokens, download images, and create webhooks for file event notifications.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=figma-design) for hosted connection flows and credentials so you do not need to configure Figma API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Figma |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Figma |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Figma API      │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Figma     │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Figma    │
   │  File    │           │ Auth     │           │ Files    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Figma again."

## Quick Start

```bash
# Get current authenticated Figma user
clawlink_call_tool --tool "figma_get_current_user" --params '{}'

# Discover file key and node IDs from a Figma URL
clawlink_call_tool --tool "figma_discover_figma_resources" --params '{"figma_url": "https://www.figma.com/file/ABC123xyz/MyFile"}'

# Get file JSON for a Figma design file
clawlink_call_tool --tool "figma_get_file_json" --params '{"file_key": "ABC123xyz"}'
```

## Authentication

All Figma tool calls are authenticated automatically by ClawLink using the user's connected Figma account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Figma API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=figma and connect Figma.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `figma` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration figma
```

**Response:** Returns the live tool catalog for Figma.

### Reconnect

If Figma tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=figma
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration figma`

## Security & Permissions

- Access is scoped to Figma files, comments, and resources accessible to the connected Figma account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete comment, delete webhook, delete reaction) are marked as high-impact and must be confirmed.
- Webhook creation requires team admin permissions for team-level webhooks, or edit access for project/file-level webhooks.

## Tool Reference

### File & Resource Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `figma_discover_figma_resources` | Extract file_key, node IDs, team_id, and project_id from any Figma URL | Read |
| `figma_get_file_metadata` | Get file name, creator, last modified, thumbnail, and access info | Read |
| `figma_get_current_user` | Get authenticated Figma user details | Read |

### File Content

| Tool | Description | Mode |
|------|-------------|------|
| `figma_get_file_json` | Get full Figma design file JSON with automatic simplification | Read |
| `figma_get_file_nodes` | Fetch JSON for specific node IDs from a file | Read |
| `figma_get_file_styles` | List published styles (colors, text, effects, grids) from a main file | Read |
| `figma_get_file_components` | List published components from a library file | Read |
| `figma_get_file_component_sets` | List published component sets from a main file | Read |

### Comments & Reactions

| Tool | Description | Mode |
|------|-------------|------|
| `figma_get_comments_in_a_file` | Get all comments from a file with author, position, and reactions | Read |
| `figma_add_a_comment_to_a_file` | Post a new comment or reply to an existing root comment | Write |
| `figma_delete_a_comment` | Delete a comment (must be original author) | Write |
| `figma_add_a_reaction_to_a_comment` | Add an emoji reaction to an existing comment | Write |
| `figma_delete_a_reaction` | Remove an emoji reaction from a comment | Write |
| `figma_get_reactions_for_a_comment` | Get all reactions for a specific comment | Read |

### Assets & Export

| Tool | Description | Mode |
|------|-------------|------|
| `figma_download_figma_images` | Download images from file nodes (PNG, SVG, JPG, PDF) | Read |
| `figma_render_images_of_file_nodes` | Render nodes as images with format and scale options | Read |
| `figma_get_image_fills` | Get temporary download URLs for all image fills in a file | Read |

### Design Tokens

| Tool | Description | Mode |
|------|-------------|------|
| `figma_extract_design_tokens` | Extract design tokens (styles, variables) from a Figma file | Read |
| `figma_design_tokens_to_tailwind` | Convert extracted design tokens to Tailwind CSS config | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `figma_create_a_webhook` | Create a webhook for file, project, or team events | Write |
| `figma_get_a_webhook` | Get details for a specific webhook | Read |
| `figma_get_team_webhooks` | List all webhooks for a team, project, or file context | Read |
| `figma_update_a_webhook` | Update webhook endpoint, event type, or status | Write |
| `figma_delete_a_webhook` | Permanently delete a webhook | Write |
| `figma_get_webhook_requests` | Get webhook request history (last 7 days) | Read |

### Teams & Projects

| Tool | Description | Mode |
|------|-------------|------|
| `figma_get_projects_in_a_team` | List projects in a Figma team | Read |
| `figma_get_files_in_a_project` | List files in a Figma project | Read |
| `figma_get_team_components` | List published components from a team's library | Read |
| `figma_get_team_styles` | List published styles from a team's library | Read |
| `figma_get_team_component_sets` | List published component sets from a team's library | Read |

## Code Examples

### Discover resources from a Figma URL

```bash
clawlink_call_tool --tool "figma_discover_figma_resources" \
  --params '{
    "figma_url": "https://www.figma.com/file/ABC123xyz/MyDesign"
  }'
```

### Get file JSON and extract a specific node

```bash
clawlink_call_tool --tool "figma_get_file_json" \
  --params '{
    "file_key": "ABC123xyz"
  }'
```

### Download an image from a file node

```bash
clawlink_call_tool --tool "figma_download_figma_images" \
  --params '{
    "file_key": "ABC123xyz",
    "images": [
      {
        "node_id": "1:2",
        "file_name": "logo.png",
        "format": "png"
      }
    ]
  }'
```

### Post a comment on a file

```bash
clawlink_call_tool --tool "figma_add_a_comment_to_a_file" \
  --params '{
    "file_key": "ABC123xyz",
    "comment": {
      "text": "Please review the updated hero section"
    }
  }'
```

### Extract design tokens and convert to Tailwind

```bash
# Step 1: Extract tokens
clawlink_call_tool --tool "figma_extract_design_tokens" \
  --params '{
    "file_key": "ABC123xyz"
  }'

# Step 2: Convert to Tailwind config (pass returned tokens)
clawlink_call_tool --tool "figma_design_tokens_to_tailwind" \
  --params '{
    "tokens": { "$schema": "...", "colors": {...} }
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Figma is connected.
2. Call `clawlink_list_tools --integration figma` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `figma`.
5. If no Figma tools appear, direct the user to https://claw-link.dev/dashboard?add=figma.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Discover file → Get JSON → Extract nodes          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview comment → User approves   │
│           → Execute post                                     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Only Design files (`figma.com/design/...`) are supported by `figma_get_file_json`. FigJam boards (`figma.com/board/...`) and Slides (`figma.com/slides/...`) return a 400 error.
- Node IDs can be found in Figma URLs after `node-id=`, or from the `figma_get_file_json` response.
- Downloaded image URLs expire after 14 days; download images immediately after generation.
- Webhook `team_id`, `project_id`, and `file_key` cannot be discovered via API — extract them from Figma URLs or use `figma_discover_figma_resources`.
- Comment replies cannot be nested; replies attach to existing root comments only.
- Design tokens not encoded as Figma styles or variables are silently omitted by `figma_extract_design_tokens`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration figma`. |
| Missing connection | Figma is not connected. Direct the user to https://claw-link.dev/dashboard?add=figma. |
| `400 File type not supported` | File is a FigJam board or Slides file, not a Design file. Only Design files work with `get_file_json`. |
| `404 Not Found` | File key, node ID, or webhook does not exist or is not accessible to the authenticated user. |
| `403 Forbidden` | Insufficient permissions for the requested operation (e.g., team admin required for team webhooks). |
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

1. Ensure the integration slug is exactly `figma`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Figma API Overview](https://www.figma.com/developers/api)
- [Figma REST API Reference](https://www.figma.com/developers/api/rest)
- [Figma Webhooks](https://www.figma.com/developers/api/webhooks)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=figma-design)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Google Sheets](https://clawhub.ai/hith3sh/google-sheets-spreadsheets) — For spreadsheet operations
- [OneDrive](https://clawhub.ai/hith3sh/onedrive-files) — For file management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=figma-design)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)