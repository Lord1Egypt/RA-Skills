# ARW probe and signal catalog

## Core probe suites

### `smoke`
Current deterministic smoke coverage lives in `arw/probes.py` and is intended to catch assistant workflow regressions early.

Current probe families include:
- routing smoke
- think-state consistency
- recall smoke

## Current signal classes surfaced by ARW

ARW is more than a raw log scraper because it emits structured signals such as:
- point-in-time probe outcomes,
- daily digest severity,
- immediate severe alerts,
- digest freshness,
- probe instability trends,
- alert deduplication/suppression,
- validation evidence coverage,
- operator summary status,
- chronic drift/streak visibility across recent artifacts.

## Operator-facing artifact types

- `arw-<suite>-*.json`: raw run artifacts
- `arw-digest-*.json` / `.md`: scorecard digest artifacts
- `arw-alert-*.json` / `.md`: severe immediate alert artifacts
- `arw-dedup-suppressed-*.json`: suppressed severe alert evidence
- `validation-*.json`: fail-closed validation artifact

## RC1 guidance

For RC1, prefer explaining ARW in terms of:
1. probes,
2. derived reliability signals,
3. operator decision outputs,
4. and validation proof.

Do not frame the product as “just log scraping.”
