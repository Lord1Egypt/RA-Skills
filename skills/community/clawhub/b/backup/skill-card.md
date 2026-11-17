## Description:

Backup and restore OpenClaw data. Use when user asks to create backups, set up automatic backup schedules, restore from backup, or manage backup rotation. Handles ~/.openclaw directory archiving with proper exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, rotate, schedule, and restore archives of local OpenClaw configuration, credentials, sessions, workspace data, and scheduled tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain credentials, tokens, sessions, private workspace files, and scheduled tasks from ~/.openclaw.

Mitigation: Store backups in an owner-only directory, encrypt archives, and avoid shared or synced locations unless separately protected.

Risk: Restore instructions replace the active ~/.openclaw directory and include destructive rollback commands.

Mitigation: Verify the selected archive before restoring, keep the temporary ~/.openclaw-old copy until validation succeeds, and review commands before execution.

## Reference(s):

- [Restore OpenClaw from Backup](references/restore.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create compressed backup archives in a user-selected backup directory when the shell script is executed.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact package metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
