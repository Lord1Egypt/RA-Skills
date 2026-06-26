# RWA Read Integration Notes

## Input Guidance

Prefer `endpoint_key` when available. Fall back to `asset_class + family + metric` only when necessary.

```json
{
  "endpoint_key": "stable-coin.aggregates",
  "query": {},
  "raw": false
}
```

## Output Shape

```json
{
  "request": {"method": "GET", "path": "/v1/c/rwa/stable-coin/aggregates"},
  "response_envelope": {"code": 0, "message": "success", "data": {}},
  "normalized_data": {},
  "display_data": {},
  "shape_family": "envelope_object",
  "schema_source": "snapshot"
}
```

## Compatibility Notes

- Successful responses may return `code=0` without a `data` field. Preserve the `empty_success` meaning.
- `dataset` payloads may contain deeply nested arrays. Do not flatten them by default.
- `display_data` is presentation-oriented formatting. `normalized_data` keeps the raw numeric values.
- Large numbers are compacted to `T/B/M/K`, and timestamp-like fields are converted to ISO UTC strings.
- If a snapshot conflicts with the live response, trust the live response and schedule a probe refresh.

## Bundled Resource Reminder

Inspect these files first during integration:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`
