# bookmark.sh Script Guide

## Overview

`scripts/bookmark.sh` is a helper script for managing the bookmark directory's git lifecycle. It handles directory initialization, git versioning, and GitHub remote synchronization.

## Commands

### `init` — Initialize Bookmark Directory

```bash
scripts/bookmark.sh init
```

Performs the following steps in order:

1. **Check environment**: Verify `$ARTICLE_BOOKMARK_DIR` is set, exit if not
2. **Create directory**: `mkdir -p $ARTICLE_BOOKMARK_DIR` if it doesn't exist
3. **Initialize git**: Run `git init` if no `.git` directory found; also creates `.gitignore` and `README.md`
4. **Configure remote** (if `$ARTICLE_BOOKMARK_GITHUB` is set):
   - Parse `$ARTICLE_BOOKMARK_GITHUB` to extract repo path and git URL
   - Add or update `origin` remote
5. **Sync from remote** (if remote repo exists):
   - `git fetch origin`
   - Detect `main` or `master` branch
   - `git pull --rebase` to sync latest changes

### `save` — Commit and Push Changes

```bash
scripts/bookmark.sh save "Add article: Some Title"
scripts/bookmark.sh save "Delete article: Old Article"
scripts/bookmark.sh save   # Default message: "Update bookmarks YYYY-MM-DD HH:MM"
```

Performs the following steps in order:

1. **Check environment**: Verify `$ARTICLE_BOOKMARK_DIR` is set and directory exists
2. **Check changes**: Skip if no modified `*.md` files (`git status --porcelain`)
3. **Stage files**: `git add *.md` and `.gitignore`
4. **Commit**: `git commit -m "<message>"`
5. **Push to remote** (if `$ARTICLE_BOOKMARK_GITHUB` is set):
   - If remote repo doesn't exist on GitHub, create it via `gh repo create` (private)
   - `git push` to origin (with `-u` on first push)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ARTICLE_BOOKMARK_DIR` | **Yes** | Absolute path to the bookmark storage directory |
| `ARTICLE_BOOKMARK_GITHUB` | No | GitHub repository identifier for remote sync |

### `ARTICLE_BOOKMARK_GITHUB` Supported Formats

All four formats are accepted and automatically parsed:

| Format | Example |
|--------|---------|
| `owner/repo` | `myuser/article-bookmarks` |
| SSH URL | `git@github.com:myuser/article-bookmarks.git` |
| HTTPS URL | `https://github.com/myuser/article-bookmarks` |
| HTTPS URL (with .git) | `https://github.com/myuser/article-bookmarks.git` |

Internally, all formats are normalized to SSH URL (`git@github.com:...`) for git operations, and `owner/repo` for `gh` CLI operations.

## External Dependencies

| Tool | Required | Purpose |
|------|----------|---------|
| `git` | **Yes** | Version control |
| `gh` | No | Auto-create GitHub repos, check remote existence |

If `gh` is not installed or not authenticated, the script gracefully skips remote operations that require it and logs a warning.

## Usage in Skill Workflow

### Adding an article

```
1. Run: scripts/bookmark.sh init
2. ... (fetch, summarize, tag, write files) ...
3. Run: scripts/bookmark.sh save "Add article: <title>"
```

### Deleting an article

```
1. Run: scripts/bookmark.sh init
2. ... (find, confirm, delete files, update index) ...
3. Run: scripts/bookmark.sh save "Delete article: <title>"
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| `$ARTICLE_BOOKMARK_DIR` not set | Exit with error |
| Directory or git not initialized on `save` | Exit with error, prompt to run `init` first |
| Invalid `$ARTICLE_BOOKMARK_GITHUB` format | Exit with error, show supported formats |
| `gh` not installed / not authenticated | Warn and skip remote create/check |
| `git pull` fails | Warn and continue with local state |
| No `.md` file changes on `save` | Log info and skip commit |
