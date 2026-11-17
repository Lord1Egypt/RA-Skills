## Description:

Create formatted Excel report workbooks from CSV files using openpyxl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ms-yun](https://clawhub.ai/user/ms-yun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to convert CSV files into formatted Excel workbooks with styling, numeric totals, table filters, and a basic chart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV content from untrusted sources can carry formula-prefixed values into a generated workbook.

Mitigation: Install and use this skill only for trusted CSV files, or review and sanitize formula-prefixed fields before opening or sharing the workbook.

Risk: Installing an unpinned openpyxl dependency globally can expose the user to dependency drift.

Mitigation: Run the conversion in an isolated environment with a pinned openpyxl version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ms-yun/skills/excel-report-msy-v1)

## Skill Output:

**Output Type(s):** [files, shell commands, markdown, guidance]

**Output Format:** [Markdown guidance with shell commands and generated .xlsx workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks may include formulas, table formatting, filters, frozen headers, autosized columns, and a simple bar chart for the first numeric column.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
