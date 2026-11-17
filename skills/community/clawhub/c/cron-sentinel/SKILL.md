---
name: cron-sentinel
version: 1.2.0
description: "Monitor scheduled/cron jobs and get alerted when one fails OR silently never runs. Use this skill when the goal is reliability or failure-detection for a recurring task the user already runs or is setting up - e.g. 'how would I even know if my cron job silently stopped,' 'my backup didn't run and nothing warned me,' 'monitor my scheduled jobs,' 'alert me when a job fails,' 'add retries and a dead-man's switch to my cron,' or 'is my nightly task still actually running.' It wraps a scheduled command so each run is recorded (exit code, duration, redacted output tail) with optional retries and a timeout, then a watchdog flags both crashed jobs and overdue jobs that silently never ran. Do NOT trigger on plain scheduling requests with no monitoring need ('remind me at 5,' 'run this once tomorrow'), or on general cron-syntax questions ('what does * * * * * mean') - only when reliability or silent-failure detection is the actual ask. Runs a local, standard-library-only Python tool that executes the user's own command directly (no shell), keeps an owner-only state file under ~/.cron-sentinel/, and prints crontab lines for the user to add themselves. It never edits a crontab, creates scheduled tasks, uses the network, or requires elevated privileges."
metadata:
  openclaw:
    emoji: 🛡️
    requires:
      bins: [python3]
      config: ["~/.cron-sentinel/state.json"]
    envVars:
      - name: CRON_SENTINEL_STATE
        required: false
        description: "Optional path override for the state file. The only environment variable the tool reads."
---

# Cron Sentinel

Everyone monitors the job that crashes. Almost nobody catches the job that just... stops. The machine was asleep at 3am, someone renamed the script, the cron daemon wasn't reloaded - the task never ran, threw no error, and the first you hear of it is when the backup you needed isn't there. Cron Sentinel is a dead-man's switch for your scheduled tasks: it records every run and alerts you both when a job fails loudly and when it goes silent.

Four jobs:

1. **wrap** - run your scheduled command through Sentinel so each run is recorded (start, end, exit code, duration, output tail), with optional retries and a per-attempt timeout.
2. **check** - the watchdog. Reports any job that crashed (non-zero exit) or is overdue (expected to have run by now but hasn't). Exits non-zero if anything is wrong, so it can drive an alert.
3. **status** - a quick table of every tracked job: last run, health, when it's next expected.
4. **crontab** - print a ready-to-paste crontab line that wraps a command, plus a watchdog line.

## Permissions & data

This skill is not informational - it runs a local tool (`cron_sentinel.py`) that touches the system. Be transparent with the user about exactly what it does, and never run it on a command they didn't ask you to wrap. Its full reach:

- **Command execution.** `wrap` runs the command placed after `--` as a direct subprocess with an argument list (`shell=False`), with optional retries and a per-attempt timeout. The command is never interpreted by a shell, and the tool never fetches, downloads, or evaluates anything else.
- **Filesystem.** Reads and writes one state file, `~/.cron-sentinel/state.json` (override with `--state` or `$CRON_SENTINEL_STATE`). The folder is created owner-only and the file is written owner-only. Nothing else on disk is touched.
- **Environment.** Reads `CRON_SENTINEL_STATE` only, to locate the state file.
- **Network.** None. Pure Python standard library; nothing leaves the machine.
- **Privileges.** Runs as the current user. It never requests elevated privileges; anything a job needs beyond that belongs in the user's own command and scheduler, not in Sentinel.
- **Scheduling.** Sentinel never edits a crontab, creates scheduled tasks, or installs startup entries. `crontab` only prints lines for the user to review and add themselves.

**Output and secrets:** so failures are diagnosable, `wrap` saves the last ~2000 characters of a job's output in the state file. Before saving, it masks common secret patterns (passwords, tokens, API keys, bearer headers, cloud and GitHub keys, private-key blocks, credentials in URLs). Redaction is best-effort, so for commands that handle credentials, add `--no-output-tail` to store no output at all. Mention this whenever you help wrap something that handles credentials.

## When to use this

Use this when the user cares about *whether a recurring job actually ran and succeeded* - reliability, alerting, or silent-failure detection. Signals: "how would I even know if it failed," "my backup didn't run and nothing warned me," "monitor my jobs," "alert me if it stops," "add retries to my cron." If they're *creating* a schedule and reliability matters, set it up wrapped from the start. If they're *debugging* a schedule that misbehaved, `status` and `check` tell you what actually happened on the last run.

**When NOT to use:** don't reach for this on a plain "schedule this" / "run it every night" request where the user just wants the job to run and hasn't expressed any concern about monitoring or failures - set that up with the normal scheduler instead. Likewise skip it for general cron-syntax help ("what does `0 3 * * *` mean") and for one-off, run-once-later reminders. Wrapping adds a tool, a state file, and a watchdog; only introduce that when failure-detection is genuinely the point. If you're unsure whether the user wants monitoring, ask before wrapping.

This is complementary to OpenClaw's own scheduler and to system cron - Sentinel doesn't replace what triggers the job, it makes whatever triggers it observable and self-reporting.

## The tool

```bash
# Wrap a command (this is what cron actually runs):
python cron_sentinel.py wrap --name backup --expect-every 1d --retries 2 -- /path/backup.sh
python cron_sentinel.py wrap --name sync --no-output-tail -- /path/sync-with-api.sh   # store no output

# The watchdog (run this on its own short schedule):
python cron_sentinel.py check          # exits 1 if any job failed or is overdue
python cron_sentinel.py status         # human-readable table

# Generate the crontab lines for the user:
python cron_sentinel.py crontab --name backup --schedule "0 3 * * *" --expect-every 1d -- /path/backup.sh
```

The command to run always goes after `--`. Job names may contain letters, digits, dot, underscore and hyphen. `--expect-every` accepts human durations (`30m`, `12h`, `1d`, `1w`) and is what makes silent-failure detection possible: it's how Sentinel knows a job *should* have run by now. State is stored in `~/.cron-sentinel/state.json` (override with `--state` or `$CRON_SENTINEL_STATE`); all timestamps are UTC so it stays correct across timezones and DST.

## The pattern to set up

The whole design is two scheduled entries:

1. **The wrapped job** - the real task, run through `wrap`, on its normal schedule.
2. **The watchdog** - `check` on a short schedule (e.g. every 30 min) that pipes its output to wherever the user gets notified.

`crontab` prints both lines. Show them to the user and let the user add them with `crontab -e`. Never run `crontab`, edit crontab files, or create scheduled tasks yourself. In OpenClaw, suggest the two scheduled tasks (the wrapped command, and a short-interval `check` whose output routes to their channel), show exactly what each would run, and create them only if the user explicitly confirms.

## How to help

1. **Setting up a new schedule:** ask for the command, how often it should run, and whether retries make sense (yes for anything network-dependent). Then produce the wrapped crontab line via `crontab`, and explain the watchdog line. Always set `--expect-every` - without it, silent failures can't be detected, which is the whole point.
2. **"Is my job still working?"** run `status` and read back the last run time and health. If it shows `overdue`, that's your silent failure.
3. **"My job failed / isn't running":** run `check`. A `💥 failed` means it ran and errored - show the captured output tail. A `🔇 overdue` means it never ran - the problem is upstream (the trigger, the machine, the path), not the command itself. That distinction saves a lot of wasted debugging.
4. **Wiring up alerts:** the `check` exit code and output are designed to feed a notifier. In OpenClaw, schedule `check` and route its output to the user's channel so they only hear from it when something is actually wrong.

## Honest interpretation

- `overdue` uses a grace window (default 50% of the interval) so a job that's merely a little late doesn't cry wolf. Tune with `--grace` if a job's timing is naturally loose.
- A `check` that reports all healthy is a real green light - say so plainly.
- Retries help with *transient* failures (a flaky network call). They won't fix a broken command, and Sentinel still records the final failure - so don't let retries mask a job that's genuinely broken.
