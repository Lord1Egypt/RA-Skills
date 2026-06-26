# Runtime Config

The skill reads its env vars and config from the OpenClaw skill entry for `cnki-watch`, typically in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "cnki-watch": {
        "env": {
          "CNKI_COOKIE": "",
          "CNKI_USERNAME": "",
          "CNKI_PASSWORD": ""
        },
        "config": {
          "browserProfile": "chrome",
          "timezone": "Asia/Shanghai",
          "defaultSchedule": "daily@09:00",
          "maxManualResults": 10,
          "maxPushResults": 20
        }
      }
    }
  }
}
```

Runtime precedence:

1. Process environment
2. `skills.entries.cnki-watch.env`
3. `skills.entries.cnki-watch.config`
4. Script defaults

Notes:

- Required env names are exactly `CNKI_COOKIE`, `CNKI_USERNAME`, and `CNKI_PASSWORD`.
- `CNKI_COOKIE` is preferred over username/password.
- `CNKI_USERNAME` and `CNKI_PASSWORD` must be used together when cookie auth is unavailable.
- `browserProfile` is part of the public config contract even if the runtime implementation chooses its own browser bootstrap path.
- `timezone` controls cron interpretation for `daily@...`, `weekly@...`, `workday@...`, and `cron:...` schedules.
- `defaultSchedule` is used whenever a subscription is created without an explicit `--schedule`.
- `maxManualResults` caps one-off query output when the caller does not set a stricter limit.
- `maxPushResults` caps the number of new papers pushed by a subscription run.
- Optional host-side env vars outside OpenClaw config:
  - `CNKI_WATCH_CHROMIUM`: absolute path to a local Chrome/Chromium/Edge executable
  - `CNKI_WATCH_AUTO_INSTALL=0`: disable first-run automatic `npm install`
