## Description:

Automates reading, writing, merging, transforming, and validating Excel (.xlsx/.xls) files for spreadsheet processing, CSV-to-Excel conversion, batch Excel workflows, and report generation from tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheneycheung](https://clawhub.ai/user/cheneycheung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to automate local Excel and CSV workflows such as merging sheets, filtering rows, deduplication, aggregation, validation, template filling, and format-preserving workbook updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Important workbooks can be overwritten or changed when scripts write outputs in place.

Mitigation: Use separate output paths or backups before running scripts on valuable spreadsheets.

Risk: Untrusted CSV or template data can carry formula-like values into generated spreadsheets.

Mitigation: Avoid untrusted spreadsheet inputs unless formula-like values are neutralized before conversion or template fill.

Risk: Runtime behavior depends on installed spreadsheet libraries.

Mitigation: Install in an isolated environment and pin openpyxl, pandas, and xlrd versions before production use.

## Reference(s):

- [Automate Excel skill page](https://clawhub.ai/cheneycheung/skills/automate-excel-0-1-3)
- [Reference documentation](reference.md)
- [Examples](examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python code examples; bundled scripts can create Excel or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file-processing outputs depend on the selected script, input files, and output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
