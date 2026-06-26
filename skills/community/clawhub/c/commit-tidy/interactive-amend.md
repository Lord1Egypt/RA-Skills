# Interactive Amend

Amend commits that are ahead of the current HEAD or when multiple commits need amending. Uses a worktree-based checkout+amend+rebase loop.

## When to Use

- Amend target is **not** the latest commit (can't use simple `--amend`)
- **2+ commits** need amending (e.g., review feedback touching multiple earlier commits)
- Commit history must stay clean without interactive rebase (`git rebase -i` is forbidden per rules)

## Prerequisites

- `/git-repo worktree` — acquire a worktree for isolated work
- Target commits identified (SHAs + what to fix in each)

## Procedure

### Step 0. Worktree Preparation

```bash
# Acquire worktree via /git-repo worktree (reuse inactive or create new)
# The worktree branch will be used as the working area
```

Invoke `/git-repo worktree` to get an isolated worktree. Record the worktree path and the original branch name.

### Step 1. Identify Amend Targets

```bash
# List commits to amend (from oldest to newest)
git log --oneline <base>..HEAD
```

Build an ordered list of `(SHA, description of fix)` pairs. Process from **oldest to newest** — amending an older commit first avoids cascading SHA changes.

### Step 2. Amend Loop (repeat for each target)

For each target commit (oldest first):

#### 2-A. Checkout target commit

```bash
cd <worktree-path>
git checkout <target-SHA>
```

This puts the worktree in detached HEAD state at the target commit.

#### 2-B. Apply fix + amend

```bash
# Make the necessary changes (Edit/Write)
git add <changed-files>
git commit --amend
```

Update the commit message if needed. Record the new SHA.

#### 2-C. Rebase remaining commits on top

```bash
# Rebase the original branch onto the amended commit
git rebase --onto HEAD <original-target-SHA> <branch-name>
```

This replays all commits after the target onto the amended version.

#### 2-D. Verify + update branch

```bash
git checkout <branch-name>
git log --oneline -5  # Verify the amended commit is in place
```

If more targets remain, go back to Step 2-A with the next target SHA. Note: SHAs of subsequent commits have changed due to rebase — use the new SHAs.

### Step 3. Force Push

After all amends are complete:

```bash
# Per git.md: force push requires CI status check (HARD STOP)
gh run list --branch <branch-name> --limit 5 --json status,conclusion
# Only force push after CI is clean or no runs exist
git push --force-with-lease origin <branch-name>
```

### Step 4. Cleanup

```bash
# Return to main repo
cd <original-repo-path>
# Worktree cleanup per /git-repo conventions
```

## Example

**Scenario**: PR has 3 commits, review feedback requires fixing commit 1 and commit 2.

```
Commit 1: feat: add user API        ← needs: fix error handling
Commit 2: feat: add user UI         ← needs: fix import path
Commit 3: test: add user tests      ← no changes needed
```

**Execution**:

1. Worktree acquired at `~/.claude/worktrees/fix-review`
2. Checkout commit 1 → fix error handling → amend → rebase commits 2,3 on top
3. Checkout new commit 2 → fix import path → amend → rebase commit 3 on top
4. Verify log: 3 commits with correct changes
5. Force push (after CI check)

## Constraints

- `git rebase -i` is forbidden (interactive mode not supported)
- `--no-verify` is forbidden — fix hook failures instead
- Force push requires CI status verification per `git.md`
- Each amend must be a single atomic change — don't batch unrelated fixes into one amend
