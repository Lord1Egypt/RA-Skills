---
name: agent-timezone-lock
description: "Stops your OpenClaw agent from reporting the wrong time. Prevents the common UTC-as-local mistake that makes agents look broken. Install this if your agent has ever said the wrong time, confused UTC with local time, or if you want all times reported in your local timezone automatically. Triggers on: what time is it, wrong time, wrong timezone, UTC, local time, set my timezone, or any heartbeat where time accuracy matters."
---
# Timezone Enforcement Skill
Enforces correct local-time awareness for this agent. Prevents the classic UTC-as-local mistake.

## What This Skill Does
When installed, this skill:
1. Reads the user timezone from USER.md (Timezone: field)
2. Ensures timezone is applied when the agent calls now.py for time output
3. Provides /timezone command for users to check/set timezone
4. Validates that the agent never reports UTC time as local time
5. Patches AGENTS.md with standing timezone instructions

## Prerequisites — Required Before Install

USER.md must contain a timezone field in this exact format:
Timezone: America/New_York

Use a valid IANA timezone string. Examples:
- America/New_York
- America/Chicago
- America/Los_Angeles
- Europe/London
- Asia/Tokyo

Do NOT use abbreviations like EST, PST, or free-text like "New York time" — these will fail.

If USER.md does not exist or has no Timezone field, timezone_setup.py will prompt the user to enter one interactively.

Invalid timezone recovery:
- If the string fails IANA validation, halt and show: "Invalid timezone: [input]. Please provide a valid IANA string e.g. America/New_York"
- Do not default silently to UTC
- Do not proceed until a valid string is confirmed

## Startup - Run Once on Install
On first use, run:
    python3 /opt/openclaw/workspace/skills/timezone/scripts/timezone_setup.py

Note: timezone_setup.py requires an interactive shell. For headless or automated environments, pre-populate tz_config.json directly with the IANA string before first run.

This script detects timezone from USER.md, writes TZ_CONFIG to tz_config.json, and patches AGENTS.md.
Do not patch AGENTS.md manually until this script has run. It requires a valid tz_config.json first.

## Answering What Time Is It
Always run:
    python3 /opt/openclaw/workspace/skills/timezone/scripts/now.py

Report the output verbatim. Never guess time from internal knowledge.
If now.py fails: report the error, ask user to run timezone_setup.py first. Do not guess.
If USER.md has no Timezone field: run timezone_setup.py before proceeding. Do not default to UTC silently.

## Heartbeat Integration
On every heartbeat where time is mentioned:
1. Call now.py to get current local time
2. If any prior message contains a UTC time presented as local time, flag it
3. If drift over 30 minutes between what agent said and actual time, self-correct
If now.py fails during heartbeat: log the failure, skip time reporting, flag to user at next opportunity.

## UTC Trap Detection
If about to output a time, ask: Is this UTC or local?
- UTC ends in Z, +00:00, or +0000 — convert before reporting
- Timestamps with no timezone offset at all are ambiguous — treat as UTC and note the assumption to the user
- Times from APIs, cron, system are usually UTC - always convert
- Times in USER.md or user messages are usually local - use as-is

## /timezone Command
When user types /timezone:
1. Show current configured timezone and current local time
2. Offer to change
3. If changing: run timezone_setup.py with their input
4. Confirm the change
If tz_config.json does not exist: run timezone_setup.py first.

## Standing Rules - patch into AGENTS.md only after timezone_setup.py has run
- NEVER report UTC time as local time
- All time output must be in users local timezone
- When in doubt: run now.py before reporting any time
- API/cron/system timestamps are UTC - always convert before displaying
- If now.py fails: flag to user, do not guess

## What This Skill Does NOT Do

- Does NOT automatically intercept all time output — the agent must explicitly call now.py before reporting any time
- Does NOT self-correct without being triggered — heartbeat integration requires the agent framework to call now.py on schedule
- Does NOT validate timezone strings at runtime beyond what the system tz database supports
- Does NOT handle multi-user or multi-timezone environments — one timezone per agent instance
- Does NOT detect if USER.md has changed since install — if timezone changes, re-run timezone_setup.py manually to sync tz_config.json
