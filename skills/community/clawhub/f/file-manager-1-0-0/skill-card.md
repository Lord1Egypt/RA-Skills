## Description:

OpenClaw file-management assistant for bulk file operations, smart organization, duplicate cleanup, batch renaming, directory synchronization, and automated file workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhenyoyo](https://clawhub.ai/user/yangzhenyoyo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide agents through file organization, batch renaming, duplicate-file cleanup, and directory synchronization tasks using the bundled Python utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file operations can move, overwrite, or permanently delete files when execution flags are used.

Mitigation: Review planned operations first, use narrow test directories, keep backups, and avoid --execute, --delete, --move, and --no-confirm unless the impact is understood.

Risk: Mirror/delete and scheduled examples can propagate mistakes across backups or remove target files.

Mitigation: Run sync jobs in preview mode first, avoid broad directories such as a home folder, and confirm backups before enabling deletion or scheduled execution.

## Reference(s):

- [File management best practices](references/best_practices.md)
- [ClawHub skill page](https://clawhub.ai/yangzhenyoyo/skills/file-manager-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce previews, operation plans, reports, JSON exports, and file-operation commands for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
