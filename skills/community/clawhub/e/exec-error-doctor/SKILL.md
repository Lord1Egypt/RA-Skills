---
name: exec-error-doctor
description: Diagnose and mitigate exec-related command failures across tools (OpenClaw exec output, shell errors, GitHub CLI, ClawHub CLI, missing binaries, auth failures, JSON field mismatch, permission errors, timeouts, and transient platform states). Use when a command returns non-zero, signal kill, ENOENT, unknown JSON field, or similar execution failures and you need fast triage + concrete next fixes.
---

# Exec Error Doctor

Triage execution failures quickly, classify root cause, and apply targeted fixes instead of random retries.

## Quick workflow

1. Run triage on raw error text:
   - `scripts/exec_error_triage.sh <error_text_or_file>`
2. Apply the category fix from `references/error-taxonomy.md`.
3. Re-run with safer wrappers when relevant:
   - GitHub CLI search schema drift: `scripts/gh_search_repos_safe.sh`
   - ClawHub publish visibility lag: `scripts/clawhub_publish_safe.sh`
4. Confirm with one clean re-run and capture outcome.

## Standard commands

### Generic triage

```bash
bash scripts/exec_error_triage.sh "Unknown JSON field: nameWithOwner"
```

### Safe GitHub repo search (schema-aware)

```bash
bash scripts/gh_search_repos_safe.sh "safe-exec skill" 15
```

### Safe ClawHub publish (retry-aware inspect)

```bash
bash scripts/clawhub_publish_safe.sh ./my-skill my-skill "My Skill" 1.0.0 "Initial release"
```

## Rules

- Prefer classification before fixes.
- Treat `Skill not found` right after publish as potentially transient if publish already returned OK.
- For `gh search repos --json`, prefer `fullName` (not `nameWithOwner`).
- Distinguish transient errors (retry/backoff) from hard errors (auth, permission, invalid args).

## Resources

- `references/error-taxonomy.md`: category→fix map.
- `scripts/exec_error_triage.sh`: pattern-based classifier.
- `scripts/gh_search_repos_safe.sh`: resilient GitHub search wrapper.
- `scripts/clawhub_publish_safe.sh`: publish + retry verification wrapper.
