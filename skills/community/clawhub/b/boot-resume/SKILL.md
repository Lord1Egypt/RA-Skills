---
name: boot-resume
description: |
  Zero-cooperation session recovery after gateway restart. No checkpoints, no hooks, no agent involvement — just reads the evidence and picks up where it left off. Use when: the gateway was killed mid-task (SIGTERM, OOM, SIGKILL, crash), sessions were interrupted mid-turn with tool calls in progress, the agent stopped responding after a restart, a user reports the agent went silent after a crash, you need to manually check whether any sessions need recovery, or you want automatic resume without writing any checkpoint logic.
version: 1.1.0
homepage: https://github.com/Belugary/boot-resume
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "⚡"
    category: ops
    tags:
      - restart
      - recovery
      - session
      - resilience
      - resume
      - crash
      - gateway
    requires:
      bins:
        - python3
        - openclaw
    files:
      - install.sh
      - scripts/boot-resume-check.sh
      - templates/boot-resume.conf
      - templates/boot-resume-wake.service
---

# Boot Resume

Zero-cooperation session recovery after gateway restart. No checkpoints, no hooks, no agent involvement — just reads the evidence and picks up where it left off.

## Problem

When the gateway restarts, any in-flight agent turn dies mid-execution. Session history is preserved on disk, but the agent doesn't know it needs to continue. Users must manually tell each interrupted session to resume.

Checkpoint-based approaches require the agent to save state _before_ dying. Unexpected kills (SIGKILL, OOM, power loss) bypass this entirely.

## Solution

A deterministic shell script runs on every gateway start via systemd `ExecStartPost`. No LLM in the detection loop.

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  Scan   │ ──▶ │  Detect  │ ──▶ │  Resume  │
│sessions │     │  JSONL   │     │ cron add │
│ .json   │     │  tail    │     │--sys-evt │
└─────────┘     └──────────┘     └──────────┘
```

1. **Scan** — finds sessions updated within the last 20 minutes
2. **Detect** — reads the last 5 JSONL lines to classify session state
3. **Resume** — schedules a one-shot `openclaw cron add --system-event --wake now` to inject a continuation prompt

Key insight: the JSONL session files already contain all the evidence needed to detect an interruption — no pre-save required.

## Detection Rules

| Last JSONL Entry | Status | Meaning |
|---|---|---|
| `toolResult` | `INTERRUPTED` | Tool returned, agent never processed it |
| `assistant` (empty text) | `INTERRUPTED` | Tool call dispatched, killed before response |
| `user` (non-trivial) | `INTERRUPTED` | Message received, never processed |
| `assistant` (with text) | `COMPLETE` | Session ended normally — skip |
| `user` (trivial: "ok", emoji) | `TRIVIAL` | No meaningful request pending — skip |

## Install

### One command

```bash
bash {baseDir}/install.sh
```

Deploys three components:
- `boot-resume-check.sh` → `~/.openclaw/workspace/scripts/`
- `boot-resume.conf` → systemd drop-in (triggers script on every gateway start)
- `boot-resume-wake.service` → systemd user service (triggers script on system wake from sleep/suspend)

### Manual

```bash
cp {baseDir}/scripts/boot-resume-check.sh ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/boot-resume-check.sh

mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cp {baseDir}/templates/boot-resume.conf ~/.config/systemd/user/openclaw-gateway.service.d/
cp {baseDir}/templates/boot-resume-wake.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable boot-resume-wake.service
```

## Verify

```bash
systemctl --user restart openclaw-gateway
sleep 20
cat /tmp/openclaw/boot-resume.log
```

Expected output:
```
[boot-resume] now=... cut=... (20min window)
[boot-resume] scanning agent: main
[boot-resume] candidates: 0 (agent=main)
[boot-resume] done
```

## Test

1. Send a message that triggers a multi-step task (web search, code analysis, etc.)
2. Wait for the agent to start processing (tool calls in flight)
3. `systemctl --user restart openclaw-gateway`
4. Agent resumes automatically within ~35 seconds

## Slash Command

When invoked as `/boot-resume`, run the script with `--no-wait` to skip the startup delay:

```bash
bash {baseDir}/scripts/boot-resume-check.sh --no-wait
```

Report results to the user: which sessions were resumed, or that none were found.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WINDOW_MINUTES` | `20` | How far back to scan for interrupted sessions |
| `DELAY` | `20s` | Delay before injecting the resume event |

Edit at the top of `scripts/boot-resume-check.sh`.

## Features

- **Dual trigger** — covers both gateway restart (ExecStartPost) and system sleep/wake (systemd sleep.target)
- **Multi-agent support** — scans all agents under `~/.openclaw/agents/`, not just `main`
- **Smart filtering** — skips system, heartbeat, cron, and subagent sessions automatically
- **Deduplication** — respects `restart-resume.json` to avoid double-resuming planned restarts
- **Log rotation** — auto-truncates log at 1000 lines
- **Error visibility** — Python and cron errors are logged, not swallowed
- **Unique job names** — timestamp-based to prevent conflicts on rapid restarts

## Comparison

| Approach | Pre-save required | Survives SIGKILL | LLM-free |
|---|---|---|---|
| Checkpoint / snapshot files | Yes | No | No |
| Pre-restart state dump | Yes | No | No |
| Session history replay | Yes | Partial | No |
| **Post-hoc JSONL detection (this skill)** | **No** | **Yes** | **Yes** |

## Logs

Output: `/tmp/openclaw/boot-resume.log`

Each run logs: timestamp, scan window, candidate count, per-session status, and whether a resume job was armed.

## Limitations

- 20-minute scan window (configurable) — sessions idle longer than this are not resumed
- Resume prompt is generic — the agent relies on session context for continuity
- Telegram/Discord message queues already handle unprocessed incoming messages — this skill targets mid-execution interruptions
- Requires systemd (Linux); macOS users need manual launchd setup

## Uninstall

```bash
rm ~/.config/systemd/user/openclaw-gateway.service.d/boot-resume.conf
systemctl --user disable boot-resume-wake.service 2>/dev/null
rm ~/.config/systemd/user/boot-resume-wake.service
systemctl --user daemon-reload
rm ~/.openclaw/workspace/scripts/boot-resume-check.sh
rm -rf ~/.openclaw/workspace/skills/boot-resume
```
