## Description:

Automatically sorts and renames files by type into structured folders with undo support, configurable filters, and dry-run preview for batch organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize cluttered local directories by moving files into type-based folders, applying consistent names, previewing changes, and restoring prior organization runs when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file-moving and renaming authority can reorganize many local files unexpectedly.

Mitigation: Use dry-run mode on a small test directory first, keep backups, and review source, target, exclude patterns, and size limits before a real run.

Risk: Undo behavior depends on the supplied log file and can move files according to paths in that log.

Mitigation: Run undo only with ORGANIZE_LOG.json files you created and control, and review the log contents before restoring files.

Risk: Unpinned installation can change the reviewed code version.

Mitigation: Prefer pinned installation commands for deployment and retain the reviewed release hash or version in change-management records.

## Reference(s):

- [File Type Patterns Reference](artifact/references/file-patterns.md)
- [File Organizer README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/indigas/skills/claw-file-organizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May move and rename local files when executed; dry-run mode previews planned changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
