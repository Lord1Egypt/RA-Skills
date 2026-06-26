# PostGrid Notes

This skill defaults to:

- Base URL: `https://api.postgrid.com/print-mail/v1`
- API key header: `x-api-key`
- Route: `letters` (overridable)

If your PostGrid account expects different routes or fields, use:

- `--postgrid-base-url`
- `--postgrid-route`
- `--postgrid-key-header`
- `--payload-overrides-json` or `--payload-overrides-file`

Common routes used by this skill:

- `letters`
- `postcards`

The script sends one API call per contact and records success/failure details for each contact id.
