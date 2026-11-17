## Description:

Use this skill when the task involves reading, searching, creating, editing, organizing, or moving Apple Notes on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lishix520](https://clawhub.ai/user/lishix520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent work with Apple Notes on macOS, including searching, reading, creating, updating, organizing, moving, and carefully deleting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private Apple Notes content when an agent searches or reads notes.

Mitigation: Approve note access only for the intended task, review proposed searches and target notes, and avoid invoking it for sensitive notes unless access is necessary.

Risk: The skill can change, move, or delete important notes when invoked through macOS Automation.

Mitigation: Review proposed edits, folder creation, moves, bulk actions, and deletions before execution; require clarification when the target note or destination is ambiguous.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lishix520/skills/apple-notes-native)
- [Skill Homepage](https://github.com/lishix520/apple-notes-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and AppleScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Apple Notes, osascript, and user-approved Automation access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
