# Plan A Architecture

## Purpose
Daily management/employee reporting based on Google Sheets.

## Inputs
- Google Sheets staff tab
- Google Sheets special-events tab

## Outputs
- Telegram management group or Discord test channel

## Rules
- Daily run at 7:00 AM local time
- Birthday comparison uses day/month, not birth year
- Special events use full date and optional remind-before setting
- Avoid duplicate sends on the same day

## Current implementation assets in workspace
- `plan-a-demo.js`
- `run-plan-a.sh`
- `com.flexclaw.plan-a.plist`
- `PLAN_A_TEST.md`
- `PLAN_A_DEMO_USAGE.md`

## Migration note
Abstract hardcoded paths into env variables when porting to a different machine.
