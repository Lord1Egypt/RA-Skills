## Description:

Meeting prep that pulls context on attendees, topics, and action items before calendar events, either automatically or on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operators use this skill to prepare for upcoming calendar meetings by compiling attendee context, relevant email threads, open tasks, prior notes, and suggested talking points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prep briefs may expose sensitive calendar, email, CRM, task, or meeting-note context through configured delivery channels.

Mitigation: Grant only required data access, start with on-demand prep, limit email lookback, and send briefs only to private destinations.

Risk: Saved meeting notes and created follow-up tasks may persist in memory, files, Notion, or other connected tools.

Mitigation: Confirm where notes and tasks will be stored before enabling post-meeting follow-up automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-meeting-prep)
- [DoctorClaw](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown meeting-prep brief with bullet points and follow-up task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar, email, CRM, task, and notes context depending on user configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
