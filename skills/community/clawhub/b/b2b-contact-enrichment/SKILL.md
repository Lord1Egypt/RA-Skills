---
name: b2b-contact-enrichment
description: "Find verified professional email addresses with the FinalScout API — by LinkedIn profile URL, by full name + company domain, or by news article URL (author lookup). Supports single lookups (long-polling waterfall or submit-and-poll), bulk batch tasks with progress tracking, paginated result dump, CSV export, webhooks, and account credits / rate-limit checks."
version: 1.1.0
metadata:
  openclaw:
    primaryEnv: FINALSCOUT_API_KEY
    envVars:
      - name: FINALSCOUT_API_KEY
        required: true
        description: "FinalScout API key. Get yours at https://finalscout.com/app/api/settings"
    emoji: "📧"
    homepage: https://finalscout.com
---

# FinalScout Email Finder & Contact Enrichment

Find verified professional email addresses. Pick the find method by what the user has:

| User has | Method | Single endpoint | Bulk endpoint |
|----------|--------|-----------------|---------------|
| LinkedIn profile URL | `linkedin` | `POST /v1/find/linkedin/single` | `POST /v1/find/linkedin/bulk` |
| Full name + company domain | `professional` | `POST /v1/find/professional/single` | `POST /v1/find/professional/bulk` |
| News article URL (find its author) | `author` | `POST /v1/find/author/single` | `POST /v1/find/author/bulk` |

**Base URLs:**
- Standard API: `https://api.finalscout.com`
- Waterfall API (long-polling single finds): `https://api-waterfall.finalscout.com`

**Auth:** every request needs the header `Authorization: $FINALSCOUT_API_KEY` (raw key, no `Bearer` prefix).

**Choosing a flow:**
- 1 to a few contacts → **Waterfall single** (one blocking call per contact, no polling).
- Many contacts (CSV, list, table, JSON) → **Bulk** (async task: submit → poll status → dump/export results).

---

## Person object per method

The `person` object (single) / `persons` array items (bulk) differ by method:

**`linkedin`** — only `linkedin_url` is required:
```json
{
  "linkedin_url": "https://www.linkedin.com/in/williamhgates/",
  "full_name": "",
  "current_positions": [
    {"company_name": "", "company_linkedin_url": "", "title": "", "location": ""}
  ],
  "meta_data": {"your_key": "your value"}
}
```
Supported `linkedin_url` formats: `https://www.linkedin.com/in/<slug>`, `https://www.linkedin.com/in/<ACoAA... id>`, Sales Navigator `https://www.linkedin.com/sales/people/<id>,name,sSHS` and `https://www.linkedin.com/sales/lead/<id>,name,sSHS`.
Supported `company_linkedin_url` formats: `https://www.linkedin.com/company/<slug|id>`, `https://www.linkedin.com/sales/company/<id>`.
Cost is 1 credit per email found whether you send just the URL or the URL plus full profile info (`full_name`, `company_name`, `company_linkedin_url`, `title`, `location`).

**`professional`** — `full_name` and `domain` are required:
```json
{
  "full_name": "Bill Gates",
  "domain": "microsoft.com",
  "domain_extra": ["gatesfoundation.org"],
  "deep_verify": false,
  "meta_data": {"your_key": "your value"}
}
```
`domain_extra` (optional): extra candidate domains. `deep_verify` (optional, default `false`): deeper email verification — only set `true` when confident the domain is valid for the person.

**`author`** — only `article_url` is required:
```json
{
  "article_url": "https://www.forbes.com/sites/.../article-slug/",
  "meta_data": {"your_key": "your value"}
}
```

`meta_data` (optional, all methods): flat object of string values (e.g. CRM contact id). Echoed back in responses, dump items, and webhook events — use it to correlate results with the user's data.

---

## Single lookup — Waterfall (preferred)

One blocking call; the server holds the connection until the task finishes or `timeout` (seconds, 30–600, default 80) is reached.

```bash
curl -s -m 130 -w "\nHTTP %{http_code}" \
  "https://api-waterfall.finalscout.com/find/professional/single?timeout=120" \
  -H "Authorization: $FINALSCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"person":{"full_name":"<name>","domain":"<domain>"}}'
```

Swap the path for `/find/linkedin/single` or `/find/author/single` with the matching `person` body. Set curl's `-m` (max time) a bit above the `timeout` value. Longer timeouts (up to 600) mean fewer round-trips; use a shorter one if your shell caps command runtime.

**Responses:**
- `HTTP 200` → task complete; read `contact`, `credits_consumed`, `credits_available` (see [Interpreting results](#interpreting-results)).
- `HTTP 408` → still running; body has `{"id": "...", "status": "Running"}`. Resubmit the same request to keep waiting, or poll `/v1/find/single/status?id=<id>`.

Optional body fields (top level, next to `person`):
- `"tags": ["tag1"]` — organize contacts in the FinalScout web app (all methods)
- `"webhook_url": "<url>"` — receive a `single_task.finished` event (all methods; see [Webhooks](#webhooks))
- `"enable_work_email": true` — default `true`; find work emails (linkedin method only)
- `"enable_personal_email": false` — default `false`; fall back to personal emails, e.g. Gmail (linkedin method only)
- `"enable_generic_email": false` — default `false`; fall back to generic emails, e.g. support@ (linkedin method only)

## Single lookup — submit + poll (alternative)

Use when a long-held connection is not an option.

**Submit** (same bodies and optional fields as waterfall):
```bash
curl -s -X POST https://api.finalscout.com/v1/find/professional/single \
  -H "Authorization: $FINALSCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"person":{"full_name":"<name>","domain":"<domain>"}}'
```

Save the returned `id`. If `status` is already `Complete`, done.

**Poll** every 3 seconds until `status` is `Complete` (works for any single find task, all three methods):
```bash
curl -s "https://api.finalscout.com/v1/find/single/status?id=<id>" \
  -H "Authorization: $FINALSCOUT_API_KEY"
```

Give up after ~40 attempts (2 minutes) and report the task `id` so the user can check later.

---

## Bulk lookup

### 1. Submit

Parse the user's input (CSV, list, table, JSON) into a `persons` array of the matching person objects. Strip empty rows.

```bash
curl -s -X POST https://api.finalscout.com/v1/find/professional/bulk \
  -H "Authorization: $FINALSCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "persons": [
      {"full_name": "Bill Gates", "domain": "microsoft.com"},
      {"full_name": "Elon Musk",  "domain": "tesla.com"}
    ],
    "name": "Bulk find - <date>",
    "duplicate": "skip_duplicates"
  }'
```

Endpoints: `/v1/find/professional/bulk`, `/v1/find/linkedin/bulk`, `/v1/find/author/bulk`.

Optional top-level fields (all bulk endpoints unless noted):
- `"name"` — task name, max 300 characters
- `"duplicate"` — `skip_duplicates` (default) or `scrape_and_update_duplicates` (re-process contacts already in the account)
- `"tags": ["tag1"]`
- `"webhook_url": "<url>"` and `"webhook_subscribe_events": ["bulk_task.finished", "contact.change"]` — see [Webhooks](#webhooks)
- `"enable_work_email"` / `"enable_personal_email"` / `"enable_generic_email"` — linkedin bulk only, same defaults as single

The response is the task: `{id, status, total, finished, success, duplicated, credits_consumed, credits_available, ...}`. Save `id`.

### 2. Poll status

```bash
curl -s "https://api.finalscout.com/v1/find/bulk/status?id=<id>" \
  -H "Authorization: $FINALSCOUT_API_KEY"
```

Poll every 5 seconds; report progress as `finished / total`. Task `status`: `Queued` → `Running` → `Completed` or `Failed`.

### 3. Dump results (after Completed)

```bash
curl -s "https://api.finalscout.com/v1/find/bulk/dump?id=<id>&page_size=100" \
  -H "Authorization: $FINALSCOUT_API_KEY"
```

Response: `{cursor, task: {id, status}, items: [{contact, meta_data}]}`. If `cursor` is non-empty, request the next page with `&cursor=<cursor>`; repeat until `cursor` is null/empty. `page_size` range 10–100 (default 50). Cursors expire after 1 day.

### 4. Present results

| Name | Input | Email | Type | Status | Score |
|------|-------|-------|------|--------|-------|
| Bill Gates | microsoft.com | bill@microsoft.com | Work email | Valid | 95 |
| ... | ... | no email found | - | - | - |

Summary line: `X / Y emails found. Z credits consumed, W credits remaining.`

### CSV export (optional)

When the user wants a file instead of (or in addition to) inline results:

```bash
curl -s "https://api.finalscout.com/v1/find/bulk/export?id=<id>" \
  -H "Authorization: $FINALSCOUT_API_KEY"
```

Response: `{"status": "Generating download link" | "Ready", "download_url": "..."}`. If still generating, retry after a few seconds until `Ready`. Warn the user: the link is public (anyone with it can download) and expires after 7 days.

---

## Account info

```bash
curl -s https://api.finalscout.com/v1/account \
  -H "Authorization: $FINALSCOUT_API_KEY"
```

Returns `owner_email`, `credits_available`, and per-endpoint `rate_limit` entries. Use this to check the balance before large bulk jobs or to diagnose 429s.

---

## Webhooks

Pass `webhook_url` in any find request to get HTTP POST callbacks instead of / in addition to polling:

- **`single_task.finished`** — single find completed. Contains `contact` when an email was found, otherwise a `message`; plus `task_id`, `credits_consumed`, `meta_data`.
- **`bulk_task.finished`** — bulk task completed. Task-level summary (`total`, `finished`, `success`, `duplicated`, `credits_consumed`, `credits_available`); no per-contact `meta_data` at this level.
- **`contact.change`** — sent during bulk tasks for each contact whose email is found (or when an existing contact is updated). Contains `contact` and that contact's `meta_data`. Nothing is sent for contacts with no email found.

Bulk requests can filter events with `webhook_subscribe_events` (array of the two bulk event names); if unset, all events are sent.

---

## Interpreting results

Contact fields that matter most:
- `email` + `email_status`: `Valid` (safe to send), `Risky`, `Invalid`, `Unknown`. Only `Valid` is guaranteed deliverable; show `Risky`/`Unknown` emails with a caveat.
- `email_type`: `Work email`, `Personal email`, or `Generic email`.
- `email_score` (0–100): deliverability confidence; higher is better.
- `email_is_catchall`: domain accepts all mail; FinalScout's verification (via BounceBan) still makes these as reliable as standard addresses — mention it, don't discard.
- No `contact` in a single find response (or a contact without `email`) → no email found; no credit charged.
- Enrichment extras when available: `title`, `company`, `location`, `linkedin`, `website`, `industry`, `company_domain`, `company_phone`, company address fields, etc. Include them if the user asked for enrichment.

Always surface `credits_consumed` and `credits_available` after an operation.

---

## Error handling

| HTTP status | Meaning | Action |
|-------------|---------|--------|
| 400 | Invalid parameter | Fix the request body/params; re-check required fields |
| 401 | Bad/missing API key | Ask the user to check `FINALSCOUT_API_KEY` (and IP whitelist at finalscout.com/app/api/settings) |
| 403 | Insufficient credits | Report `credits_required` vs `credits_available` from the response body |
| 405 | Account blocked | Tell the user to contact dev@finalscout.com |
| 408 | Waterfall timeout (waterfall endpoints only) | Task still running — resubmit the same request or poll `/v1/find/single/status` |
| 429 | Rate limited | Wait 2 seconds and retry once; if repeated, slow down (limits via `/v1/account`) |
| 500 | Server error | Retry once; if it fails again, report the error |

## Rate limits (typical defaults — actual values via `/v1/account`)

| Endpoint | Limit |
|----------|-------|
| /find/linkedin/single | 50 / second |
| /find/author/single, /find/professional/single | 5 / second |
| /find/single/status, /find/bulk/status, /find/bulk/export | 25 / second |
| /find/*/bulk (all three) | 2 / second |
| /account | 5 / second |

## Credits

Universal credits: each email successfully found costs 1 credit, regardless of method. No charge when no email is found. Need test credits or higher limits → dev@finalscout.com.
