# Soft Reset Amend

Amend the top N commits by soft-resetting them into the staging area, then selectively re-committing. A simpler alternative to `interactive-amend` when all target commits are at the top of the branch.

## When to Use

- All commits to modify are the **top N** commits (HEAD~1, HEAD~2, etc.)
- You need to **re-partition** files across commits (e.g., move a file from commit 2 to commit 1)
- You need to **rewrite commit messages** for recent commits
- You want a simpler flow than worktree-based rebase

## When NOT to Use

- Only a **middle commit** needs amending while keeping surrounding commits intact (e.g., fix only HEAD~3, leave HEAD~2 and HEAD~1 as-is) -- use [interactive-amend](./interactive-amend.md) instead
- Commits are **already pushed** and shared with others (rewriting shared history is destructive)
- The commit range includes **merge commits** -- soft reset flattens merge structure

## Comparison: interactive-amend vs soft-reset-amend

| Aspect | interactive-amend | soft-reset-amend |
|--------|-------------------|------------------|
| Target location | Any commit in history | Top N commits only |
| Mechanism | Worktree checkout + amend + `rebase --onto` | `git reset --soft` + selective re-commit |
| Preserves middle commits | Yes -- only target commit changes | No -- all N commits are dissolved and rebuilt |
| Complexity | Higher (worktree setup, SHA tracking) | Lower (linear stage + commit loop) |
| Best for | Surgical fix to one commit deep in history | Restructuring / re-partitioning top commits |

## Procedure

### Step 0. Backup Commit Messages

Save the messages of all commits that will be reset. They are lost after `git reset --soft`.

```bash
# Save messages for the top N commits (oldest first)
git log --reverse --format="%H %s" HEAD~N..HEAD
# Optionally save full messages:
git log --reverse --format="--- %H ---%n%B" HEAD~N..HEAD > /tmp/commit-messages.txt
```

Record the SHA, subject, and changed files for each commit:

```bash
git log --reverse --format="%H" HEAD~N..HEAD | while read sha; do
  echo "=== $sha ==="
  git log -1 --format="%s" "$sha"
  git diff-tree --no-commit-id --name-only -r "$sha"
  echo
done
```

### Step 1. Soft Reset

```bash
# Dissolve the top N commits into the staging area
git reset --soft HEAD~N
```

After this command:
- All changes from the N commits are **staged** (in the index)
- Working directory is unchanged
- Commit history is rewound by N commits
- The branch pointer moves back N commits

Verify the state:

```bash
git status          # All files should appear as staged
git diff --cached --stat   # Should show the combined diff of all N commits
```

### Step 2. Selective Stage + Commit Loop

For each new commit to create (following the planned partition):

#### 2-A. Unstage files not belonging to this commit

```bash
# Unstage everything first (move all from index to working directory)
git reset HEAD -- .

# Then stage only files for this commit
git add <file1> <file2> ...
```

Or alternatively, unstage only specific files:

```bash
# Unstage specific files that belong to a later commit
git reset HEAD -- <file-for-later-commit>
```

#### 2-B. Commit with the appropriate message

```bash
git commit -m "feat: ..."
```

Use the backed-up message from Step 0 (adjusted if needed).

#### 2-C. Repeat for remaining files

Stage the next batch of files and commit. Continue until all changes are committed.

### Step 3. Verify

```bash
# Check the new commit history
git log --oneline -N

# Verify no uncommitted changes remain
git status

# Verify the combined diff matches the original
git diff HEAD~N..HEAD --stat
```

### Step 4. Force Push (if already pushed)

```bash
# Per git.md: force push requires CI status check (HARD STOP)
gh run list --branch $(git branch --show-current) --limit 5 --json status,conclusion
# Only force push after CI is clean or no runs exist
git push --force-with-lease origin $(git branch --show-current)
```

## Example

**Scenario**: PR has 3 commits. Review feedback says file `src/utils.ts` was committed in commit 2 but belongs in commit 1.

```
Commit 1 (HEAD~2): feat: add user API       -- src/api/user.ts, src/api/types.ts
Commit 2 (HEAD~1): feat: add user UI        -- src/components/Profile.tsx, src/utils.ts  <-- utils.ts belongs in commit 1
Commit 3 (HEAD):   test: add user tests     -- tests/user.test.ts
```

**Execution**:

1. Backup messages: `feat: add user API`, `feat: add user UI`, `test: add user tests`
2. `git reset --soft HEAD~3` -- all 5 files now staged
3. Stage commit 1 files: `git add src/api/user.ts src/api/types.ts src/utils.ts` -- commit with `feat: add user API`
4. Stage commit 2 files: `git add src/components/Profile.tsx` -- commit with `feat: add user UI`
5. Stage commit 3 files: `git add tests/user.test.ts` -- commit with `test: add user tests`
6. Verify: `git log --oneline -3` shows 3 clean commits
7. Force push (after CI check)

## Constraints

- `git rebase -i` is forbidden (interactive mode not supported)
- `--no-verify` is forbidden -- fix hook failures instead
- Force push requires CI status verification per `git.md`
- Always backup commit messages before `git reset --soft` -- they cannot be recovered after reset
- If the reset range includes commits from other contributors, do NOT proceed -- use `interactive-amend` or AskUserQuestion
