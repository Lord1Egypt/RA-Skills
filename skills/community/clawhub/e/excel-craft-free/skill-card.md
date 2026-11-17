## Description: <br>
Excel Craft Free helps agents generate local Python/openpyxl workflows for Excel workbooks with multiple sheets, formulas, charts, and basic formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and spreadsheet users can use this skill to ask an agent for repeatable Excel workbook generation, including reports, inventory sheets, project trackers, and personal finance workbooks. It is best suited to explicit local workbook-generation tasks rather than broad document conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to generate and execute local Python/openpyxl scripts. <br>
Mitigation: Use it only for explicit workbook-generation tasks, specify the intended output path, and review generated code before execution. <br>
Risk: The artifact contains broad wording around document conversion and content extraction that is wider than the Excel-generation use case. <br>
Mitigation: Scope use to Excel workbook creation and avoid relying on the skill for general document conversion or content extraction. <br>
Risk: Generated formulas, chart ranges, or formatting can be incorrect for the user's data. <br>
Mitigation: Open and verify generated workbooks in the target office application before using the results for operational or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/excel-craft-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python code blocks and shell commands; generated .xlsx files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python/openpyxl workflow; review generated code before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
