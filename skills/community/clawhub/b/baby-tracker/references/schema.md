# Baby Tracker Schema Reference

## events.csv columns

- `event_id`: UUID generated at append time.
- `timestamp_local`: ISO timestamp in the event timezone.
- `timestamp_utc`: UTC timestamp for stable ordering.
- `timezone`: usually `Europe/London`.
- `baby_id`: defaults to `baby-1`; allows future multi-baby support.
- `type`: broad category, e.g. `diaper`, `feed`, `sleep`, `growth`, `temperature`, `medication`, `correction`.
- `subtype`: narrower category, e.g. `both`, `wet`, `weight`, `bottle`, `breast`.
- `metric`: numeric measurement name, e.g. `weight`, `height`, `temperature`, `volume`, `duration`, `dose`.
- `value`: numeric value as text.
- `unit`: `kg`, `g`, `cm`, `C`, `ml`, `min`, etc.
- `details_json`: JSON object for extensible key/value detail.
- `notes`: human note.
- `source_text`: original message or source CSV row text.
- `created_at_utc`: append timestamp.

## Principles

- Prefer one flexible CSV over many fragmented CSVs until scale demands splitting.
- Preserve raw/source text for auditability.
- Append, do not mutate, by default.
- Use metric/value/unit for anything that should be chartable.
- Use details_json for everything else.
