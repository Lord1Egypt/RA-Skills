# Dashboard and remote access

Use this file when the user wants the CLIProxy dashboard or management UI reachable beyond localhost.

## First decide exposure mode

- local only
- LAN only
- public internet behind reverse proxy

If the user did not ask for public exposure, do not default to it.

## Preferred pattern

For public access, prefer:
- reverse proxy on 80 or 443
- upstream bound to localhost or a private interface
- only the minimum required firewall openings

Prefer a clean external URL over exposing raw high ports directly.

## What to confirm

Before opening access, state clearly:
- which URL will be reachable
- which ports will be opened
- whether the dashboard includes sensitive controls

## Verification

After exposure is configured, verify:
- local upstream still works
- external URL resolves and loads
- reverse proxy does not break streaming if the API uses it
- firewall rules match the intended exposure and nothing wider

## Security reminders

- management UIs and dashboards may expose tokens, account controls, or model routing settings
- avoid binding sensitive surfaces to all interfaces unless that is explicitly intended
- prefer HTTPS when the dashboard is reachable over the internet
