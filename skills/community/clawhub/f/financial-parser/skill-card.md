## Description:

Extract and analyze data from invoices, receipts, bank statements, and financial documents. Categorize expenses, track recurring charges, and generate expense reports. Use when user provides financial PDFs or images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bankgpt](https://clawhub.ai/user/bankgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Small business users and finance teams use the skill to extract, categorize, and summarize information from invoices, receipts, statements, expense reports, and tax documents, then prepare expense reports and CSV-ready data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Misread or unclear financial figures can lead to incorrect totals or expense categories.

Mitigation: Check extracted figures against the source document, reconcile totals, and flag unclear data instead of guessing.

Risk: Financial documents may contain sensitive account details.

Mitigation: Mask account numbers in output and include only the last four digits when needed.

Risk: Tax-related categories or calculations may be incomplete or inaccurate.

Mitigation: Treat tax-related analysis as a starting point and verify it against the source documents and applicable tax guidance.

## Reference(s):

- [BankGPT website](https://bankgpt.io/)
- [ClawHub skill listing](https://clawhub.ai/bankgpt/skills/financial-parser)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV-ready data, JSON]

**Output Format:** [Markdown summaries and tables with CSV-ready data; JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves stated amounts and currencies, flags unclear or discrepant data, and masks account numbers.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
