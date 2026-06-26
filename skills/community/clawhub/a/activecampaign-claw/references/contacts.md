# Contacts API Reference

ActiveCampaign v3 contacts API. All IDs are strings. Auth header is `Api-Token`, not `Bearer`.

## Upsert (sync) a contact

The primary way to create or update contacts. Matches by email — creates if new, updates if exists.

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contact":{"email":"jane@example.com","firstName":"Jane","lastName":"Doe","phone":"555-1234"}}' \
  "$AC_API_URL/api/3/contact/sync" | jq
```

Returns the contact object with `id`. Use this ID for all subsequent operations.

## Get a contact

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/{id}" | jq
```

## List / search contacts

```bash
# By email
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?email=jane@example.com" | jq

# By list membership
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?listid=1" | jq

# By tag
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?tagid=42" | jq

# By date created
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?filters[created_after]=2026-01-01" | jq

# Full-text search
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?search=acme" | jq
```

### Available filters

| Parameter | Description |
|---|---|
| `email` | Exact email match |
| `email_like` | Partial email match |
| `search` | Full-text across name/email/org |
| `listid` | Contacts on a specific list |
| `tagid` | Contacts with a specific tag |
| `segmentid` | Contacts in a segment |
| `status` | Contact status: `-1` (any), `0` (unconfirmed), `1` (active), `2` (unsubscribed), `3` (bounced) |
| `filters[created_before]` | ISO 8601 date |
| `filters[created_after]` | ISO 8601 date |
| `filters[updated_before]` | ISO 8601 date |
| `filters[updated_after]` | ISO 8601 date |

### Pagination

Default: 20 per page. Max: 100.

```bash
# Page through results
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?limit=100&offset=0" | jq

# Faster at scale: cursor-based
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts?limit=100&orders[id]=ASC&id_greater=500" | jq
```

The `meta.total` field in the response gives the total count matching your filters.

## Delete a contact

> **STOP — requires explicit user confirmation.** Deleting a contact is permanent. There is no undo, no recycle bin. All associated data (tags, field values, deal associations, automation history) is destroyed. Prefer changing contact status to unsubscribed or tagging for suppression instead. Only delete if the user specifically says "delete" — not "remove", "clean up", or "suppress".

```bash
curl -s -X DELETE -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/{id}" | jq
```

## Tags

### Add a tag to a contact

Look up the tag ID from `state.json` first.

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contactTag":{"contact":"123","tag":"42"}}' \
  "$AC_API_URL/api/3/contactTags" | jq
```

### Remove a tag

> Confirm with user before removing tags. Show which tag is being removed and from which contact.

First get the `contactTag` ID (not the tag ID):

```bash
# Find the contactTag ID
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/123/contactTags" | jq

# Delete by contactTag ID
curl -s -X DELETE -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contactTags/{contactTagId}" | jq
```

## List membership

### Subscribe a contact to a list

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contactList":{"list":"1","contact":"123","status":"1"}}' \
  "$AC_API_URL/api/3/contactLists" | jq
```

Status values: `1` = subscribed, `2` = unsubscribed.

### Get a contact's list memberships

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/123/contactLists" | jq
```

## Automation enrollment

### Enroll a contact in an automation

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contactAutomation":{"contact":"123","automation":"7"}}' \
  "$AC_API_URL/api/3/contactAutomations" | jq
```

### Check automation status

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/123/contactAutomations" | jq
```

Returns `completedElements`, `totalElements`, and status for each automation.

## Bounce logs

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/123/bounceLogs" | jq
```

Returns bounce type (`hard`/`soft`), campaign ID, timestamp, and error details.

## Contact scores

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/contacts/123/scoreValues" | jq
```

## Bulk import

For 10+ contacts, use the bulk import API (separate from v3):

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contacts": [
      {"email":"a@ex.com","first_name":"A"},
      {"email":"b@ex.com","first_name":"B"}
    ]
  }' \
  "$AC_API_URL/api/3/import/bulk_import" | jq
```

Limits: 250 contacts per request. 20 req/min (single), 100 req/min (multi).

## Gotchas

- **Custom field values are NOT on the contact object.** Use the `fieldValues` resource (see `references/custom-fields.md`).
- **Contact `id` is a string**, even though it looks numeric.
- **`contact/sync` is idempotent** — safe to call repeatedly with the same email.
- **Rate limit**: 5 req/sec. On 429, respect `Retry-After` header.
- **Webhooks are at-least-once** — build idempotent handlers.
