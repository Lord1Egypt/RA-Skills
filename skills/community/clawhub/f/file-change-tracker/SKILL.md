---
name: file-change-tracker
description: Mandatory before the first file-changing action in a new edit batch. Use before creating, editing, overwriting, patching, renaming, moving, deleting, or generating files. Run PRE once at batch start with the explicit target paths, then run POST when the batch is complete. Do not use for read-only inspection, search, grep, diff-only review, or explanation-only tasks.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["git"],"anyBins":["bash","sh"]},"emoji":"🛟"}}
---

# File Change Tracker

Mandatory before the first file-changing action in a new edit batch.

This is a safety skill.
If the task will create a file, create a script, create a README, edit content, overwrite a file, apply a patch, rename or move files, delete files, change config, update docs, refactor code, or run a command that generates files, stop first, decide the target paths, and run `pre` before making any file change.
Mandatory not to make any file change first and try to protect it later.
Mandatory not to skip this skill just because the task looks small, easy, or easy to recreate.
Mandatory not to run `pre` before every incremental change inside the same batch.
Mandatory to run `pre` once at batch start, then perform the file changes, then run `post` when the batch is complete.

## Trigger rule

Use this skill as soon as the plan includes any file-changing action.
The trigger is the planned file change, not the implementation mechanism.
Do not wait for a git-specific task, a large task, or a risky task.
If any file will be created, edited, overwritten, patched, renamed, moved, deleted, or generated, this skill applies.

## Do not use it for

Do not use it for read-only inspection, explanation-only tasks, search, grep, listing files, or diff-only review.

## What this skill does

This skill adds a lightweight local protection layer around file changes.
The current helper implementation uses local git to record recovery points, scope checks to explicit paths, and provide rollback guidance.

Before the first file-changing action, it creates or records a recovery point for the explicit target paths of the task.
After the task finishes, it records the result when needed, shows recent commits, and tells the user that rollback is available.
Each `pre` call opens a distinct file change session under `.git/.guarded-edit/sessions/`, so overlapping edit batches do not overwrite each other's state.

## When to use it

Mandatory for tasks such as:

- editing existing files
- creating new files such as a script, helper, config file, README, doc, or prompt
- deleting, renaming, or moving files
- refactoring across a known file set
- changing configuration files
- applying patches to known paths
- running shell commands that mutate a known file set
- generating code or other files into known paths

Do not use it for read-only inspection, explanation-only tasks, search, grep, or diff-only review.

## Scope rule

This version is path-explicit.

Before the first file-changing action, gather the files or directories that are expected to change and pass them to `pre`.
If the target paths are not fixed yet, decide them first, then run `pre` before any `write`, `apply_patch`, overwrite, rename, move, delete, or file-creating shell command.
The helper will then scope its status checks, staging, and commits to those target paths instead of the whole workspace.

If the target path set grows later, Mandatory not to keep editing silently.
Run a new `pre` with the expanded path list before touching those newly added paths.

## Mandatory exclusion rule

File Change Tracker uses a dedicated gitignore-style exclusion file instead of embedding default patterns in `SKILL.md`.

The active exclusion file is always:

1. `{baseDir}/guarded-edit.ignore`

Mandatory not to include target paths that match the active exclusion rules.
Any path that does not match the active exclusion rules may be included in the file change scope, subject to explicit task intent.

This lets the user control ignored paths by editing a single file that lives next to `SKILL.md`, instead of editing the skill text itself.

## Index safety rule

This helper is intentionally conservative about the index.

If the declared target paths already contain staged changes, `pre` and `post` must fail instead of trying to restage those paths.
This avoids flattening hunk-level staging or otherwise rewriting the user's existing staged state for the guarded files.
Resolve, commit, or stash those staged changes first, then start a clean file change batch on those target paths.

## Required workflow

### 1. Before the first file-changing action

Run:

```bash
{baseDir}/scripts/helper.sh pre "<short reason>" -- <path> [<path> ...]
```

Examples:

```bash
{baseDir}/scripts/helper.sh pre "fix login validation" -- src/auth/login.ts src/auth/schema.ts
{baseDir}/scripts/helper.sh pre "create news script and docs" -- scripts/news_hotspot.py scripts/README.md
{baseDir}/scripts/helper.sh pre "update skill metadata" -- SKILL.md README.md README.user.md
{baseDir}/scripts/helper.sh pre "regenerate parser output" -- src/parser generated/
```

### 2. Perform the changes

Change only the declared target paths for this file change batch.

### 3. Validate if needed

Run tests, linters, type checks, or a focused sanity check when the task warrants it.

### 4. After the changes finish

Run:

```bash
{baseDir}/scripts/helper.sh post "<short reason>"
{baseDir}/scripts/helper.sh report 5
{baseDir}/scripts/helper.sh rollback-help
```

If another file change batch was started before this one finished, select the intended session explicitly.
When multiple open sessions exist, `post` and `rollback-help` fail instead of guessing.

```bash
{baseDir}/scripts/helper.sh sessions 5
{baseDir}/scripts/helper.sh post "<short reason>" --session <session-id>
{baseDir}/scripts/helper.sh rollback-help --session <session-id>
```

### 5. Report back to the user

`report` should keep PRE and POST visible, and also include the most recent 3 to 5 path-scoped records. PRE, POST, and the recent records should all be rendered as `id + comment` so the user does not have to infer meaning from a bare SHA.

Always tell the user:

- what the PRE snapshot is, shown as id + comment
- what the POST snapshot is or why it was not created, shown as id + comment
- what repo was used by the current helper implementation
- what target paths were protected
- the current session id
- the current session comment
- whether the current session is still open or already closed
- the most recent 3 to 5 saved sessions, with session id and comment shown together
- the most recent 3 to 5 path-scoped commit records, shown as id + comment
- that rollback is supported
- the safest rollback command for this task
- the active exclusion file

## Reporting template

```text
已完成本次修改，并已做文件变更保护。

仓库: <repo_root>

当前会话:
- id: <session_id>
- status: <open_or_closed>
- comment: <session_comment>

保护路径:
- <path1>
- <path2>

PRE 快照: <pre_sha> <pre_subject>
POST 快照: <post_sha or none> <post_subject or reason>

最近 5 次记录:
- <sha1> <subject1>
- <sha2> <subject2>
- <sha3> <subject3>
- <sha4> <subject4>
- <sha5> <subject5>

最近会话:
<sessions output with session id + session comment + pre/post summary>

支持回退。
如需回到本次修改前，优先使用 rollback-help 输出的按路径 restore 命令，例如:
  git restore --source=<pre_sha> --staged --worktree --pathspec-from-file=<session_paths_file> --pathspec-file-nul
如需查看还能恢复到哪里，可用:
  git reflog -n 10
```

If a POST commit exists and the user may prefer a history-preserving rollback, also mention:

```bash
git revert <post_sha>
```

## Behavior rules

- Mandatory to initialize a local git repository automatically if the current helper implementation needs one and the current directory is not already one.
- Mandatory to set repo-local `user.name` and `user.email` if git identity is missing for the current helper implementation.
- Mandatory to respect `.gitignore` and `{baseDir}/guarded-edit.ignore`.
- Mandatory to scope checks, staging, and commits to the explicit target paths from `pre`.
- Mandatory to keep each file change batch in its own saved session under `.git/.guarded-edit/sessions/`.
- Mandatory for `post` and `rollback-help` to require `--session <session-id>` instead of guessing when more than one file change session is still open.
- Mandatory to fail if a declared target path is excluded by `{baseDir}/guarded-edit.ignore`.
- Non-ignored new files, generated artifacts, binaries, and accidentally placed sensitive files inside the declared target paths may also be included in the snapshot.
- Never push unless the user explicitly asked.
- Never rewrite history unless the user explicitly asked.
- Never hide failures.
- If PRE fails, stop risky changes and tell the user.
- If the target paths already have staged changes, fail instead of rewriting the target-path index state.
- If no PRE snapshot exists for the current file change session, do not run POST silently.
- `post` uses the stored path set from `pre`. It should not silently widen scope.
- `rollback-help` must prefer path-scoped restore guidance over whole-repo hard reset guidance.
- Commands shown to the user should be shell-safe.

## Commit policy

### PRE step

- If the repo already has a clean `HEAD` for the declared target paths, reuse it as the recovery point.
- If the declared target paths already have unstaged or untracked changes and no staged changes in those paths, commit those paths as a PRE snapshot.
- If the declared target paths already have staged changes, fail and ask the user to resolve that index state first.
- If there is no `HEAD` yet, create an initial anchor commit when needed.

### POST step

- Only run POST after a valid PRE snapshot for the same file change session exists.
- Mark the file change session closed after `post`, even when no POST commit was needed.
- If the declared target paths produced new unstaged or untracked changes and no staged changes in those paths, commit them as a POST snapshot.
- If the declared target paths already have staged changes, fail and ask the user to resolve that index state first.
- If nothing changed in the declared target paths after the task, report that no POST commit was needed.

This keeps history useful without creating unnecessary empty commits and avoids sweeping unrelated workspace changes into the guarded snapshot.

## Preferred commands

```bash
{baseDir}/scripts/helper.sh pre "reason" -- <path> [<path> ...]
{baseDir}/scripts/helper.sh post "reason"
{baseDir}/scripts/helper.sh report 5
{baseDir}/scripts/helper.sh recent 5
{baseDir}/scripts/helper.sh sessions 5
{baseDir}/scripts/helper.sh rollback-help
```

## Exclusion file

The exclusion file is:

```text
{baseDir}/guarded-edit.ignore
```

Users can edit this file directly to control what File Change Tracker must exclude.
Use gitignore-style patterns.
Later matching patterns win, and `!` can re-include a path inside the exclusion file.

## Fallback manual commands

If the helper script is unavailable, use a conservative manual flow:

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init -q
if ! git config user.name >/dev/null 2>&1; then git config user.name "OpenClaw Tracker"; fi
if ! git config user.email >/dev/null 2>&1; then git config user.email "openclaw@local.invalid"; fi

ACTIVE_GUARD_IGNORE=""
if [ -f "{baseDir}/guarded-edit.ignore" ]; then
  ACTIVE_GUARD_IGNORE="{baseDir}/guarded-edit.ignore"
fi

# replace the path list below with the explicit target paths of this task
TARGETS=(src/file1.ts src/file2.ts)

# refuse excluded target paths
if [ -n "$ACTIVE_GUARD_IGNORE" ]; then
  for p in "${TARGETS[@]}"; do
    if git -c core.excludesFile="$ACTIVE_GUARD_IGNORE" check-ignore --no-index -q -- "$p"; then
      echo "Refusing because target path is excluded by active file-change-tracker rules: $p" >&2
      exit 1
    fi
  done
fi

# refuse to continue if the guarded paths already have staged changes
if ! git diff --cached --quiet -- "${TARGETS[@]}"; then
  echo "Refusing because target paths already have staged changes. Resolve or stash them first." >&2
  exit 1
fi

if git status --porcelain=v1 --untracked-files=all -- "${TARGETS[@]}" | grep -q .; then
  git add -A -- "${TARGETS[@]}"
  if ! git diff --cached --quiet -- "${TARGETS[@]}"; then
    git commit -m "guard(pre): <reason>" --only -- "${TARGETS[@]}"
  fi
fi

PRE_SHA="$(git rev-parse HEAD)"

# ...perform changes...

if ! git diff --cached --quiet -- "${TARGETS[@]}"; then
  echo "Refusing POST because target paths already have staged changes. Resolve or stash them first." >&2
  exit 1
fi

if git status --porcelain=v1 --untracked-files=all -- "${TARGETS[@]}" | grep -q .; then
  git add -A -- "${TARGETS[@]}"
  if ! git diff --cached --quiet -- "${TARGETS[@]}"; then
    git commit -m "guard(post): <reason>" --only -- "${TARGETS[@]}"
  fi
fi

git log --oneline -n 5
git restore --source "$PRE_SHA" --staged --worktree -- "${TARGETS[@]}"
git reflog -n 10
```
