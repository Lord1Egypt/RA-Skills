---
name: apollo-sales
description: Search prospects, accounts, contacts, and outreach data in Apollo.io via the Apollo API. Use this skill when users want to find leads, enrich company and contact data, manage sales sequences, or update CRM records.
---

# Apollo

![Apollo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/apollo.svg)

Work with Apollo from chat — search prospects, accounts, contacts, and outreach data via the Apollo API with API key authentication.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apollo-sales) for hosted connection flows and credentials so you do not need to configure Apollo API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Apollo |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Apollo |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Apollo API       │
│   (User Chat)   │     │   (API Key)  │     │ (Enrichment/CRM) │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Apollo    │                       │
         │                       │  4. Secure Key │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Apollo  │
   │  File    │           │ Auth     │           │ Enrich │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Apollo again."

## Quick Start

```bash
# Search for contacts
clawlink_call_tool --tool "apollo_search_contacts" --params '{"query": "software engineer", "person_titles": ["engineer"]}'

# Enrich a person by email
clawlink_call_tool --tool "apollo_people_enrichment" --params '{"email": "john@example.com"}'

# Search for organizations
clawlink_call_tool --tool "apollo_organization_search" --params '{"query": "acme.com"}'
```

## Authentication

All Apollo tool calls are authenticated automatically by ClawLink using the user's connected Apollo account.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every Apollo API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=apollo and connect Apollo.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_integrations
```

**Response:** Returns all connected integrations. Look for `apollo` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration apollo
```

**Response:** Returns the live tool catalog for Apollo.

### Reconnect

If Apollo tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=apollo
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration apollo`

## Security & Permissions

- Access is scoped to the connected Apollo account's data and credits.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete contact, remove from sequence) are marked as high-impact and must be confirmed.
- Enrichment and search operations consume Apollo credits — confirm before large bulk operations.

## Tool Reference

### People & Contact Search

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_people_search` | Search Apollo contacts by keywords, title, seniority, and other filters | Read |
| `apollo_people_enrichment` | Enrich a person profile by email, LinkedIn URL, or name+company | Read |
| `apollo_bulk_people_enrichment` | Enrich up to 10 people profiles simultaneously | Read |
| `apollo_get_contact` | Get detailed information about a specific contact by ID | Read |
| `apollo_search_contacts` | Search contacts by keywords or stage IDs | Read |

### Organization Search & Enrichment

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_organization_search` | Search organizations by domain, name, or other filters | Read |
| `apollo_organization_enrichment` | Enrich organization data by domain | Read |
| `apollo_bulk_organization_enrichment` | Enrich up to 10 organizations by domain | Read |
| `apollo_get_organization` | Get detailed organization information by ID | Read |
| `apollo_get_organization_job_postings` | Get job postings for an organization | Read |

### Accounts

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_create_account` | Create a new account in Apollo | Write |
| `apollo_create_bulk_accounts` | Create up to 100 accounts in one call | Write |
| `apollo_update_account` | Update account attributes | Write |
| `apollo_bulk_update_account_stage` | Bulk update the stage for multiple accounts | Write |
| `apollo_search_accounts` | Search existing accounts in your Apollo database | Read |
| `apollo_get_account` | Get account details by Apollo ID | Read |

### Contacts (Create/Update)

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_create_contact` | Create a new contact (deduplication not automatic — search first) | Write |
| `apollo_create_bulk_contacts` | Create up to 100 contacts in one call | Write |
| `apollo_update_contact` | Update contact attributes | Write |
| `apollo_update_contacts_bulk` | Bulk update multiple contacts | Write |
| `apollo_update_contact_ownership` | Change contact owner | Write |
| `apollo_update_contact_stage` | Update contact stage in a sequence | Write |

### Sequences & Email

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_add_contacts_to_sequence` | Add contacts to an email sequence | Write |
| `apollo_update_contact_status_in_sequence` | Update a contact's status within a sequence | Write |
| `apollo_search_sequences` | Search available email sequences | Read |
| `apollo_search_outreach_emails` | Search emails sent through Apollo sequences | Read |

### Tasks & Calls

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_create_task` | Create a task for a contact | Write |
| `apollo_search_tasks` | Search tasks by keywords, date, priority, or assignee | Read |
| `apollo_create_call_record` | Log a call record from an external system | Write |
| `apollo_update_call_record` | Update a call record | Write |
| `apollo_search_calls` | Search logged call records | Read |

### Deals

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_create_deal` | Create a new sales opportunity/deal | Write |
| `apollo_update_deals` | Update deal fields | Write |
| `apollo_list_deals` | List deals from Apollo | Read |
| `apollo_get_deal` | Get deal details by ID | Read |

### Reference Data

| Tool | Description | Mode |
|------|-------------|------|
| `apollo_list_users` | List team members (needed for owner IDs) | Read |
| `apollo_list_account_stages` | Get available account stage IDs | Read |
| `apollo_list_contact_stages` | Get available contact stage IDs | Read |
| `apollo_get_opportunity_stages` | Get deal stage IDs | Read |
| `apollo_get_labels` | Get available labels for contacts/accounts | Read |
| `apollo_list_fields` | Get all field definitions | Read |
| `apollo_get_typed_custom_fields` | Get typed custom field definitions | Read |
| `apollo_view_api_usage_stats` | Check API usage and credit quota | Read |

## Code Examples

### Search for contacts by title

```bash
clawlink_call_tool --tool "apollo_search_contacts" \
  --params '{
    "query": "product manager",
    "person_titles": ["product manager"],
    "per_page": 10
  }'
```

### Enrich a person by email

```bash
clawlink_call_tool --tool "apollo_people_enrichment" \
  --params '{
    "email": "sarah.chen@techcorp.io"
  }'
```

### Create a new contact

```bash
clawlink_call_tool --tool "apollo_create_contact" \
  --params '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@company.com",
    "organization_name": "Acme Corp",
    "title": "VP Engineering"
  }'
```

### Add contacts to a sequence

```bash
clawlink_call_tool --tool "apollo_add_contacts_to_sequence" \
  --params '{
    "contact_ids": ["CONTACT_ID_1", "CONTACT_ID_2"],
    "sequence_id": "SEQUENCE_ID",
    "emailer_campaign_id": "CAMPAIGN_ID",
    "send_email_from_email_account_id": "EMAIL_ACCOUNT_ID"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Apollo is connected.
2. Call `clawlink_list_tools --integration apollo` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `apollo`.
5. If no Apollo tools appear, direct the user to https://claw-link.dev/dashboard?add=apollo.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe, but may consume credits)           │
│  search → enrich → get → list → call                        │
│                                                             │
│  Example: Search contacts → Enrich → Show results          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                   │
│  search → describe → preview → confirm → call              │
│                                                             │
│  Example: Search first → Preview create → User approves     │
│           → Execute create                                 │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Apollo does not auto-deduplicate contacts — always search via `apollo_search_contacts` before creating a new contact to avoid duplicates.
- Enrichment operations consume credits per person or organization enriched.
- Bulk enrichment may trigger HTTP 429 under burst usage — respect Retry-After headers.
- `org_not_found` and null email/phone fields in enrichment results are valid outcomes, not errors.
- Labels must be validated against `apollo_get_labels` before use on contacts or accounts.
- Custom field types must match the schema from `apollo_get_typed_custom_fields` or updates will fail.
- Sequence IDs and email campaign IDs must be retrieved from listing/search endpoints — they cannot be inferred from names.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration apollo`. |
| Missing connection | Apollo is not connected. Direct the user to https://claw-link.dev/dashboard?add=apollo. |
| `org_not_found` | Organization not found in Apollo database. Try a broader search. |
| `HTTP 429` | Rate limit hit. Wait and retry with exponential backoff. |
| `HTTP 422` | Invalid request — often missing required IDs or mismatched label/field values. |
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

1. Ensure the integration slug is exactly `apollo`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Apollo API Documentation](https://apolloio.github.io/apollo-api-docs/)
- [Apollo Contact Search API](https://apolloio.github.io/apollo-api-docs/#search-contacts)
- [Apollo Organization Enrichment](https://apolloio.github.io/apollo-api-docs/#organization-enrichment)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apollo-sales
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [HubSpot](https://clawhub.ai/hith3sh/hubspot-crm) — For HubSpot CRM operations
- [Salesforce](https://clawhub.ai/hith3sh/salesforce-crm) — For Salesforce CRM operations
- [LinkedIn](https://clawhub.ai/hith3sh/linkedin-professional) — For LinkedIn outreach operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apollo-sales)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
