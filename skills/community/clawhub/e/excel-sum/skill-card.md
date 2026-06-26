## Description: <br>
计算 Excel 文件第一列数值的总和，当用户请求对 Excel 文件进行求和、统计第一列总和或类似操作时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujialin1517-source](https://clawhub.ai/user/liujialin1517-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to total numeric values from the first column of an Excel spreadsheet and report the total, counted cells, and skipped non-numeric cells. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the specific Excel file path supplied by the user, which may expose spreadsheet contents to the local execution environment. <br>
Mitigation: Use the skill only with spreadsheets intended for this calculation and avoid unrelated or sensitive files. <br>
Risk: The script depends on openpyxl being installed from a trusted package source. <br>
Mitigation: Install openpyxl from a trusted package index and verify the runtime environment before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujialin1517-source/excel-sum) <br>
- [Publisher profile](https://clawhub.ai/user/liujialin1517-source) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text calculation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the numeric sum, number of summed cells, and count of skipped empty or non-numeric cells.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
