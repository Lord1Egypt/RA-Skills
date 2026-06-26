## Description: <br>
Spreadsheet Engineering helps agents design, audit, document, and automate reliable spreadsheets for financial models, dashboards, data systems, and operational templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, finance teams, and developers use this skill to plan spreadsheet architecture, write and review formulas, build dashboards, add validation, and decide when to migrate from spreadsheets to dedicated systems. It applies across Google Sheets, Excel 365, and LibreOffice workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or copied Apps Script and VBA automation can change workbook data or run with access to sensitive spreadsheet contents. <br>
Mitigation: Test automation on a copy first, keep a backup or named version snapshot, and review the code before running it against live files. <br>
Risk: Automation snippets may send email, move rows, or delete rows if adapted without safeguards. <br>
Mitigation: Verify recipients and data sensitivity, and add confirmation or dry-run behavior before enabling destructive or outbound actions. <br>
Risk: Spreadsheet formulas and dashboards can produce misleading results when assumptions, ranges, or imported data are wrong. <br>
Mitigation: Use the skill's validation, documentation, named-range, and review practices before relying on outputs for business decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-spreadsheet-engineering) <br>
- [Publisher Profile](https://clawhub.ai/user/1kalin) <br>
- [README](README.md) <br>
- [Skill Documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with spreadsheet formulas, rubric tables, YAML-style planning templates, and Apps Script or VBA code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are platform-aware for Google Sheets, Excel 365, and LibreOffice and should be reviewed before applying automation to live workbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
