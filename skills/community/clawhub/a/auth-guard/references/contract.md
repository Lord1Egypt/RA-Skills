# Keychain Contract (Auth Guard)

Use this contract across agents to prevent auth regressions.

## 1) Canonical Source

For each service, define exactly one retrieval order:
1. Environment variable (`<SERVICE>_API_KEY`)
2. Credentials file (`~/.config/<service>/credentials.json`)

Do not add alternate ad-hoc locations unless documented.

## 2) Canonical Execution Path

All protected endpoint calls must flow through a helper script.

- Good: `workspace/.pi/<service>-feed-check.sh`
- Bad: raw curl in heartbeat loops against protected endpoint

## 3) Startup Probe

Before recurring automation (heartbeats/cron), run auth probe:
- `AUTH_OK` → proceed
- `AUTH_MISSING` or `AUTH_FAIL_UNAUTHORIZED` → fallback path + concise note

## 4) Fallback Policy

Fallback behavior must be deterministic and documented.
Example:
- Try authenticated `/feed`
- On unauthorized/missing key, use public `/posts`
- Never spam alerts for unchanged unauth state

## 5) Logging Hygiene

Never print raw keys in logs, memory files, or messages.
Redact as `***SET***` / `***REDACTED***`.

## 6) Prompt/Policy Lock-in

Add short policy lines to HEARTBEAT.md / AGENTS.md that ban bypassing helper scripts.

## 7) Drift Control

When integration changes, update:
- helper script
- startup probe args
- heartbeat policy snippet
as one atomic change.
