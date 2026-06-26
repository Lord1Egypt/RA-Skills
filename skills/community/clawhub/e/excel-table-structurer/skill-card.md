## Description: <br>
Structures hierarchical Excel (.xlsx) tables by filling parent values down, preserving group headers, filling group-level fields, and improving filtering and formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations users use this skill to restructure uploaded hierarchical Excel workbooks such as test cases, project task lists, and ledger detail tables. The agent analyzes column roles, prepares a JSON specification, runs the restructuring script, and returns a formatted workbook plus row and group counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded spreadsheets may contain sensitive business data. <br>
Mitigation: Use the skill only on files the user intends the agent to read and transform. <br>
Risk: An incorrect output path or JSON column specification can produce an unwanted workbook layout. <br>
Mitigation: Confirm the input file, output path, worksheet, and column-role JSON specification before running the restructuring script. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/runkecheng/excel-table-structurer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown guidance with JSON specifications and shell commands, plus a generated .xlsx workbook and JSON statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints total row and group counts after saving the restructured workbook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
