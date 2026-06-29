---
name: youtube-channel
description: Manage YouTube channels, videos, comments, playlists, and creator workflows via the YouTube Data API v3. Use this skill when users want to inspect channel analytics, manage video metadata, moderate comments, or automate publishing workflows.
---

# YouTube Channel

![YouTube Channel](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/youtube.svg)

Access YouTube via the YouTube Data API v3 with managed OAuth authentication. Inspect channels, videos, comments, playlists, and manage creator workflows from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clawlink-youtube) for hosted connection flows and credentials so you do not need to configure YouTube API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect YouTube |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect YouTube |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  YouTube Data │
│   (User Chat)   │     │   (OAuth)    │     │      API v3      │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect YouTube    │                       │
          │                       │  4. Secure Token      │
          │                       │  5. Proxy Requests    │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ YouTube  │
    │  File    │           │ Auth     │           │ Console  │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for YouTube again."

## Quick Start

```bash
# List connected integrations
clawlink_list_integrations

# List YouTube tools
clawlink_list_tools --integration youtube

# Search for a specific tool
clawlink_search_tools --query "channel" --integration youtube
```

## Authentication

All YouTube tool calls are authenticated automatically by ClawLink using the user's connected Google/YouTube account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every YouTube API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=youtube and connect YouTube.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `youtube` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration youtube
```

**Response:** Returns the live tool catalog for YouTube.

### Reconnect

If YouTube tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=youtube
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration youtube`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm YouTube is connected.
2. Call `clawlink_list_tools --integration youtube` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `youtube`.
5. If no YouTube tools appear, direct the user to https://claw-link.dev/dashboard?add=youtube.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List videos → Get details → Show results         │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Tool Reference

Tools are available dynamically from the live ClawLink catalog. Call `clawlink_list_tools --integration youtube` to see the full list.

### Typical Tool Categories

| Category | Description | Mode |
|----------|-------------|------|
| Channels | Inspect channel metadata, settings, and branding | Read |
| Videos | List, get, search, and manage video metadata | Read/Write |
| Playlists | Manage playlists and playlist items | Read/Write |
| Comments | Read and moderate comments | Read/Write |
| Subscriptions | Manage channel subscriptions | Read/Write |
| Analytics | Retrieve channel and video insights | Read |

## Code Examples

### List channel videos

```bash
clawlink_call_tool --tool "youtube_list_videos" \
  --params '{
    "channel_id": "YOUR_CHANNEL_ID",
    "max_results": 10
  }'
```

### Get video details

```bash
clawlink_call_tool --tool "youtube_get_video" \
  --params '{
    "video_id": "YOUR_VIDEO_ID"
  }'
```

### Search videos

```bash
clawlink_call_tool --tool "youtube_search_videos" \
  --params '{
    "query": "search term",
    "max_results": 10
  }'
```

## Security & Permissions

- Access is scoped to the connected YouTube account's data.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting comments, videos, or playlists) are marked as high-impact and must be confirmed.
- Channel permissions can be inspected to verify admin access before making changes.

## Notes

- YouTube Data API v3 has quota limits. Prefer batch operations and avoid unnecessary API calls.
- Video IDs are stable identifiers; use them instead of titles for precise operations.
- Some tools require a verified Google Cloud project with YouTube Data API enabled.
- When piping shell output, environment variables may not expand correctly in some shells; prefer explicit JSON parameters.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration youtube`. |
| Missing connection | YouTube is not connected. Direct the user to https://claw-link.dev/dashboard?add=youtube. |
| `notFound` | Resource (video, channel, playlist) does not exist. Check the ID. |
| `forbidden` | No permission to access this resource. Verify account access. |
| Quota exceeded | API quota limit reached. Wait or reduce request frequency. |
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

1. Ensure the integration slug is exactly `youtube`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube API Reference](https://developers.google.com/youtube/v3/docs)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clawlink-youtube
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clawlink-youtube)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
