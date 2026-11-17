## Description:

将工作簿中的多个表格合并为一个表格，基于指定的两列（项目名称及特征、生产规格）进行匹配汇总，合计件数和数量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smxtx](https://clawhub.ai/user/smxtx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to merge multiple Excel shipment or statistics worksheets into one summarized workbook. It matches rows by project name/features and production specification, totals count and quantity columns, filters irrelevant rows, and sorts by configured Chinese construction keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook text copied into the output could preserve attacker-controlled spreadsheet formulas.

Mitigation: Sanitize names and specifications that begin with =, +, -, @, tab, carriage return, or newline before writing the output workbook, and review the skill before using untrusted workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smxtx/skills/excel-multi-table-merge)
- [ClawHub publisher profile](https://clawhub.ai/user/smxtx)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance, Files]

**Output Format:** [Markdown with Python code and workbook file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or adapts local openpyxl-based workbook merge logic and may generate a summarized .xlsx workbook.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
