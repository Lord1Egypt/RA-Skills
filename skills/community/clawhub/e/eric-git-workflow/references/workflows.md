# Git Workflow Patterns

## GitHub Flow (Recommended for most teams)

```
main ── feat/a ── feat/b ── hotfix/urgent
         │                     │
         └─ PR & merge ────────┘
```

Process:
1. Create branch from `main`: `git checkout -b feat/login`
2. Make commits
3. Push: `git push -u origin feat/login`
4. Open PR on GitHub
5. After review → squash-merge to `main`
6. Delete feature branch

**Pros**: Simple, fast deployment, good for CI/CD
**Cons**: No release isolation

## GitFlow (For versioned releases)

```
main ────── release/1.0 ──── release/1.1
  \                        /
   develop ── feat/a ── feat/b
               │
               └── hotfix/1.0.1 ──→ main (tagged) & develop
```

Process:
1. `develop` is default branch
2. Features branch from `develop`: `git checkout -b feat/x develop`
3. Releases branch from `develop`: `git checkout -b release/1.0 develop`
4. Release → merge to `main` (tagged) AND `develop`
5. Hotfixes branch from `main`: `git checkout -b hotfix/1.0.1 main`

**Pros**: Clean release management, hotfix isolation
**Cons**: Complex, can be overkill for small teams

## Trunk-based (For large CI/CD teams)

```
main ─── feat/a (short) ─── feat/b (short) ───
```

Process:
1. Create short-lived feature branches (hours/days, not weeks)
2. Feature flags for incomplete work
3. Daily merge to main
4. Automatic deployment after merge

**Pros**: Fast, no merge hell, true CI/CD
**Cons**: Requires feature flags, team discipline

## Rebase vs Merge

| Operation | Command | History | Best for |
|-----------|---------|---------|----------|
| Merge | `git merge` | Preserves branch structure | Shared branches, release merges |
| Squash merge | PR squash | Single commit | Completing a feature |
| Rebase | `git rebase` | Linear history | Updating feature branches before merge |
| Interactive rebase | `git rebase -i` | Cleaned commits | Before opening PR |

## Conflict Resolution Patterns

### During merge:
```bash
git merge feature/login
# CONFLICT in src/auth.js
# Fix the conflict markers
git add src/auth.js
git merge --continue
```

### During rebase:
```bash
git rebase main
# resolve conflict
git add resolved-file.js
git rebase --continue
```

### Conflict markers:
```
<<<<<<< HEAD
our change
=======
their change
>>>>>>> feature/login
```

## Commit Message Templates

For teams using Conventional Commits:
```
git config --local commit.template .gitmessage
```

Example `.gitmessage`:
```
# <type>(<scope>): <subject>
# |<---- 50 chars max ---->|
#
# <body> (optional, 72 chars per line)
#
# <footer> (optional)
#
# Types: feat, fix, chore, docs, refactor, test, style, perf
```
