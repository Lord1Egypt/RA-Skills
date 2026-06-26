---
name: coinfound-rwa-read
description: Read-only CoinFound RWA data skill backed by a bundled endpoint catalog and schema snapshots.
version: 0.1.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
---

# CoinFound RWA Read

Self-contained read-only access to CoinFound RWA `GET` endpoints.

## Scope

- Supports `aggregates`, `timeseries`, `pie`, `list`, and `dataset` routes under `v1/c/rwa/*`.
- Does not refresh schema snapshots. Hand unresolved schema gaps to `$coinfound-rwa-schema-probe`.

## Workflow

1. Read the bundled endpoint catalog and schema snapshots before constructing a request.
2. Resolve the route by `endpoint_key` or by `asset_class + family + metric`.
3. Run the bundled fetch script and return both the envelope and normalized payload.
4. If the schema is missing or conflicts with live data, delegate to `$coinfound-rwa-schema-probe`.

## Bundled Resources

Read first:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`

Run:

- `shared/coinfound_rwa/scripts/fetch_rwa.py`

## Minimal Examples

```bash
python3 shared/coinfound_rwa/scripts/fetch_rwa.py \
  --endpoint-key stable-coin.market-cap.timeseries \
  --query '{"groupBy":"network"}'
```

```bash
python3 shared/coinfound_rwa/scripts/fetch_rwa.py \
  --asset-class private-credit \
  --family aggregates
```

## Expected Output

Default output should include:

- `request`
- `response_envelope`
- `normalized_data`
- `display_data`
- `shape_family`
- `schema_source`

## References

- `references/rwa-read-workflow.md`
- `references/rwa-read-capabilities.md`
- `references/rwa-read-integration-notes.md`
