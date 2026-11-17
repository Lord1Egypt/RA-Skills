## Description:

Converts local iCalendar (ICS) files into structured JSON for Feishu calendar integration and AI-agent processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to convert local calendar exports into JSON for Feishu calendar workflows. It supports merging events from multiple ICS files into one JSON file or splitting output by source file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON can expose private calendar details such as event titles, organizers, times, reminders, and identifiers.

Mitigation: Keep generated JSON private, redact sensitive events before sharing, and point the converter only at intended calendar export directories.

Risk: Calendar synchronization setup can access unintended calendars, credentials, or local files if configured too broadly.

Mitigation: Use trusted package sources, scoped calendar credentials, and reviewed sync paths before running any synchronization workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/goog/skills/feishu-candy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The converter emits structured event JSON containing event identifiers, summaries, status, organizer, start and end times, and alarms.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
