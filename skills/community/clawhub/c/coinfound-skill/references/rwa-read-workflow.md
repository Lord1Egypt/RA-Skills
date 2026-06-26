# RWA Read Workflow

This file defines the standard read flow for the packaged skill bundle.

## Preflight

Check these bundled files first:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`

If neither source provides a stable structure for the target endpoint, hand the task to `$coinfound-rwa-schema-probe`.

## Standard Steps

1. Resolve `asset_class`, `family`, and `metric` from the user request.
2. Find the unique `endpoint_key` in `endpoint_catalog.json`.
3. Execute the request with `fetch_rwa.py`.
4. Return the response envelope, normalized payload, and `schema_source`.

## Command Examples

```bash
python3 shared/coinfound_rwa/scripts/fetch_rwa.py \
  --endpoint-key commodity.market-cap.pie
```

```bash
python3 shared/coinfound_rwa/scripts/fetch_rwa.py \
  --asset-class market-overview \
  --family list \
  --metric asset-classes
```
