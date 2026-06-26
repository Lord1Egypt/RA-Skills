---
name: activecampaign-marketing
description: Manage contacts, campaigns, automations, lists, and marketing workflows in ActiveCampaign via the ActiveCampaign API. Use this skill when users want to search contacts, manage lists, create campaigns, configure automations, handle deals, or work with account and deal pipelines.
---

# ActiveCampaign

![ActiveCampaign](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/activecampaign.svg)

Manage ActiveCampaign from chat — contacts, campaigns, automations, lists, deals, and marketing workflows via the ActiveCampaign API with OAuth authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=activecampaign-marketing) for hosted connection flows and credentials so you do not need to configure ActiveCampaign API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect ActiveCampaign |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect ActiveCampaign |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ ActiveCampaign API │
│   (User Chat)   │     │   (OAuth)    │     │   (Contacts/Campaigns)│
└─────────────────┘     └──────────────┘     └──────────────────────┘
 │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect AC         │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Active │
   │  File    │           │ Auth     │           │ Campaign │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for ActiveCampaign again."

## Quick Start

```bash
# List all contacts
clawlink_call_tool --tool "activecampaign_list_contacts" --params '{"limit": 20}'

# Search for a contact by email
clawlink_call_tool --tool "activecampaign_get_contact" --params '{"contact_id": "CONTACT_ID"}'

# Add a contact to a list
clawlink_call_tool --tool "activecampaign_add_contact_to_list" --params '{"list_id": "LIST_ID", "contact_id": "CONTACT_ID"}'
```

## Authentication

All ActiveCampaign tool calls are authenticated automatically by ClawLink using the user's connected ActiveCampaign account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every ActiveCampaign API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=activecampaign and connect ActiveCampaign.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `activecampaign` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration activecampaign
```

**Response:** Returns the live tool catalog for ActiveCampaign.

### Reconnect

If ActiveCampaign tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=activecampaign
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration activecampaign`

## Security& Permissions

- Access is scoped to the connected ActiveCampaign account's data.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete contact, delete account, delete deal) are marked as high-impact and must be confirmed.

## Tool Reference

### Contacts

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_create_or_update_contact` | Create a new contact or update an existing one by email (upsert) | Write |
| `activecampaign_add_contact_to_list` | Subscribe or unsubscribe a contact from a list | Write |
| `activecampaign_add_contact_to_automation` | Enroll an existing contact in an automation workflow | Write |
| `activecampaign_add_tag_to_contact` | Associate a tag with a contact | Write |
| `activecampaign_add_contact_note` | Add a note to a contact record | Write |
| `activecampaign_create_contact_task` | Create a task associated with a contact | Write |
| `activecampaign_delete_contact` | Permanently delete a contact | Write |

### Accounts & Deals

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_create_account` | Create a new account/organization in ActiveCampaign | Write |
| `activecampaign_create_deal` | Create a new deal in a pipeline | Write |
| `activecampaign_create_deal_note` | Add a note to a deal | Write |
| `activecampaign_add_secondary_contact_to_deal` | Add a secondary contact to a deal | Write |
| `activecampaign_create_deal_pipeline` | Create a new deal pipeline with default stages | Write |
| `activecampaign_delete_deal` | Permanently delete a deal | Write |

### Campaigns & Automations

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_create_campaign` | Create a new email campaign | Write |
| `activecampaign_create_duplicate_campaign` | Duplicate an existing campaign | Write |
| `activecampaign_create_message` | Create an email message template | Write |
| `activecampaign_create_segment` | Create an advanced contact segment | Write |

### Lists & Tags

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_create_list` | Create a new subscriber list | Write |
| `activecampaign_add_list_group_permission` | Grant a user group access to a list | Write |
| `activecampaign_create_tag` | Create a new tag with explicit type | Write |

### Custom Fields

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_add_custom_field` | Create a new custom contact field | Write |
| `activecampaign_add_custom_field_options` | Add options to a dropdown/radio custom field | Write |
| `activecampaign_create_account_custom_field_meta` | Create a custom field for accounts | Write |
| `activecampaign_create_deal_custom_field_meta` | Create a custom field for deals | Write |

### E-Commerce & Events

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_create_an_order` | Record an e-commerce order | Write |
| `activecampaign_create_customer` | Create an e-commerce customer | Write |
| `activecampaign_create_event_tracking_event` | Whitelist a new event name for tracking | Write |
| `activecampaign_create_browse_session_cart` | Track add-to-cart event | Write |

### Webhooks & Connections

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_create_webhook` | Create a webhook for real-time notifications | Write |
| `activecampaign_create_connection` | Create a connection to an external service | Write |

### Bulk Operations

| Tool | Description | Mode |
|------|-------------|------|
| `activecampaign_bulk_import_contacts` | Import up to 250,000 contacts asynchronously | Write |
| `activecampaign_bulk_delete_accounts` | Delete multiple accounts in one operation | Write |

## Code Examples

### Add a contact to a list

```bash
clawlink_call_tool --tool "activecampaign_add_contact_to_list" \
  --params '{
    "list_id": "YOUR_LIST_ID",
    "contact_id": "YOUR_CONTACT_ID"
  }'
```

### Create or update a contact (upsert)

```bash
clawlink_call_tool --tool "activecampaign_create_or_update_contact" \
  --params '{
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1-555-0100"
  }'
```

### Enroll a contact in an automation

```bash
clawlink_call_tool --tool "activecampaign_add_contact_to_automation" \
  --params '{
    "contact_email": "john.doe@example.com",
    "automation_id": "YOUR_AUTOMATION_ID"
  }'
```

### Create a new deal

```bash
clawlink_call_tool --tool "activecampaign_create_deal" \
  --params '{
    "title": "Enterprise Deal - Acme Corp",
    "pipeline_id": "YOUR_PIPELINE_ID",
    "stage_id": "YOUR_STAGE_ID",
    "owner_id": 1
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm ActiveCampaign is connected.
2. Call `clawlink_list_tools --integration activecampaign` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `activecampaign`.
5. If no ActiveCampaign tools appear, direct the user to https://claw-link.dev/dashboard?add=activecampaign.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                     │
│                                                             │
│  Example: List contacts → Search by email → Show results     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                   │
│  list → get → describe → preview → confirm → call            │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- ActiveCampaign contact IDs are numeric. Use the contact's email or search tools to find IDs before performing operations.
- Automation IDs must correspond to existing, active automations in the account.
- Bulk import is asynchronous — the API returns immediately with a batch ID. Use the callback parameter to get notified when complete.
- Deal pipelines must exist before creating deals — retrieve pipeline IDs via the ActiveCampaign UI or API first.
- Table and worksheet IDs containing `{` and `}` must be URL-encoded (`%7B` and `%7D`) in raw API URLs. ClawLink handles this automatically.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration activecampaign`. |
| Missing connection | ActiveCampaign is not connected. Direct the user to https://claw-link.dev/dashboard?add=activecampaign. |
| `ContactNotFound` | Contact does not exist. Use search or list tools to find the correct ID. |
| `AutomationNotFound` | Automation ID does not exist or is not active. |
| `ListNotFound` | List ID does not exist. Retrieve list IDs via the ActiveCampaign UI. |
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

1. Ensure the integration slug is exactly `activecampaign`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [ActiveCampaign API Overview](https://developers.activecampaign.com/reference/overview)
- [ActiveCampaign Contact API](https://developers.activecampaign.com/reference/create-contact)
- [ActiveCampaign Deal API](https://developers.activecampaign.com/reference/deals)
- [ActiveCampaign Automation API](https://developers.activecampaign.com/reference/automations)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=activecampaign-marketing
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Mailchimp](https://clawhub.ai/hith3sh/mailchimp-email-marketing) — For Mailchimp email marketing operations
- [Brevo](https://clawhub.ai/hith3sh/brevo-email) — For Brevo/Sendinblue email campaigns
- [Klaviyo](https://clawhub.ai/hith3sh/klaviyo-email-marketing) — For Klaviyo e-commerce email marketing

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=activecampaign-marketing)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
