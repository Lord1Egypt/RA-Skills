## Description:

Build .xlsx files with formulas, merged cells, data validation, conditional formatting, pivot tables, and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmy974](https://clawhub.ai/user/jimmy974)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to create structured Excel workbooks such as spreadsheets, financial tables, data entry forms, and formatted reports with formulas, validation, pivot-ready data, and charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to create or modify Excel files.

Mitigation: Confirm the intended output path and review generated workbooks before using or sharing them.

Risk: The artifact suggests installing openpyxl or xlsxwriter without pinned versions when dependencies are missing.

Mitigation: Install pinned dependency versions in a dedicated virtual environment before running generated workbook code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmy974/skills/excel-builder)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and generated .xlsx file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Excel files on disk and return sheet names, row counts, and absolute output paths.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
