## Description:

Automates bookkeeping workflows for freelancers and small and medium-sized businesses with receipt analysis, income-surplus reporting, DATEV CSV export, invoice generation, and tax-preparation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

External freelancers and small and medium-sized businesses use this skill to analyze accounting PDFs, categorize income and expenses, prepare income-surplus reports, export DATEV-compatible CSV data, and generate invoice PDFs for tax workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial records and generated accounting outputs.

Mitigation: Run it only in a trusted local workspace, limit access to input and output folders, and review generated files before sharing them.

Risk: CSV exports may preserve spreadsheet formula-like values from input data.

Mitigation: Sanitize or neutralize formula-leading characters before opening exported CSV files in spreadsheet software.

Risk: Scripts can process broad folders and write to caller-provided output paths without strong path containment or overwrite protection.

Mitigation: Use explicit safe input and output directories, avoid broad folder targets, and keep backups of existing accounting files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akkualle/skills/akkualle-accounting-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/akkualle)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; scripts can produce JSON receipt analysis, Markdown or CSV reports, DATEV CSV exports, and PDF invoices.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may contain sensitive financial data and should be reviewed before sharing or opening in spreadsheet software.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
