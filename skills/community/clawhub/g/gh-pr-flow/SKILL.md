---
name: gh-pr-manager
description: GitHub Pull Request lifecycle management — create, review, merge, changelog generation, CI checks, conflict resolution, and draft management via gh CLI. Use when Codex needs to manage PR workflows, check review status, generate changelogs from merged PRs, or automate the PR creation/review/merge cycle.
---

# GitHub PR Manager

## Overview

Streamline GitHub Pull Request workflows: create, review, merge, changelog generation, CI checks, and draft management via `gh` CLI. Use when Codex needs to manage PR lifecycle, check review status, handle merge conflicts, or generate changelogs.

## Quick Start

### Prerequisites
- `gh` CLI installed and authenticated (`gh auth status`)
- Git repository with remote on GitHub

### Check your PR overview
```bash
bash scripts/gh-pr-review.sh --mine
```

### Create a PR with auto-generated content
```bash
python3 scripts/gh-pr-create.py --draft --label review-needed
```

### Generate changelog from merged PRs
```bash
python3 scripts/gh-pr-changelog.py --from v1.0 --to v2.0
```

## Common Tasks

### Creating & managing PRs

```bash
# Create draft PR
gh pr create --draft --title "WIP: Add login" --body "In progress"

# Create PR with labels
gh pr create --label enhancement --label needs-review

# View PR details
gh pr view <number>         # view in terminal
gh pr view <number> --web   # open in browser

# Update PR
gh pr edit <number> --title "New title" --add-label ready
```

### Review workflow

```bash
# Check what needs my review
gh pr list --search "review-required:@me" --state open

# Approve
gh pr review <number> --approve --body "LGTM"

# Request changes
gh pr review <number> --request-changes --body "Please fix the tests"

# Add comment
gh pr review <number> --comment --body "Nice work!"

# Check review status on a PR
gh pr view <number> --json reviewDecision,reviews
```

### CI & merge

```bash
# Check CI status
gh pr checks <number>            # detailed status
gh pr view <number> --json statusCheckRollup

# Merge when checks pass
gh pr merge <number> --squash    # squash and merge
gh pr merge <number> --rebase    # rebase and merge
gh pr merge <number> --merge     # merge commit
gh pr merge <number> --auto      # auto-merge after checks pass

# Check mergeability
gh pr view <number> --json mergeable,mergeStateStatus
```

### Conflict resolution

```bash
# Check if PR has conflicts
gh pr view 42 --json mergeable
# → "CONFLICTING" if there are conflicts

# Fix locally
git checkout <pr-branch>
git fetch origin
git merge origin/main                # resolve conflicts
git push

# Alternative: rebase instead
git rebase origin/main               # resolve conflicts
git push --force-with-lease
```

### Working with branches

```bash
# Checkout a PR locally for testing
gh pr checkout <number>

# List your branches with PR status
gh pr list --author "@me" --json headRefName,title,state,isDraft

# Compare branches
gh pr diff <number>              # view diff
gh pr diff <number> --name-only  # just filenames
```

## Reference

- **`scripts/gh-pr-create.py`** — PR creation with auto-generated title/body from commits
- **`scripts/gh-pr-review.sh`** — Overview of pending reviews and CI status
- **`scripts/gh-pr-changelog.py`** — Generate changelog from merged PRs between releases
- See `references/pr-templates.md` for PR template examples
- See `references/label-conventions.md` for label conventions
