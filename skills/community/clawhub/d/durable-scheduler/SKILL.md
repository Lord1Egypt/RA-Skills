---
name: openclaw-scheduler
description: Use when the user needs durable, audited job scheduling beyond OpenClaw's built-in cron -- SQLite-backed scheduler with shell + agent steps, retries, approvals, and full run history. External service that calls the gateway over HTTP; survives gateway restarts.
---

# OpenClaw Scheduler

A durable orchestration runtime for OpenClaw agents and shell workflows. SQLite-backed, runs as a separate launchd service (`ai.openclaw.scheduler`), keeps full run history, and supports chains like `shell check -> agent diagnosis -> human approval -> remediation`.

**Source:** github.com/amittell/openclaw-scheduler -- MIT
**Service label:** ai.openclaw.scheduler (LaunchAgent or LaunchDaemon)
**Default location:** ~/.openclaw/scheduler/
**Runtime:** Node.js 22+ (ESM), SQLite via better-sqlite3, cron via croner

## When to use

Reach for openclaw-scheduler when one or more of these apply:

- Scheduled jobs need a real audit trail, not "it probably ran" buried in logs.
- Shell jobs must keep running when the gateway is unhealthy or restarting.
- Workflows have multiple steps that need retries, approvals, or escalation.
- Agent jobs need to stay isolated from the operator's personal chats.
- Built-in cron lacks the failure-handling or chaining you need.

If the user just wants one cron line that fires occasionally, built-in OpenClaw cron is enough. Don't suggest the scheduler.

## Install

```bash
npm install -g openclaw-scheduler
openclaw-scheduler init
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.scheduler.plist
openclaw-scheduler jobs list
```

The init step creates `~/.openclaw/scheduler/scheduler.db` and the launchd plist. `jobs list` confirms the service is talking to its DB.

## Define a job

```bash
openclaw-scheduler jobs add \
  --name "weekly digest" \
  --cron "0 9 * * 1" \
  --kind agent \
  --to "@channel-id" \
  --prompt "Summarize last week's incidents and post to #digest"
```

For shell jobs, swap `--kind agent --prompt ...` with `--kind shell --command ...`.

## Multi-step workflows

Workflows chain steps with explicit retries and approvals:

```bash
openclaw-scheduler workflows add disk-watcher \
  --step shell:check --command 'df -h | awk "$5+0>85"' \
  --on-output --step agent:diagnose --to "@ops" \
    --prompt "Investigate the failing disk and propose a fix" \
  --then --step approval --approver "@alex" --timeout 30m \
  --on-approve --step shell:remediate --command 'sudo /opt/sbin/cleanup-tmp.sh'
```

Each step persists state, retries on failure, and surfaces the run in `jobs runs`.

## Gateway interaction

Agent jobs require the gateway to be reachable. The dispatcher calls `waitForGateway(timeoutMs, intervalMs)` before delivering; jobs queue up if the gateway is restarting and fire when it's ready again. Shell jobs run independently of gateway health.

## Operator commands

- `openclaw-scheduler jobs list` -- running, scheduled, paused
- `openclaw-scheduler jobs runs <id>` -- full run history with stdout/stderr
- `openclaw-scheduler jobs approve <id>` / `reject <id>` -- for approval steps
- `openclaw-scheduler jobs pause/unpause <id>` -- disable without deleting
- `openclaw-scheduler workflows list` -- multi-step workflow status

## Boundary

This tool replaces OpenClaw's built-in cron/heartbeat for hosts that need durability. It is not bundled with OpenClaw and not loaded as a plugin. The two can coexist (built-in cron handles agent heartbeats, openclaw-scheduler handles operator workflows), or operators can disable built-in cron and route everything through the scheduler.

## Known gaps

- macOS first-class; Linux works; Windows requires WSL2.
- No native gateway-side UI yet; runs are read via the CLI.
- See github.com/amittell/openclaw-scheduler/issues for open work.
