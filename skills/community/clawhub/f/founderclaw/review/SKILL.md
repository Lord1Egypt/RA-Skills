---
name: review
description: >
  Pre-landing PR review. Analyzes diff against the base branch for SQL safety,
  race conditions, LLM trust boundaries, conditional side effects, and structural
  issues that tests don't catch.
  Use when: "review this PR", "code review", "pre-landing review", "check my diff",
  "review my changes".
---

# Pre-Landing Code Review

Analyze the current branch's diff against the base branch for structural issues that tests don't catch.

---

## Step 0: Detect Platform and Base Branch

Detect the git hosting platform from the remote URL:

```bash
git remote get-url origin 2>/dev/null
```

- URL contains "github.com" → **GitHub**
- URL contains "gitlab" → **GitLab**
- Check `gh auth status 2>/dev/null` → **GitHub**
- Check `glab auth status 2>/dev/null` → **GitLab**
- Neither → **git-native only**

Determine the base branch:

**GitHub:** `gh pr view --json baseRefName -q .baseRefName` or `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`

**GitLab:** `glab mr view -F json 2>/dev/null` → extract `target_branch`

**Fallback:** `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'` → then try `origin/main` → `origin/master` → `main`

Print the detected base branch.

---

## Step 1: Check Branch

1. Run `git branch --show-current`
2. If on the base branch: **"Nothing to review — you're on the base branch."** STOP.
3. Run `git fetch origin <base> --quiet && git diff origin/<base> --stat`
4. If no diff: **"No changes against base branch."** STOP.

---

## Step 2: Scope Drift Check

Before reviewing code quality, check: **did they build what was requested?**

1. Check for intent signals: PR description, commit messages (`git log origin/<base>..HEAD --oneline`), TODOs in the repo.
2. Run `git diff origin/<base>...HEAD --stat` and compare files changed against stated intent.

Evaluate:
- **SCOPE CREEP:** Files changed unrelated to stated intent. "While I was in there..." changes.
- **MISSING REQUIREMENTS:** Stated goals not addressed in the diff.

Output:
```
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary of what was requested>
Delivered: <1-line summary of what the diff actually does>
[If drift: list out-of-scope changes]
[If missing: list unaddressed requirements]
```

This is **INFORMATIONAL** — does not block the review.

---

## Step 3: Get the Diff

```bash
git fetch origin <base> --quiet
git diff origin/<base>
```

Full diff including committed and uncommitted changes.

---

## Step 4: Two-Pass Review

Apply the checklist in two passes:

### Pass 1 — CRITICAL

| Category | What to look for |
|----------|-----------------|
| **SQL & Data Safety** | Raw SQL interpolation, missing parameterization, unsanitized user input in queries, missing WHERE clauses on UPDATE/DELETE |
| **Race Conditions** | Check-then-act without locks, shared mutable state without synchronization, TOCTOU bugs |
| **LLM Trust Boundary** | LLM output used in SQL, shell commands, file paths, HTML rendering, or auth decisions without validation |
| **Enum & Value Completeness** | New enum values without corresponding handling in switch/match/if-else chains. **Requires reading code OUTSIDE the diff** — grep for all files referencing sibling values |

### Pass 2 — INFORMATIONAL

| Category | What to look for |
|----------|-----------------|
| **Conditional Side Effects** | Side effects (API calls, writes, mutations) inside conditionals that might not execute |
| **Magic Numbers & String Coupling** | Hardcoded values that should be constants, string comparisons that break if renamed |
| **Dead Code & Consistency** | Unused imports, unreachable code, inconsistent naming patterns |
| **Test Gaps** | Changed code paths without corresponding test changes. New functions without tests |
| **Performance** | N+1 queries, unbounded loops, missing pagination, unnecessary re-renders |
| **Error Handling** | Swallowed errors, missing try/catch, unchecked null returns |
| **Security** | Hardcoded secrets, overly permissive CORS, missing auth checks on new endpoints |

### Enum Deep Dive

When the diff introduces a new enum value, status, or type constant:
1. Grep for all files referencing sibling values
2. Read those files
3. Check if the new value is handled everywhere the old ones are

---

## Step 5: Output

### Review Report Format

```
REVIEW REPORT
════════════════════════════════════════
Branch: {branch} → {base}
Files changed: {N}
Lines: +{added} / -{removed}

Scope Check: {CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING}

## CRITICAL ({count})
  [{severity}] {file}:{line}
    Issue: {what's wrong}
    Fix: {how to fix it}

## INFORMATIONAL ({count})
  [{severity}] {file}:{line}
    Issue: {what's wrong}
    Fix: {how to fix it}

## Test Gaps
  - {file}:{function} — no test coverage for {edge case}

## Summary
  Verdict: {PASS / CHANGES REQUESTED / BLOCKED}
  Critical issues: {N}
  Informational issues: {N}
  Test gaps: {N}
════════════════════════════════════════
```

### Severity Levels
- **CRITICAL** — Must fix before merge. Data loss, security hole, crash risk.
- **HIGH** — Should fix before merge. Likely bug in production.
- **MEDIUM** — Fix soon. Code quality, maintainability.
- **LOW** — Nice to have. Style, naming, minor improvements.

---

## Step 6: Auto-Fix (Optional)

For mechanical fixes (unused imports, formatting, missing null checks), offer to fix them directly:

> I found {N} mechanical fixes I can apply automatically (unused imports, missing null guards, etc). Want me to fix them?

If yes, fix and commit atomically: `git add -p && git commit -m "review: fix {description}"`

---

## Important Rules

- **Read the full file, not just the diff hunks.** Context matters for understanding impact.
- **Name the exact file and line number.** Not "there's an issue in auth" but "auth.ts:47, token check returns undefined when session expires."
- **Connect to user outcomes.** "This matters because your user will see a 3-second spinner" not "this is inefficient."
- **Be direct about quality.** "Well-designed" or "this is a mess." Don't dance around.
- **If you can't verify a fix works, don't suggest it.** Run the tests.
- **Completion status:**
  - DONE — review complete, all findings reported
  - DONE_WITH_CONCERNS — review complete with critical issues flagged
  - BLOCKED — cannot access diff or repo state
  - NEEDS_CONTEXT — unclear what branch/PR to review
