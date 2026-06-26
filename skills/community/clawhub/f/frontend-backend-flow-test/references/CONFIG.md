# Live Configuration Reference

This file documents configuration for the **secondary live verification helper** `scripts/generate_tests.py`.

If you only need the main skill value, stop here and use static audit instead:

```bash
python3 scripts/audit_contracts.py \
  --frontend /path/to/frontend \
  --backend /path/to/backend \
  --output-dir ./out/audit
```

For live follow-up usage, see also [LIVE-MODE.md](LIVE-MODE.md).

## Supported configuration areas

- service metadata and API base URL
- authentication header/cookie configuration
- test account login flow
- CRUD-like operation definitions for targeted follow-up checks

## Important warning

This configuration is **not** the product core.
It exists to support limited dev/staging verification after an audit has already highlighted suspicious paths.
