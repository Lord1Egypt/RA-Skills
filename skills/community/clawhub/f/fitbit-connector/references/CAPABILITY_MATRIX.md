# Fitbit Capability Matrix (Docs-First, Inspire 3 Oriented)

This matrix is intentionally **deterministic** and built from Fitbit API contract + known tracker/account dependencies.

- API contract source: `fitbit-web-api-swagger.json`
- Runtime command: `python3 scripts/fitbit_tools.py capability-matrix`
- No probe loops required.

## Scope model

Maximum configured scope set:

`activity cardio_fitness electrocardiogram heartrate irregular_rhythm_notifications location nutrition oxygen_saturation profile respiratory_rate settings sleep social temperature weight`

## Sync strategy (rate-limit-safe)

1. **Normal operation:** use `store-sync-day` once daily (or a single `store-sync-range` for bounded backfill).
2. **No broad probing in production** (`discover-capabilities` only for explicit diagnostics).
3. **Treat domain support as contract-first:**
   - `missing_scope` => OAuth grant issue
   - `rate_limited` => defer/retry later
   - `no_data` => user did not log / no qualifying signal
   - `device_unsupported_or_not_found` => account/device/endpoint mismatch
4. **Fetch from cache first** (`fetch-range` / `fetch-latest`), API refresh only when needed.

## Reauth trigger

Reauthorize when either is true:

- `.env FITBIT_SCOPES` changed, or
- `auth-status` shows granted scopes missing required domains.

Use these commands:

```bash
python3 scripts/fitbit_auth.py auth-url
# Open URL, approve scopes, copy code + state from redirect URL
python3 scripts/fitbit_auth.py exchange --code "<CODE>" --state "<STATE>"
python3 scripts/fitbit_tools.py auth-status
```
