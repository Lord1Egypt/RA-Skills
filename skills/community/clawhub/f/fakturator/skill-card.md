## Description:

Fakturownik helps agents generate Polish VAT invoices with buyer and seller details, line items, VAT calculations, invoice numbering, and text, CSV, or JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomasz-pedzierski-infinity](https://clawhub.ai/user/tomasz-pedzierski-infinity)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, small businesses, and business-support agents use this skill to prepare Polish VAT invoice content from company, buyer, and invoice line-item data. It is suited for invoice drafting and export workflows where the user can review tax, customer, and payment details before sending or storing the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated invoices can contain business and customer data that may be sensitive.

Mitigation: Use the skill only with business data approved for generated invoice files, and review invoice content before storing, sharing, or sending it.

Risk: CSV exports from untrusted customer-supplied fields can carry spreadsheet-safety concerns.

Mitigation: Inspect or sanitize customer-provided invoice fields before opening exported CSV content in spreadsheet tools.

Risk: Email sending and invoice history features may require SMTP credentials or local retention in PRO versions.

Mitigation: Verify the exact PRO implementation before providing SMTP credentials or relying on local invoice history.

## Reference(s):

- [Fakturownik on ClawHub](https://clawhub.ai/tomasz-pedzierski-infinity/skills/fakturator)
- [Publisher profile](https://clawhub.ai/user/tomasz-pedzierski-infinity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with invoice text, CSV, JSON, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated invoice content may include business identifiers, customer data, VAT amounts, payment terms, and local files when the optional PRO or demo workflows are used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
