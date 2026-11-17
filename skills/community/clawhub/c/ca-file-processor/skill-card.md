## Description:

Processes financial documents for Indian CA firms by routing PDF, Excel, CSV, JPG, and PNG uploads to local parsers or OCR and extracting text, tables, and fields such as GSTIN, invoice numbers, totals, and dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[purvik6062](https://clawhub.ai/user/purvik6062)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and accounting teams can use this skill to process uploaded Indian financial, tax, banking, and audit documents, then use the extracted text, tables, field values, and summaries to answer document-specific questions. The skill is most relevant when an agent needs local processing for PDFs, spreadsheets, CSV exports, and scanned document images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial, tax, banking, and payroll data can be processed automatically from uploads and passed into the agent context.

Mitigation: Use the skill only for explicit user-initiated uploads, disable broad automatic attachment triggers, and prefer redacted or summary-only outputs for PAN, GSTIN, account, and payroll fields.

Risk: Untrusted document parsing and OCR can expose environments to stale or vulnerable parsing dependencies.

Mitigation: Review the skill before use with real client records and update vulnerable or stale parser dependencies before processing untrusted files.

Risk: OCR and field extraction can produce low-confidence or incorrect numeric values.

Mitigation: Flag low-confidence OCR results and require user confirmation before relying on extracted numeric fields.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/purvik6062/skills/ca-file-processor)
- [Declared Project Homepage](https://github.com/purvik6062/ca-file-processor)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON dictionaries with extracted text, tables, field values, summaries, confidence labels, and error fields for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include large document contents and are capped or previewed by individual processors for CSV, Excel, PDF, and image inputs.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
