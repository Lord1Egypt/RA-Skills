## Description:

Invoice & Expense Tracker helps an agent parse natural-language invoice and expense updates into a local ledger, reports, alerts, and accounting-ready CSV exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipstark](https://clawhub.ai/user/philipstark)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, finance operators, and team assistants use this skill to log business spending in plain English, keep a local ledger, summarize expenses, detect duplicates or alerts, and export CSV files for accounting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial records are saved as plaintext files in the working directory.

Mitigation: Keep ./data and ./exports out of source control and shared folders, and avoid storing account numbers, tax identifiers, or other sensitive identifiers.

Risk: Parsed entries and CSV exports may be incomplete or unsuitable for bookkeeping or accounting imports without review.

Mitigation: Review ledger entries and generated CSV exports before relying on them or importing them into accounting tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/philipstark/skills/fl-invoice-tracker)
- [Publisher Profile](https://clawhub.ai/user/philipstark)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown summaries plus JSON ledger and CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local plaintext data under ./data and generated CSV exports under ./exports.]

## Skill Version(s):

1.0.0 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
