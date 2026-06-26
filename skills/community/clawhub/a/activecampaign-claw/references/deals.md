# Deals API Reference

ActiveCampaign v3 deals (CRM) API. Deal values are in **cents** — `100000` = $1,000.00.

## Create a deal

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "deal": {
      "title": "Acme Corp — Enterprise",
      "value": "5000000",
      "currency": "usd",
      "group": "1",
      "stage": "1",
      "owner": "1",
      "contact": "123",
      "description": "Enterprise plan, annual contract"
    }
  }' \
  "$AC_API_URL/api/3/deals" | jq
```

Required fields: `title`, `value`, `currency`, `group` (pipeline ID), `stage`, `owner`.

## Get a deal

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals/{id}" | jq
```

## Update a deal

```bash
curl -s -X PUT -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"deal":{"stage":"3","value":"7500000"}}' \
  "$AC_API_URL/api/3/deals/{id}" | jq
```

Common updates: stage movement, value change, owner reassignment, status change.

## List / filter deals

```bash
# All open deals
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals?filters[status]=0" | jq

# Deals in a specific pipeline
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals?filters[d_groupid]=1" | jq

# Deals by stage
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals?filters[d_stageid]=2" | jq

# Deals by owner
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals?filters[d_owner]=1" | jq

# Search by title
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals?filters[search]=Acme" | jq
```

### Deal status values

| Status | Meaning |
|---|---|
| `0` | Open |
| `1` | Won |
| `2` | Lost |

### Pagination

Same as contacts: `limit` (max 100) + `offset`.

## Pipelines (deal groups)

```bash
# List all pipelines
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/dealGroups" | jq

# Get a specific pipeline
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/dealGroups/{id}" | jq
```

Pipelines are called `dealGroups` in the API. Each has stages.

## Stages

```bash
# List all stages across all pipelines
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/dealStages" | jq

# Get a specific stage
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/dealStages/{id}" | jq
```

Each stage has a `group` field pointing to its pipeline ID, an `order` field, and a `title`.

## Deal notes

### Create a note

```bash
curl -s -X POST -H "Api-Token: $AC_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note":{"note":"Call with CTO — they want a pilot in Q3. Follow up Thursday."}}' \
  "$AC_API_URL/api/3/deals/{id}/notes" | jq
```

### List notes on a deal

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals/{id}/notes" | jq
```

## Deal activities

Activity log for a deal — includes notes, tasks, stage changes, creation.

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals/{id}/dealActivities" | jq
```

Use this to determine when the last meaningful activity occurred (for stale deal detection).

## Deal scores

```bash
curl -s -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals/{id}/scoreValues" | jq
```

## Deal custom fields

See `references/custom-fields.md` for reading/writing deal custom field values.

## Delete a deal

> **STOP — requires explicit user confirmation.** Deleting a deal is permanent — no soft-delete, no recycle bin. All deal notes, activities, and custom field values are destroyed. Prefer moving the deal to a "Closed Lost" stage instead. Only delete if the user specifically says "delete this deal."

```bash
curl -s -X DELETE -H "Api-Token: $AC_API_TOKEN" \
  "$AC_API_URL/api/3/deals/{id}" | jq
```

## Gotchas

- **Value is in cents.** $1,000 = `100000`. Always divide by 100 for display.
- **`group` means pipeline.** The API calls pipelines "deal groups."
- **All IDs are strings.**
- **`mdate` is last modified date** — useful for detecting stale deals.
- **`nextdate` is expected close date** — deals past this date are slipping.
- **Deal custom field values** are separate from the deal object (see `references/custom-fields.md`).
- **Deleting a deal is permanent.** There is no soft-delete or recycle bin via API.
