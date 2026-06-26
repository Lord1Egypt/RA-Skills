# Backup Packs

This document describes packs in the `backup` category.

## Packs in this Category

- [BorgBackup](#backupborg)
- [Rclone](#backuprclone)
- [Restic](#backuprestic)
- [Velero](#backupvelero)

---

## BorgBackup

**Pack ID:** `backup.borg`

Protects against destructive borg operations like delete, prune, compact, and recreate.

### Keywords

Commands containing these keywords are checked against this pack:

- `borg`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `borg-list` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+list\b` |
| `borg-info` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+info\b` |
| `borg-diff` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+diff\b` |
| `borg-check` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+check\b` |
| `borg-create` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+create\b` |
| `borg-extract` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+extract\b` |
| `borg-mount` | `borg(?:\s+--?\S+(?:\s+\S+)?)*\s+mount\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `borg-delete` | borg delete removes archives or entire repositories. | high |
| `borg-prune` | borg prune removes archives based on retention rules. | high |
| `borg-compact` | borg compact reclaims space after deletions. | high |
| `borg-recreate` | borg recreate can drop data from archives. | high |
| `borg-break-lock` | borg break-lock forces removal of repository locks. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "backup.borg:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "backup.borg:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Rclone

**Pack ID:** `backup.rclone`

Protects against destructive rclone operations like sync, delete, purge, dedupe, and move.

### Keywords

Commands containing these keywords are checked against this pack:

- `rclone`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `rclone-copy` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+copy\b` |
| `rclone-ls` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+ls\b` |
| `rclone-lsd` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+lsd\b` |
| `rclone-lsl` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+lsl\b` |
| `rclone-size` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+size\b` |
| `rclone-check` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+check\b` |
| `rclone-config` | `rclone(?:\s+--?\S+(?:\s+\S+)?)*\s+config\b` |
| `rclone-dry-run` | `rclone\b(?:\s+\S+)*\s+--dry-run\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `rclone-sync` | rclone sync deletes destination files not present in the source. | high |
| `rclone-delete` | rclone delete removes files and directories from the target. | high |
| `rclone-deletefile` | rclone deletefile removes a single file from the target. | high |
| `rclone-purge` | rclone purge deletes a path and all its contents. | high |
| `rclone-cleanup` | rclone cleanup removes old/malformed uploads. | high |
| `rclone-dedupe` | rclone dedupe can delete or rename duplicate files. | high |
| `rclone-move` | rclone move deletes source files after copying. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "backup.rclone:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "backup.rclone:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Restic

**Pack ID:** `backup.restic`

Protects against destructive restic operations like forgetting snapshots, pruning data, removing keys, and cache cleanup.

### Keywords

Commands containing these keywords are checked against this pack:

- `restic`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `restic-snapshots` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+snapshots\b` |
| `restic-ls` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+ls\b` |
| `restic-stats` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+stats\b` |
| `restic-check` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+check\b` |
| `restic-diff` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+diff\b` |
| `restic-find` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+find\b` |
| `restic-backup` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+backup\b` |
| `restic-restore` | `restic(?:\s+--?\S+(?:\s+\S+)?)*\s+restore\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `restic-forget` | restic forget removes snapshots and can permanently delete backup data. | high |
| `restic-prune` | restic prune removes unreferenced data and is irreversible. | high |
| `restic-key-remove` | restic key remove deletes encryption keys and can make backups unrecoverable. | high |
| `restic-unlock-remove-all` | restic unlock --remove-all force-removes repository locks. | high |
| `restic-cache-cleanup` | restic cache --cleanup removes cached data from disk. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "backup.restic:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "backup.restic:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Velero

**Pack ID:** `backup.velero`

Protects against destructive velero operations like deleting backups, schedules, and locations.

### Keywords

Commands containing these keywords are checked against this pack:

- `velero`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `velero-backup-get` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+backup\s+get\b` |
| `velero-backup-describe` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+backup\s+describe\b` |
| `velero-backup-logs` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+backup\s+logs\b` |
| `velero-backup-create` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+backup\s+create\b` |
| `velero-schedule-get` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+schedule\s+get\b` |
| `velero-restore-create` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+restore\s+create\b` |
| `velero-version` | `velero(?:\s+--?\S+(?:\s+\S+)?)*\s+version\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `velero-backup-delete` | velero backup delete removes a backup and its data. | high |
| `velero-schedule-delete` | velero schedule delete removes scheduled backups. | high |
| `velero-restore-delete` | velero restore delete removes restore records. | high |
| `velero-backup-location-delete` | velero backup-location delete removes a backup storage location. | high |
| `velero-snapshot-location-delete` | velero snapshot-location delete removes a snapshot location. | high |
| `velero-uninstall` | velero uninstall removes the Velero deployment and related resources. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "backup.velero:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "backup.velero:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

