---
name: auto_authenticator_local
description: Use when the user wants a local-first TOTP helper for accounts they personally own or are explicitly authorized to access. This skill stores TOTP seeds in system-level secure credential stores, generates 6-digit codes only on explicit request, helps wire approved login flows, and explains safe local secret handling. Do not use it to bypass MFA policies, evade platform restrictions, hide OTP generation, or automate access without authorization.
---

# Auto Authenticator Local

Auto Authenticator Local is a privacy-first skill for generating TOTP codes on the user's machine.

## What this skill does

- Adds a TOTP seed to the operating system credential vault under a user-chosen alias.
- Generates the current 6-digit code for a single alias on explicit request.
- Deletes a stored alias when the user rotates or removes access.
- Helps the user integrate approved local login flows for accounts they own or are authorized to manage.

## Hard safety rules

- Refuse any request framed as bypassing MFA, avoiding rate limits, defeating anti-abuse systems, or "hiding" OTP generation from security controls.
- Do not store TOTP seeds in plaintext files, shell history, screenshots, prompts, git, or chat transcripts.
- Do not bulk-export secrets or dump all aliases.
- Do not generate codes silently in the background. Require an explicit alias each time.
- If the account ownership or authorization is unclear, pause and ask for confirmation before helping.

## Platform assumptions

- The bundled scripts are cross-platform through `keyring`, which maps to OS-native secure storage.
- macOS also has a built-in fallback through the `security` CLI.
- If the host machine does not have a working secure storage backend, help the user install one rather than falling back to plaintext.

## Files to use

- `scripts/totp_add.py`: store or update a TOTP seed in secure storage
- `scripts/totp_code.py`: generate the current 6-digit code for one alias
- `scripts/totp_delete.py`: delete an alias from secure storage
- `references/security.md`: storage and publication guidance

## Default workflow

1. Confirm the user owns the account or is authorized to manage it.
2. Ask for a short alias that does not leak unnecessary sensitive context.
3. Store the seed with:
   - `python3 scripts/totp_add.py --alias <alias> --issuer <issuer> --account <account>`
4. Generate a code only when explicitly requested:
   - `python3 scripts/totp_code.py --alias <alias>`
5. Remove the seed if the account is decommissioned or rotated:
   - `python3 scripts/totp_delete.py --alias <alias>`

## Response style

- Keep generated output minimal.
- Prefer returning only the code and its expiry when that is what the user asked for.
- When discussing storage or rollout, emphasize privacy, explicit invocation, and device-local handling.
- If the user asks about publishing, position the skill as a local privacy and convenience tool for legitimate access.

## Good deliverables

- A local setup guide
- A security checklist
- A migration plan from plaintext secrets to Keychain
- A small integration for approved local login steps

## Avoid

- Marketing copy about bypassing protections
- Stealth or hidden code generation
- Unauthorized access flows
- Secret export or exfiltration helpers
