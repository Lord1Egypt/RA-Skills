## Description:

Query Matt's calendars with the gog CLI for schedules, events, availability, and reminders, prioritizing Flowcode work calendar results and adding personal calendar context when relevant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamsmatt](https://clawhub.ai/user/williamsmatt)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or agents assisting Matt use this skill to answer schedule, availability, event, and reminder questions by querying his work calendar first and adding personal calendar notes when relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read both work and personal calendar data through an already-authenticated CLI.

Mitigation: Use it only where Matt has intentionally authorized calendar access, and require explicit user permission before reading the personal calendar.

Risk: Broad calendar queries can expose more sensitive event details than needed.

Mitigation: Limit date ranges and summarize or redact sensitive event details by default.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with calendar summaries and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should separate work calendar events from relevant personal calendar notes and call out all-day events.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
