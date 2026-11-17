## Description:

Generate professional Word, Excel, and PDF documents with rich formatting, tables, images, and layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnblxj](https://clawhub.ai/user/lnblxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create formatted Word documents, Excel spreadsheets, and PDFs from JSON configurations for reports, invoices, data exports, templates, and similar document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documents can read templates or images and write output files at configured paths.

Mitigation: Use safe, intended input and output paths and review them before running a generation script.

Risk: Spreadsheet formulas supplied from untrusted data may execute or recalculate when the workbook is opened.

Mitigation: Review spreadsheet formulas before generation and treat untrusted formula-like values as text unless formulas are explicitly intended.

Risk: Dependency or font differences can affect local rendering behavior, especially for PDF and multilingual output.

Mitigation: Install the skill in a virtual environment with pinned dependencies and verify generated documents before distribution.

## Reference(s):

- [Word document configuration schema](references/word_schema.md)
- [Excel spreadsheet configuration schema](references/excel_schema.md)
- [PDF document configuration schema](references/pdf_schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and generated DOCX/XLSX/PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to user-selected output paths and may use local templates, images, fonts, and Python document libraries.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
