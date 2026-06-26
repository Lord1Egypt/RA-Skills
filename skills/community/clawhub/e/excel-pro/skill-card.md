## Description: <br>
Excel is a spreadsheet diagnostic engine that selects the best tool, such as a formula, pivot table, cleaning workflow, or VBA, and delivers copy-paste-ready solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIsearch](https://clawhub.ai/user/AGIsearch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Spreadsheet users, finance analysts, and operations teams use this skill to diagnose spreadsheet problems and choose resilient formulas, pivot tables, cleaning workflows, modeling structures, or VBA automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated VBA macros can modify workbooks, reference local file paths, or change data if run without review. <br>
Mitigation: Review macro code, file paths, ranges, and workbook changes; keep backups; run only macros the user understands and explicitly chooses to execute. <br>
Risk: Spreadsheet guidance can produce incorrect results when source data assumptions, platform version, or workbook structure are wrong. <br>
Mitigation: Verify target platform, source structure, formulas, pivots, and outputs against representative data before relying on the workbook. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AGIsearch/excel-pro) <br>
- [README.md](README.md) <br>
- [examples.md](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with structured assessment sections, formulas, optional VBA code, build steps, warnings, and next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include copy-paste-ready spreadsheet formulas or VBA macros; generated macros require review before execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
