## Description: <br>
Build .xlsx files with formulas, merged cells, data validation, conditional formatting, pivot tables, and charts. Use when creating Excel spreadsheets, financial tables, data entry forms, or any structured .xlsx deliverable requiring formulas or formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmy974](https://clawhub.ai/user/jimmy974) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate structured Excel workbooks for reports, financial tables, budgets, invoices, data entry forms, and pivot-ready datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workbook generation can overwrite or modify existing spreadsheets when the output path targets an existing file. <br>
Mitigation: Confirm the absolute output path before saving, use a copy when modifying existing workbooks, and report path conflicts before returning results. <br>
Risk: Formulas and workbook content depend on user-provided data and instructions and may be inaccurate if left unreviewed. <br>
Mitigation: Review generated formulas, ranges, validation rules, and chart references before sharing or using the workbook for decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with Python code snippets and generated .xlsx workbook paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the absolute path to the saved workbook and, for multi-sheet workbooks, a brief summary of sheet names and row counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
