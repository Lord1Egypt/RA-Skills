## Description:

Generate polished .xlsx workbooks from structured JSON -- multiple sheets, frozen headers, filters, typed columns, formulas, totals, and French/Morocco formatting defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xvespertine](https://clawhub.ai/user/0xvespertine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn structured JSON or normalized SQL query results into polished .xlsx workbook files with typed columns, formulas, totals, filters, and French/Morocco formatting defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula-containing workbook specs from untrusted parties can run or fetch external content when opened in a spreadsheet client.

Mitigation: Only generate formula columns from trusted specs, and review formulas before opening or sharing the workbook.

Risk: Unpinned xlsxwriter installations can make workbook generation less reproducible over time.

Mitigation: Pin xlsxwriter in the execution environment when reproducibility matters.

## Reference(s):

- [SQL to Excel Export Recipe](references/SQL_TO_EXCEL_RECIPE.md)
- [Excel Export ClawHub release page](https://clawhub.ai/0xvespertine/skills/excel-export)

## Skill Output:

**Output Type(s):** [files, json, shell commands, configuration, guidance]

**Output Format:** [XLSX workbook files plus a JSON success summary; supporting guidance is Markdown with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates new workbooks only; it does not read, edit, or preserve existing Excel files.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
