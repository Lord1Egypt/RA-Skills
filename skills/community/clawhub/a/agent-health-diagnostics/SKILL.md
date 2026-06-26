---
name: agent-health-diagnostics
description: Diagnose and fix the 4 most common OpenClaw agent failures — heartbeat spam, API rate limit cascades, channel death loops, and memory/embedding errors. Battle-tested across a 6-agent multi-host deployment.
version: 1.0.0
tags:
  - diagnostics
  - monitoring
  - health
  - heartbeat
  - troubleshooting
  - multi-agent
  - ops
---

# Agent Health Diagnostics

**Scripts available in the [Collective Skills repo](https://github.com/Bobalouie44/collective-skills/tree/main/references)**

## Overview

When an OpenClaw agent misbehaves — spamming messages, going dark, burning API credits, or looping on dead channels — this skill provides the diagnostic playbook. Covers the 4 most common failure modes with exact commands to diagnose and fix each one.

Battle-tested across a 6-agent deployment spanning 3 hosts (Windows + Linux + Proxmox).

## When to Use This Skill

Use when you observe any of these symptoms:
- Agent sending repeated heartbeat/status messages to Telegram/Discord/etc.
- Agent goes silent despite gateway showing "active"
- Logs show `429 Too many tokens` or `rate_limit` errors
- Channel connection loops: `auto-restart attempt 1/10`, `2/10`, etc.
- Memory search errors: `input length exceeds context length`
- Gateway says "active" but agent doesn't respond to messages

## The 4 Failure Modes

### 1. Heartbeat Spam
**Symptom:** Agent sends repeated messages every N minutes.
**Root cause:** Heartbeat interval too low (10m = 144 messages/day) + verbose prompt that always generates output instead of HEARTBEAT_OK.
**Quick fix:**
```bash
# Check interval
grep -A5 heartbeat ~/.openclaw/openclaw.json

# Fix: set to 30m minimum, simplify prompt to checklist + HEARTBEAT_OK default
# Then restart gateway
openclaw gateway restart
```
**Prevention:** Never set heartbeat below 20 minutes. Heartbeat prompts should CHECK things, not CREATE things.

### 2. API Rate Limit Cascade
**Symptom:** All models fail, agent goes dark.
**Root cause:** Heartbeat + N crons = (N+1) API calls per interval. Exceeds provider TPM limit → all fallbacks exhausted simultaneously.
**Quick fix:**
```bash
# Check for rate limits
journalctl -u <service> --since '1h ago' | grep '429\|rate_limit'

# Count your crons (each burns tokens)
openclaw cron list

# Fix: reduce heartbeat to 30-60m, disable non-essential crons, stagger schedules
```
**Prevention:** Calculate token budget before adding crons. Each run ≈ 2K-10K tokens. Route heartbeats to cheap/local models.

### 3. Channel Death Loop
**Symptom:** Logs show repeated `auto-restart attempt N/10` for IRC/Discord/etc.
**Root cause:** Target server unreachable → health monitor restarts → fails again → loop. Each restart may trigger model calls, burning API tokens.
**Quick fix:**
```bash
# Check for loops
journalctl -u <service> --since '1h ago' | grep 'auto-restart\|timed out'

# Test connectivity
nc -zv <target-ip> <target-port> -w 5

# Fix: disable the broken channel in openclaw.json
# channels.<name>.enabled = false
openclaw gateway restart
```
**Prevention:** Test connectivity BEFORE enabling channels. Disable channels you can't reach.

### 4. Memory/Embedding Overflow
**Symptom:** `memory sync failed` or `input length exceeds context length` errors.
**Root cause:** File too large for embedding model's context window (mxbai-embed-large = 8K tokens).
**Quick fix:** Archive old sections of large files (MEMORY.md → memory/archive/). Keep active files under 8K tokens.
**Prevention:** Don't let MEMORY.md grow unbounded. Archive quarterly.

## Remote Diagnostic Quick Reference

| What | Command |
|------|---------|
| Service status | `systemctl is-active <service>` |
| Recent logs | `journalctl -u <service> --since '1h ago' --no-pager \| tail -40` |
| Live tail | `journalctl -u <service> -f` |
| Rate limits | `journalctl -u <service> --since '1h ago' \| grep '429'` |
| Cron list | `openclaw cron list` |
| Port test | `nc -zv <ip> <port> -w 5` |
| Config backup | `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak` |

## Golden Rules

1. **Always back up config before editing.** `cp openclaw.json openclaw.json.bak`
2. **Always restart gateway after config changes.** Hot reload doesn't catch everything.
3. **Check logs before guessing.** `journalctl` tells you what's wrong 90% of the time.
4. **Calculate your API budget.** Heartbeat freq × (crons + 1) × avg tokens = burn rate.
5. **Disable what you can't reach.** Dead channels create loops that waste resources.
6. **"Configured" ≠ "working."** Verify with actual output after every change.
