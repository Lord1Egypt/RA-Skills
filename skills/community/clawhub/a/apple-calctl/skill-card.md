## Description:

Calctl guides agents in helping macOS users install and use the calctl EventKit CLI to list, create, edit, delete, and inspect Apple Calendar events, including recurring events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianteohx](https://clawhub.ai/user/christianteohx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to provide practical calctl installation and command guidance for managing Apple Calendar events from a macOS terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned external CLI can expose users to supply-chain risk.

Mitigation: Review the upstream calctl project before installing and prefer a pinned, verified release when available.

Risk: Calendar access can expose event details, and attendee output can expose invitee names, email addresses, and participation status.

Mitigation: Grant Calendar access only when needed, avoid attendee output unless necessary, and revoke Calendar access when the skill is no longer required.

Risk: Edit and delete commands can change or remove calendar events.

Mitigation: Review generated commands and target event IDs before running mutating operations.

## Reference(s):

- [Calctl ClawHub Skill Page](https://clawhub.ai/christianteohx/skills/apple-calctl)
- [calctl Project Homepage](https://github.com/christianteohx/calctl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read or modify local Apple Calendar data.]

## Skill Version(s):

1.2.9 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
