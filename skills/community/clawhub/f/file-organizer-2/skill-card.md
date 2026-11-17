## Description:

File Organizer helps an agent safely analyze local folders, find duplicates, propose organization plans, and perform confirmed file moves, renames, and trash-only cleanup with backups and small batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolz1](https://clawhub.ai/user/carolz1)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill when they want an agent to inspect a specific local folder, identify duplicates or disorganized files, and propose a safe cleanup plan before any changes are made. It is suited for downloads, desktop, documents, archives, photos, and similar file triage workflows where explicit confirmation and backups are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accepted file moves, renames, or trash actions can affect user data.

Mitigation: Use the skill only on specific directories, review every proposed action, require backups, and keep deletion limited to the system trash.

Risk: Duplicate or similar-size reports can be mistaken for authorization to remove files.

Mitigation: Treat duplicate findings as review input only; confirm retained copies and use small, verified batches before any cleanup.

Risk: Folder scans can expose private file names and metadata to the agent session.

Mitigation: Define the target directory and exclusions before scanning, and avoid broad or sensitive directories unless the user explicitly scopes them.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/CarolZ1/file-organizer)
- [ClawHub skill page](https://clawhub.ai/carolz1/skills/file-organizer-2)
- [Duplicate scanner](artifact/scripts/scan_duplicates.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON duplicate reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis first; file changes require explicit confirmation, backups, trash-only deletion, and batches of no more than 10 files.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
