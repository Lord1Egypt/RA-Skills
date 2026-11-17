## Description:

Dev Backup creates named project snapshots for rollback and provides explicit backup, list, and destructive restore commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincsta](https://clawhub.ai/user/vincsta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Dev Backup to create rollback snapshots before risky changes or refactoring, list existing snapshots, and restore a selected project snapshot after an explicit request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore operations can overwrite local project files and may not remove files created after a snapshot.

Mitigation: Run restore only on trusted project paths, preview with --dry-run first, and keep an independent copy of important unsaved work before confirming restore.

Risk: Backups and restores read and write whole project directories.

Mitigation: Limit use to intended development project directories and review the target project and output paths before running commands.

Risk: Snapshots with missing or mismatched checksums may be corrupted or altered.

Mitigation: Avoid restoring snapshots when checksum verification is missing or reports a mismatch unless the project owner has manually inspected the snapshot.

Risk: The tar fallback and local shell execution path can carry file-safety and command-execution risk.

Mitigation: Prefer environments with rsync available, inspect commands before execution, and use the skill only from trusted releases.

## Reference(s):

- [Dev Backup README](artifact/README.md)
- [ClawHub Dev Backup release page](https://clawhub.ai/vincsta/skills/dev-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands and local snapshot directories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project snapshot directories, maintains a .latest symlink, and reports checksum status for snapshots.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
