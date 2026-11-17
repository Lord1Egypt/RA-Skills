---
name: agent-timezone-lock
description: "Stops an OpenClaw agent from reporting the wrong time. Prevents the UTC-as-local mistake. Use when (1) the user reports a wrong time, (2) asks what time it is, (3) says 'set my timezone', or (4) agent output shows a time clearly off. Does NOT trigger on generic mentions of UTC, timezone, or heartbeats — only when time accuracy is explicitly at issue."
permissions:
  read:
    - USER.md
    - skills/timezone/tz_config.json
  write:
    - skills/timezone/tz_config.json
  write_conditional:
    - path: AGENTS.md
      condition: "Only when user explicitly runs timezone_setup.py --patch-agents and confirms"
  exec:
    - timedatectl
    - /etc/localtime (read-only)
---
# Timezone Enforcement Skill

Enforces correct local-time awareness. Prevents the classic UTC-as-local mistake.

## What This Skill Does
- Reads user timezone from USER.md (`Timezone:` field)
- Provides `now.py` script for accurate local time output
- Provides `timezone_setup.py` for one-time configuration
- **Optionally** patches AGENTS.md with standing timezone rules — ONLY when user explicitly runs `--patch-agents` and confirms. This is not default behavior.

⚠️ **User Warning:** Running `timezone_setup.py --patch-agents` will write standing instructions into AGENTS.md. This persists across sessions and affects all future agent behavior. Only do this if you want the timezone rule to apply permanently.

## What This Skill Does NOT Do
- Does NOT automatically intercept all time output — agent must call `now.py` explicitly
- Does NOT patch AGENTS.md without explicit `--patch-agents` flag
- Does NOT handle multi-user or multi-timezone environments
- Does NOT detect timezone changes after install — re-run `timezone_setup.py` if timezone changes

## Permissions Required
This skill may:
- **Read** USER.md (to detect timezone)
- **Read/write** `skills/timezone/tz_config.json` (to save config)
- **Optionally write** AGENTS.md (only when user explicitly approves `--patch-agents`)
- **Execute** `timedatectl` or read `/etc/localtime` (system timezone detection only)

## Prerequisites
USER.md should contain a timezone field:
```
Timezone: America/New_York
```
Use a valid IANA timezone string (e.g. `America/New_York`, `Europe/London`, `Asia/Tokyo`).
Aliases like ET, PT, CT are also accepted.

## Setup — Run Once on Install
```bash
python3 skills/timezone/scripts/timezone_setup.py
```
This detects timezone from USER.md or system, writes `tz_config.json`. Does NOT touch AGENTS.md unless user runs with `--patch-agents`.

To also patch AGENTS.md (optional, requires user confirmation):
```bash
python3 skills/timezone/scripts/timezone_setup.py --patch-agents
```

## Reporting Time
Always run `now.py` before reporting any time — never guess from internal knowledge:
```bash
python3 skills/timezone/scripts/now.py
```
Report output verbatim. If it fails: tell the user, ask them to run `timezone_setup.py` first.

## UTC Trap Detection
Before outputting any time, ask: is this UTC or local?
- Timestamps ending in `Z`, `+00:00`, or `+0000` → convert before reporting
- API/cron/system timestamps → treat as UTC, always convert
- User-provided times → treat as local, use as-is

## /timezone Command
When user types `/timezone`:
1. Show configured timezone and current local time (run `now.py`)
2. Offer to change
3. If changing: run `timezone_setup.py --set "<IANA_NAME>"`
4. Confirm change

---

*Custom implementations and questions: pods@agentmail.to*
