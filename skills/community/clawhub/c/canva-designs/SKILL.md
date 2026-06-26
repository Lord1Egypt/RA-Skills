---
name: canva-designs
description: Create and manage Canva designs, upload assets, export content, and manage brand templates via the Canva Connect API. Use this skill when users want to automate design workflows, manage brand assets, or coordinate Canva content creation from chat.
---

# Canva

![Canva](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/canva.svg?v=2)

Access Canva via the Canva Connect API with managed OAuth authentication. Create designs, upload assets, export content, and manage brand templates from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=canva-designs) for hosted connection flows and credentials so you do not need to configure Canva API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Canva |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Canva |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Canva Connect │
│   (User Chat)   │     │   (OAuth)    │     │      API          │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Canva     │                       │
          │                       │  4. Secure Token      │
          │                       │  5. Proxy Requests    │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │   Canva   │
    │  File    │           │ Auth     │           │   Hub │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Canva again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Canva tools
clawlink_list_tools --integration canva

# Search for a specific tool
clawlink_search_tools --query "design" --integration canva
```

## Authentication

All Canva tool calls are authenticated automatically by ClawLink using the user's connected Canva account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Canva API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=canva and connect Canva.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `canva` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration canva
```

**Response:** Returns the live tool catalog for Canva.

### Reconnect

If Canva tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=canva
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration canva`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Canva is connected.
2. Call `clawlink_list_tools --integration canva` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `canva`.
5. If no Canva tools appear, direct the user to https://claw-link.dev/dashboard?add=canva.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List designs → Get metadata → Show results       │
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

Tools are available dynamically from the live ClawLink catalog. Call `clawlink_list_tools --integration canva` to see the full list.

### Typical Tool Categories

| Category | Description | Mode |
|----------|-------------|------|
| Designs | Create, list, get, and manage designs | Read/Write |
| Assets | Upload and manage brand assets | Read/Write |
| Exports | Export designs in various formats | Write |
| Brand Templates | Manage brand templates | Read/Write |
| User Profile | Get current user details | Read |

## Code Examples

### List designs

```bash
clawlink_call_tool --tool "canva_list_designs" \
  --params '{
    "limit": 20
  }'
```

### Get design metadata

```bash
clawlink_call_tool --tool "canva_get_design" \
  --params '{
    "design_id": "YOUR_DESIGN_ID"
  }'
```

### Upload an asset

```bash
clawlink_call_tool --tool "canva_upload_asset" \
  --params '{
    "name": "brand-logo.png",
    "asset_type": "image"
  }'
```

### Export a design

```bash
clawlink_call_tool --tool "canva_create_export" \
  --params '{
    "design_id": "YOUR_DESIGN_ID",
    "format": "PNG"
  }'
```

## Security& Permissions

- Access is scoped to the connected Canva account's designs and assets.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting designs, assets) are marked as high-impact and must be confirmed.
- Brand template management affects team-wide design standards; confirm before changes.

## Notes

- Canva API has rate limits; avoid excessive API calls in short succession.
- Export operations may be asynchronous; poll for completion if needed.
- Some Canva features require specific subscription plans (Canva Pro, Teams).
- Asset uploads are subject to file size and format restrictions.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration canva`. |
| Missing connection | Canva is not connected. Direct the user to https://claw-link.dev/dashboard?add=canva. |
| `Design not found` | The design ID does not exist or is not accessible. |
| `Export pending` | Export is still processing. Poll for completion. |
| `Upload failed` | The file could not be uploaded. Check file format and size. |
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

1. Ensure the integration slug is exactly `canva`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Canva Developer Documentation](https://www.canva.com/developers/)
- [Canva Connect API](https://www.canva.com/developers/docs/connect/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=canva-designs
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=canva-designs)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
