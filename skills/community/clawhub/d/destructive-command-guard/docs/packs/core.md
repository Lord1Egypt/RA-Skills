# Core Packs

This document describes packs in the `core` category.

## Packs in this Category

- [Core Git](#coregit)
- [Core Filesystem](#corefilesystem)

---

## Core Git

**Pack ID:** `core.git`

Protects against destructive git commands that can lose uncommitted work, rewrite history, or destroy stashes

### Keywords

Commands containing these keywords are checked against this pack:

- `git`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `checkout-new-branch` | `git\s+(?:\S+\s+)*checkout\s+-b\s+` |
| `checkout-orphan` | `git\s+(?:\S+\s+)*checkout\s+--orphan\s+` |
| `restore-staged-long` | `git\s+(?:\S+\s+)*restore\s+--staged\s+(?!.*--worktree)(?!.*-W\b)` |
| `restore-staged-short` | `git\s+(?:\S+\s+)*restore\s+-S\s+(?!.*--worktree)(?!.*-W\b)` |
| `clean-dry-run-short` | `git\s+(?:\S+\s+)*clean\s+-[a-z]*n[a-z]*` |
| `clean-dry-run-long` | `git\s+(?:\S+\s+)*clean\s+--dry-run` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `checkout-discard` | git checkout -- discards uncommitted changes permanently. Use 'git stash' first. | high |
| `checkout-ref-discard` | git checkout <ref> -- <path> overwrites working tree. Use 'git stash' first. | high |
| `restore-worktree` | git restore discards uncommitted changes. Use 'git stash' or 'git diff' first. | high |
| `restore-worktree-explicit` | git restore --worktree/-W discards uncommitted changes permanently. | high |
| `reset-hard` | git reset --hard destroys uncommitted changes. Use 'git stash' first. | critical |
| `reset-merge` | git reset --merge can lose uncommitted changes. | high |
| `clean-force` | git clean -f/--force removes untracked files permanently. Review with 'git clean -n' first. | critical |
| `push-force-long` | Force push can destroy remote history. Use --force-with-lease if necessary. | critical |
| `push-force-short` | Force push (-f) can destroy remote history. Use --force-with-lease if necessary. | critical |
| `branch-force-delete` | git branch -D/--force deletes branches without checks. Recoverable via 'git reflog'. | medium |
| `stash-drop` | git stash drop deletes a single stash. Recoverable via `git fsck` (unreachable objects). | medium |
| `stash-clear` | git stash clear permanently deletes ALL stashed changes. | critical |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "core.git:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "core.git:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Core Filesystem

**Pack ID:** `core.filesystem`

Protects against dangerous rm -rf commands outside temp directories

### Keywords

Commands containing these keywords are checked against this pack:

- `rm`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `rm-rf-tmp` | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-fr-tmp` | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-rf-var-tmp` | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:/var/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-fr-var-tmp` | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:/var/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-rf-tmpdir` | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:\$TMPDIR/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-fr-tmpdir` | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:\$TMPDIR/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-rf-tmpdir-brace` | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:\$\{TMPDIR(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-fr-tmpdir-brace` | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:\$\{TMPDIR(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-rf-tmpdir-quoted` | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:"\$TMPDIR/(?!(?:[^"]*/)?\.\.(?:/\|"))[^"]*"(?:\s+\|$))+$` |
| `rm-fr-tmpdir-quoted` | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:"\$TMPDIR/(?!(?:[^"]*/)?\.\.(?:/\|"))[^"]*"(?:\s+\|$))+$` |
| `rm-rf-tmpdir-brace-quoted` | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:"\$\{TMPDIR(?!(?:[^"]*/)?\.\.(?:/\|"))[^"]*"(?:\s+\|$))+$` |
| `rm-fr-tmpdir-brace-quoted` | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:"\$\{TMPDIR(?!(?:[^"]*/)?\.\.(?:/\|"))[^"]*"(?:\s+\|$))+$` |
| `rm-r-f-tmp` | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-f-r-tmp` | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-r-f-var-tmp` | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:/var/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-f-r-var-tmp` | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:/var/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-r-f-tmpdir` | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:\$TMPDIR/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-f-r-tmpdir` | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:\$TMPDIR/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-r-f-tmpdir-brace` | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:\$\{TMPDIR(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-f-r-tmpdir-brace` | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:\$\{TMPDIR(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-recursive-force-tmp` | `^rm\s+.*--recursive.*--force\s+(?:/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-force-recursive-tmp` | `^rm\s+.*--force.*--recursive\s+(?:/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-recursive-force-var-tmp` | `^rm\s+.*--recursive.*--force\s+(?:/var/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-force-recursive-var-tmp` | `^rm\s+.*--force.*--recursive\s+(?:/var/tmp/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-recursive-force-tmpdir` | `^rm\s+.*--recursive.*--force\s+(?:\$TMPDIR/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-force-recursive-tmpdir` | `^rm\s+.*--force.*--recursive\s+(?:\$TMPDIR/(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-recursive-force-tmpdir-brace` | `^rm\s+.*--recursive.*--force\s+(?:\$\{TMPDIR(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |
| `rm-force-recursive-tmpdir-brace` | `^rm\s+.*--force.*--recursive\s+(?:\$\{TMPDIR(?!\.\.(?:/\|\s\|$)\|[^\s]*/\.\.(?:/\|\s\|$))\S*(?:\s+\|$))+$` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `rm-rf-root-home` | rm -rf on root or home paths is EXTREMELY DANGEROUS. This command will NOT be executed. Ask the user to run it manually if truly needed. | critical |
| `rm-rf-general` | rm -rf is destructive and requires human approval. Explain what you want to delete and why, then ask the user to run the command manually. | high |
| `rm-r-f-separate` | rm with separate -r -f flags is destructive and requires human approval. | high |
| `rm-recursive-force-long` | rm --recursive --force is destructive and requires human approval. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "core.filesystem:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "core.filesystem:*"
reason = "Your reason here"
risk_acknowledged = true
```

---
