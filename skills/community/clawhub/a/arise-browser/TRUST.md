# AriseBrowser Trust & Security Model

## What AriseBrowser Does

AriseBrowser is a local HTTP server that controls a Chromium browser via Playwright. It:
- Listens on localhost only (127.0.0.1) by default
- Does NOT contact external services
- Does NOT send telemetry or analytics
- Does NOT store data beyond the current session

## Security Boundaries

### Network
- Binds to 127.0.0.1 by default (local only)
- Optional Bearer token authentication (`ARISE_BROWSER_TOKEN`)
- No TLS built-in (use reverse proxy for remote access)

### Browser
- Uses Playwright's Chromium (not your system Chrome)
- Default: fresh profile with no saved data
- `--profile` mode: accesses saved logins, cookies, history
- Stealth headers enabled by default to avoid bot detection

### Data
- Snapshots and actions are ephemeral (not persisted)
- Recordings are in-memory only, cleared on server restart
- No data is written to disk unless `--profile` is used

## Recommendations

1. **Always set `ARISE_BROWSER_TOKEN`** when the API is accessible to other processes
2. **Never use `--profile` with your daily browser profile** — create a dedicated one
3. **Never bind to 0.0.0.0** without token authentication
4. **Review `/evaluate` usage** — it executes arbitrary JavaScript in the page context

## Dependencies

- `playwright` — Browser automation (Microsoft, Apache-2.0)
- `fastify` — HTTP framework (MIT)
- `pino` — Logging (MIT)

All dependencies are widely used, well-maintained, and open source.
