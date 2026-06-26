# Codex Multi-Account Rotation Guide

Use this guide when a user asks about running multiple Codex accounts/profiles, rotating profiles, or improving resilience when one profile fails usage checks.

## Scope and safety
- Only use legitimately authorized accounts.
- Do not automate bypasses of provider limits or anti-abuse controls.
- Prefer transparent failover and clear user messaging.

## Quick answer template (short mode)
Use this when the user asks casually:

"Yes — you can set up multiple Codex profiles and rotate between them. Add each account as its own `openai-codex:<name>` profile, keep one as `default`, and fail over on repeated 401/403/429 errors with cooldown before retrying. You don’t need Codex CLI just for usage checks. If usage endpoint auth is rejected (401), keep local profile health output and switch to another healthy profile."

## Setup pattern
1. Create distinct profile IDs:
   - `openai-codex:default`
   - `openai-codex:work`
   - `openai-codex:personal`
   - `openai-codex:backup`
2. Keep names stable and descriptive (owner/purpose).
3. Ensure each profile has valid OAuth material in `auth-profiles.json`.
4. Keep one primary default and at least one fallback.

## Rotation policy (recommended)
Use deterministic, debuggable rotation:

1. Try `default` first.
2. On profile error, classify and act:
   - `401 auth_not_accepted_by_usage_endpoint`: endpoint rejected token/session format. Mark profile degraded for this check path and fail over.
   - `403 forbidden_by_usage_endpoint`: likely permission/scope issue. Fail over.
   - `429` or rate-limit style failures: fail over + cooldown.
   - transport timeout/network: retry once, then fail over.
3. Cooldown degraded profile (e.g., 15-30 min for 401/403, shorter for transient network issues).
4. Re-test cooled-down profiles later before promoting back to default.

## Operational thresholds
- Retry count: 1
- Request timeout: 20-25s
- Failover trigger: 2 consecutive hard failures for the same profile
- Recovery trigger: 2 consecutive successful checks before promotion

## Suggested user-facing messages
### Healthy
"Usage check complete. Primary profile is healthy; fallback profiles available."

### Fallback activated
"Primary profile had repeated endpoint auth/rate-limit errors, so I switched to a fallback profile and continued."

### All degraded
"All configured Codex profiles are currently degraded for remote usage checks. I can still report local token/profile health while you refresh or rotate credentials."

## Safe cleanup / profile removal
Prefer detach-only first, then hard delete if requested.

- Detach only (safer):
```bash
python3 skills/codex-profiler/scripts/codex_usage.py --delete-profile openai-codex:work --confirm-delete
```

- Hard delete (permanent, with backup):
```bash
python3 skills/codex-profiler/scripts/codex_usage.py --delete-profile openai-codex:work --confirm-delete --hard-delete
```

## Deep-dive response template
Use when user asks "how do I set it up?":

1. "Create 2-4 Codex profiles (default + fallbacks) with clear names."
2. "Run usage check on `all` profiles to baseline health and recent failures."
3. "Route requests through `default`, fail over on repeated 401/403/429 or timeout failures."
4. "Apply cooldown before retrying failed profiles; auto-promote only after repeated success."
5. "Use detach-only delete first for bad profiles; hard-delete only when sure."
6. "No Codex CLI install is required for this usage-check flow."

## Troubleshooting notes
- `401` on `chatgpt.com/backend-api/wham/usage` can happen even with valid OAuth profile state.
- Treat `401` as endpoint auth incompatibility for that profile/session path, not immediate evidence that local profile storage is broken.
- Always avoid printing full callback URLs or tokens in chat output.
