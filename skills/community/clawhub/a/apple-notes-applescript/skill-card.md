## Description:

Apple Notes.app integration for macOS. List folders, read, create, search, edit, and delete notes via AppleScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shad0wca7](https://clawhub.ai/user/shad0wca7)

### License/Terms of Use:


## Use Case:

Developers and macOS users use this skill to let an agent operate Apple Notes through bundled shell scripts that call AppleScript for listing folders, reading notes, searching, creating, editing, deleting, and exporting note attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete personal Apple Notes.

Mitigation: Back up Notes before use, keep operations scoped to explicit folders, and review edit or delete targets before execution.

Risk: Read, attachment, and PDF export workflows can expose private note content or write attachments to a shared temporary directory.

Mitigation: Avoid export workflows unless the output directory is private and explicitly approved; prefer folder-scoped reads and searches.

Risk: Input-handling issues could allow unintended commands or unintended Apple Notes operations.

Mitigation: Use only trusted note names, folder names, queries, and limits, and inspect proposed shell commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shad0wca7/skills/apple-notes-applescript)
- [Publisher profile](https://clawhub.ai/user/shad0wca7)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands, terminal text output, and exported attachment file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on macOS with Apple Notes access; attachment and PDF workflows may write files under /tmp/notes-export.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
