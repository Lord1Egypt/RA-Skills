## Description:

Manage Apple Notes via the `memo` CLI on macOS (create, view, edit, delete, search, move, and export notes). Use when a user asks Clawdbot to add a note, list notes, search notes, or manage note folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[readbyte-ai](https://clawhub.ai/user/readbyte-ai)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Apple Notes from an agent-assisted terminal workflow on macOS, including creating, searching, editing, moving, exporting, and deleting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide operations that read, export, edit, move, or delete Apple Notes through a third-party CLI.

Mitigation: Install only from a trusted memo CLI source, grant Notes.app Automation access deliberately, and review selected notes before any edit, move, export, or delete action.

Risk: Deleted notes may be difficult or impossible to recover.

Mitigation: Confirm delete targets carefully and prefer export or backup workflows before destructive changes.

Risk: The skill is macOS-only and depends on local terminal access, the memo binary, Apple Notes.app availability, and Automation permissions.

Mitigation: Use it only on macOS systems where memo is installed and Notes.app Automation permissions are configured.

## Reference(s):

- [memo GitHub repository](https://github.com/antoniorodr/memo)
- [Apple Notes 1.0.0 on ClawHub](https://clawhub.ai/readbyte-ai/skills/apple-notes-1-0-0)
- [readbyte-ai publisher profile](https://clawhub.ai/user/readbyte-ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide interactive terminal operations that read, export, edit, move, or delete Apple Notes through the memo CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
