## Description:

Manage Apple Calendar events on macOS 14+ using apple-calendar-cli: list, get, create, update, and delete events with ISO 8601 date support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sichengchen](https://clawhub.ai/user/sichengchen)

### License/Terms of Use:


## Use Case:

Developers and agents working on macOS use this skill to inspect and manage Apple Calendar calendars and events from the command line. It supports scheduling workflows such as listing calendars, checking date ranges, creating events, rescheduling events, and deleting events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar access can expose sensitive event data and allows event changes or deletion.

Mitigation: Grant Calendar access only after review, and require the agent to ask before reading broad date ranges or changing or deleting events.

Risk: The skill installs a third-party CLI without pinned release verification in the provided evidence.

Mitigation: Prefer a pinned and verified apple-calendar-cli release before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sichengchen/skills/apple-calendar-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON output schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends --json output for reliable parsing.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
