## Description:

Organizes desktop files by backing up the desktop, categorizing files and folders with configurable rules, moving them into target folders, and reporting results across macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hujxhed](https://clawhub.ai/user/hujxhed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and desktop support agents use this skill to organize desktop files on macOS, Linux, and Windows. It provides a backup-first workflow, configurable categorization rules, conflict handling, and a post-operation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk desktop reorganization can move many local files and folders without a clear confirmation step.

Mitigation: Run a dry run first and require explicit user confirmation before any move operation.

Risk: A backup command that exits without verifying copied content may not guarantee recovery if copying fails.

Mitigation: Verify the backup directory and a restore path before moving files, and keep the backup until the user confirms the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hujxhed/skills/desktop-organizer)
- [ClawHub publisher profile](https://clawhub.ai/user/hujxhed)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-move plans, backup commands, conflict-handling guidance, and organization reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
