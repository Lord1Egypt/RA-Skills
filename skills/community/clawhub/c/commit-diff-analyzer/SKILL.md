---
name: commit-diff-analyzer
description: Analyzes code changes between two git commits. Use when user provides two commit IDs and wants to understand what changed between them, including file modifications, additions, deletions, and commit context.
---

# Commit Diff Analyzer

## Usage Pattern

When user provides two commit IDs (in any order or format), analyze the changes between them:

1. **Validate commits exist**: Run `git cat-file -t <commit>` for each commit ID
2. **Get commit info**: Run `git log -1 --format=fuller <commit>` for both commits
3. **Show diff**: Run `git diff <older-commit>..<newer-commit>` (chronological order)
4. **Show stats**: Run `git diff --stat <older-commit>..<newer-commit>`

## Output Organization

Present the analysis with:

1. **Commit metadata** - Author, date, commit message for both commits
2. **Change summary** - Files changed, insertions, deletions
3. **Detailed diff** - Line-by-line changes with context
4. **File breakdown** - Group by: Modified, Added, Deleted files

## Key Commands

```bash
# Validate commits exist
git cat-file -t <commit-id>

# Get full commit info
git log -1 --format="Hash: %H%nAuthor: %an%nDate: %ad%nMessage: %s%n" <commit-id>

# Chronological diff (older..newer)
git diff <older-commit>..<newer-commit>

# Diff stat
git diff --stat <older-commit>..<newer-commit>

# Show files changed
git diff --name-only <older-commit>..<newer-commit>
```

## Handling Edge Cases

- **Invalid commit IDs**: Report error and suggest running `git log` to see recent commits
- **Same commit**: Notify user both IDs point to the same commit
- **Non-git directory**: Error - skill only works in git repositories
- **Reverse order**: Detect which commit is older and adjust command accordingly

## Commit ID Formats

Accept various formats:
- Full SHA: `abc123def456...`
- Short SHA: `abc123d` (at least 7 chars)
- Branch names (if they point to commits)
- HEAD references like `HEAD~5`

## Example Output Structure

```
=== Commit A ===
Hash: abc123...
Author: John Doe
Date: 2024-01-15 10:30:00
Message: feat: add user login

=== Commit B ===
Hash: def456...
Author: Jane Smith
Date: 2024-01-20 14:45:00
Message: fix: resolve auth bug

=== Changes Summary ===
5 files changed, 120 insertions(+), 35 deletions(-)

=== File Breakdown ===
Modified: src/auth.js, src/login.html
Added: src/auth-utils.ts
Deleted: src/old-auth.php

=== Diff ===
... (detailed diff output)
```
