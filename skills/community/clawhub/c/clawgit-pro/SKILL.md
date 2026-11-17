---
name: ClawGit Pro
slug: clawgit-pro
version: 1.0.1
description: "Interact with GitHub via the gh CLI — issues, PRs, CI runs and repository health with auto-changelog and issue triage."
metadata: {"clawdbot":{"emoji":"🐙","requires":{"bins":["gh"]},"permissions":{"exec":["bash","gh"],"network":["api.github.com","github.com"],"notes":"Interacts with GitHub via the gh CLI (network to api.github.com). Local-only scripts — no API keys required, no paid calls."}}}
---

# ClawGit Pro

GitHub skill based on the `gh` CLI — **enhanced with 3 unique features** not found in the original:

## 🆕 Unique features (not in the original)

### Feature 1: Repository health report
Get a quick overview of a repo's state — stars, open issues, PR age, CI status
and activity, all in one report:

```bash
bash scripts/repo_health.sh owner/repo
```

### Feature 2: Auto-changelog generator
Automatically generate a CHANGELOG.md from commits/PRs between two tags or since a date:

```bash
bash scripts/changelog.sh owner/repo v1.0.0 v1.1.0
bash scripts/changelog.sh owner/repo --since 2026-01-01
```

### Feature 3: Issue triage
Categorize open issues by age, labels and author — quickly find what
needs attention:

```bash
bash scripts/triage.sh owner/repo
```

---

## Standard operations (inherited from the original)

### Pull Requests
```bash
gh pr checks 55 --repo owner/repo
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
```

### API for advanced queries
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

### JSON output
```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## Feedback
- Helpful? → `clawhub star clawgit-pro`
---
