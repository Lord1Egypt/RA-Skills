# Setup Manual

Use this manual when adapting the OpenClaw cron health kit to a destination instance.

## 1. Locate OpenClaw Runtime Facts

Find these values from the destination server only:

- OpenClaw home directory
- scheduler jobs file, if present
- structured scheduler list command, if present
- log directories relevant to scheduled jobs
- delivery target or origin chat/topic

Do not copy values from another instance.
Do not use the service manager as the OpenClaw scheduler source. OpenClaw cron
inventory must come from a structured OpenClaw cron list command, API output,
or read-only scheduler jobs file.

## 2. Configure OpenClaw Job Source

Prefer a JSON list command if the instance supports it. Configure it as a structured `argv` object, not a shell string:

```json
{"argv": ["openclaw", "cron", "list", "--json"]}
```

Otherwise configure a read-only jobs file path.

If the jobs file does not expose `nextRun`, do not treat that alone as broken. It is metadata unavailable from the source, not proof of failure.

## 3. Configure System Crons Correctly

Keep crontab files separate from run-parts directories:

- `crontab_commands`: structured commands that output crontab syntax, such as `{"argv": ["crontab", "-l"]}`
- `crontab_files`: files that contain crontab syntax, such as `/etc/crontab` and `/etc/cron.d/*`
- `run_parts_dirs`: directories containing executable scripts, such as `/etc/cron.daily`

Never parse scripts inside `/etc/cron.daily` or similar directories as if their contents were crontab lines.

## 4. Configure Known Jobs

Leave `known_system_jobs` empty until you have local evidence. Add a job only when you know:

- its name
- command or script
- expected schedule/frequency
- log file, scheduler metadata, or fixed diagnostic probe
- freshness threshold

Set freshness slightly above the expected interval. For example, a daily job can use 1500-1800 minutes.

## 5. Configure Project Validations

Add `known_project_validations` only for projects present on the instance and prefer log, scheduler metadata, or status files as proof.

The portable checker only executes these fixed diagnostic argv forms:

- `{"argv": ["openclaw", "cron", "list", "--json"]}`
- `{"argv": ["crontab", "-l"]}`
- `{"argv": ["systemctl", "--failed", "--no-pager", "--plain"]}`
- `{"argv": ["systemctl", "list-timers", "--all", "--no-pager", "--plain"]}`
- `{"argv": ["systemctl", "is-active", "<service>"]}`

Do not use shell syntax, pipes, redirects, inline environment assignments, `sudo`, shell wrappers, network clients, remote-copy tools, absolute command paths, or project-specific commands in the portable checker. If a deployment needs a project-specific command, create a local derivative that hard-codes and documents that fixed argv template.

## 6. Run Manual Validation

Before scheduling, run:

```bash
python3 /absolute/path/openclaw_cron_health_check.py /absolute/path/config.json
```

Confirm:

- no placeholders appear in the report
- command probes are structured `argv` objects
- command probes match the fixed diagnostic allowlist
- run-parts scripts are not expanded into false cron entries
- missing scripts are reported as `CRITICAL`
- shell-complex commands are rejected or reported as `WARNING`, not executed
- long log lines are truncated
- secrets are redacted

## 7. Schedule

Do not create or update the scheduled job unless the user explicitly asks for that operational change. When authorized, create it as script-only/no-agent from the destination chat/topic when possible. Then list the job and verify name, schedule, next run, script path, delivery target, and no-agent/script-only mode.
