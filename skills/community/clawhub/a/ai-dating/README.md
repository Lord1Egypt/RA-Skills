# ai-dating

`ai-dating` is a Codex skill for dating and matchmaking workflows.
It uses direct HTTP API calls with `curl` instead of `dating-cli`.

## What Changed

This version is built around the dating backend API:

- authenticate with `/register` and `/login`
- update profile with `PUT /member-profile`
- upload photos with `POST /minio/upload`
- create or update match tasks with `/match-tasks`
- check candidates with `GET /match-tasks/{taskId}/check`
- reveal contact details with `/match-results/{matchId}/reveal-contact`
- submit reviews with `/match-results/{matchId}/reviews`

The skill no longer depends on local CLI installation or local CLI config files.

## External Backend And Privacy Review

This skill sends user data to an external dating backend.

- Default base URL: `https://api.aidating.top` unless `AIDATING_BASE_URL` overrides it
- Expected tools: `curl`, and preferably `jq`
- Expected capability: outbound network access

Review the endpoint owner, privacy policy, retention policy, and internal approval requirements before installing or using the skill.
Do not use it where policy forbids sending photos, profile traits, or contact details to third-party services.

Use data minimization:

- only send fields needed for the current action
- do not upload photos without explicit user consent
- do not reveal contact details without explicit user selection and consent
- avoid sending highly sensitive identifiers or unrelated secrets

## Files

- `SKILL.md`: agent-facing workflow and guardrails
- `references/curl-api-operations.md`: verified request shapes and `curl` examples
- `LICENSE`: skill license

## Intended Use

Use this skill when a user wants to:

- make friends
- find a partner
- run matchmaking
- update a dating profile
- upload profile photos
- create or update match criteria
- inspect candidates
- reveal contact details
- submit a review after communication

## Quick Start

such as `bash`, `sh`, `zsh`, Git Bash, or WSL:

```bash
BASE_URL="${AIDATING_BASE_URL%/}"
if [ -z "$BASE_URL" ]; then
  BASE_URL="https://api.aidating.top"
fi
```

Typical workflow:

1. Register or log in.
2. Save `token`, `tokenHead`, `taskId`, and `matchId` from responses.
3. Update profile and upload photos.
4. Create or update a match task.
5. Poll `/match-tasks/{taskId}/check?page=1`.
6. Pick the best candidate.
7. Reveal contact details only after the user chooses a candidate.
8. Submit a review after communication if needed.

## Important Notes

- The current public polling endpoint is `GET /match-tasks/{taskId}/check`.
- Several write endpoints return success-only envelopes with `data = null`.
- There is no public list-tasks endpoint, so created `taskId` values must be preserved.
- `preferredContactChannel` is accepted by the DTO but is not currently used by matching logic.
- The skill should tell the user which external base URL will receive their data before the first write request when that is not already clear.

## Validation And Packaging

This repository includes helper scripts under `.codex/skills/skill-creator/scripts`.

Validate with Python 3:

```bash
python .codex/skills/skill-creator/scripts/quick_validate.py .codex/skills/ai-dating
```

Package with Python 3:

```bash
python .codex/skills/skill-creator/scripts/package_skill.py .codex/skills/ai-dating dist
```

The packaged artifact is written to:

```text
dist/ai-dating.skill
```

## Reference

For endpoint details and request examples, read:

- `SKILL.md`
- `references/curl-api-operations.md`
