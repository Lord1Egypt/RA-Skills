## Description:

Creates a backup before important file edits, asks the user to review the modified file, and deletes the backup only after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaqi-guo-0114](https://clawhub.ai/user/jiaqi-guo-0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve recovery copies before editing configuration files, core mechanism files, or other user-designated sensitive files. It guides the agent to retain backups until the user confirms they can be removed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup copies can duplicate sensitive file contents.

Mitigation: Use a private backup directory for sensitive files and remove stale backups when they are no longer needed.

Risk: Deleting the wrong backup path can remove the recovery copy before the edit has been verified.

Mitigation: Verify backup paths before deletion and wait for explicit user confirmation before removing backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiaqi-guo-0114/skills/file-backup)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline shell commands and backup file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local backup copies and cleanup commands; backup retention depends on user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
