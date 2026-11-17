## Description:

Tracks sent invoices, flags overdue payments, and drafts payment follow-up reminders for review on demand or on a weekly schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and finance operators use this skill to review outstanding invoices, identify overdue accounts, generate aging and revenue summaries, and prepare payment reminder drafts before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice data may be sensitive if the skill is granted broad access to files, sheets, accounting systems, or delivery channels.

Mitigation: Configure only the intended invoice source and digest destination before installation.

Risk: Email or accounting integrations can affect customer communications or invoice records if permissions are granted too broadly.

Mitigation: Grant email or accounting access only when needed, keep reminders as drafts, and require explicit approval before sending reminders or updating records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-invoice-tracker)
- [Publisher profile](https://clawhub.ai/user/ceobotson-bot)
- [DoctorClaw website](https://www.doctorclaw.ceo)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown invoice digest, reminder email drafts, revenue summaries, aging reports, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reminder emails are drafted for user approval before sending; invoice sources, delivery channels, schedules, and integrations are configurable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
