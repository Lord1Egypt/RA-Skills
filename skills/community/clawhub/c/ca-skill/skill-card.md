## Description:

Ca Skill helps agents connect to a locally running TallyPrime instance to read accounting reports and prepare or send XML-over-HTTP workflows for vouchers, masters, inventory, GST, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[purvik6062](https://clawhub.ai/user/purvik6062)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting users and CA workflows use this skill to work with local TallyPrime company data, including report exports, ledger and inventory master setup, voucher posting, voucher alteration or cancellation, GST checks, and invoice-to-entry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change TallyPrime accounting data.

Mitigation: Use it only for intended accounting workflows and require explicit review before any voucher, master, alteration, or cancellation is sent.

Risk: A non-local or incorrect TALLY_URL could expose accounting operations to the wrong endpoint.

Mitigation: Set TALLY_URL to a loopback address such as localhost or 127.0.0.1 and avoid remote HTTP endpoints.

Risk: Wrong company, report period, or voucher details could affect financial records or produce misleading exports.

Mitigation: Confirm the company, report date range, ledger names, GST fields, voucher totals, and operation type before export or write actions.

## Reference(s):

- [Ca Skill on ClawHub](https://clawhub.ai/purvik6062/skills/ca-skill)
- [Errors & Troubleshooting - TallyPrime XML](reference/errors.md)
- [Inventory (Stock Groups / Items / UOM) + Item Invoices](reference/inventory.md)
- [Masters (Ledgers / Groups) - TallyPrime XML](reference/masters.md)
- [Reports & Data Export (TallyPrime XML)](reference/reports.md)
- [Vouchers (Create / Alter / Cancel) - TallyPrime XML](reference/vouchers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with XML templates, shell commands, and concise accounting-operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided TALLY_URL for a local TallyPrime XML-over-HTTP endpoint.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
