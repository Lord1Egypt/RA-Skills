# API Reference

## Apollo.io API

### Authentication
Header: `X-Api-Key: YOUR_KEY`

### Search People
```
POST https://api.apollo.io/api/v1/mixed_people/api_search
```
⚠️ Use `api_search` NOT `search` — the latter returns 403 on Basic plans.

**Body:**
```json
{
  "q_organization_keyword_tags": ["aesthetic clinic", "med spa"],
  "person_titles": ["Owner", "Founder", "CEO"],
  "person_locations": ["United States"],
  "per_page": 100,
  "page": 1
}
```

**Response:** Returns people with `id`, `first_name`, `last_name_obfuscated`, `title`, `organization.name`, `has_email` flag. Does NOT return actual emails.

### Enrich Person (get email)
```
POST https://api.apollo.io/api/v1/people/match
```
**Body:** `{"id": "apollo_person_id"}`

**Response:** Full person object with `email`, `email_status`, `name`, `title`, `organization`.

Costs 1 credit per enrichment. Only enrich people where `has_email: true`.

### Bulk Enrich
```
POST https://api.apollo.io/api/v1/people/bulk_match
```
**Body:** `{"details": [{"first_name": "X", "last_name": "Y", "organization_name": "Z"}]}`

⚠️ Bulk match with `id` field returns null. Use `first_name` + `last_name` + `organization_name`.

---

## Saleshandy API

### Authentication
Header: `x-api-key: YOUR_KEY` (lowercase!)
Base URL: `https://open-api.saleshandy.com`

⚠️ NOT `api.saleshandy.com` (different API, different auth format)

### List Sequences
```
GET /v1/sequences
```
Returns all sequences with their step IDs.

### Import Prospects (with field names)
```
POST /v1/sequences/prospects/import-with-field-name
```
**Body:**
```json
{
  "prospectList": [
    {
      "First Name": "John",
      "Last Name": "Smith",
      "Email": "john@example.com",
      "Company": "ACME",
      "Job Title": "CEO"
    }
  ],
  "stepId": "STEP_ID",
  "verifyProspects": true,
  "conflictAction": "noUpdate"
}
```

Valid `conflictAction` values: `overwrite`, `noUpdate`, `addMissingFields`

### List Email Accounts
```
POST /v1/email-accounts
```
**Body:** `{"page": 1, "pageSize": 20}`

### Add Email Account to Sequence
```
POST /v1/sequences/{sequenceId}/email-accounts/add
```
**Body:** `{"emailAccountIds": ["id1", "id2"]}`

### Get Step Content
```
GET /v1/sequences/{sequenceId}/steps/{stepId}
```

### Activate/Pause Sequence
```
POST /v1/sequences/status
```
**Body:** `{"sequenceIds": ["id"], "status": "active"}` or `"paused"`
