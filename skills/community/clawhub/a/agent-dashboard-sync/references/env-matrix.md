# Env Matrix

## Worker (`agent-fleet-backend`)

- `INGEST_TOKEN` (secret): auth for `POST /ingest`
- `READ_TOKEN` (secret): auth for `GET /fleet`
- `EVENTS_MAX` (var): recent events ring buffer size (default 200)

## Collector (`openclaw-state-collector`)

- `REPORT_MODE`: `local` or `cloudflare`
- `REPORT_ENDPOINT`: Worker base URL, e.g. `https://<worker>.workers.dev`
- `REPORT_TOKEN`: ingest token (same as `INGEST_TOKEN`)
- `AGENT_ID`: stable unique id per node

## Dashboard (`agent-dashboard`)

- `NEXT_PUBLIC_DATA_SOURCE_MODE`: `cloudflare`
- `FLEET_API_ENDPOINT`: Worker base URL
- `DASHBOARD_READ_TOKEN`: read token (server-side env only)

## Secret Handling

- Do not store secrets in `SKILL.md`, repo README, or examples committed to git.
- Use Wrangler/Vercel secret managers.
- Use placeholders (`<REDACTED>`) in shared snippets.
