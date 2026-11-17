# Unattended Runs — cron, systemd Timers, launchd

"It works when I run it" is not a claim about the script; it is a claim about your interactive environment. A scheduler gives the script almost none of it.

## What Cron Does Not Give You

| You have interactively | Cron job has |
|---|---|
| PATH from your profile | A minimal PATH, typically `/usr/bin:/bin` — the cause of most "command not found" (`debugging.md`) |
| `~/.bashrc`, `~/.profile`, nvm/pyenv/rbenv shims | Nothing sourced at all; version managers are invisible |
| bash | `/bin/sh` unless the crontab sets `SHELL=/bin/bash` — so bashisms fail with "unexpected operator" |
| Your working directory | `$HOME` (per-user crontabs) — every relative path resolves elsewhere |
| A TTY | None: any prompt, `sudo` password, or `read` blocks forever |
| Your locale and TZ | Often `LANG` unset (C locale): different `sort` order and date formats |
| Your ulimits and umask | The daemon's, which are usually stricter |
| Secrets in your shell environment | Nothing — they must come from a file the job reads |

Simulate the difference before deploying: `env -i /bin/sh -c '/path/to/script.sh'` reproduces the empty-environment failure in one second.

## Crontab Rules People Learn The Hard Way

```cron
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=ops@example.com
# m h dom mon dow  command
17 3 * * *  /opt/jobs/backup.sh >> /var/log/backup.log 2>&1
```

- `%` is not a percent sign: cron turns it into a newline and everything after the first one becomes stdin. Escape it — `date +\%F` — which is why so many jobs write files named `+`
- Cron mails ANY output; silence means success. A job that chats on stdout mails you every run until you stop reading the mail entirely. Redirect to a log, print only on failure
- No environment expansion in the command field beyond simple `$VAR` from the crontab's own assignments; write absolute paths for the script AND for anything it calls
- Files in `/etc/cron.d/` are ignored by `run-parts` if the filename contains a dot — `backup.sh` there never runs, `backup` does. `/etc/cron.d` and `/etc/crontab` also take a USER field before the command; a personal crontab does not
- A crontab file must end with a newline; some cron implementations silently drop the last line without one
- `crontab -e` validates syntax; copying a file over `/var/spool/cron/…` by hand does not

## The Wrapper Pattern

Give the scheduler one line and put everything else in the script:

```bash
#!/usr/bin/env bash
set -euo pipefail
export PATH=/usr/local/bin:/usr/bin:/bin
cd "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1
[[ -r /etc/app/env ]] && set -a && . /etc/app/env && set +a   # secrets from a file, not the crontab
exec >>/var/log/app/job.log 2>&1                              # self-logging from here on
printf '=== %s start pid=%d\n' "$(date -u +%FT%TZ)" "$$"
trap 'printf "=== %s end rc=%d\n" "$(date -u +%FT%TZ)" "$?"' EXIT
```

- One line in the crontab means the schedule is the only thing you edit as root
- Log rotation is not automatic: an append-only log from a per-minute job fills the disk in weeks. Add a logrotate rule or write date-stamped files with a retention pass
- The start/end pair with the exit code is what makes a log answerable after the fact ("did it run at all?" vs "did it fail?")

## Overlap, Catch-Up, and Clocks

- A job that occasionally takes longer than its interval WILL overlap; cron starts a second copy regardless. Wrap it: `*/5 * * * * flock -n /var/lock/job.lock /opt/jobs/job.sh` — `-n` skips the run if the previous one is still going (in-script locking: `redirection.md`)
- Cron does not catch up: a host asleep or down at 03:17 simply misses the run. If missed runs matter, use a systemd timer with `Persistent=true`, or make the job idempotent and run it more often
- DST: behavior is implementation-specific, so do not rely on it. On a daemon with no DST handling, a job at 02:30 local runs twice on the fall-back day and zero times on the spring-forward day; Vixie cron/cronie (Debian, RHEL) compensate for shifts under 3 h — a skipped fixed-time job runs once right after the change, and a job repeated by the fall-back hour runs only once. Schedule outside 01:00-03:00, or set `CRON_TZ=UTC` (Vixie cron) / run the daemon in UTC
- Herd effects: every host firing at `0 * * * *` hammers the same endpoint. Stagger with a per-host offset — `$(( RANDOM % 300 ))` seconds of sleep inside the job, or a distinct minute per host

## systemd Timers (Linux, when cron is not enough)

```ini
# /etc/systemd/system/backup.service        # /etc/systemd/system/backup.timer
[Service]                                   [Timer]
Type=oneshot                                OnCalendar=*-*-* 03:17:00
ExecStart=/opt/jobs/backup.sh               Persistent=true
User=backup                                 RandomizedDelaySec=600
```

- Advantages that decide it: `Persistent=true` runs a missed job at next boot, output goes to the journal with the unit name (`journalctl -u backup`), the exit code shows in `systemctl status`, and resource limits/sandboxing come free
- `systemctl list-timers` shows last and next run — the answer to "did it run?" that cron never gives
- Timers do not stack: while the service is active the next trigger is skipped, so overlap protection is built in
- Test without waiting: `systemctl start backup.service`
- Environment is even emptier than cron's; set what you need with `Environment=` or `EnvironmentFile=`

## launchd (macOS)

- `~/Library/LaunchAgents/<label>.plist` for user jobs, `/Library/LaunchDaemons/` for system ones; `StartCalendarInterval` for a schedule, `StartInterval` for "every N seconds", `RunAtLoad` for boot
- Missed runs while asleep fire once on wake (unlike cron, which skips), so a job that assumes exactly-once-per-day must handle a late double
- Capture output explicitly with `StandardOutPath`/`StandardErrorPath`; there is no mail
- macOS privacy protection applies to scheduled jobs: a job touching `~/Documents`, `~/Desktop`, or an external volume fails with "Operation not permitted" until the executing binary (often `/bin/bash` or the terminal app) is granted Full Disk Access
- Reload after editing: `launchctl unload` then `launchctl load` the plist; editing alone changes nothing

## Knowing It Ran

- Exit codes are the interface: nonzero must mean "a human needs to look". A script that catches every error and exits 0 makes the scheduler useless
- Dead-man's-switch beats alert-on-failure for scheduled work: ping a monitoring endpoint at the END of a successful run and alert when the ping is missing — that also catches "cron never started it" and "the host is off"
- Write a state file with the last successful run timestamp; a five-line check on it is a better health check than reading logs
- Keep a manual override path: every scheduled script should be safe to run by hand at any time, which is the same property as idempotence (`files.md`)
