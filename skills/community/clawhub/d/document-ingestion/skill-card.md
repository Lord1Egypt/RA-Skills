## Description:

Process raw accounting source documents such as PDFs, CSVs, bank statements, invoices, and receipts into standardized transaction records for QBO import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting operators and agent users use this skill to process document drops for month-end close into standardized QBO-ready transaction records. The skill helps categorize transactions, identify duplicates, flag exceptions, and prepare import-ready outputs for accounting review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial documents and QBO-related data.

Mitigation: Run it only in trusted projects and keep QBO tokens and source financial documents in access-controlled locations.

Risk: Dependency installation and optional OCR or QBO tooling can affect extraction quality and local environment exposure.

Mitigation: Use a virtual environment or container, pin dependency versions where possible, and prefer --no-qbo-coa or --sandbox unless live QBO chart data is needed.

Risk: Auto-categorization, duplicate detection, and OCR/PDF extraction can produce records that still require accounting review.

Mitigation: Review the Exceptions, Duplicates, and confidence fields before importing generated CSVs into QBO.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and generated workbook/CSV file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pipeline outputs include an Excel workbook, QBO import CSV, exception flags, duplicate flags, category confidence, and CDC cache metrics.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
