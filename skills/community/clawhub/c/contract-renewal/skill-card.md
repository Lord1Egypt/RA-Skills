## Description:

Contract Renewal helps property operations teams identify upcoming tenant contract expirations from an Excel workbook, analyze customer profiles, generate renewal plans, and send WeCom renewal reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Property operations and leasing teams use this skill to monitor expiring tenant contracts, classify renewal urgency, create renewal plans, and prepare renewal follow-up messages. It is intended for workflows that rely on an approved contract workbook and reviewed notification recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tenant and business records may be included in renewal messages sent through an externally configurable WeCom webhook.

Mitigation: Use only an approved production workbook, restrict the webhook to the intended corporate endpoint, and gate outbound notifications until recipients and message fields are approved.

Risk: Workbook writes can mutate business records such as renewal plans and status updates.

Mitigation: Back up the workbook, keep an audit trail for changes, and validate inputs before allowing write operations.

Risk: Renewal plans and urgency classifications may be based on incomplete or incorrect workbook data.

Mitigation: Require human review of generated plans, warnings, and success-rate estimates before they drive tenant outreach or commercial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/skills/contract-renewal)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Text summaries, Markdown reminders, JSON reports, and workbook updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write renewal plans to the configured Excel workbook and produce JSON renewal reports.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
