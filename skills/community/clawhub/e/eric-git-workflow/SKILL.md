---
name: git-workflow
description: "Expert-level Git workflow guidance covering branching strategies, commit conventions, merge/rebase workflows, conflict resolution, and CI/CD integration. Use when the user needs help with: (1) Choosing a branching strategy (GitFlow, GitHub Flow, trunk-based), (2) Writing conventional commits, (3) Resolving merge conflicts, (4) Interactive rebase and squashing, (5) Git hooks and automation, (6) Submodules and monorepos, (7) Recovering from mistakes (reset, reflog, amend)."
---

# Git Workflow Assistant

## Branching Strategies

### When to use what:

| Strategy | Best for | Key structures |
|----------|----------|----------------|
| **GitHub Flow** | Continuous deployment, small teams | `main` + feature branches → PR → deploy |
| **GitFlow** | Release cycles, multiple versions | `main` → `develop` → `feature/*` → `release/*` → `hotfix/*` |
| **Trunk-based** | CI/CD, large teams | Short-lived feature branches → merge to `main` daily |
| **GitLab Flow** | Environments per branch | `main` → `pre-production` → `production` |

## Commit conventions

Follow Conventional Commits: `<type>(<scope>): <description>`

```
feat: add user authentication
fix(api): handle null response from payment gateway
chore(deps): upgrade express to 4.18
docs(readme): update installation guide
refactor(db): extract query builder
test(auth): add login flow tests
```

## Common Workflows

### Feature branch → PR

```bash
git checkout -b feat/my-feature main
# ... code, commits ...
git push -u origin feat/my-feature
# → Open PR on GitHub/GitLab/Azure DevOps
```

### Rebase before merge (linear history)

```bash
git fetch origin
git rebase origin/main
# fix conflicts if any
git push --force-with-lease
```

### Interactive rebase (squash/split)

```bash
git rebase -i HEAD~3
# pick, squash, reword, edit as needed
git push --force-with-lease
```

## Conflict Resolution

**Strategy:**
1. `git merge <branch>` → resolve conflicts in files
2. Mark resolved: `git add <file>`
3. Continue: `git merge --continue`

For rebase conflicts:
```bash
git rebase --continue   # after resolving each step
git rebase --abort      # to cancel
git rebase --skip       # to skip a commit
```

## Recovery

- **Undo last commit (keep changes)**: `git reset --soft HEAD~1`
- **Undo last commit (discard changes)**: `git reset --hard HEAD~1`
- **Recover deleted branch**: `git reflog` → find SHA → `git checkout -b <branch> <sha>`
- **Undo a pushed commit**: `git revert <sha>` (safe for shared branches)

## Useful Aliases

```bash
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.undo "reset --soft HEAD~1"
git config --global alias.amend "commit --amend --no-edit"
```

## References

See [references/workflows.md](references/workflows.md) for detailed workflow patterns.
