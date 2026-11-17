## Description:

Manage macOS Calendar events from the command line using EventKit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halbotley](https://clawhub.ai/user/halbotley)

### License/Terms of Use:


## Use Case:

Developers and automation-focused macOS users use this skill to list calendars, view events, and create all-day, multi-day, or timed Calendar events without AppleScript dialogs or UI interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party Homebrew binary that can read and create events in sensitive calendars.

Mitigation: Review the upstream calmly project and Homebrew tap before installing, prefer a pinned and verified release when available, and grant Calendar access only when the installed binary is trusted.

Risk: Events created through the CLI may affect iCloud, local, or CalDAV calendars and sync automatically.

Mitigation: Verify calendar names, dates, and times before running generated commands, especially batch loops for recurring events.

## Reference(s):

- [calmly ClawHub Skill Page](https://clawhub.ai/halbotley/skills/calmly)
- [halbotley ClawHub Publisher Profile](https://clawhub.ai/user/halbotley)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Homebrew installation commands, calmly CLI commands, date verification commands, and notes about macOS Calendar permissions.]

## Skill Version(s):

1.3.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
