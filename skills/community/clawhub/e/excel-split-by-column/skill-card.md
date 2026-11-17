## Description:

Splits a local Excel workbook by a selected or auto-detected column into separate worksheets or XLSX files, with sanitized names and a summary of row counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dont4getme-2](https://clawhub.ai/user/dont4getme-2)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, operations teams, and other spreadsheet users use this skill to split a large local Excel workbook by department, city, category, status, or another grouping column. It helps prepare grouped worksheets or separate XLSX files for review or distribution while preserving the source workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local spreadsheets and writes derived Excel files that may contain sensitive source data.

Mitigation: Run it only on spreadsheets intended for processing and review the output directory before sharing generated files.

Risk: Spreadsheet processing depends on the local Python environment and the openpyxl package.

Mitigation: Install dependencies in a virtual environment with pinned package versions where possible.

Risk: Splitting by column can create multiple files or sheets whose names are derived from spreadsheet values.

Mitigation: Use an explicit output directory and inspect generated names and grouping statistics before distribution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands, plain-text split statistics, and generated XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local Excel outputs in either one workbook with multiple sheets or multiple XLSX files, and reports per-group row counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
