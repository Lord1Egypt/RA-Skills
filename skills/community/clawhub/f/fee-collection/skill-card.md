## Description:

费用催缴管理 supports fee-collection workflows by classifying overdue accounts, calculating overdue periods and combined amounts, generating reminder copy, and preparing WeCom notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Property operations and finance teams use this skill to check fee-payment status from a configured Excel workbook, classify overdue records by age, generate customer-facing reminders, and prepare daily or monthly collection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive overdue-payment notices may be sent through WeCom without sufficient approval, scoping, or redaction.

Mitigation: Configure the webhook only to an approved corporate destination and require operator preview and approval before sending reminders or @all escalations.

Risk: Billing workbooks, generated reports, and backups can contain customer and financial records.

Mitigation: Restrict access to the intended Excel file and treat generated reports and backups as sensitive financial records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/fee-collection)
- [Reference Documentation for Fee Collection](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration]

**Output Format:** [Chinese reminder text, Markdown summaries, and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes overdue-age classifications, fee totals, reminder messages, and report records.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
