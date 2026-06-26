---
name: constant-contact
description: |
  Constant Contact API integration with managed OAuth. This is a write-capable integration — it can read, create, update, delete, and bulk-modify contacts, email campaigns, contact lists, tags, custom fields, segments, and marketing analytics.
  Use this skill when users want to interact with Constant Contact marketing data. All write operations (POST, PUT, DELETE, bulk actions, campaign sending/scheduling) require explicit user approval with specific resource identifiers before execution.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Constant Contact

Access the Constant Contact V3 API with managed OAuth authentication. Manage contacts, email campaigns, contact lists, tags, custom fields, segments, bulk operations, and marketing analytics.

## Quick Start

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/constant-contact/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/constant-contact/v3/{resource}
```

Maton proxies requests to `api.cc.email/v3` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Constant Contact OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=constant-contact&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'constant-contact'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T07:41:05.859244Z",
    "last_updated_time": "2026-02-07T07:41:32.658230Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "constant-contact",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Constant Contact connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/constant-contact/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

Always include the `Maton-Connection` header to ensure requests go to the intended account, especially before any write operation. If you have multiple connections and omit this header, the gateway uses the default connection, which may not be the intended account.

## Security & Permissions

- Access is scoped to contacts, email campaigns, lists, segments, tags, custom fields, and marketing analytics within the connected Constant Contact account. Only install if you need Constant Contact administration. Revoke unused connections promptly.
- **Default to read-only operations.** Always start by listing or retrieving resources to confirm identifiers before proposing any changes.
- **All write operations require explicit user approval with specific identifiers.** Before executing any POST, PUT, PATCH, or DELETE call:
  1. Retrieve and display the target resource (contact email, list name, campaign name/ID) so the user can verify.
  2. Clearly describe the intended effect (e.g., "This will delete contact 'john@example.com' (ID: abc123) from your account").
  3. Wait for explicit user confirmation before proceeding.
- **High-impact operations require extra caution.** Sending/scheduling email campaigns, bulk contact deletions, bulk list membership changes, and importing contacts can affect large numbers of marketing contacts and external recipients. These actions must include a summary of consequences and require confirmation.
- **Campaign sending is irreversible** — emails are delivered to external recipients immediately. Always preview the campaign and confirm recipients, subject, and content before sending or scheduling.

## API Reference

### Account

#### Get Account Summary

```bash
GET /constant-contact/v3/account/summary
```

**Response:**
```json
{
  "contact_email": "user@example.com",
  "contact_phone": "5551234567",
  "country_code": "us",
  "encoded_account_id": "abc123",
  "first_name": "John",
  "last_name": "Doe",
  "organization_name": "Acme Inc",
  "state_code": "CA",
  "time_zone_id": "US/Eastern"
}
```

#### Update Account Summary

```bash
PUT /constant-contact/v3/account/summary
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "organization_name": "Acme Inc",
  "time_zone_id": "US/Eastern"
}
```

#### Get Account Emails

Returns confirmed sender email addresses for the account.

```bash
GET /constant-contact/v3/account/emails
```

**Response:**
```json
[
  {
    "email_id": 1,
    "email_address": "marketing@example.com",
    "roles": ["BILLING", "CONTACT", "DEFAULT_FROM", "REPLY_TO"],
    "confirm_status": "CONFIRMED",
    "confirm_time": "2026-02-05T07:32:49.766+0000",
    "confirm_source_type": "SITE_OWNER"
  }
]
```

#### Add Account Email

```bash
POST /constant-contact/v3/account/emails
Content-Type: application/json

{
  "email_address": "newsender@example.com"
}
```

A confirmation email will be sent to the address. The email must be confirmed before it can be used as a sender.

#### Get User Privileges

```bash
GET /constant-contact/v3/account/user/privileges
```

### Contacts

#### List Contacts

```bash
GET /constant-contact/v3/contacts
```

Query parameters:
- `status` - Filter by status: `all`, `active`, `deleted`, `not_set`, `pending_confirmation`, `temp_hold`, `unsubscribed`
- `email` - Filter by exact email address
- `lists` - Filter by list ID(s), comma-separated
- `segment_id` - Filter by segment ID
- `tags` - Filter by tag ID(s), comma-separated
- `updated_after` - ISO-8601 date filter (e.g., `2026-04-01T00:00:00Z`)
- `include` - Include subresources: `custom_fields`, `list_memberships`, `taggings`, `notes` (comma-separated)
- `limit` - Results per page (default 50, max 500)

**Example with filters:**
```bash
GET /constant-contact/v3/contacts?email=john@example.com&status=all
GET /constant-contact/v3/contacts?updated_after=2026-04-01T00:00:00Z&limit=100
GET /constant-contact/v3/contacts?include=custom_fields,list_memberships,taggings&limit=50
```

#### Get Contact

```bash
GET /constant-contact/v3/contacts/{contact_id}
```

Query parameters:
- `include` - Include subresources: `custom_fields`, `list_memberships`, `taggings`, `notes` (comma-separated)

**Example:**
```bash
GET /constant-contact/v3/contacts/{contact_id}?include=custom_fields,list_memberships,taggings,notes
```

**Response:**
```json
{
  "contact_id": "uuid",
  "email_address": {
    "address": "john@example.com",
    "permission_to_send": "implicit",
    "created_at": "2026-04-28T21:46:22Z",
    "updated_at": "2026-04-28T21:46:22Z",
    "opt_in_source": "Account",
    "opt_in_date": "2026-04-28T21:46:22Z",
    "confirm_status": "off"
  },
  "first_name": "John",
  "last_name": "Doe",
  "create_source": "Account",
  "created_at": "2026-04-28T21:46:22Z",
  "updated_at": "2026-04-28T21:46:22Z",
  "custom_fields": [],
  "list_memberships": ["list-uuid"],
  "taggings": [],
  "notes": []
}
```

#### Create Contact

**IMPORTANT:** The `create_source` field is required.

```bash
POST /constant-contact/v3/contacts
Content-Type: application/json

{
  "email_address": {
    "address": "john@example.com",
    "permission_to_send": "implicit"
  },
  "first_name": "John",
  "last_name": "Doe",
  "job_title": "Developer",
  "company_name": "Acme Inc",
  "create_source": "Account",
  "list_memberships": ["list-uuid-here"]
}
```

Valid `create_source` values: `Account`, `Contact`, `Landing Page`

#### Update Contact

**IMPORTANT:** The `update_source` field is required.

```bash
PUT /constant-contact/v3/contacts/{contact_id}
Content-Type: application/json

{
  "email_address": {
    "address": "john@example.com"
  },
  "first_name": "John",
  "last_name": "Smith",
  "update_source": "Account"
}
```

Valid `update_source` values: `Account`, `Contact`, `Landing Page`

#### Delete Contact

```bash
DELETE /constant-contact/v3/contacts/{contact_id}
```

Returns `204 No Content` on success.

#### Create or Update Contact (Sign-Up Form)

Use this endpoint to create a new contact or update an existing one by email address without checking if they exist first:

```bash
POST /constant-contact/v3/contacts/sign_up_form
Content-Type: application/json

{
  "email_address": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "list_memberships": ["list-uuid-here"]
}
```

**Response:**
```json
{
  "contact_id": "uuid",
  "action": "created"
}
```

The `action` field indicates whether the contact was `created` or `updated`.

#### Get Contact Counts

```bash
GET /constant-contact/v3/contacts/counts
```

**Response:**
```json
{
  "total": 150,
  "explicit": 100,
  "implicit": 40,
  "pending": 5,
  "unsubscribed": 5
}
```

### Contact Lists

#### List Contact Lists

```bash
GET /constant-contact/v3/contact_lists
```

Query parameters:
- `include_count` - Include total list count (`true`/`false`)
- `include_membership_count` - Include contact count per list: `all`, `active`, `unsubscribed`
- `limit` - Results per page

**Example:**
```bash
GET /constant-contact/v3/contact_lists?include_membership_count=all
```

**Response:**
```json
{
  "lists": [
    {
      "list_id": "uuid",
      "name": "Newsletter Subscribers",
      "description": "Main newsletter",
      "favorite": false,
      "created_at": "2026-02-05T07:19:59Z",
      "updated_at": "2026-02-05T07:19:59Z",
      "membership_count": 150
    }
  ],
  "lists_count": 1
}
```

#### Get Contact List

```bash
GET /constant-contact/v3/contact_lists/{list_id}
```

Query parameters:
- `include_membership_count` - Include membership count: `all`, `active`, `unsubscribed`

#### Create Contact List

```bash
POST /constant-contact/v3/contact_lists
Content-Type: application/json

{
  "name": "Newsletter Subscribers",
  "description": "Main newsletter list",
  "favorite": false
}
```

#### Update Contact List

```bash
PUT /constant-contact/v3/contact_lists/{list_id}
Content-Type: application/json

{
  "name": "Updated List Name",
  "description": "Updated description",
  "favorite": true
}
```

#### Delete Contact List

```bash
DELETE /constant-contact/v3/contact_lists/{list_id}
```

Returns `202 Accepted` (deletion is asynchronous).

### Tags

#### List Tags

```bash
GET /constant-contact/v3/contact_tags
```

Query parameters:
- `limit` - Results per page

#### Create Tag

```bash
POST /constant-contact/v3/contact_tags
Content-Type: application/json

{
  "name": "VIP Customer"
}
```

#### Update Tag

```bash
PUT /constant-contact/v3/contact_tags/{tag_id}
Content-Type: application/json

{
  "name": "Premium Customer"
}
```

#### Delete Tag

```bash
DELETE /constant-contact/v3/contact_tags/{tag_id}
```

Returns `202 Accepted` (deletion is asynchronous).

### Custom Fields

#### List Custom Fields

```bash
GET /constant-contact/v3/contact_custom_fields
```

#### Create Custom Field

```bash
POST /constant-contact/v3/contact_custom_fields
Content-Type: application/json

{
  "label": "Customer ID",
  "type": "string"
}
```

Valid types: `string`, `date`

**Response:**
```json
{
  "custom_field_id": "uuid",
  "label": "Customer ID",
  "name": "customer_id",
  "type": "string",
  "version": 1,
  "created_at": "2026-04-28T21:45:57Z",
  "updated_at": "2026-04-28T21:45:57Z"
}
```

#### Delete Custom Field

```bash
DELETE /constant-contact/v3/contact_custom_fields/{custom_field_id}
```

### Email Campaigns

#### List Email Campaigns

```bash
GET /constant-contact/v3/emails
```

Query parameters:
- `limit` - Results per page (default 50)
- `before_date` - ISO-8601 date filter
- `after_date` - ISO-8601 date filter

**Response:**
```json
{
  "campaigns": [
    {
      "campaign_id": "uuid",
      "name": "March Newsletter",
      "current_status": "Draft",
      "type": "CUSTOM_CODE_EMAIL",
      "type_code": 26,
      "created_at": "2026-04-28T21:47:35.000Z",
      "updated_at": "2026-04-28T21:47:35.000Z"
    }
  ]
}
```

#### Get Email Campaign

```bash
GET /constant-contact/v3/emails/{campaign_id}
```

**Response includes campaign activity IDs:**
```json
{
  "campaign_activities": [
    {
      "campaign_activity_id": "uuid",
      "role": "primary_email"
    },
    {
      "campaign_activity_id": "uuid",
      "role": "permalink"
    }
  ],
  "campaign_id": "uuid",
  "current_status": "DRAFT",
  "name": "March Newsletter",
  "type": "CUSTOM_CODE_EMAIL"
}
```

#### Create Email Campaign

```bash
POST /constant-contact/v3/emails
Content-Type: application/json

{
  "name": "March Newsletter",
  "email_campaign_activities": [
    {
      "format_type": 5,
      "from_name": "Company Name",
      "from_email": "marketing@example.com",
      "reply_to_email": "reply@example.com",
      "subject": "March Newsletter",
      "html_content": "<html><body><h1>Hello!</h1></body></html>"
    }
  ]
}
```

The `from_email` must be a confirmed account email address (see Account Emails).

#### Rename Email Campaign

```bash
PATCH /constant-contact/v3/emails/{campaign_id}
Content-Type: application/json

{
  "name": "New Campaign Name"
}
```

#### Delete Email Campaign

```bash
DELETE /constant-contact/v3/emails/{campaign_id}
```

Returns `204 No Content` on success.

### Email Campaign Activities

Campaign activities are the content/configuration of a campaign. Use the `campaign_activity_id` with role `primary_email` from the campaign response.

#### Get Campaign Activity

```bash
GET /constant-contact/v3/emails/activities/{campaign_activity_id}
```

**Response:**
```json
{
  "campaign_activity_id": "uuid",
  "campaign_id": "uuid",
  "role": "primary_email",
  "contact_list_ids": [],
  "segment_ids": [],
  "current_status": "DRAFT",
  "format_type": 5,
  "from_email": "marketing@example.com",
  "from_name": "Company",
  "reply_to_email": "reply@example.com",
  "subject": "Newsletter"
}
```

#### Update Campaign Activity

Updates the email content, targeting, and sender information. All fields in the request body are replaced.

```bash
PUT /constant-contact/v3/emails/activities/{campaign_activity_id}
Content-Type: application/json

{
  "from_name": "Updated Name",
  "from_email": "marketing@example.com",
  "reply_to_email": "reply@example.com",
  "subject": "Updated Subject",
  "html_content": "<html><body><h1>Updated Content</h1></body></html>",
  "contact_list_ids": ["list-uuid-here"]
}
```

**IMPORTANT:** `from_email` is required in the update body. Omitting it returns a validation error.

#### Preview Campaign Activity

Returns the rendered HTML and text preview of the email.

```bash
GET /constant-contact/v3/emails/activities/{campaign_activity_id}/previews
```

**Response:**
```json
{
  "campaign_activity_id": "uuid",
  "from_email": "marketing@example.com",
  "from_name": "Company",
  "preview_html_content": "<html>...</html>",
  "preview_text_content": "Plain text version...",
  "reply_to_email": "reply@example.com",
  "subject": "Newsletter"
}
```

#### Send Test Email

Sends a test/proof version of the email to specified addresses.

```bash
POST /constant-contact/v3/emails/activities/{campaign_activity_id}/tests
Content-Type: application/json

{
  "email_addresses": ["test@example.com"],
  "personal_message": "Please review this draft"
}
```

Returns `204 No Content` on success.

#### Schedule Email Campaign

```bash
POST /constant-contact/v3/emails/activities/{campaign_activity_id}/schedules
Content-Type: application/json

{
  "scheduled_date": "2026-06-01T10:00:00Z"
}
```

**Note:** The campaign activity must have a valid `from_email`, a physical address on the account, and at least one target list or segment before scheduling.

#### Get Campaign Schedule

```bash
GET /constant-contact/v3/emails/activities/{campaign_activity_id}/schedules
```

#### Unschedule Email Campaign

```bash
DELETE /constant-contact/v3/emails/activities/{campaign_activity_id}/schedules
```

#### Get Non-Opener Resend

```bash
GET /constant-contact/v3/emails/activities/{campaign_activity_id}/non_opener_resends
```

Returns resend details for sent campaigns. Returns empty array if no resend is configured.

#### Get A/B Test

```bash
GET /constant-contact/v3/emails/activities/{campaign_activity_id}/abtest
```

### Segments

#### List Segments

```bash
GET /constant-contact/v3/segments
```

Query parameters:
- `sort_by` - Sort field (e.g., `name`, `date`)
- `sort_order` - `asc` or `desc`

#### Get Segment

```bash
GET /constant-contact/v3/segments/{segment_id}
```

#### Create Segment

Segments use a criteria object to define the audience filter:

```bash
POST /constant-contact/v3/segments
Content-Type: application/json

{
  "name": "Engaged Subscribers",
  "segment_criteria": {
    "version": "3.0.0",
    "criteria": { ... }
  }
}
```

**Note:** The `segment_criteria` must be a JSON object (not a string). The criteria schema is complex and version-dependent. Refer to the [Constant Contact Segments Documentation](https://developer.constantcontact.com/api_guide/segment_overview.html) for the full criteria format.

#### Update Segment

```bash
PUT /constant-contact/v3/segments/{segment_id}
Content-Type: application/json

{
  "name": "Updated Segment Name",
  "segment_criteria": { ... }
}
```

#### Delete Segment

```bash
DELETE /constant-contact/v3/segments/{segment_id}
```

### Bulk Activities

Bulk activities run asynchronously. After creating a bulk activity, poll the activity status endpoint until completion.

#### List Activities

```bash
GET /constant-contact/v3/activities
```

Query parameters:
- `limit` - Results per page
- `state` - Filter by state: `processing`, `completed`, `cancelled`, `failed`, `timed_out`

#### Get Activity Status

```bash
GET /constant-contact/v3/activities/{activity_id}
```

**Response:**
```json
{
  "activity_id": "uuid",
  "state": "completed",
  "started_at": "2026-04-28T21:48:16Z",
  "completed_at": "2026-04-28T21:48:16Z",
  "created_at": "2026-04-28T21:48:15Z",
  "updated_at": "2026-04-28T21:48:16Z",
  "percent_done": 100,
  "activity_errors": [],
  "status": {
    "items_total_count": 1,
    "items_completed_count": 1
  }
}
```

#### Add Contacts to Lists

```bash
POST /constant-contact/v3/activities/add_list_memberships
Content-Type: application/json

{
  "source": {
    "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
  },
  "list_ids": ["list-uuid"]
}
```

The `source` can also use `list_ids` to copy contacts from other lists:

```bash
{
  "source": {
    "list_ids": ["source-list-uuid"]
  },
  "list_ids": ["target-list-uuid"]
}
```

#### Remove Contacts from Lists

```bash
POST /constant-contact/v3/activities/remove_list_memberships
Content-Type: application/json

{
  "source": {
    "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
  },
  "list_ids": ["target-list-uuid"]
}
```

#### Add Tags to Contacts

```bash
POST /constant-contact/v3/activities/contacts_taggings_add
Content-Type: application/json

{
  "source": {
    "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
  },
  "tag_ids": ["tag-uuid"]
}
```

#### Remove Tags from Contacts

```bash
POST /constant-contact/v3/activities/contacts_taggings_remove
Content-Type: application/json

{
  "source": {
    "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
  },
  "tag_ids": ["tag-uuid"]
}
```

#### Export Contacts

```bash
POST /constant-contact/v3/activities/contact_exports
Content-Type: application/json

{
  "contact_ids": ["contact-uuid-1", "contact-uuid-2"],
  "fields": ["first_name", "last_name", "email"]
}
```

The response includes a `results` link to download the export:

```json
{
  "activity_id": "uuid",
  "state": "initialized",
  "_links": {
    "self": { "href": "/v3/activities/{activity_id}" },
    "results": { "href": "/v3/contact_exports/{export_id}" }
  }
}
```

#### Download Contact Export

After the export activity completes, download the CSV:

```bash
GET /constant-contact/v3/contact_exports/{export_id}
```

Returns CSV data.

#### Import Contacts

```bash
POST /constant-contact/v3/activities/contacts_file_import
Content-Type: multipart/form-data

{file: contacts.csv, list_ids: ["list-uuid"]}
```

#### Delete Contacts in Bulk

```bash
POST /constant-contact/v3/activities/contact_delete
Content-Type: application/json

{
  "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
}
```

### Reporting

#### Email Campaign Summaries

```bash
GET /constant-contact/v3/reports/summary_reports/email_campaign_summaries
```

**Response:**
```json
{
  "bulk_email_campaign_summaries": [...],
  "aggregate_percents": {
    "click": 5.2,
    "open": 22.1,
    "did_not_open": 72.7,
    "bounce": 1.3,
    "unsubscribe": 0.2
  }
}
```

#### Get Email Campaign Report

Returns detailed metrics for a specific sent campaign activity.

```bash
GET /constant-contact/v3/reports/email_reports/{campaign_activity_id}
```

**Note:** Only available for sent campaigns. Draft campaigns return 404.

#### Contact Activity Summary

```bash
GET /constant-contact/v3/reports/contact_reports/{contact_id}/activity_summary
```

**Response:**
```json
{
  "contact_id": "uuid",
  "campaign_activities": [
    {
      "campaign_activity_id": "uuid",
      "sends": 1,
      "opens": 1,
      "clicks": 0,
      "bounces": 0
    }
  ]
}
```

## Pagination

The API uses cursor-based pagination with a `limit` parameter:

```bash
GET /constant-contact/v3/contacts?limit=50
```

Response includes pagination links:

```json
{
  "contacts": [...],
  "_links": {
    "next": {
      "href": "/v3/contacts?cursor=abc123"
    }
  }
}
```

Use the cursor from the `next` link for subsequent pages:

```bash
GET /constant-contact/v3/contacts?cursor=abc123
```

When there are no more pages, the `_links.next` field is absent from the response.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/constant-contact/v3/contacts?limit=50',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/constant-contact/v3/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 50}
)
data = response.json()
```

## Notes

- Resource IDs use UUID format (36 characters with hyphens)
- All dates use ISO-8601 format: `YYYY-MM-DDThh:mm:ss.sZ`
- Maximum 1,000 contact lists per account
- A contact can belong to up to 50 lists
- Bulk operations are asynchronous - check activity status for completion
- Email campaigns require confirmed sender email addresses
- `format_type: 5` for custom HTML emails
- `create_source` is required when creating contacts; `update_source` is required when updating
- Scheduling a campaign requires a valid physical address on the account and at least one target list
- Delete operations on tags and lists return `202 Accepted` (asynchronous); contacts and campaigns return `204 No Content`
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Constant Contact connection or invalid request |
| 401 | Invalid or missing Maton API key, or OAuth token expired |
| 403 | Insufficient permissions for the requested operation |
| 404 | Resource not found |
| 409 | Conflict (e.g., duplicate email address) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Constant Contact API |

### Error Response Format

```json
[
  {
    "error_key": "contacts.api.validation.error",
    "error_message": "create_source is missing, create_source does not have a valid value"
  }
]
```

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `constant-contact`. For example:

- Correct: `https://api.maton.ai/constant-contact/v3/contacts`
- Incorrect: `https://api.maton.ai/v3/contacts`

## Resources

- [Constant Contact V3 API Overview](https://developer.constantcontact.com/api_guide/getting_started.html)
- [API Reference](https://developer.constantcontact.com/api_reference/index.html)
- [Technical Overview](https://developer.constantcontact.com/api_guide/v3_technical_overview.html)
- [Contacts Overview](https://developer.constantcontact.com/api_guide/contacts_overview.html)
- [Email Campaigns Guide](https://developer.constantcontact.com/api_guide/email_campaigns_get_started.html)
- [Contact Lists Overview](https://v3.developer.constantcontact.com/api_guide/lists_overview.html)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
