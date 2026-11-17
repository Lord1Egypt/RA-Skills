## Description:

Booking Manager helps an agent connect to booking systems, monitor appointments, notify business owners, manage confirmations, reschedules, cancellations, customer emails, calendar invites, and schedule summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cskar10](https://clawhub.ai/user/cskar10)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and staff use this skill to let an agent monitor booking data, surface new appointment requests, confirm or modify bookings, send customer emails with calendar invites, and summarize schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses booking-system and SMTP authority while handling customer and business-provided booking text in outbound emails.

Mitigation: Use least-privilege booking and SMTP credentials, review generated email behavior before deployment, and HTML-escape or sanitize booking fields and policy text before sending.

Risk: Free-form onboarding text can be persisted into agent instruction files and influence later behavior.

Mitigation: Collect business setup data only, reject pasted credentials, review onboarding content before saving, and store configuration as data where possible.

Risk: Incorrect booking updates, lock cleanup, or reminder timing can affect customer appointments.

Mitigation: Require owner confirmation for confirm, reschedule, and delete actions, use parameterized queries, release booking locks after changes, and track reminder sends to prevent duplicates.

## Reference(s):

- [Booking Manager ClawHub listing](https://clawhub.ai/cskar10/skills/booking-manager)
- [Data Source Connection Patterns](references/data-sources.md)
- [Email Templates](references/email-templates.md)
- [ICS Calendar Invite Format](references/ics-format.md)
- [Customer Onboarding Form](references/onboarding-form.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets, SQL examples, HTML email templates, and iCalendar content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce setup changes, booking data actions, outbound email content, and calendar invites when used with configured credentials.]

## Skill Version(s):

1.3.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
