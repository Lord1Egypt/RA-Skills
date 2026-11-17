## Description:

Enterprise-grade backup and recovery toolkit supporting file backup, database backup, incremental backup, scheduled tasks, and disaster recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, schedule, and restore file and database backups for data protection and disaster recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore and backup-path handling can overwrite files outside intended folders.

Mitigation: Review and preferably fix path validation before installation; restore only trusted archives into empty staging directories.

Risk: Database backup examples and commands may expose long-lived database passwords through command-line arguments or process environments.

Mitigation: Use least-privileged database accounts and avoid passing long-lived passwords on command lines.

Risk: Dependencies may change over time if installed from broad version ranges.

Mitigation: Pin or remove dependencies before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/backup-recovery-toolkit)
- [Publisher Profile](https://clawhub.ai/user/kaiyuelv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe file paths, backup names, database settings, schedules, and restore procedures.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
