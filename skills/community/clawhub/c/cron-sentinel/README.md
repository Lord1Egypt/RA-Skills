# Cron Sentinel 🛡️

A dead-man's switch for your scheduled tasks. Bulletproof scheduling that alerts you when a job **silently** fails.

Everyone monitors the job that crashes. Almost nobody catches the job that just... stops — the machine was asleep at 3am, someone renamed the script, the cron daemon wasn't reloaded. The task never ran, threw no error, and the first you hear of it is when the backup you needed isn't there. Cron Sentinel catches both the loud failures and the silent ones.

## What it does

- **wrap** — run your command through Sentinel so each run is recorded (start, end, exit code, duration, output tail), with optional retries and a per-attempt timeout.
- **check** — the watchdog. Flags any job that crashed *or* is overdue (should have run by now but didn't). Exits non-zero so it can drive an alert.
- **status** — a quick table of every tracked job: last run, health, next expected.
- **crontab** — prints a ready-to-paste wrapped crontab line plus a watchdog line.

## Quick start

```bash
# What cron actually runs:
python cron_sentinel.py wrap --name backup --expect-every 1d --retries 2 -- /path/backup.sh

# The watchdog (its own short schedule):
python cron_sentinel.py check       # exits 1 if anything failed or went silent
python cron_sentinel.py status

# Generate the crontab lines:
python cron_sentinel.py crontab --name backup --schedule "0 3 * * *" --expect-every 1d -- /path/backup.sh
```

The command always goes after `--`. `--expect-every` (`30m`, `12h`, `1d`, `1w`) is what makes silent-failure detection possible — it's how Sentinel knows a job *should* have run. State lives in `~/.cron-sentinel/state.json` (override with `--state` or `$CRON_SENTINEL_STATE`); all timestamps are UTC, so it's correct across timezones and DST.

## The whole idea in two lines

1. The **wrapped job** runs your real task on its normal schedule.
2. The **watchdog** runs `check` every few minutes and pings you only when something's wrong.

A `💥 failed` means it ran and errored (show the output tail). A `🔇 overdue` means it never ran — the problem is upstream, not the command. That distinction alone saves hours of debugging.

## Requirements

- Python 3.8+ (standard library only). No API key, no external services.
