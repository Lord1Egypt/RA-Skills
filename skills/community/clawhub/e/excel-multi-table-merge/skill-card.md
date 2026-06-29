## Description: <br>
将工作簿中的多个表格合并为一个表格，基于指定的两列（项目名称及特征、生产规格）进行匹配汇总，合计件数和数量。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smxtx](https://clawhub.ai/user/smxtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to merge multiple shipment or statistics tables from an Excel workbook into a single summary keyed by project name/features and production specification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A fixed or user-selected output workbook path could replace an existing spreadsheet. <br>
Mitigation: Confirm the input workbook path and verify the output filename before running the merge. <br>
Risk: Local workbook contents are processed by the script. <br>
Mitigation: Use the skill only with Excel files the user is comfortable processing locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smxtx/excel-multi-table-merge) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with Python code and generated Excel workbook output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local Excel workbooks with openpyxl and writes a merged summary workbook.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
