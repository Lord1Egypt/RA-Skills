# Conflict Resolution Guide

## First Principle: Never Lose Code

**CRITICAL**: When resolving conflicts, the absolute priority is preserving all code. If you cannot determine the correct merge strategy with confidence, you MUST:

1. Summarize the conflict clearly
2. Present both versions to the user
3. Ask for guidance
4. **NEVER** automatically choose one side over the other

## Conflict Resolution Workflow

### Step 1: Detect and Document Conflicts

When a merge or rebase results in conflicts:

1. **Save pre-merge state** (if not already done):
   ```bash
   scripts/save_diff.sh
   ```

2. **Visualize conflicts**:
   ```bash
   scripts/visualize_conflicts.sh
   ```

3. **List conflicted files**:
   ```bash
   git diff --name-only --diff-filter=U
   ```

### Step 2: Analyze Each Conflict

For each conflicted file, understand:

1. **What changed in our branch** (HEAD/current)
2. **What changed in their branch** (incoming)
3. **The common ancestor** (base)

Use the analysis script for comprehensive view:
```bash
scripts/analyze_conflicts.sh
```

Or manually check three-way diff:
```bash
git show :1:path/to/file  # Common ancestor
git show :2:path/to/file  # Our version (HEAD)
git show :3:path/to/file  # Their version (incoming)
```

### Step 3: Deep Analysis for Complex Conflicts

When both sides modified the same code, perform careful analysis:

#### A. Understand the Intent

For each conflicting change, determine:
- **What problem does it solve?**
- **What functionality does it add/remove/modify?**
- **Is it a bug fix, feature, refactor, or optimization?**

#### B. Compare the Approaches

Analyze the differences:
- **Logic differences**: Do they implement different algorithms?
- **API changes**: Do they change function signatures or interfaces?
- **Dependencies**: Do they add/remove different dependencies?
- **Side effects**: Do they have different impacts on other code?

#### C. Determine the Resolution Strategy

Based on analysis, choose one of these strategies:

**Strategy 1: Keep Both (Merge)**
- Both changes are valuable and compatible
- They address different aspects of the same area
- Example: One adds error handling, the other adds logging
- Action: Combine both changes carefully

**Strategy 2: Keep Ours (HEAD)**
- Our change is more recent/complete
- Their change is outdated or superseded
- Our change fixes a bug that their change doesn't address
- Action: Keep our version, document why

**Strategy 3: Keep Theirs (Incoming)**
- Their change is more correct/complete
- Our change is outdated or has issues
- Their change includes our changes plus more
- Action: Keep their version, document why

**Strategy 4: Keep Neither (Rewrite)**
- Both approaches have issues
- A better solution exists that combines insights from both
- Action: Write new code that incorporates best of both

**Strategy 5: Cannot Decide (Ask User)**
- Changes are equally valid but incompatible
- Business logic decision required
- Risk of breaking functionality
- Action: Present analysis to user, ask for guidance

### Step 3.5: Decision Making Framework

**Safe to resolve automatically** (rare cases only):
- Pure whitespace differences
- Non-overlapping changes in different sections
- Identical changes on both sides
- One side only adds comments/documentation

**Require careful analysis** (common cases):
- Logic changes that overlap
- Different implementations of same feature
- Refactoring vs feature addition
- Performance vs readability trade-offs

**Require user input** (complex cases):
- Deletions vs modifications of same code
- Incompatible API changes
- Different architectural approaches
- Business logic decisions
- Any ambiguity about intent or correctness

### Step 4: Present to User

When you cannot safely resolve, create a summary:

```markdown
## Conflict Summary

**File**: path/to/file.js
**Lines**: 45-67

### Our Version (HEAD):
```
[code from our branch]
```

### Their Version (incoming):
```
[code from their branch]
```

### Question:
Which version should we keep, or should we combine them? Please advise.
```

### Step 5: After Resolution

Once conflicts are resolved (by user or with user approval):

1. **Generate diff document**:
   ```bash
   git diff --cached > .git/merge-diffs/resolution_$(date +%Y%m%d_%H%M%S).diff
   ```

2. **Create visual summary**:
   ```bash
   git diff --cached --stat
   git diff --cached
   ```

3. **Save resolution record**:
   ```bash
   # Create a markdown summary
   echo "# Merge Resolution - $(date)" > merge-resolution.md
   echo "" >> merge-resolution.md
   echo "## Files Changed" >> merge-resolution.md
   git diff --cached --stat >> merge-resolution.md
   echo "" >> merge-resolution.md
   echo "## Full Diff" >> merge-resolution.md
   echo '```diff' >> merge-resolution.md
   git diff --cached >> merge-resolution.md
   echo '```' >> merge-resolution.md
   ```

## Conflict Markers Explained

Git marks conflicts with these markers:

```
<<<<<<< HEAD (our version)
[our code]
=======
[their code]
>>>>>>> branch-name (their version)
```

- `<<<<<<< HEAD`: Start of our changes
- `=======`: Separator between versions
- `>>>>>>> branch-name`: End of their changes

## Forbidden Actions

**NEVER do these without explicit user approval:**
- Automatically choose one side (`git checkout --ours` / `--theirs`)
- Delete code sections without understanding their purpose
- Merge conflicting logic without user review
- Continue merge/rebase with unresolved conflicts

## Safe Abort

If conflicts are too complex or risky:
```bash
git merge --abort    # Abort merge
git rebase --abort   # Abort rebase
```

This returns to the pre-merge/rebase state safely.

## Submodule Conflicts

**Scenario**: Conflicts in git submodules (different commit references).

**Detection**: Conflicted file is listed in `.gitmodules` or shows as a directory in conflict list.

**Handling**:

1. **Identify the submodule**:
   ```bash
   git config -f .gitmodules --get-regexp path
   ```

2. **Check submodule status**:
   ```bash
   git submodule status
   ```

3. **Understand the conflict**:
   - Our branch points to commit X in the submodule
   - Their branch points to commit Y in the submodule
   - Both are valid commits, but different

4. **Resolution strategy**:
   
   **Option A: Keep our submodule version**
   ```bash
   git checkout --ours <submodule-path>
   git add <submodule-path>
   ```
   
   **Option B: Keep their submodule version**
   ```bash
   git checkout --theirs <submodule-path>
   git add <submodule-path>
   ```
   
   **Option C: Update to latest** (if both are outdated)
   ```bash
   cd <submodule-path>
   git fetch
   git checkout <desired-commit-or-branch>
   cd ..
   git add <submodule-path>
   ```

5. **Verify submodule state**:
   ```bash
   git submodule status
   cd <submodule-path> && git log --oneline -5
   ```

**Important**: Submodule conflicts are usually about which commit to reference, not code conflicts within the submodule. If there are actual code conflicts within a submodule, you must:
1. Enter the submodule directory
2. Resolve conflicts there using normal conflict resolution
3. Commit in the submodule
4. Return to parent and stage the submodule reference

**When to ask user**:
- If unsure which submodule commit is correct
- If submodule commits have diverged significantly
- If updating submodule might break parent project

## Detached HEAD State

**Detection**: `git branch --show-current` returns empty.

**Implications**:
- Commits made in detached HEAD are not on any branch
- Risk of losing commits if you checkout another branch

**Safe operations in detached HEAD**:
- Viewing history: `git log`
- Analyzing changes: `git diff`
- Creating commits (but save them to a branch!)

**Before making changes**:
```bash
# Create a branch from current HEAD
git checkout -b temp-branch-name
```

**If already made commits in detached HEAD**:
```bash
# Save the commits to a branch
git branch recovery-branch
git checkout recovery-branch
```

**Recommendation**: Always work on a named branch. If you find yourself in detached HEAD, create a branch immediately before making changes.

## Special Case: Rebase to Branch with Less Code

**Scenario**: Branch A has less code than Branch B. You want to rebase B onto A.

**Command**: `git checkout B && git rebase A`

**What happens**: Git will replay all commits from B on top of A. This operation itself **does not lose code** — all of B's commits will be reapplied.

**However, conflicts may arise when:**

1. **A deleted files that B modified**
   - Git will show conflict: "deleted by them, modified by us"
   - Resolution: Usually keep B's version (the modifications are newer work)
   
2. **A removed code that B depends on**
   - Git will show conflict in the file
   - Resolution: Keep B's code and restore any dependencies it needs from A's history
   
3. **A and B have divergent implementations**
   - Git will show conflict with both versions
   - Resolution: Requires careful analysis (see below)

### Handling This Scenario:

**Step 1: Create Safety Net**
```bash
# On branch B
git branch B-before-rebase  # Backup branch
scripts/save_diff.sh        # Save current diff
```

**Step 2: Understand the Divergence**
```bash
# See what A has that B doesn't
git log B..A --oneline --stat

# See what B has that A doesn't  
git log A..B --oneline --stat

# Compare file-level differences
git diff A...B --stat
```

**Step 3: Execute Rebase with Caution**
```bash
git rebase A
```

**Step 4: When Conflicts Occur**

Run detailed analysis:
```bash
scripts/analyze_conflicts.sh
```

For each conflict, determine:

- **If A deleted code that B needs**: Keep B's version (B's work is more recent)
- **If A simplified code that B enhanced**: Merge both (keep B's enhancements on A's simplification)
- **If A and B took different approaches**: Analyze which is better or if both are needed

**Step 5: Verify No Code Loss**
```bash
# After resolving all conflicts and completing rebase
git diff B-before-rebase B

# Check that all B's functionality is preserved
# Review the diff carefully - any unexpected deletions indicate lost code
```

**Step 6: If Code Was Lost**
```bash
# Abort and restore
git reset --hard B-before-rebase

# Analyze what went wrong
git log B-before-rebase..B  # Should be empty if we're back
```

### Decision Framework for "Less Code" Scenarios

When A has less code than B:

**Default assumption**: B's additional code is intentional and valuable. Bias toward preserving B's work.

**Questions to ask:**
1. Did A intentionally remove code (cleanup/refactor)?
2. Did B intentionally add code (new features)?
3. Are the changes compatible or mutually exclusive?

**Resolution priorities:**
1. **Preserve all functionality** - Don't lose working features
2. **Combine improvements** - If A cleaned up and B added features, keep both
3. **Respect intent** - If A deliberately removed something, understand why before restoring it
4. **When in doubt** - Present both versions to user with analysis

### Example Analysis Template

When presenting complex conflicts to user:

```markdown
## Conflict Analysis: path/to/file.js

### Context
- Branch A (target): Removed 50 lines, simplified error handling
- Branch B (current): Added 80 lines, enhanced error handling with retry logic

### The Conflict
Lines 45-95: Both branches modified error handling

### Our Version (B - current branch):
```javascript
// Enhanced error handling with retry
try {
  await fetchData();
} catch (error) {
  await retryWithBackoff(error);
  logError(error);
}
```

### Their Version (A - target branch):
```javascript
// Simplified error handling
try {
  await fetchData();
} catch (error) {
  console.error(error);
}
```

### Analysis
- **A's intent**: Simplify code, remove complex retry logic
- **B's intent**: Add robust retry mechanism for reliability
- **Compatibility**: Incompatible - different error handling philosophies

### Recommendation
**Strategy: Keep Both (Merge with modification)**

Reasoning:
- B's retry logic adds valuable reliability
- A's simplification is good, but removing retry may cause issues
- Combine: Keep B's retry logic but simplify the implementation

Suggested resolution:
```javascript
try {
  await fetchData();
} catch (error) {
  await retry(fetchData, 3);  // Simplified retry
  console.error(error);
}
```

### Question for User
Does this approach work, or do you prefer:
1. Keep only A's simple version (no retry)
2. Keep only B's complex version (full retry logic)
3. Use the suggested merged version above
```

