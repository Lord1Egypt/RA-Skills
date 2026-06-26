# Finishing a Development Branch Reference

Source: obra/superpowers finishing-a-development-branch skill

## State Manager Integration

**Before starting Phase 5, check current state:**
```bash
bash scripts/workflow/state-manager.sh check
```

**Current branch and base branch are in `state.json`:**
- `feature_branch`: current feature branch name
- Read base branch via: `git merge-base HEAD main`

**Phase 5 does NOT change `current_phase`** until completion.

---

## Overview

Verify tests → Present options → Execute choice.

Announce at start: "I'm using the finishing-a-development-branch skill to complete this work."

## Step 1: Verify Tests

Run the project's test suite. If tests fail — stop. Do not proceed.

```bash
# Python
pytest -q

# Node/TS
pnpm test

# Rust
cargo test

# Go
go test ./...
```

Show failures clearly. Cannot merge/PR until tests pass.

## Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
git branch --show-current
```

Or ask: "This branch split from main — is that correct?"

## Step 3: Present Options

Present exactly these 4 options — no extra explanation:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

## Step 4: Execute Choice

### Option 1: Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<run tests>
git branch -d <feature-branch>
```

### Option 2: Push + PR

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "## Summary
- <bullet 1>
- <bullet 2>

## Test Plan
- [ ] <verification step>"
```

### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. You can return to it later."

### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits since <base-branch>

Type 'discard' to confirm.
```

Wait for exact word "discard". Then:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

## Quick Reference

| Option | Merge | Push | Keep Branch | Delete Branch |
|--------|-------|------|-------------|---------------|
| 1. Merge locally | ✓ | — | — | ✓ |
| 2. Create PR | — | ✓ | ✓ | — |
| 3. Keep as-is | — | — | ✓ | — |
| 4. Discard | — | — | — | ✓ (force) |

## Common Mistakes

- Skipping test verification before offering options → always verify first
- Merging without pulling latest base → always `git pull` before merge
- Deleting branch before confirming PR merged → wait for merge confirmation

---

## HARD GATE HG-5: Finishing Complete

**Before declaring Phase 5 complete, you MUST verify ALL of the following:**

- [ ] Full test suite passes (HG-3 subset + regression)
- [ ] Base branch correctly identified
- [ ] User selected one of the 4 options
- [ ] If Option 4 (discard): user typed exact word `discard`
- [ ] Gate file created: `.workflow/gate/p5-complete.json`

**Gate file format:**
```json
{
  "gate": "HG-5",
  "passed_at": "ISO8601",
  "option_selected": 1|2|3|4,
  "action_taken": "merged|pr_created|kept|discarded"
}
```

**To check gate:**
```bash
bash scripts/workflow/phase-gate-check.sh finish
```

**If gate not passed:** You CANNOT complete the workflow. Continue until gate is satisfied.
