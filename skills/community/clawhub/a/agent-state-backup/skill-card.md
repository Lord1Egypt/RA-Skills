## Description:

Auto-backs up OpenClaw core state files daily via cron into compressed archives and supports restore in a new environment to reduce context loss after restart or migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benxiao2026](https://clawhub.ai/user/benxiao2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure recurring and manual backups of identity, memory, user, and knowledge files, then restore those archives during restart, migration, or recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run local backup, restore, and cron setup scripts that are not included in the artifact for direct review.

Mitigation: Review the referenced shell scripts, confirm their ownership and permissions, and verify the cron entry before enabling automatic backups.

Risk: Restore overwrites current OpenClaw state files.

Mitigation: Create or preserve a current backup before restore and treat restore as a destructive operation.

Risk: Backup archives may contain memory, user information, identity files, and knowledge files.

Mitigation: Store backup archives with appropriate access controls and limit access to trusted users.

## Reference(s):

- [Agent State Backup skill source](artifact/SKILL.md)
- [Agent State Backup on ClawHub](https://clawhub.ai/benxiao2026/skills/agent-state-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup and restore command paths, cron setup guidance, backup location, retention guidance, and restore warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
