# Command Reference

## Storage Rules

- Databases live under `~/.cookie_alive/<db_name>.db` by default.
- Override the home directory with `COOKIE_ALIVE_HOME` or `SESSION_COOKIE_ONLINE_HOME`.
- Override the default database name with `COOKIE_ALIVE_DB_NAME` or `SESSION_COOKIE_ONLINE_DB_NAME`.
- `db_name` accepts letters, digits, `_`, `-`, and `.` only. The script appends `.db` automatically.
- Each database can contain multiple named profiles.

## Main Commands

### Upsert a profile

```bash
python {baseDir}/scripts/cookie_alive.py upsert \
  --db-name example_site \
  --profile dashboard \
  --refresh-url https://example.com/api/session/ping \
  --cookie-header "sessionid=abc123; csrftoken=xyz789" \
  --header "User-Agent: Mozilla/5.0" \
  --interval-seconds 600
```

Use `--cookie-json '{"sessionid":"abc123","csrftoken":"xyz789"}'` when the cookie is already structured.

### Read a cookie for another program

```bash
python {baseDir}/scripts/cookie_alive.py get \
  --db-name example_site \
  --profile dashboard \
  --format header
```

Use `--format json` for the raw cookie map or `--format record` for the full profile metadata.

### Refresh once

```bash
python {baseDir}/scripts/cookie_alive.py refresh \
  --db-name example_site \
  --profile dashboard
```

The script sends the stored HTTP request, merges any `Set-Cookie` headers back into SQLite, and updates `last_refreshed_at`, `last_status_code`, and `last_error`.

### Check whether one session is still alive

```bash
python {baseDir}/scripts/cookie_alive.py check \
  --db-name example_site \
  --profile dashboard
```

Behavior:

- exit code `0`: the session is still alive and the keepalive request succeeded
- exit code `1`: the session is no longer alive, redirected to login, or returned an error

The JSON output includes `alive`, `last_status_code`, and `last_error`.

### Export a cookie for another program

Read the current cookie without refreshing:

```bash
python {baseDir}/scripts/cookie_alive.py pull \
  --db-name example_site \
  --profile dashboard \
  --format header
```

Refresh first, then return the updated cookie in one command:

```bash
python {baseDir}/scripts/cookie_alive.py pull \
  --db-name example_site \
  --profile dashboard \
  --refresh \
  --format header
```

Formats:

- `--format header`: print a raw `Cookie` header value for direct HTTP use
- `--format json`: print only the cookie object
- `--format record`: print the full stored record including metadata

### Keep the session alive in a loop

```bash
python {baseDir}/scripts/cookie_alive.py run \
  --db-name example_site \
  --profile dashboard
```

Optional loop controls:

- `--iterations 3`: stop after a fixed number of refreshes
- `--wait-seconds 5`: override the stored interval for this run
- `--stop-on-error`: stop immediately when a refresh fails

### Run all active websites with their own trigger times

```bash
python {baseDir}/scripts/cookie_alive.py run-all \
  --db-name websites
```

This scheduler:

- loads every active profile from one SQLite database
- respects each profile's own `interval_seconds`
- refreshes profiles only when they become due
- sleeps between due windows instead of hammering every site continuously

Useful options:

- `--iterations 5`: stop after 5 refresh attempts across all profiles
- `--max-sleep-seconds 30`: wake up at most every 30 seconds while waiting for the next due profile
- `--stop-on-error`: stop the whole scheduler if any profile fails

### Inspect or clean up

```bash
python {baseDir}/scripts/cookie_alive.py list --db-name example_site
python {baseDir}/scripts/cookie_alive.py delete --db-name example_site --profile dashboard
```

## Website Data Needed

To connect one real website, gather these fields first:

- a stable `refresh_url`
  Prefer a cheap authenticated endpoint such as `/api/session/ping`, `/me`, `/heartbeat`, or a lightweight page request.
- the current authenticated cookie
  Usually copied from browser devtools as a `Cookie` header string.
- any required extra request headers
  Common examples are `User-Agent`, `Referer`, `Origin`, `X-CSRF-Token`, and site-specific auth headers.
- the HTTP method and optional body
  Most sites work with `GET`, but some keepalive routes require `POST` plus a small JSON or form body.
- the refresh interval
  Pick a value lower than the session expiry window. For example, refresh every 5 to 15 minutes when the site expires idle sessions after 30 minutes.
- the success rule
  Define what counts as a healthy refresh: HTTP 200, no redirect to login, expected JSON field, or a renewed `Set-Cookie` header.

Optional but useful:

- whether different accounts should be stored as separate profiles in one database
- whether downstream programs need `Cookie` header output or JSON output
- whether the site rotates cookies on every refresh or only on re-login

## Managing Many Websites

Use one database as a hub and one profile per website or account.

Recommended naming:

- `--db-name websites`
- `--profile chsi-main`
- `--profile github-work`
- `--profile internal-admin`

Each profile stores its own:

- refresh URL
- cookie
- headers
- timeout
- `interval_seconds`

Typical workflow:

```bash
python {baseDir}/scripts/cookie_alive.py --db-name websites upsert --profile chsi-main ...
python {baseDir}/scripts/cookie_alive.py --db-name websites upsert --profile github-work ...
python {baseDir}/scripts/cookie_alive.py --db-name websites list --active-only
python {baseDir}/scripts/cookie_alive.py --db-name websites run-all
```

## Passing Cookies To Another Program

Recommended integration patterns:

- CLI stdout
  Let the other program run `pull --format header` and read stdout.
- JSON bridge
  Let the other program run `pull --format json` and parse the returned JSON.
- Refresh-and-use
  Let the other program run `pull --refresh --format header` so it gets the newest cookie in one step.
- Local HTTP wrapper
  Let the other program call a local HTTP server instead of spawning `cookie_alive.py` directly.

Example in Python:

```python
import subprocess

cookie_header = subprocess.check_output(
    [
        "python",
        "scripts/cookie_alive.py",
        "--db-name",
        "chsi",
        "pull",
        "--profile",
        "main",
        "--refresh",
        "--format",
        "header",
    ],
    text=True,
).strip()
```

Example with the local HTTP wrapper:

```bash
python {baseDir}/scripts/examples/http_api_wrapper.py --host 127.0.0.1 --port 8787
curl "http://127.0.0.1:8787/pull?db_name=chsi&profile=main&refresh=1&format=header"
curl "http://127.0.0.1:8787/check?db_name=chsi&profile=main"
```

## Example: CHSI

For the CHSI account page below, use the account page itself as the first refresh target and treat redirects to `/passport/login` as session expiry:

```bash
python {baseDir}/scripts/cookie_alive.py --db-name chsi upsert \
  --profile main \
  --refresh-url "https://account.chsi.com.cn/account/account!show.action" \
  --cookie-header "<paste the live Cookie header here>" \
  --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" \
  --header "Referer: https://www.chsi.com.cn/" \
  --interval-seconds 600
```

Then verify once:

```bash
python {baseDir}/scripts/cookie_alive.py --db-name chsi refresh --profile main
python {baseDir}/scripts/cookie_alive.py --db-name chsi get --profile main --format record
```

## Limits

- The runtime preserves the cookie name/value pairs required for HTTP requests. It does not attempt to model a full browser cookie jar with domain/path matching rules.
- Use a separate browser automation flow when the site only stays alive through browser-side JavaScript or non-HTTP activity.
