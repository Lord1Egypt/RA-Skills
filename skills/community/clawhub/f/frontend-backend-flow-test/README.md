# Frontend-Backend Flow Test

Audit-first skill for comparing frontend request behavior against backend API contracts.

## Product stance

This project is centered on **static contract audit**.
Its main value is to surface API mismatches before runtime testing:
- missing endpoints
- method/path drift
- query/body/auth hint mismatches
- backend-only or orphaned routes

Live request generation exists only as a secondary, limited capability.
Do not treat it as the product core.

## Primary entrypoint

```bash
python3 scripts/audit_contracts.py \
  --frontend /path/to/frontend \
  --backend /path/to/backend \
  --output-dir ./out/audit
```

Outputs:
- `audit-report.json`
- `audit-report.md`

## Secondary entrypoint

`python3 scripts/generate_tests.py ...`

This remains available only as an **experimental live helper** for narrow dev/staging follow-up checks.
Do **not** treat it as your main API regression test system, rollback-safe runner, or replacement for `workspace-qa/tests/`.
See `references/LIVE-MODE.md`.
