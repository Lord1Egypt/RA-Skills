## Description:

Manage Drafts app notes via CLI on macOS: create, view, list, edit, append, prepend, and run actions on drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerveband](https://clawhub.ai/user/nerveband)

### License/Terms of Use:


## Use Case:

Developers and macOS users use this skill to manage Drafts notes from an agent through the local Drafts CLI. It supports creating, listing, reading, editing, appending, prepending, and running Drafts actions when Drafts is running on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and modify local Drafts notes through macOS Automation.

Mitigation: Install and invoke it only when you intend to let the local Drafts CLI manage Drafts notes, and review commands before actions that edit content.

Risk: The skill depends on an unpinned third-party CLI install path.

Mitigation: Prefer a pinned reviewed release or a verified commit and checksum before installing the CLI.

Risk: A broad activation trigger may route unrelated note-management requests to the Drafts CLI.

Mitigation: Use the skill only for Drafts-specific tasks and confirm destructive or bulk operations before running commands.

## Reference(s):

- [Drafts CLI ClawHub listing](https://clawhub.ai/nerveband/skills/drafts)
- [Drafts app](https://getdrafts.com)
- [Drafts CLI homepage](https://github.com/nerveband/drafts)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the local Drafts CLI on macOS; Drafts must be running and Automation permissions may be required.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
