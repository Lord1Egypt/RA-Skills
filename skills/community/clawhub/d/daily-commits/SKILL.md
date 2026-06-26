---
name: daily-commits
description: Summarize a person's git commits for a specific date, grouped by feature points, in English. Use when reviewing daily work output.
argument-hint: [date:YYYY.MM.DD] [author-name]
allowed-tools: Bash, Read
---

# Daily Commits Summary

Summarize all git commits by **$1** on **$0**, grouped by feature/functional area, in English.

## Steps

1. Run `git log` filtered by date and author:

```
git log --after="<start-of-day>" --before="<end-of-day>" --author="$1" --pretty=format:"%h %s" --no-merges
```

Convert the date `$0` (format: `YYYY.MM.DD`) to proper git date range:
- `--after` = the date at 00:00:00
- `--before` = the next day at 00:00:00

2. Also run `git log` with `--stat` to understand the scope of changes:

```
git log --after="<start-of-day>" --before="<end-of-day>" --author="$1" --stat --no-merges
```

3. Analyze all commits and group them by feature/functional area based on:
   - Commit message prefixes (feat, fix, refactor, docs, style, test, chore, etc.)
   - Related file paths and modules
   - Logical grouping of related changes

4. Output a clean summary in this format:

```
## Daily Commits Summary: <author> — <date>

### <Feature Area 1>
- <concise description of what was done> (`commit-hash`)
- ...

### <Feature Area 2>
- <concise description of what was done> (`commit-hash`)
- ...

**Total: X commits**
```

## Rules

- Output in **English** only
- Group by logical feature, not by commit type prefix
- Each bullet should be a concise human-readable description (not just the raw commit message)
- If a commit message already has a conventional prefix like `feat(meeting):`, use the scope as a hint for grouping
- Omit merge commits
- If no commits found, state that clearly
