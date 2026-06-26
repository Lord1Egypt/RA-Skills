---
name: ci-failure-fixer
description: Monitor GitHub Actions CI pipelines for failures and automatically fix common issues. Use when asked to watch CI, fix build failures, monitor GitHub Actions, set up CI auto-repair, or diagnose failed builds. Detects failures via `gh` CLI, reads build logs, matches against known fix patterns (dependency issues, snapshot mismatches, lint errors, E2E failures), applies fixes automatically, and reports unfixable issues with diagnosis. Works as a cron job or on-demand. Requires `gh` CLI authenticated with GitHub.
---

# CI Failure Fixer

Monitor GitHub Actions for failures. Auto-fix what's fixable, report what's not.

## How It Works

1. `scripts/check-ci-failures.sh` polls repos for new failed runs
2. If failures found → read build logs via `gh run view --log`
3. Match error against known patterns → auto-fix if safe
4. Push fix → wait 90s → verify build passes
5. Report results (fixed or diagnosis-only)

## Quick Start

### On-demand
```bash
bash scripts/check-ci-failures.sh
```

Output: `OK` (no failures) or `FAILURES` with details.

### As Cron Job (OpenClaw)

Set up a cron that runs every 30 minutes:
- **Script:** `bash scripts/check-ci-failures.sh`
- **Model:** Haiku (cheap, sufficient)
- **On failure:** Read logs, attempt auto-fix, report

## Configuration

Environment variables:
- `GITHUB_OWNER` — GitHub username (auto-detected from `gh` if not set)
- `CI_REPOS` — Space-separated repo names (auto-discovers all repos if not set)
- `CI_STATE_FILE` — Path to state JSON (tracks last check time)

## Auto-Fixable Patterns

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Dependency issues | `npm ERR! Could not resolve` | `npm install` + push |
| Test snapshots | `Snapshot mismatch` | `npm test -- --update` + push |
| Lint errors | `eslint`, `Formatting` | `eslint --fix` + push |
| E2E snapshots | Playwright snapshot diff | `playwright --update-snapshots` + push |

## Report-Only (Human Needed)

- Token/auth errors (secrets rotation)
- TypeScript errors (complex type issues)
- Build timeouts (resource/loop issues)
- Unknown errors

## Fix Patterns Reference

Read `references/fix-patterns.md` for detailed decision tree, log reading commands, and all known patterns with fix scripts.

## Reading Logs

```bash
# Latest failed run logs
gh run view --repo OWNER/REPO --log 2>&1 | tail -50

# Filter for errors
gh run view <run-id> --repo OWNER/REPO --log 2>&1 | grep -A5 "error\|FAIL"
```

## After Fixing

Always verify the fix worked:
```bash
sleep 90  # Wait for new CI run
gh run list --repo OWNER/REPO --limit 1 --json conclusion -q '.[0].conclusion'
# Should be "success"
```
