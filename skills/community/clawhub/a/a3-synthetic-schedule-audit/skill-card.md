## Description:

Detect overlapping synthetic calendar events and suggest free task slots from an exported schedule, without calendar credentials or writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viswabharathi-k-a](https://clawhub.ai/user/viswabharathi-k-a)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people reviewing synthetic schedules can identify overlapping timed events and find the earliest task slot that fits the supplied working window. The result is limited to the schedule data provided and does not account for unstated preferences or deadlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected schedule JSON may include private calendar details.

Mitigation: Review the input and use synthetic or otherwise approved schedule data; include only details needed for the audit.

## Reference(s):

- [ClawHub release](https://clawhub.ai/viswabharathi-k-a/skills/a3-synthetic-schedule-audit)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON audit results with a concise natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on the supplied working window, timed events, and task duration; does not modify schedules or send messages.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
