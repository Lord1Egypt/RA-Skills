# Session Diagnosis Reference

Use this reference to inspect a high-context session before deciding whether recovery is needed. It is intentionally read-only.

## Inspect

1. Run `openclaw status` and identify the high-context session key.
2. Run `openclaw sessions --json` and match the key, token totals, context limit, and session identifier.
3. Confirm the session belongs to the expected agent and conversation before discussing any recovery.

## Recovery boundary

Do not run cleanup, reset, editing, or deletion commands from this skill. If a recovery is necessary, obtain explicit user approval, use the platform's currently documented recovery procedure, and preserve any material state required for investigation.
