---
name: clawhub-rate-limited-publisher
description: Queue and publish local skills to ClawHub with a strict 5-per-hour cap using the local clawhub CLI and host scheduler.
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🦀","os":["darwin","linux"],"requires":{"bins":["python3","clawhub"]},"homepage":"https://github.com/openclaw/clawhub"}}
---

# ClawHub Rate Limited Publisher

Use this skill when the user wants to publish one or more local skills to ClawHub without exceeding the platform's publish cap.

## What this skill does

This skill does **not** magically grant shell permissions. It provides a safe local queue + scheduler workflow around the user's own `clawhub` CLI.

Follow this procedure:

1. Verify the skill folder exists and contains `SKILL.md`.
2. Build or update a queue JSON file.
3. Ask the host to run the helper script from `{baseDir}/scripts/clawhub_rate_limited_uploader.py`.
4. Prefer a host scheduler such as cron or systemd timer so uploads happen automatically every 12 minutes.
5. Never exceed **5 publish attempts in any rolling 3600-second window**.
6. Log stdout/stderr for each attempt and mark queue items as `published` or `failed`.

## Required runtime conditions

- `clawhub` must already be installed and authenticated on the host.
- The host must allow command execution. In OpenClaw this usually means enabling runtime tools such as `bash`/`exec`, or running the Python script directly outside chat.
- New sessions may be required after changing skill/config state because eligible skills are snapshotted per session.

## Recommended invocation patterns

### One-off manual run

Run:

`python3 "{baseDir}/scripts/clawhub_rate_limited_uploader.py" --queue "/absolute/path/to/queue.json" --execute`

### Dry run

Run:

`python3 "{baseDir}/scripts/clawhub_rate_limited_uploader.py" --queue "/absolute/path/to/queue.json" --dry-run`

### Cron schedule

Run every 12 minutes using the example in `{baseDir}/resources/cron.example`.

## Queue file shape

See `{baseDir}/examples/queue.sample.json`.

Each item may contain:

- `path`: absolute path to one skill directory
- `command`: optional command template, default `clawhub publish "{path}"`

## Safety rules

- Use absolute paths.
- Do not use `curl|bash`, base64 piping, or hidden remote installers.
- Keep `command` limited to the local `clawhub publish "{path}"` pattern unless the user explicitly audits and accepts a custom command.
- Count failures toward the hourly cap to avoid hammering ClawHub when auth or validation is broken.
