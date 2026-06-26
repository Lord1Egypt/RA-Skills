# Pattern Audit Report
Generated: 2026-01-10T17:39:52.939979

## `src/packs/cicd/github_actions.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `gh-actions-secret-list` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| safe | `gh-actions-variable-list` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| safe | `gh-actions-workflow-list` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| safe | `gh-actions-workflow-view` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| safe | `gh-actions-run-list` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| safe | `gh-actions-run-view` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| safe | `gh-actions-api-explicit-get` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| destructive | `gh-actions-secret-remove` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| destructive | `gh-actions-variable-remove` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| destructive | `gh-actions-workflow-disable` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| destructive | `gh-actions-run-cancel` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| destructive | `gh-actions-api-delete-secrets` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |
| destructive | `gh-actions-api-delete-variables` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:secret\|var...` |

## `src/packs/containers/compose.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `compose-down-no-volumes` | Found '!' | `(?:docker-compose\|docker\s+compose)\s+down(?!\s+.*(?:-v\...` |

## `src/packs/core/filesystem.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `rm-rf-tmp` | Found '!' | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:/tmp/(?!\.\....` |
| safe | `rm-fr-tmp` | Found '!' | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:/tmp/(?!\.\....` |
| safe | `rm-rf-var-tmp` | Found '!' | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:/var/tmp/(?!...` |
| safe | `rm-fr-var-tmp` | Found '!' | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:/var/tmp/(?!...` |
| safe | `rm-rf-tmpdir` | Found '!' | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:\$TMPDIR/(?!...` |
| safe | `rm-fr-tmpdir` | Found '!' | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:\$TMPDIR/(?!...` |
| safe | `rm-rf-tmpdir-brace` | Found '!' | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:\$\{TMPDIR(?...` |
| safe | `rm-fr-tmpdir-brace` | Found '!' | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:\$\{TMPDIR(?...` |
| safe | `rm-rf-tmpdir-quoted` | Found '!' | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:"\$TMPDIR/(?...` |
| safe | `rm-fr-tmpdir-quoted` | Found '!' | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:"\$TMPDIR/(?...` |
| safe | `rm-rf-tmpdir-brace-quoted` | Found '!' | `^rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f[a-zA-Z]*\s+(?:"\$\{TMPDIR(...` |
| safe | `rm-fr-tmpdir-brace-quoted` | Found '!' | `^rm\s+-[a-zA-Z]*f[a-zA-Z]*[rR][a-zA-Z]*\s+(?:"\$\{TMPDIR(...` |
| safe | `rm-r-f-tmp` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:/tm...` |
| safe | `rm-f-r-tmp` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:/tm...` |
| safe | `rm-r-f-var-tmp` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:/va...` |
| safe | `rm-f-r-var-tmp` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:/va...` |
| safe | `rm-r-f-tmpdir` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:\$T...` |
| safe | `rm-f-r-tmpdir` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:\$T...` |
| safe | `rm-r-f-tmpdir-brace` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-[rR]\s+(-[a-zA-Z]+\s+)*-f\s+(?:\$\...` |
| safe | `rm-f-r-tmpdir-brace` | Found '!' | `^rm\s+(-[a-zA-Z]+\s+)*-f\s+(-[a-zA-Z]+\s+)*-[rR]\s+(?:\$\...` |
| safe | `rm-recursive-force-tmp` | Found '!' | `^rm\s+.*--recursive.*--force\s+(?:/tmp/(?!\.\.(?:/\|\s\|$...` |
| safe | `rm-force-recursive-tmp` | Found '!' | `^rm\s+.*--force.*--recursive\s+(?:/tmp/(?!\.\.(?:/\|\s\|$...` |
| safe | `rm-recursive-force-var-tmp` | Found '!' | `^rm\s+.*--recursive.*--force\s+(?:/var/tmp/(?!\.\.(?:/\|\...` |
| safe | `rm-force-recursive-var-tmp` | Found '!' | `^rm\s+.*--force.*--recursive\s+(?:/var/tmp/(?!\.\.(?:/\|\...` |
| safe | `rm-recursive-force-tmpdir` | Found '!' | `^rm\s+.*--recursive.*--force\s+(?:\$TMPDIR/(?!\.\.(?:/\|\...` |
| safe | `rm-force-recursive-tmpdir` | Found '!' | `^rm\s+.*--force.*--recursive\s+(?:\$TMPDIR/(?!\.\.(?:/\|\...` |
| safe | `rm-recursive-force-tmpdir-brace` | Found '!' | `^rm\s+.*--recursive.*--force\s+(?:\$\{TMPDIR(?!\.\.(?:/\|...` |
| safe | `rm-force-recursive-tmpdir-brace` | Found '!' | `^rm\s+.*--force.*--recursive\s+(?:\$\{TMPDIR(?!\.\.(?:/\|...` |

## `src/packs/core/git.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `restore-staged-long` | Found '!' | `git\s+(?:\S+\s+)*restore\s+--staged\s+(?!.*--worktree)(?!...` |
| safe | `restore-staged-short` | Found '!' | `git\s+(?:\S+\s+)*restore\s+-S\s+(?!.*--worktree)(?!.*-W\b)` |
| destructive | `checkout-ref-discard` | Found '!' | `git\s+(?:\S+\s+)*checkout\s+(?!-b\b)(?!--orphan\b)[^\s]+\...` |
| destructive | `restore-worktree` | Found '!' | `git\s+(?:\S+\s+)*restore\s+(?!--staged\b)(?!-S\b)` |
| destructive | `push-force-long` | Found '!' | `git\s+(?:\S+\s+)*push\s+.*--force(?![-a-z])` |

## `src/packs/database/mongodb.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `mongodump-no-drop` | Found '!' | `mongodump\s+(?!.*--drop)` |

## `src/packs/database/postgresql.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `pg-dump-no-clean` | Found '!' | `pg_dump\s+(?!.*--clean)(?!.*-c\b)` |

## `src/packs/database/redis.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| destructive | `shutdown` | Found '!' | `(?i)\bSHUTDOWN\b(?!\s+NOSAVE)` |

## `src/packs/infrastructure/ansible.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| destructive | `playbook-all-hosts` | Found '!' | `ansible-playbook\s+(?!.*(?:--check\|--limit\|--diff)).*-i...` |

## `src/packs/infrastructure/terraform.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `terraform-plan` | Found '!' | `terraform\s+plan(?!\s+.*-destroy)` |

## `src/packs/kubernetes/helm.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| destructive | `uninstall` | Found '!' | `helm\s+(?:uninstall\|delete)\b(?!.*--dry-run)` |
| destructive | `rollback` | Found '!' | `helm\s+rollback\b(?!.*--dry-run)` |

## `src/packs/kubernetes/kubectl.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| destructive | `delete-workload` | Found '!' | `kubectl\s+delete\s+(?:deployment\|statefulset\|daemonset\...` |
| destructive | `delete-pvc` | Found '!' | `kubectl\s+delete\s+(?:pvc\|persistentvolumeclaim)\b(?!.*-...` |
| destructive | `delete-pv` | Found '!' | `kubectl\s+delete\s+(?:pv\|persistentvolume)\b(?!.*--dry-run)` |

## `src/packs/kubernetes/kustomize.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `kustomize-build` | Found '!' | `kustomize\s+build(?!\s*\\|)` |
| safe | `kubectl-kustomize` | Found '!' | `kubectl\s+kustomize(?!\s*\\|)` |
| destructive | `kubectl-delete-k` | Found '!' | `kubectl\s+delete\s+-k\b(?!.*--dry-run)` |

## `src/packs/package_managers/mod.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `apt-get-list` | Found '!' | `apt-get\s+(?:update\|upgrade)(?!\s+.*-y)` |
| destructive | `npm-publish` | Found '!' | `npm\s+publish\b(?!.*--dry-run)` |
| destructive | `yarn-publish` | Found '!' | `yarn\s+publish\b(?!.*--dry-run)` |
| destructive | `pnpm-publish` | Found '!' | `pnpm\s+publish\b(?!.*--dry-run)` |
| destructive | `cargo-publish` | Found '!' | `cargo\s+publish\b(?!.*--dry-run)` |
| destructive | `poetry-publish` | Found '!' | `poetry\s+publish\b(?!.*--dry-run)` |

## `src/packs/platform/github.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `gh-repo-list-view` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| safe | `gh-gist-list-view` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| safe | `gh-release-list-view` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| safe | `gh-issue-list-view` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| safe | `gh-ssh-key-list` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| safe | `gh-api-explicit-get` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-repo-delete` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-repo-archive` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-gist-delete` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-release-delete` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-issue-delete` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-ssh-key-delete` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |
| destructive | `gh-api-delete-repo` | Found '!' | `gh(?:\s+--?[A-Za-z][A-Za-z0-9-]*\b(?:\s+(?!(?:repo\|gist\...` |

## `src/packs/system/disk.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| destructive | `fdisk-edit` | Found '!' | `fdisk\s+/dev/(?!.*-l)` |
| destructive | `parted-modify` | Found '!' | `parted\s+/dev/\S+\s+(?!print)` |

## `src/packs/system/permissions.rs`

| Kind | Name | Reason | Regex Preview |
|------|------|--------|---------------|
| safe | `chmod-non-recursive` | Found '!' | `chmod\s+(?!-[rR])(?:\d{3,4}\|[ugoa][+-][rwxXst]+)\s+[^/]` |

