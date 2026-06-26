# Strict Git Packs

This document describes packs in the `strict_git` category.

## Packs in this Category

- [Strict Git](#strict_git)

---

## Strict Git

**Pack ID:** `strict_git`

Stricter git protections: blocks all force pushes, rebases, and history rewriting operations

### Keywords

Commands containing these keywords are checked against this pack:

- `git`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `git-status` | `git\s+status` |
| `git-log` | `git\s+log` |
| `git-diff` | `git\s+diff` |
| `git-show` | `git\s+show` |
| `git-branch-list` | `git\s+branch\s*$\\|git\s+branch\s+-[alv]` |
| `git-remote-v` | `git\s+remote\s+-v` |
| `git-fetch` | `git\s+fetch` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `push-force-any` | Force push (even with --force-with-lease) can rewrite remote history. Disabled in strict mode. | high |
| `rebase` | git rebase rewrites commit history. Disabled in strict mode. | high |
| `commit-amend` | git commit --amend rewrites the last commit. Disabled in strict mode. | high |
| `cherry-pick` | git cherry-pick can introduce duplicate commits. Review carefully. | high |
| `filter-branch` | git filter-branch rewrites entire repository history. Extremely dangerous! | high |
| `filter-repo` | git filter-repo rewrites repository history. Review carefully. | high |
| `reflog-expire` | git reflog expire removes reflog entries needed for recovery. | high |
| `gc-aggressive` | git gc with aggressive/prune options can remove recoverable objects. | high |
| `worktree-remove` | git worktree remove deletes a linked working tree. | high |
| `submodule-deinit` | git submodule deinit removes submodule configuration. | high |
| `push-master` | Direct push to master is blocked. Use a Pull Request. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "strict_git:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "strict_git:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

