# Plan Template

Save to: `docs/plans/YYYY-MM-DD-<feature>.md`

## Template

```markdown
# Plan: [Feature Name]

**Date:** YYYY-MM-DD
**Author:** [agent/human]
**Status:** Draft / Approved / In Progress / Complete

## Goal

[One sentence: what this achieves when done]

## Design Decision

[Approach chosen from brainstorming, with brief rationale]

## Tasks

### Task 1: [Name]

**Files:** [exact paths to create/modify/test]
**Depends on:** none

Steps:
1. Write failing test in `[test file path]`:
   ```typescript
   [complete test code]
   ```
2. Run: `pnpm test -- [test file]` → expect 1 failure
3. Implement in `[source file path]`:
   ```typescript
   [complete implementation code]
   ```
4. Run: `pnpm test -- [test file]` → expect 0 failures
5. Commit: `git commit -m "feat: [description]"`

**Verification:** `pnpm test` → all green, exit 0

---

### Task 2: [Name]

**Files:** [exact paths]
**Depends on:** Task 1

[Same step format]

---

### Task N: Integration & Final Verification

Steps:
1. Run full test suite: `pnpm test` → expect 0 failures
2. Run build: `pnpm build` → expect exit 0
3. Run lint: `pnpm check` → expect 0 errors
4. Manual smoke test: [specific steps]
5. Commit: `git commit -m "feat: [summary]"`

**Verification:** All commands above pass with evidence.
```

## Guidelines

- Each task = 2-5 minutes of work
- Include COMPLETE code, not "add validation here"
- Include EXACT commands with EXPECTED output
- Tests come BEFORE implementation in every task
- Dependencies between tasks must be explicit
- Final task always includes full verification suite
