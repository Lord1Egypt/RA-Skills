---
name: facebook-pages
description: Manage Facebook Pages, posts, comments, messages, and insights via the Facebook Graph API. Use this skill when users want to post content, read engagement metrics, moderate comments, or automate Facebook Page workflows from chat.
---

# Facebook

![Facebook](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/facebook.svg)

Access Facebook Pages via the Graph API with managed OAuth authentication. Post content, read engagement, manage comments and messages, and view insights from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=facebook-pages) for hosted connection flows and credentials so you do not need to configure Facebook API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Facebook |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Facebook |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Facebook Graph  │
│   (User Chat)   │     │   (OAuth)    │     │      API          │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Facebook  │                       │
          │                       │  4. Secure Token      │
          │                       │  5. Proxy Requests    │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Facebook │
 │  File    │           │ Auth     │           │ Business  │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Facebook again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Facebook tools
clawlink_list_tools --integration facebook

# Search for a specific tool
clawlink_search_tools --query "post" --integration facebook
```

## Authentication

All Facebook tool calls are authenticated automatically by ClawLink using the user's connected Facebook account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Facebook Graph API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=facebook and connect Facebook.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `facebook` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration facebook
```

**Response:** Returns the live tool catalog for Facebook.

### Reconnect

If Facebook tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=facebook
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration facebook`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Facebook is connected.
2. Call `clawlink_list_tools --integration facebook` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `facebook`.
5. If no Facebook tools appear, direct the user to https://claw-link.dev/dashboard?add=facebook.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List posts → Get insights → Show results         │
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

### Pages& Profiles

| Tool | Description | Mode |
|------|-------------|------|
| `facebook_list_managed_pages` | List Pages the user manages | Read |
| `facebook_get_page_details` | Get Page metadata and settings | Read |
| `facebook_get_page_roles` | Get Page roles and permissions | Read |
| `facebook_update_page_settings` | Update Page settings | Write |

### Posts

| Tool | Description | Mode |
|------|-------------|------|
| `facebook_get_page_posts` | Get posts from a Page | Read |
| `facebook_get_post` | Get a specific post | Read |
| `facebook_create_post` | Create a text or link post | Write |
| `facebook_create_photo_post` | Create a photo post | Write |
| `facebook_update_post` | Update an existing post | Write |
| `facebook_delete_post` | Delete a post | Write |
| `facebook_get_scheduled_posts` | Get scheduled posts | Read |
| `facebook_publish_scheduled_post` | Publish a scheduled post | Write |

### Comments

| Tool | Description | Mode |
|------|-------------|------|
| `facebook_get_comments` | Get comments on a post | Read |
| `facebook_get_comment` | Get a specific comment | Read |
| `facebook_create_comment` | Create a comment on a post | Write |
| `facebook_update_comment` | Update a comment | Write |
| `facebook_delete_comment` | Delete a comment | Write |

### Messaging

| Tool | Description | Mode |
|------|-------------|------|
| `facebook_get_page_conversations` | Get Page conversations | Read |
| `facebook_get_conversation_messages` | Get messages in a conversation | Read |
| `facebook_send_message` | Send a message from the Page | Write |
| `facebook_send_media_message` | Send media (image/video) message | Write |
| `facebook_mark_message_seen` | Mark a message as seen | Write |

### Insights& Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `facebook_get_page_insights` | Get Page analytics and metrics | Read |
| `facebook_get_post_insights` | Get post-specific insights | Read |
| `facebook_get_post_reactions` | Get reactions on a post | Read |

### Photo Albums

| Tool | Description | Mode |
|------|-------------|------|
| `facebook_create_photo_album` | Create a photo album | Write |
| `facebook_get_page_photos` | Get Page photos | Read |
| `facebook_upload_photos_batch` | Upload multiple photos | Write |

## Code Examples

### List managed Pages

```bash
clawlink_call_tool --tool "facebook_list_managed_pages" \
  --params '{}'
```

### Get Page posts

```bash
clawlink_call_tool --tool "facebook_get_page_posts" \
  --params '{
    "page_id": "YOUR_PAGE_ID",
    "limit": 20
  }'
```

### Create a post

```bash
clawlink_call_tool --tool "facebook_create_post" \
  --params '{
    "page_id": "YOUR_PAGE_ID",
    "message": "Hello from ClawLink! This is an automated post."
  }'
```

### Get post insights

```bash
clawlink_call_tool --tool "facebook_get_post_insights" \
  --params '{
    "post_id": "YOUR_POST_ID"
  }'
```

## Security & Permissions

- Access is scoped to the connected Facebook account's managed Pages and their permissions.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting posts, comments) are marked as high-impact and must be confirmed.
- Publishing posts affects the Page's public-facing content; confirm all write operations.
- Messaging operations deliver to real users; confirm before sending.

## Notes

- Facebook Graph API uses cursor-based pagination for large result sets.
- CDN-based media URLs (from `source` field) are time-limited; download promptly if long-term access is needed.
- Rate limits apply to API calls (error codes 4,17, 613); use backoff for high-volume operations.
- The API version is v23.0 (released May 2025); older versions are deprecated.
- Some permissions require Facebook app review before use in production.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration facebook`. |
| Missing connection | Facebook is not connected. Direct the user to https://claw-link.dev/dashboard?add=facebook. |
| `(#404) Page not found` | The Page ID does not exist or is not accessible. |
| `(#200) Permission denied` | The app does not have the required permission. |
| `(#190) Token expired` | The access token has expired. Reconnect Facebook. |
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

1. Ensure the integration slug is exactly `facebook`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api/)
- [Facebook Graph API Reference](https://developers.facebook.com/docs/graph-api/reference/)
- [Facebook Graph API Changelog](https://developers.facebook.com/docs/graph-api/changelog)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=facebook-pages
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=facebook-pages)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
