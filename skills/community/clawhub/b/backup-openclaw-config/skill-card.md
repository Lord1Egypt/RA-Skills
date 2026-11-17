## Description:

Backup and restore OpenClaw configuration files for upgrades, machine transfers, recovery, and system maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexjunanjing-2](https://clawhub.ai/user/alexjunanjing-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create local backups of OpenClaw configuration, workspace, skills, memory, and user data, then restore those archives during upgrades, transfers, or disaster recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives may contain sensitive OpenClaw configuration, credentials, memory, skills, and agent instructions.

Mitigation: Write archives to a private backup directory, encrypt sensitive backups, restrict access, and do not share archives publicly.

Risk: Restoring an archive can overwrite current OpenClaw configuration and user data.

Mitigation: Restore only trusted archives, inspect the listed contents first, keep the generated .bak copies until validation is complete, and restart OpenClaw services only after review.

Risk: The shell backup workflow deletes matching backups older than 15 days in the chosen backup directory.

Mitigation: Review the retention behavior before running the script, choose a dedicated backup directory, and disable or adjust cleanup when longer retention is required.

## Reference(s):

- [OpenClaw Configuration Locations](references/config-locations.md)
- [ClawHub Skill Page](https://clawhub.ai/alexjunanjing-2/skills/backup-openclaw-config)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that create local tar.gz backup archives, metadata files, and restore operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
