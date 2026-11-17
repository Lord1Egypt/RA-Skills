## Description:

Watch an inbox for vendor invoices, extract the key fields, dedupe against the AP log, log them, forward to the AP system, and file the email. Use for daily accounts-payable intake when you want to automate the clerical part and keep a human in the loop before anything gets paid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillsandagentsco](https://clawhub.ai/user/skillsandagentsco)

### License/Terms of Use:

MIT-0

## Use Case:

Accounts-payable teams use this skill to automate invoice intake from email, update an AP log, forward invoices to the AP system, and keep each new invoice marked for human review before payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice fields may be unreadable, conflicting, or incorrectly extracted.

Mitigation: Require every extracted value to cite its source, mark unclear values as "uncertain, needs review", and have a person audit new AP-log rows before payment.

Risk: Duplicate detection or card-charge exclusions could skip a legitimate invoice.

Mitigation: Dedupe only by vendor plus invoice number, use the configured card-charge pattern rather than vendor identity alone, and send uncertain cases to review.

Risk: Automated forwarding and filing could affect the wrong mailbox, AP log, or AP-system destination.

Mitigation: Confirm the inbox or label, AP-log columns, forwarding destination, exclude patterns, and lookback window before installation; use a limited mailbox or label when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillsandagentsco/skills/ap-invoice-processing)
- [AP Invoice Processing overview](https://skillsandagents.co/skills/ap-invoice-processing/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown run summary with AP-log entries and email action notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [New invoices are marked for human review; the skill does not approve or pay invoices.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
