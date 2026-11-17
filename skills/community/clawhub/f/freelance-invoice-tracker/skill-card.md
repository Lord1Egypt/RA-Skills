## Description:

Automated invoice tracking and payment follow-up for Indian freelancers. Monitors a Google Sheet of invoices, auto-sends polite follow-up emails or WhatsApp messages at configurable intervals, tracks GST amounts, and generates monthly income reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utsavs](https://clawhub.ai/user/utsavs)

### License/Terms of Use:


## Use Case:

Freelancers in India use this skill to monitor invoice status, calculate GST amounts, send payment reminders, and produce income summaries from a Google Sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically contact clients about overdue invoices without enough confirmation and control safeguards.

Mitigation: Use least-privilege Google credentials, verify client contact fields, keep reminder sending in preview or approval mode when possible, and avoid unattended cron sending until limits, logs, and a pause mechanism are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utsavs/skills/freelance-invoice-tracker)
- [ClawHub homepage](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, message templates, cron commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Sheets credentials and an invoice sheet ID; may also use email or WhatsApp reminder settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
