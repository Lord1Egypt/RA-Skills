---
name: airtable-records
description: Browse Airtable bases and tables, inspect records, create records, and manage fields, comments, and table actions via the Airtable API. Use this skill when users want to read or write data in Airtable, manage base schemas, or automate record operations.
---

# Airtable

![Airtable](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/airtable.svg)

Work with Airtable from chat — browse bases and tables, read and create records, manage fields, comments, and table operations via the Airtable API with OAuth authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=airtable-records) for hosted connection flows and credentials so you do not need to configure Airtable API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Airtable |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Airtable |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Airtable API     │
│   (User Chat)   │     │   (OAuth)     │     │   (Bases/Records)│
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Airtable  │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Airtable│
   │  File    │           │ Auth     │           │ Bases   │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Airtable again."

## Quick Start

```bash
# List all accessible bases
clawlink_call_tool --tool "airtable_list_bases" --params '{}'

# Get base schema (tables and fields)
clawlink_call_tool --tool "airtable_get_base_schema" --params '{"base_id": "YOUR_BASE_ID"}'

# List records from a table
clawlink_call_tool --tool "airtable_list_records" --params '{"base_id": "YOUR_BASE_ID", "table_id": "YOUR_TABLE_ID", "max_records": 20}'
```

## Authentication

All Airtable tool calls are authenticated automatically by ClawLink using the user's connected Airtable account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Airtable API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=airtable and connect Airtable.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `airtable` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration airtable
```

**Response:** Returns the live tool catalog for Airtable.

### Reconnect

If Airtable tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=airtable
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration airtable`

## Security& Permissions

- Access is scoped to the bases and tables accessible to the connected Airtable account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete record, delete multiple records, delete field) are marked as high-impact and must be confirmed.
- Record deletion is permanent and cannot be undone.

## Tool Reference

### Base & Schema Operations

| Tool | Description | Mode |
|------|-------------|------|
| `airtable_list_bases` | List all Airtable bases accessible to the authenticated user | Read |
| `airtable_get_base_schema` | Get detailed schema for a base including tables and fields | Read |
| `airtable_create_base` | Create a new Airtable base with tables and fields | Write |
| `airtable_create_table` | Add a new table to an existing base | Write |
| `airtable_update_table` | Update table name, description, or date dependency settings | Write |

### Record Operations

| Tool | Description | Mode |
|------|-------------|------|
| `airtable_list_records` | List records from a table with filtering, sorting, and pagination | Read |
| `airtable_get_record` | Retrieve a specific record by its record ID | Read |
| `airtable_create_records` | Create up to 10 new records in a table | Write |
| `airtable_create_record_from_natural_language` | Create a record from a natural language description | Write |
| `airtable_update_record` | Update specific fields of an existing record | Write |
| `airtable_update_multiple_records` | Update up to 10 records with partial field modifications | Write |
| `airtable_delete_record` | Permanently delete a single record | Write |
| `airtable_delete_multiple_records` | Delete up to 10 records in one operation | Write |

### Field Operations

| Tool | Description | Mode |
|------|-------------|------|
| `airtable_create_field` | Add a new field to a table | Write |
| `airtable_update_field` | Update a field's name or description | Write |

### Comment Operations

| Tool | Description | Mode |
|------|-------------|------|
| `airtable_list_comments` | List comments on a specific record | Read |
| `airtable_create_comment` | Add a comment to a record, with optional threaded replies | Write |
| `airtable_update_comment` | Update an existing comment's text | Write |
| `airtable_delete_comment` | Delete a comment from a record | Write |

### Attachment Operations

| Tool | Description | Mode |
|------|-------------|------|
| `airtable_upload_attachment` | Upload a file attachment to a record field (base64-encoded) | Write |

### User Info

| Tool | Description | Mode |
|------|-------------|------|
| `airtable_get_user_info` | Get the authenticated user's ID and permission scopes | Read |

## Code Examples

### List records from a table

```bash
clawlink_call_tool --tool "airtable_list_records" \
  --params '{
    "base_id": "appXXXXXXXXXXXXXX",
    "table_id": "tblXXXXXXXXXXXXXX",
    "max_records": 20
  }'
```

### Create a new record

```bash
clawlink_call_tool --tool "airtable_create_records" \
  --params '{
    "base_id": "appXXXXXXXXXXXXXX",
    "table_id": "tblXXXXXXXXXXXXXX",
    "records": [
      {
        "fields": {
          "Name": "Alice Johnson",
          "Email": "alice@example.com",
          "Status": "Active"
        }
      }
    ]
  }'
```

### Update a record

```bash
clawlink_call_tool --tool "airtable_update_record" \
  --params '{
    "base_id": "appXXXXXXXXXXXXXX",
    "table_id": "tblXXXXXXXXXXXXXX",
    "record_id": "recXXXXXXXXXXXXXX",
    "fields": {
      "Status": "Completed",
      "Notes": "Updated via ClawLink"
    }
  }'
```

### Add a comment to a record

```bash
clawlink_call_tool --tool "airtable_create_comment" \
  --params '{
    "base_id": "appXXXXXXXXXXXXXX",
    "table_id": "tblXXXXXXXXXXXXXX",
    "record_id": "recXXXXXXXXXXXXXX",
    "text": "This record needs review - please check the details."
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Airtable is connected.
2. Call `clawlink_list_tools --integration airtable` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `airtable`.
5. If no Airtable tools appear, direct the user to https://claw-link.dev/dashboard?add=airtable.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                    │
│                                                             │
│  Example: List bases → Get schema → List records → Show    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                   │
│  list → get → describe → preview → confirm → call          │
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

- Base IDs start with `app` (e.g., `appXXXXXXXXXXXXXX`). Table IDs start with `tbl`. Record IDs start with `rec`.
- Empty field values are not returned in API responses.
- Attachments must be provided as base64-encoded strings.
- Rate limit: 5 requests per second per base.
- Maximum 10 records can be created or updated in a single batch operation.
- Comments support threaded replies via `parentCommentId`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration airtable`. |
| Missing connection | Airtable is not connected. Direct the user to https://claw-link.dev/dashboard?add=airtable. |
| `NOT_FOUND` | Base, table, or record does not exist. Check the IDs. |
| `INVALID_PERMISSIONS` | The authenticated user lacks permission for this operation. |
| `INVALIDArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `RATE_LIMIT_EXCEEDED` | Too many requests. Wait and retry. |
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

1. Ensure the integration slug is exactly `airtable`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [Airtable Base Schema](https://airtable.com/developers/web/api/schema)
- [Airtable Records](https://airtable.com/developers/web/api/records)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=airtable-records
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Notion](https://clawhub.ai/hith3sh/notion-workspace) — For Notion workspace operations
- [Google Sheets](https://clawhub.ai/hith3sh/google-sheets-spreadsheets) — For Google Workspace spreadsheet operations
- [Microsoft Excel](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) — For Microsoft Excel workbook operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=airtable-records)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
