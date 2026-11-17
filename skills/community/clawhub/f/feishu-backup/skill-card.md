## Description:

Back up files uploaded to a Feishu group chat to a local backup directory with smart matching by count, filename, file type, and recent time range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caigang78](https://clawhub.ai/user/caigang78)

### License/Terms of Use:


## Use Case:

Agents and users handling Feishu group chat files use this skill to download selected recent uploads into a local backup directory and report success or failure honestly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies real Feishu chat files into a local backup directory, which may expose sensitive or unauthorized data if used on files the user should not store locally.

Mitigation: Use the skill only for files the user is allowed to retain locally and review the backup destination before execution.

Risk: The backup script executes sibling shared helper files that were outside the reviewed artifact.

Mitigation: Verify and trust the shared Feishu helper files before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caigang78/skills/feishu-backup)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command invocations and success or error status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional environment variables such as LIMIT, NAME_PREFIX, NAME_CONTAINS, MINUTES, FILE_TYPE, and BACKUP_DIR to control file matching and backup location.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
