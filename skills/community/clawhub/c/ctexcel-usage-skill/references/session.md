# Session lifecycle

## What is stored

`ctexcel-usage` keeps one record per account in a private state file:

```
<user config dir>/ctexcel-usage/state.json
```

Override with `CTEXCEL_USAGE_STATE_DIR`. The file is created with mode `0600`
and the directory with `0700`.

```json
{
  "version": 1,
  "accounts": {
    "07XXXXXXXX": {
      "account": "07XXXXXXXX",
      "cookies": {"SESSION": "<server-issued cookie>"},
      "login_at": "2026-11-06T15:15:34Z",
      "last_valid_at": "2026-11-06T15:16:59Z",
      "last_checked_at": "2026-11-06T15:16:59Z",
      "first_invalid_at": null
    }
  },
  "pending_login": null,
  "last_sms_at": {"07XXXXXXXX": "2026-11-07T02:31:00Z"}
}
```

No password and no verification code are ever written.

`pending_login` bridges the two login commands. It holds the anonymous session
created by `--request-sms` and expires after 10 minutes. `last_sms_at` enforces
the local 10-minute SMS cooldown per account.

## How long does a session last?

The CTExcel `SESSION` cookie is a server-side session cookie with **no
client-side expiry** (`Set-Cookie` has no `Max-Age` or `Expires`). The real
lifetime is therefore controlled by the server and is not published. This CLI
does not guess it.

What the CLI does instead:

1. Every `status` and `usage` call hits an authenticated endpoint first.
2. On success it refreshes the stored cookie and sets `last_valid_at`.
3. On `code: 1001` it sets `first_invalid_at`, exits with code `3`, and tells
   the caller to log in again.
4. `status --output json` reports `login_at`, `last_valid_at`,
   `last_checked_at`, `first_invalid_at`, and `days_since_login`.

Observed behavior in practice determines the maintenance strategy:

- **Sliding expiration**: each successful request extends the server-side
  session, so a daily `usage` keeps it alive indefinitely.
- **Absolute expiration**: the session dies at a fixed age; the timestamps show
  the observed lifetime, and the user must log in again at that point.
- **Idle timeout**: a gap in queries kills the session; resuming requires a new
  SMS code.

Because the cookie has no client-side expiry, the CLI relies on server
validation rather than a local timer. Do not add a guessed TTL.

## Keepalive

No dedicated keepalive is configured. A daily `usage` is the default heartbeat
and refreshes `last_valid_at`.

If an idle timeout is observed later, choose a `status` interval from the
observed timeout instead of guessing one now. `status` never sends SMS, so a
keepalive cannot trigger the SMS cooldown.

## SMS cooldown

The CLI refuses `--request-sms` within 10 minutes of the previous successful
request for the same account and exits with code `5`. This is intentional:
rapid re-sends are wasteful, often ignored, and can make the account look
abusive. Do not bypass it by deleting the state file.

## Re-login

```bash
ctexcel-usage login --account <phone> --request-sms
ctexcel-usage login --account <phone> --code <code>
```

The `--request-sms` step is valid for 10 minutes. Re-sends are rate-limited for
about 180 seconds. A new login replaces the old cookie; the old session becomes
irrelevant.

## Multiple accounts

Every command accepts `--account`. With one stored account the flag is
optional; with several, omitting it is an error. `logout` removes only the
selected account.

## Failure modes

| Symptom | Meaning | Action |
| --- | --- | --- |
| Exit `3` / `session_valid: false` | Server rejected the cookie | Log in again |
| Exit `2` with "no stored session" | Never logged in, or `logout` was run | Log in |
| Exit `2` with "verification request expired" | Pending login older than 10 minutes | Run `--request-sms` again |
| Exit `5` | Local 10-minute SMS cooldown active | Wait the reported seconds; do not retry |
| Exit `4` | Network or API failure | Check connectivity/proxy, retry once |

## Privacy

The state file grants account access. Never copy it into notes, repositories,
chat, issue trackers, or backups. Use `ctexcel-usage logout` to delete it.