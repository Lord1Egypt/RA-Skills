## Description:

Extract structured data from invoices, receipts, and bills using DeepRead schemas for vendor, line items, totals, tax, and due dates, with confidence flags for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, and developer teams use this skill to extract invoice, receipt, purchase order, and bill fields into structured JSON for accounts payable, expense processing, bookkeeping, audit, and invoice matching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected invoices, receipts, or bills are sent to DeepRead's hosted service using the user's API key.

Mitigation: Confirm organizational rules for confidential financial documents, retention, and regulated data before uploading customer, vendor, tax, or payment information.

Risk: Extracted fields can include confidence flags and may still require human review.

Mitigation: Review fields marked with hil_flag before using results in payment, approval, accounting, or audit workflows.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead BYOK dashboard](https://www.deepread.tech/dashboard/byok)
- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-invoice)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python, cURL, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends selected documents to DeepRead's hosted API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
