## Description:

A text-based calendar and scheduling application. Use strictly for CLI-based calendar management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers and CLI users use this skill to query calcurse schedules, add appointments, add todos, and run the calcurse TUI from an agent-assisted shell workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated add or update commands can modify local calcurse calendar entries and todos.

Mitigation: Review proposed calcurse commands, dates, durations, priorities, and target data before execution.

Risk: The workflow depends on the local calcurse binary and the user's existing calcurse data setup.

Mitigation: Install and configure calcurse before use, and run commands only in the intended local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/calcurse)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the local calcurse binary and may modify local calendar or todo data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
