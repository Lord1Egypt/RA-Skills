---
name: dr-session-cleaner
description: "Install an alert-only OpenClaw session sentinel that reports high context use without resetting or deleting sessions."
---

# DR Session Guard

Use this skill to install or run an alert-only session monitor. It detects high context use and notifies this agent's approved local operator. It never resets, cleans up, edits, or deletes a session.

## Procedure

1. Load the operator notification target from this agent's protected local manifest. Do not place a real user ID in this shared skill or a fleet-wide default.
2. Use the installer with an immutable Discord DM target, for example:
   ```bash
   ./scripts/install_guard.sh --target user:<operator-id> --interval 15 --threshold 0.8 --channel discord --state ~/.openclaw/session-guard/state.json --log ~/.openclaw/session-guard/guard.log --cooldown 60
   ```
   First use `--dry-run`; inspect the generated cron entry and confirm it contains only the intended local target and paths.
3. Verify one read-only scan with `python3 scripts/session_guard.py` using the same local manifest target. Confirm either a redacted alert receipt or `no sessions above threshold`.
4. On an alert, inspect the affected session with `openclaw status` and `openclaw sessions --json`. Start a new conversation when practical. Any cleanup, reset, or deletion is a separate recovery action that requires explicit user approval and its own safety review.

## Guardrails

- The installer accepts only a Discord immutable DM target (`user:<numeric-id>`), state/log files inside the dedicated `~/.openclaw/session-guard/` directory, and validated numeric settings.
- Keep the notification target and operational state local to the agent. Do not include target IDs in shared skill content, receipts, or logs.
- The monitor sends only its own agent-originated operational alert. It is not an engineer-requested relay.
- The monitor's receipt must not include session transcript content, credentials, or other secrets.

## Reference

Use [`references/manual-reset.md`](references/manual-reset.md) only for read-only diagnosis. It intentionally contains no reset, cleanup, or deletion command.
