## Description:

Display the current local date and time from the command line in a user-supplied format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use this skill to generate formatted current local date and time strings for logs, scripts, or quick checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises timezone conversion, date differences, and timestamp parsing, but the included script only formats the current local datetime.

Mitigation: Use the skill for current local date/time formatting unless those advertised capabilities are implemented and reviewed in a later release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/date-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text date/time strings and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formats the current local datetime using Python strftime-compatible format strings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
