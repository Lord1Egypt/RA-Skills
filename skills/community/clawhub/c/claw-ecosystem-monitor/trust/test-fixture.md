# Test Fixture

## Fixture Goal

Verify that the collector:

- writes one JSON snapshot,
- stores metadata only,
- includes canonical source URLs,
- reports request statuses,
- stops with a warning on pause-trigger HTTP statuses.

## Manual Smoke Test

Run from this skill directory:

```bash
node scripts/collect-openclaw-ecosystem.mjs
```

Expected:

- exit code `0` when all sources return OK,
- printed path ending with `data/YYYY-MM-DD/openclaw-ecosystem-snapshot.json`,
- JSON contains `source_policy`, `records`, `request_status`, and `warnings`,
- `warnings` is an array.

## Metadata-Only Checks

The output must not contain:

- package tarballs,
- full README text,
- full issue body text,
- full docs page text,
- cookies,
- authorization headers,
- payment data.
