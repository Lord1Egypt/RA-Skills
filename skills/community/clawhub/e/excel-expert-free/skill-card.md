## Description: <br>
Excel Expert Free helps agents diagnose spreadsheet tasks and return copy-ready formulas, pivot-table setups, data-cleaning steps, compatibility notes, and failure warnings for Excel and related spreadsheet tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, operations teams, analysts, and finance users use this skill to choose robust spreadsheet methods for lookups, conditional logic, cleaning, summaries, automation, modeling, and visualization. The skill produces formulas, pivot-table layouts, cleaning workflows, compatibility notes, and failure-point checks for Excel 365, older Excel versions, Google Sheets, Numbers, and LibreOffice Calc. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad write and exec authority exceeds the needs of a spreadsheet-advice skill. <br>
Mitigation: Install only after write and exec use is removed or tightly limited, and require review before any command execution or file modification. <br>
Risk: Unclear activation and unrelated trigger text could cause the skill to run outside spreadsheet tasks. <br>
Mitigation: Narrow triggers to Excel, spreadsheet, workbook, formula, pivot-table, and data-cleaning requests before deployment. <br>
Risk: Generated formulas, macros, or cleaning steps could change business data or produce misleading results. <br>
Mitigation: Test outputs on copies of workbooks, review formulas and macros before use, and validate results against known rows or summaries. <br>
Risk: Credential-backed data sources may expose sensitive spreadsheet or database data if connected carelessly. <br>
Mitigation: Use least-privilege credentials, avoid sharing secrets in prompts or files, and review any data-source connection guidance before applying it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/excel-expert-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with spreadsheet formulas, optional code snippets, and step-by-step configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic classification, recommended spreadsheet tools, compatibility alternatives, and likely failure points.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
