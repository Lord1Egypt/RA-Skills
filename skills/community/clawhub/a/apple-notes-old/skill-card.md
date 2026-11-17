## Description:

Manage Apple Notes via the memo CLI on macOS, including creating, viewing, editing, deleting, searching, moving, and exporting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Apple Notes from an agent through the memo CLI on macOS for note and folder management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a third-party CLI and granting macOS Automation access may expose Apple Notes data to software outside the agent.

Mitigation: Install only after reviewing and trusting the memo CLI source, Homebrew tap, and required macOS permissions.

Risk: Delete operations can remove the wrong note or be difficult to recover.

Mitigation: Confirm the selected note before deletion and keep backups for important Apple Notes content.

Risk: The skill cannot edit notes that contain images or attachments.

Mitigation: Use the skill for text-based notes and manage attachment-heavy notes directly in Apple Notes.

## Reference(s):

- [memo GitHub repository](https://github.com/antoniorodr/memo)
- [ClawHub skill page](https://clawhub.ai/huangfeng1995/skills/apple-notes-old)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include memo CLI commands for creating, viewing, editing, deleting, moving, searching, and exporting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
