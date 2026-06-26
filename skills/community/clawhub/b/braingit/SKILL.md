---
name: braingit
description: Markdown-only git snapshot commits (stage+commit *.md only). Article: https://github.com/gleb-urvanov/braingit/blob/master/braingit-article.md
---

# Braingit

Commit Markdown-only deltas in a git repository (typically a notes/workspace repo) using a deterministic script.

Article: https://github.com/gleb-urvanov/braingit/blob/master/braingit-article.md

## Quick start

### Commit Markdown changes (default: `*.md`)
From inside the target git repo:

```bash
./scripts/commit_md_changes.sh "md: snapshot"
```

Or specify a repo path:

```bash
BRAINGIT_REPO=/path/to/repo ./scripts/commit_md_changes.sh "md: snapshot"
```

### Change what files are included

```bash
BRAINGIT_PATTERN='*.md' ./scripts/commit_md_changes.sh
```

## Behavior
- Reads `git status --porcelain -z`
- Stages **only** matching files (default `*.md`)
- Commits only if something is staged
- Exits `0` when there is nothing to do

## Scripts
- `scripts/commit_md_changes.sh`
  - Env:
    - `BRAINGIT_REPO` (default: cwd)
    - `BRAINGIT_PATTERN` (default: `*.md`)
    - `BRAINGIT_DRY_RUN=1`

## References
- `references/protocol.md` — conventions + an OpenClaw cron example
