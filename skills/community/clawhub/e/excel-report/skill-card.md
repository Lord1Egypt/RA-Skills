## Description: <br>
Generates styled Excel workbooks from CSV, JSON, or Excel data using bundled industry report templates, KPI formulas, and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, operations teams, and developers use this skill to turn tabular business data into multi-sheet Excel reports for retail, manufacturing, finance, internet, medical, and general KPI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template formula handling can execute unsafe expressions. <br>
Mitigation: Use only trusted bundled templates and avoid third-party or edited templates until formula evaluation is replaced with a safe parser. <br>
Risk: Automatic file opening can launch generated output on the host. <br>
Mitigation: Run the skill in a controlled environment and review output paths before enabling automatic opening. <br>
Risk: Reports may process sensitive business, financial, or medical data. <br>
Mitigation: Use approved data-handling controls and avoid unnecessary sensitive data in input files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sqlskills/excel-report) <br>
- [Artifact usage guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with command examples; generated Excel workbooks as .xlsx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports bundled JSON templates, workbook styling, KPI formulas, charts, batch generation, and optional email delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
