## Description: <br>
Read Azure DevOps projects, teams, team members, saved queries, and work items securely; run WIQL-based reporting; and export spreadsheet-ready reports with summaries and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webspeaks](https://clawhub.ai/user/webspeaks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and project teams use this skill to inspect Azure DevOps projects, teams, sprints, saved queries, and work items, then generate local JSON, CSV, or Excel reports with summaries and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A read-capable Azure DevOps PAT can expose project, team, sprint, and work item data. <br>
Mitigation: Use least-privilege read scopes, keep the .env file private, and install only where local report generation from Azure DevOps data is acceptable. <br>
Risk: Broad trigger examples may use stored Azure DevOps credentials when a request is not clearly about Azure DevOps reporting. <br>
Mitigation: Phrase requests explicitly with Azure DevOps context and confirm the intended project, team, sprint, query, or report before running commands. <br>
Risk: Generated local reports may contain sensitive project or work item information. <br>
Mitigation: Keep generated report files local, restrict output to the skill directory, and review files before sharing them. <br>


## Reference(s): <br>
- [API Notes](references/api-notes.md) <br>
- [Charting](references/charting.md) <br>
- [Field Mapping](references/field-mapping.md) <br>
- [Report Types](references/report-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV, Excel workbook] <br>
**Output Format:** [Markdown guidance with command examples plus generated local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, Python 3, pip3, AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT, and the xlsxwriter Python package.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
