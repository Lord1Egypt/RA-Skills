---
name: careful
description: >
  Safety guardrails for destructive commands. Warns before rm -rf, DROP TABLE,
  force-push, git reset --hard, kubectl delete, and similar destructive operations.
  Use when touching prod, debugging live systems, or in shared environments.
  Use when: "be careful", "safety mode", "prod mode", "careful mode".
---

# Careful — Destructive Command Guardrails

Safety mode is **active**. Before running any bash command, check it against the destructive patterns below. If detected, warn the user and wait for confirmation before proceeding.

## Destructive Patterns

### File System
- `rm -rf` / `rm -r` on critical paths (`/`, `/home`, `~`, project root)
- `mv` or `cp` that overwrites without backup
- `chmod 777` or overly permissive permissions
- `chown -R` on system directories

### Git
- `git reset --hard` (loses uncommitted work)
- `git push --force` / `git push -f` (rewrites history)
- `git clean -fd` (deletes untracked files)
- `git branch -D` (force deletes branch)

### Database
- `DROP TABLE` / `DROP DATABASE`
- `DELETE FROM ...` without WHERE
- `TRUNCATE`
- Mass UPDATE without WHERE

### Kubernetes / Docker
- `kubectl delete` on production namespaces
- `docker rm` / `docker rmi` on running containers
- `docker system prune -a`

### Package Management
- `npm uninstall` / `pip uninstall` of core dependencies
- `rm node_modules` while dev server is running

## How to Respond

When a destructive command is detected:

1. **Name the risk:** "This will {specific consequence}."
2. **Ask for confirmation:** "Proceed? (yes/no)"
3. **If no:** suggest a safer alternative
4. **If yes:** run the command

**Never block indefinitely.** The user can always override. Your job is to make sure they know what they're doing, not to prevent them from doing it.

## Safe Alternatives

| Dangerous | Safer |
|-----------|-------|
| `rm -rf dir/` | `trash dir/` or `mv dir/ dir.bak/` |
| `git reset --hard` | `git stash` then reset |
| `git push --force` | `git push --force-with-lease` |
| `DROP TABLE` | Archive table first, then drop |
| `DELETE FROM x` | `DELETE FROM x WHERE ... LIMIT 100` |
