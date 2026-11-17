## Description:

Automatically backs up files before deletion, restores deleted files from timestamped backups, searches backup manifests, and cleans expired backups and logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to back up files before deletion, recover accidentally deleted files, verify backup integrity, and manage opt-in cleanup of temporary workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deletion and cleanup workflows can cause data loss or out-of-scope deletion if executed without careful review.

Mitigation: Review deletion paths before installation and use dry-run, explicit opt-in, and backup verification before allowing cleanup actions.

Risk: Backup deletion can remove recovery data when backup folder names are not strictly validated.

Mitigation: Restrict delete_backup usage to validated backup folder names and review the selected backup target before removal.

Risk: Workspace cleaner fallback backups may not be reliable enough for recovery in the current release.

Mitigation: Do not rely on workspace_cleaner fallback backups for recoverability until directory restore and metadata format handling are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudcode-hans/skills/delete-recovery)
- [ClawHub publisher profile](https://clawhub.ai/user/cloudcode-hans)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-operation guidance for backup, restore, verification, manifest search, backup cleanup, and opt-in workspace cleanup workflows.]

## Skill Version(s):

0.11.1 (source: server release metadata; artifact content describes v0.11.0 behavior with no code changes in this release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
