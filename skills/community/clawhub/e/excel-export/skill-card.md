## Description: <br>
Generate polished .xlsx workbooks from structured JSON with multiple sheets, frozen headers, filters, typed columns, formulas, totals, and French/Morocco formatting defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xvespertine](https://clawhub.ai/user/0xvespertine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured JSON, database results, or context-derived data into polished Excel workbook files for reporting and delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A mistaken input JSON file or output path could produce the wrong workbook or write the file somewhere unintended. <br>
Mitigation: Review the JSON input path and output path before execution, and prefer the documented export directory for generated workbooks. <br>
Risk: Formula columns are carried into the workbook and recalculated by the recipient's Excel client. <br>
Mitigation: Use formula definitions only from trusted sources and review formula columns before sharing the workbook. <br>
Risk: The setup command installs xlsxwriter without a pinned version. <br>
Mitigation: Pin xlsxwriter in controlled or reproducible environments. <br>


## Reference(s): <br>
- [SQL to Excel Export Recipe](references/SQL_TO_EXCEL_RECIPE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/0xvespertine/excel-export) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [.xlsx workbook files from JSON input, with a JSON success summary on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates new workbooks only; it does not read, edit, or preserve existing Excel files.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
