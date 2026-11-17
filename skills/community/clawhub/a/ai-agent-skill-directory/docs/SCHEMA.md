# Schema Guide — curated-brain

## Schema Version 1.0

This document describes the canonical entry format for curated-brain catalogs.

## Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | auto | Unique identifier (auto-generated) |
| `topic` | string | yes | Category or subject heading |
| `fact` | string | yes | The knowledge statement itself |
| `source` | string | yes | Provenance trace in `type:identifier:date` format |
| `confidence` | float | yes | 0.0–1.0, where higher is more certain |
| `added_at` | ISO 8601 | auto | Timestamp when the entry was created |
| `last_verified` | ISO 8601 | auto | Timestamp of last human or agent verification |
| `deprecated` | boolean | no | True if the entry is outdated |
| `deprecation_reason` | string | no | Why the entry was deprecated |
| `schema_version` | string | auto | Schema version for migration tracking |

## Source Format Convention

Use colon-delimited triplets:

```
type:identifier:YYYY-MM-DD
```

Valid types:
- `email` — `email:alice@example.com:2026-04-20`
- `slack` — `slack:#general:2026-04-20`
- `meeting` — `meeting:Q3-Planning:2026-04-15`
- `document` — `document:quarterly-report-v3:2026-04-10`
- `web` — `web:https://example.com/page:2026-04-20`
- `inference` — `inference:session-abc123:2026-04-20`

## Confidence Guidelines

| Range | Meaning | Action |
|-------|---------|--------|
| 0.95–1.00 | Directly confirmed | Treat as reliable |
| 0.80–0.94 | Secondhand reliable | Treat as likely correct |
| 0.60–0.79 | Agent inference, low uncertainty | Flag for verification if critical |
| 0.40–0.59 | Agent inference, moderate uncertainty | Verify before relying on |
| 0.20–0.39 | Agent inference, high uncertainty | Do not rely on without verification |
| 0.00–0.19 | Speculation | Flag for human triage |

## Migration Notes

When `schema_version` increments, a migration script will be provided in `scripts/migrate/`.
