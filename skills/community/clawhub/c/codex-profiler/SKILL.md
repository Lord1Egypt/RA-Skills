---
name: codex-profiler
description: Maintained Codex operations skill: unified /codex_usage + /codex_auth path. Standalone codex-usage/codex-auth are deprecated.
---

> ✅ **Maintained path:** use `codex-profiler` for all Codex profile operations.
> Standalone `codex-usage` and `codex-auth` skills are deprecated.

This skill consolidates both scripts:
- `scripts/codex_usage.py` (usage/limits)
- `scripts/codex_auth.py` (OAuth helper for start/status)

For auth/profile mutation, this skill now standardizes on gateway-native `openclaw models auth ...` commands.

## Safe defaults
- Usage checks are read-only by default.
- Auth state is runtime-managed; one-shot direct file edits are unreliable and can be overwritten by in-memory/cooldown state.
- Treat `auth-profiles.json` as gateway-managed state. Never mutate it directly in normal operations.
- Prefer gateway-native auth mutation commands (`openclaw models auth ...`, `openclaw models auth order ...`) over script-level file writes.
- Use dry-run/read-only preflight first, then apply, then verify (strict anti-drift flow below).
- See `RISK.md` for allowed/denied operation boundaries.

## Commands
### Usage
- `/codex_usage` → selector (default / all / discovered profiles)
- `/codex_usage <profile>`

### Auth
- `/codex_auth` → selector (profiles)
- `/codex_auth <profile>`
- `/codex_auth finish <profile> <callback_url>` (helper only; profile/order mutation must use gateway-native commands)

## UX requirements (cross-channel)
For `/codex_usage`, send immediate progress message first as a separate message:
- "Running Codex usage checks now…"

Delivery rule:
- If progress is sent through channel message tool path, send final result through the same path (same target/session), then return `NO_REPLY`.
- Avoid mixed delivery (tool progress + plain reply final).

For auth/profile/order mutation, warn that writes are gateway-managed and enforce verify-after-apply:
- "I will apply this via `openclaw models auth ...` and then verify with `models status` + `auth order get`."
- "I won’t hand-edit auth files directly because runtime state can drift/overwrite one-shot edits."

### Interaction adapter
- If inline buttons are supported: use selector buttons.
- If inline buttons are not supported: use text fallback prompts.
- Apply duplicate-request suppression per user for ~20s.
- Never echo full callback URLs in responses.

## Profile removal policy (MANDATORY)
1. **Best method (default): operational retire, not hard delete**
   - Remove the target profile from active provider order (`openclaw models auth order set ...`) so it is never selected.
   - Keep profile data intact unless the user explicitly requests permanent deletion.
2. **Hard delete only on explicit user instruction**
   - Perform permanent profile deletion only when the user clearly asks to hard delete/remove permanently.
   - If gateway-native delete is unavailable in the installed OpenClaw version, do not improvise risky live edits; use a controlled maintenance window flow.

## Strict anti-drift auth mutation flow (MANDATORY)
For auth/profile/order changes, use this exact 3-step flow:

1) **Preflight (read-only)**
```bash
openclaw models status --json
openclaw models auth order get --provider openai-codex --agent <agent-id>
```

2) **Apply (gateway-native command)**
```bash
openclaw models auth order set --provider openai-codex --agent <agent-id> <profile1> <profile2>
# or
openclaw models auth order clear --provider openai-codex --agent <agent-id>
# or provider login flow
openclaw models auth login --provider openai-codex
```

3) **Verify (post-apply, no assumptions)**
```bash
openclaw models status --json
openclaw models auth order get --provider openai-codex --agent <agent-id>
```

Never skip verification. If results mismatch expectation, do not hand-edit files; diagnose and re-apply via gateway-native commands.

## How to run
```bash
# Usage checks (read-only)
python3 skills/codex-profiler/scripts/codex_usage.py --profile all --timeout-sec 25 --retries 1 --debug
python3 skills/codex-profiler/scripts/codex_usage.py --profile all --format text

# OAuth helper (callback parsing/status only)
python3 skills/codex-profiler/scripts/codex_auth.py start --profile default
python3 skills/codex-profiler/scripts/codex_auth.py status
```

## Safety posture
- No remote shell execution (`curl|bash`, `wget|sh`) is allowed by this skill.
- No `sudo`/SSH/system-level host mutation commands are part of this skill path.
- Usage checks are restricted to trusted HTTPS endpoint host allowlist (`chatgpt.com`).
- Callback URLs and token material must be treated as sensitive and never echoed in full.

## Multi-account rotation guidance
When asked about running multiple Codex accounts/profiles, rotation policy, or fallback strategy, read:
- `references/multi-account-rotation.md`

Use the short template for quick chat answers and the deep-dive template for setup/troubleshooting requests.

## Notes
- Uses auth profiles at `~/.openclaw/agents/main/agent/auth-profiles.json` by default.
- Current source of truth is `auth-profiles.json`; `auth.json` is legacy compatibility and should not be used as primary state.
- If profile routing behaves unexpectedly, check for mixed state (missing/stale `auth-profiles.json`, leftover legacy files, or stale runtime cooldown) before assuming model fallback bugs.
- Same `accountId` across two profile labels is not automatically a defect. In this environment, multiple labels can map to the same workspace/account identity while still operating correctly. Treat it as healthy when both profiles are auth-valid and usable in `/codex_usage`; investigate only when auth failures or routing failures appear.
- Codex usage endpoint: `https://chatgpt.com/backend-api/wham/usage`.
- Usage script now surfaces `401` as `auth_not_accepted_by_usage_endpoint` with a clear hint, while still returning local profile health.
- Usage output now includes top-level `summary`, `formatted_profiles`, and `suggested_user_message` for cleaner slash-command formatting.
- Preferred strict output format for `/codex_usage` (single line per profile):
  - `🟢 \`%profile%\` — 5h **%5h_left%** | week **%week_left%** | r5 **%5h_reset%** | rw **%week_reset%**`
  - Use `🟠` when limited and `🔴` when unusable/auth-invalid.
  - No preface, no table, no trailing summary unless explicitly requested.
- OAuth flow: OpenAI auth endpoints + localhost callback on port 1455.
- Preferred mutation path is gateway-native (`openclaw models auth ...` / `openclaw models auth order ...`) with mandatory preflight + verify.
- `codex_auth.py status --profile <profile>` remains useful for per-profile helper status checks.
- Keep temporary payload/token artifacts only until verification succeeds, then clean them up.
- Codex CLI installation is not required for usage endpoint reads in this skill path.
