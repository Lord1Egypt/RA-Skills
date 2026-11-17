## Description:

Apple Notes Writer helps agents create, update, read, and list Apple Notes on macOS from HTML or converted Markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnmuin](https://clawhub.ai/user/johnmuin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Apple Notes workflows on macOS, including creating or updating formatted notes from HTML or Markdown and managing note folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, list, create, and overwrite Apple Notes, including notes that may contain sensitive personal or business information.

Mitigation: Install only when local Apple Notes automation access is acceptable, and require explicit confirmation before writes or updates.

Risk: Unsafe AppleScript construction could execute unintended local automation when untrusted titles, folder names, account names, or note IDs are used.

Mitigation: Avoid untrusted values for AppleScript-interpolated inputs until interpolation is fixed, and review proposed actions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnmuin/skills/apple-notes-writer)
- [Skill instructions](artifact/SKILL.md)
- [Reference guide](artifact/REFERENCE.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and Python snippets; executed actions return text status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Apple Notes.app, and local automation permissions; supports create, update, read, list, and folder creation operations.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
