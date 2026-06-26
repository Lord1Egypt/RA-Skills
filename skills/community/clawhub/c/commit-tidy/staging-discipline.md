# Staging Discipline

Pre-commit staging audit + sensitive-directory commit gate. Replaces the bare `git status` check with a full `git diff --cached --name-only` dump + 1:1 intent comparison.

## When to use

- Before every `git commit` invocation
- When the staged area accumulates across multiple operations
- When working on a branch that may have stale staged files from a prior turn or tool
- When editing inside sensitive directories (`rules/`, `agents/`, `docs/`, or any user-defined "never auto-commit" path)

## Core rule: explicit `git add` only (HARD STOP)

**Forbid `git add .` and `git add -A` outside of initial-import scenarios.** Every commit's staging set must come from explicit per-file or per-directory `git add` invocations the assistant chose.

| # | Don't | Do |
|---|-------|-----|
| 1 | `git add .` or `git add -A` to stage everything | `git add <file1> <file2>` or `git add apps/dt/` — explicit paths |
| 2 | Run `git commit` without running `git status` first | After `git add`, run `git status` and confirm nothing unintended (SVG, configs, etc.) got staged |
| 3 | Batch `add` over many modified files at once | Use `git add -p` (patch mode) to review and stage hunks one at a time |
| 4 | Trust `git status` alone (staged + unstaged are mixed and hard to disambiguate by sight) | **Right before every `git commit`, run `git diff --cached --name-only` to dump the full staged list** → match 1:1 against intent → commit only if all match |
| 5 | Ignore the possibility that something (user or tool) staged files in a prior turn | Read every line of `git diff --cached --name-only` and verify each was staged by an `add` you explicitly issued this session. Any out-of-scope entry → `git restore --staged <file>` before commit |

The one exception: a new project's very first import commit, or a user-requested "stage everything" instruction.

## Sensitive-directory commit gate (HARD STOP)

**Files under `rules/`, `agents/`, `docs/` (or any user-marked sensitive directory) commit ONLY when the user explicitly named them in an `add` instruction in this session.** A prior-turn modified-but-unstaged state must not be carried along by a different commit.

| # | Don't | Do |
|---|-------|-----|
| 1 | Out-of-scope modified files are staged; commit them anyway | Before commit, run `git diff --cached --name-only` → any out-of-scope staged entry → `git restore --staged <file>` or split into a separate commit |
| 2 | `rules/*.md` auto-committed without user instruction | Edits to `rules/` require **both** an explicit user `add` instruction **and** an explicit commit-message instruction. Do not let them ride along on another commit |
| 3 | `agents/*.md`, `docs/` auto-committed | Same rule — only on explicit user instruction |
| 4 | "I'll notice if the intended file isn't in the commit, then fix it" thinking | **Pre-commit visual check of the full staged list is the only first-line defense.** Post-commit correction requires `git reset` / `git rebase` |

### Self-check (every time before `git commit`)

1. Run `git diff --cached --name-only` and dump the output
2. Match each line 1:1 against your intent (your own `git add` history this session)
3. Any line not matching intent → halt commit → `git restore --staged <file>` → re-verify
4. Any line under `rules/`, `agents/`, `docs/` → confirm the user explicitly instructed adding that file in this session

## Procedure (every commit)

1. `git status` to enumerate dirty state (staged + unstaged + untracked)
2. Explicit `git add <paths>` for each intended file (no `.` / `-A`)
3. `git diff --cached --name-only` to dump the full staged list
4. Visual 1:1 match: every dumped line must trace to an `add` you ran this session
5. Out-of-scope entry? → `git restore --staged <file>` → return to step 3
6. Sensitive-directory entry? → verify the user explicitly named it → otherwise restore-stage
7. `git commit` only when steps 4-6 pass cleanly

## Failure pattern

See the user-local `~/.claude/skills/cleanup/data/failed-attempts.md` HOT entry "staged files leaked into a different commit" (this file is external to the repo — not checked into version control). The standard scenario: the assistant runs `git add <intended-file>`, but a prior-turn modification is already staged, and the commit ends up with the wrong fileset. The pre-commit `git diff --cached --name-only` dump catches this every time.

## Related topics

- `interactive-amend` — when the wrong fileset is already committed and needs amend recovery
- `soft-reset-amend` — when multiple wrong commits need a soft-reset re-stage cycle
- `security-scan` — pre-commit secret scan for PUBLIC repos (runs AFTER staging-discipline gate passes)
- `message-discipline` — commit-message conventions once the staged set is verified
