---
metadata:
  author: es6kr
  version: "0.1.1"
name: commit-tidy
depends-on:
  - git-repo
description: >-
  Analyze staged/committed changes and recommend split, squash, or commit-message strategy.
  Topics — interactive-amend (worktree-based amend+rebase loop),
  soft-reset-amend (soft-reset top N + selective re-commit),
  staging-discipline (`git diff --cached --name-only` audit + sensitive-dir gate for rules/agents/docs),
  security-scan (PUBLIC repo 4-grep secret pattern check before commit),
  message-discipline (Conventional Commit tags, PUBLIC English enforcement, operation-type continuity, --amend refresh, source-code .md behavior verbs).
  Use when: "commit split", "squash commits", "tidy commits", "amend earlier", "interactive amend",
  "soft reset", "rewrite commits", "PUBLIC repo commit", "secret in commit", "commit message",
  "commit author identity", "commit message English", "staging discipline".
---

# Commit Tidy

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| interactive-amend | Worktree-based amend+rebase loop for earlier/multiple commits | [interactive-amend.md](./interactive-amend.md) |
| message-discipline | Commit message conventions — Conventional Commit tags, PUBLIC English enforcement, --amend refresh, source-code .md behavior verbs, operation-type continuity | [message-discipline.md](./message-discipline.md) |
| security-scan | PUBLIC repo commit body 4-grep secret pattern check (PAT/Vault/API key/Base64) before commit | [security-scan.md](./security-scan.md) |
| soft-reset-amend | Soft-reset top N commits and selectively re-commit (simpler than worktree rebase) | [soft-reset-amend.md](./soft-reset-amend.md) |
| staging-discipline | `git diff --cached --name-only` audit + sensitive-dir gate (rules/agents/docs) before commit | [staging-discipline.md](./staging-discipline.md) |

Analyze staged/unstaged changes and recommend whether to split into multiple commits.

## When to use

- Before committing large changesets
- User asks "should I split this commit?"
- Reviewing changes that touch many files
- Ensuring atomic, reviewable commits

## Split Decision Criteria

### Split when

1. **Unrelated functionality changes**
   - Feature A + Bug fix B → 2 commits
   - UI change + API change (if independent) → 2 commits

2. **Wide file spread**
   - Changes span 5+ directories with no common purpose
   - Frontend + Backend + Config all modified

3. **Mixed change types**
   - Refactoring + New feature → 2 commits
   - Formatting + Logic change → 2 commits
   - Dependency update + Code change → 2 commits

4. **Large diff size**
   - 500+ lines changed across unrelated areas
   - Multiple components modified independently

5. **Different reviewers needed**
   - Changes require different domain expertise
   - Security-sensitive + general changes

### Keep together when

1. **Single logical change**
   - Feature requires touching multiple files
   - Refactoring that must be atomic

2. **Dependent changes**
   - API change + caller updates
   - Schema change + migration + model update

3. **Related cleanup**
   - Feature + directly related tests
   - Bug fix + regression test

## Squash Criteria

When analyzing multiple commits, **recommend squashing as well as splitting**.

### Squash when

1. **Same type + same purpose**
   - `test: A test` + `test: B test` (tests for the same feature) → squash into 1
   - `fix: typo A` + `fix: typo B` (same review feedback) → squash into 1

2. **Commits split per loop by automated agents**
   - Autonomous agents like Ralph commit per loop → squash if same purpose
   - Example: proxy test in loop 1, OIDC test in loop 2 → `test: add unit tests`

3. **Consecutive WIP commits**
   - `wip: in progress` + `feat: complete` → squash into one feat

### Don't squash

1. **Commits with different types** — keep `test` + `chore` + `feat` separate
2. **Commits belonging to different PRs/issues**
3. **Independent changes that may need to be reverted**

### Output format (when recommending squash)

```
### Recommendation: Squash 2 commits → 1

**Before** (2 commits):
- 441b966a test(dt): OIDC auth, proxy, SSO tests
- e2b6503a test(dt): OIDC route tests (login, callback, me)

**After** (1 commit):
Subject: test(dt): add OIDC auth unit tests
Body:
  Consolidates OIDC unit tests from the prior per-loop splits — covers the
  auth flow, proxy interaction, SSO behavior, and route handlers
  (login / callback / me) in a single coherent test commit.

**Reasoning**: Same type (test), same feature (OIDC auth), agent loop split
```

The body in every recommended commit follows `message-discipline.md` "Default commit message structure" — body is recommended by default, free-form (not restricted to per-file enumeration), footer optional.

## Instructions

### Step 0: Determine scope

When ARGUMENTS specify a range (e.g., "since main", "last 3 commits", "PR #N"), analyze **all changes in that range** — both committed and uncommitted.

```bash
# Range specified (e.g., "X changes since main")
git log --oneline <base>..HEAD -- <path>     # committed changes
git diff <base>..HEAD --stat -- <path>        # committed diff
git diff HEAD --stat -- <path>                # uncommitted diff
```

The analysis must cover **committed commits (squash/split candidates) + uncommitted changes (new commit candidates)** as a single unified view. Do not analyze only uncommitted changes when a range is specified.

When no range is specified, default to staged + unstaged changes only.

### Step 1: Analyze changes

```bash
# Check staged changes
git diff --cached --stat
git diff --cached --name-only

# Check unstaged changes
git diff --stat
git status
```

### Step 2: Categorize files

Group changed files by:
- **Feature/Component**: Which feature does this belong to?
- **Change type**: feat, fix, refactor, style, test, docs, chore
- **Directory**: Are changes localized or spread out?

### Step 3: Identify boundaries

Look for natural split points:
- Different conventional commit types
- Independent functionality
- Separate test files from implementation (if tests are for different features)

### Step 4: Recommend split strategy

Provide specific recommendations. **Every recommended commit includes a body by default** (see `message-discipline.md` "Default commit message structure"). The body is free-form — it does not have to enumerate per-file changes.

```
## Analysis Results

### Changed Files (N files)
- src/api/... (3 files) - API endpoints
- src/components/... (2 files) - UI components
- tests/... (2 files) - Tests

### Recommendation: Split into N commits

**Commit 1**:
  Subject: feat: add user profile API
  Body:
    Adds POST /users/profile and GET /users/profile/:id endpoints backed by a
    shared validation schema. Both endpoints reuse the existing auth middleware
    and return consistent error shapes. Unit tests cover happy path plus
    validation-error branches.
  Footer (optional): Closes #<issue>
  Files:
    - src/api/user.ts
    - src/api/types.ts
    - tests/api/user.test.ts

**Commit 2**:
  Subject: feat: add profile UI component
  Body:
    Adds a Profile component that consumes the new API endpoints, including
    loading and error states. CSS extracted into a sibling module to keep the
    component file focused on behavior. Component tests stub the API client to
    exercise the loading / success / error branches independently.
  Files:
    - src/components/Profile.tsx
    - src/components/Profile.css
    - tests/components/Profile.test.tsx

### Reasoning
- API and UI can function independently
- Each can be reviewed by different reviewers
```

### Step 4.5: Local commit-type rule self-check (HARD STOP — before Step 5)

**Before executing the recommended split, run the working-tree-specific commit-type override self-check.** Workspaces with `<repo>/.claude/rules/*.md` defining their own commit-type / version-bump mapping take precedence over the global tag-selection defaults applied in Step 4.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
find "$REPO_ROOT/.claude/rules/" -name '*.md' 2>/dev/null
```

If the find returns one or more files, grep them for commit-type semantics (recursive to match the `find` scope above):

```bash
grep -rliE 'commit type|conventional commit|version bump|feat|fix|topic' \
  "$REPO_ROOT/.claude/rules/" --include='*.md' 2>/dev/null
```

Read each matched file. If a local mapping exists (e.g., "new topic = `feat:`, in-place edit of existing topic = `fix:`"), **re-classify each recommended subject under the local mapping before invoking Step 5**. Example reclassification:

| Step 4 draft (global default) | Local rule | Step 5 subject |
|------------------------------|-----------|----------------|
| `feat(skill-X): add HARD STOP for Y` (no new topic file) | `branch-policy.md` "in-place edit = `fix:`" | `fix(skill-X): require Y` |
| `feat(skill-X): add new-topic.md` (new topic file present) | same rule | `feat(skill-X): add new-topic topic` (unchanged) |

See `message-discipline.md` → "Working-tree-specific commit-type override (HARD STOP)" for the full self-check.

### Step 5: Execute split (if requested)

Use HEREDOC (`git commit -F -`) so the body and optional footer land in the commit message exactly as drafted. Per `message-discipline.md`, single `-m "<subject>"` invocations are reserved for the rare subject-only acceptable cases (typo / routine dep bump).

```bash
# Unstage all
git reset HEAD

# Stage first commit files
git add src/api/ tests/api/
git commit -F - <<'EOF'
feat: add user profile API

Adds POST /users/profile and GET /users/profile/:id endpoints backed by a
shared validation schema. Both endpoints reuse the existing auth middleware
and return consistent error shapes. Unit tests cover happy path plus
validation-error branches.
EOF

# Stage second commit files
git add src/components/ tests/components/
git commit -F - <<'EOF'
feat: add profile UI component

Adds a Profile component that consumes the new API endpoints, including
loading and error states. CSS extracted into a sibling module to keep the
component file focused on behavior. Component tests stub the API client to
exercise the loading / success / error branches independently.
EOF
```

## Quick Reference

### File spread heuristic

| Files | Directories | Recommendation |
|-------|-------------|----------------|
| 1-5 | 1-2 | Usually single commit |
| 5-10 | 2-3 | Review for split |
| 10+ | 4+ | Likely needs split |

### Change type combinations to split

| Combination | Split? |
|-------------|--------|
| feat + feat (unrelated) | ✅ Yes |
| feat + related test | ❌ No |
| fix + unrelated refactor | ✅ Yes |
| refactor + style (same files) | ❌ No |
| chore(deps) + feat | ✅ Yes |

## Output Format

Analysis results should include:

1. List of changed files with categories
2. Whether split is needed and why
3. Specific commit splitting plan
4. Suggested commit messages for each — **subject + body by default** (free-form body, footer optional). See `message-discipline.md` "Default commit message structure". Subject-only is reserved for typo / routine dep bump
5. Per-commit body draft — free-form prose / bullets / sections, NOT restricted to per-file enumeration
6. Execution commands (if requested) — use `git commit -F - <<'EOF'…EOF` HEREDOC form so the drafted body / footer lands in the commit message verbatim
