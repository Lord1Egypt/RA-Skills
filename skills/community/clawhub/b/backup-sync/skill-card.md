## Description:

Intelligent file backup with compression and verification. Backup, sync, verify integrity, dedup, and restore. Manifest tracking. Zero external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Smart Backup to create local backups, sync directory copies, verify backup manifests, restore files, and identify duplicate content during workspace maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local backup, sync, and restore operations may read, write, overwrite, delete, or restore files outside the locations a user intended.

Mitigation: Review paths before execution, run on non-sensitive test directories first, use dry-run previews, and avoid --force or --delete unless the affected paths have been inspected.

Risk: Backups and manifests may expose sensitive file contents, full paths, sizes, and directory structure.

Mitigation: Store backups and manifests only in trusted locations with appropriate access controls, and avoid using the skill on sensitive directories until the release has been reviewed.

Risk: Advertised compression, destination selection, symlink safety, and full SHA-256 integrity behavior may not match the implementation.

Mitigation: Do not rely on those claims for critical recovery workflows until implementation fixes are reviewed and verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jlacroix82/skills/backup-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local backup, sync, verification, restore, deduplication, and status guidance for agent workflows.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
