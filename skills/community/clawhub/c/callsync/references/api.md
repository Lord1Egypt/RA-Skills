# CallSync REST API reference

Base URL `https://mcp.callsyncapp.com/api/v1`, header `Authorization: Bearer $CALLSYNC_API_KEY`. Bodies are JSON with `Content-Type: application/json`.

A wrong key, or a workspace whose integrations are off, gets HTTP `401` with the plain-text body `Unauthorized`. Other errors are JSON: `{"status": "error", "message": "…"}`.

`page` starts at 1. `limit` defaults to 5 and is capped at 10.

## Calls

### `GET /calls`

Query: `search`, `direction` (`incoming`, `outgoing`, `missed`, `rejected`, `blocked`), `page`, `limit`. Newest first. `search` matches the caller's phone and name, call and contact notes, the team member, and the AI summary, transcript, reason and sentiment.

```json
{
  "status": "success",
  "data": [
    {
      "id": 239,
      "time": "2026-10-13T05:00:00+00:00",
      "direction": "incoming",
      "duration": "184s",
      "caller": { "phone": "+919876543210", "name": "Rahul Verma", "identity_note": "Wants a 2BHK", "labels": ["hot lead"] },
      "staff": "Priya Sharma",
      "note": "Site visit on Saturday",
      "recording": "https://…",
      "status": "Reviewed",
      "ai": { "status": "completed", "summary": "…", "sentiment": "positive", "analysis": { "…": "…" }, "updated_at": "…", "credit_used": 1, "attempts": 1 }
    }
  ],
  "pagination": { "page": 1, "limit": 5, "total": 42 }
}
```

`caller.name` is `"Unknown"` when the number is not saved. `recording` is a shareable link, or `null` when there is no recording. `ai` is `null` until the call has been analysed.

### `GET /analysis?call_id=<id>`

The AI analysis of one call. `data.status` is `pending`, `processing`, `completed` or `failed`; a call never analysed returns `{"data": {"status": "not_found"}}`. Useful fields: `summary`, `sentiment`, `call_reason`, `transcription`, `analysis.tasks` (suggested follow-ups) and `analysis.labels`.

### `GET /callers`

Everyone who has called or been called, most recent first. Query: `search` (phone, name, note), `page`, `limit`. Each row: `phone`, `name`, `note`, `labels`, and `activity` with `total_calls`, `total_duration`, `last_interaction`, `last_type`. Pagination as for calls.

### `GET /employees`

The team members whose phones sync calls. Query: `search` (name, phone, email, device), `include_archived=true`. Each row: `id`, `name`, `phone`, `device_phone`, `email`, `device_model`, `last_sync`, `is_archived`. Returns every match with `total`; there are no pages.

## CRM

### `GET /crm/config`

The workspace's pipeline settings: `stages`, `priorities`, `segments` and `sources`, each a list of `{ "id", "label", "color" }`, plus `existing_labels` (every contact label in use). Contacts and tasks store the `id`, so look labels up here.

### `GET /crm/contacts`

Query: `search` (name, phone, email, sales note), `stage_id`, `priority_id`, `segment_id`, `label`, `is_in_pipeline` (`true`/`false`), `sortField` (default `updated_at`), `sortDir` (`asc`/`desc`), `page`, `limit`. Returns `data`, `total`, `page`, `perPage`.

A contact has `id` (use it as `person_id` for tasks, notes and timelines), `name`, `phone`, `email`, `company`, `about`, `sales_note`, `labels`, `budget`, `stage_id`, `priority_id`, `segment_id`, `source_id`, `is_in_pipeline`, `is_starred`, `activity_count`, `last_activity_at`, `created_at` and `updated_at`.

### `POST /crm/contacts`

Body: `phone` (needed to match calls), `name`, `email`, `company`, `about`, `sales_note`, `labels` (array of strings), `budget`, `stage_id`, `priority_id`, `segment_id`, `source_id`, `is_in_pipeline`. If the phone number already belongs to a caller, the contact is attached to that caller's call history. Returns the new contact in `data`.

### `PUT /crm/contacts`

Body: `id` plus only the fields to change, from the list above, and `is_starred` or `is_archived`. Returns the updated contact.

### `GET /crm/timeline?person_id=<contact id>`

A contact's history, newest first: calls (with `metadata.summary`, `metadata.transcription`, `metadata.sentiment`, `metadata.duration`) and notes or activities. Each entry has `type`, `title`, `description` and `timestamp`.

### `POST /crm/activities`

Adds an entry to a contact's timeline. Body: `person_id`, `type` (`NOTE`, `CALL`, `EMAIL`, `FOLLOW_UP`, `MEETING`, `SITE_VISIT`), `title`, and optional `description`. Each request adds a new entry.

### `GET /crm/tasks`

Query: `person_id`, `status` (`PENDING`, `COMPLETED`, `CANCELLED`), `due_date` (`YYYY-MM-DD`). Sorted by due date, all matches at once. A task has `id`, `person_id`, `contact_name`, `type`, `description`, `due_date`, `due_time`, `priority_id`, `status`, `show_reminder`, `reminder_minutes_before` and `completed_at`.

### `POST /crm/tasks`

Body: `person_id` (required), `type` (`CALL`, `EMAIL`, `FOLLOW_UP`, `MEETING`, `TO_DO`; default `TO_DO`), `description`, `due_date` (`YYYY-MM-DD`), `due_time` (`HH:MM:SS`, the team's local time), `priority_id`, `show_reminder` (`true` reminds the team in the app), `reminder_minutes_before`. New tasks are `PENDING`. Returns the task.

### `PUT /crm/tasks`

Body: `id` plus the fields to change, from the list above, and `status`. Setting `status` to `COMPLETED` records `completed_at`. Returns the task.
