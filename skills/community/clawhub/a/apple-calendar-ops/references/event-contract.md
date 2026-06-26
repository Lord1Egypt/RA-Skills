# Normalized event contract

All scripts in this skill should return or consume a normalized event object where possible.

## Event shape

```json
{
  "id": "https://.../event.ics",
  "calendar": {
    "id": "calendar-id",
    "name": "Calendar"
  },
  "title": "Example event",
  "start": "2026-03-12T14:00:00+08:00",
  "end": "2026-03-12T15:00:00+08:00",
  "allDay": false,
  "location": "Optional location",
  "notes": "Optional notes",
  "raw": {
    "uid": "VEVENT-UID",
    "etag": "\"etag\"",
    "resourceUrl": "https://.../event.ics"
  }
}
```

## Field guidance

- `id`: the canonical event resource URL; use this for update/delete
- `calendar.id`: provider-side calendar identifier when available
- `calendar.name`: human-readable calendar name
- `title`: event summary/title
- `start` / `end`: ISO 8601 with timezone when available
- `allDay`: boolean
- `location`: optional
- `notes`: optional description/body
- `raw.uid`: underlying VEVENT uid
- `raw.etag`: provider etag when available
- `raw.resourceUrl`: same canonical URL as `id`

## Create/update payloads

Use these fields for writes when possible:

```json
{
  "calendar": "Calendar",
  "title": "Example event",
  "start": "2026-03-12T14:00:00+08:00",
  "end": "2026-03-12T15:00:00+08:00",
  "allDay": false,
  "location": "Optional location",
  "notes": "Optional notes"
}
```

## Design rule

The contract should stay stable even if the underlying CalDAV implementation changes.
