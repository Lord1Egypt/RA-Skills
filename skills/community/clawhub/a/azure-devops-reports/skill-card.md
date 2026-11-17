## Description:

Read Azure DevOps projects, teams, team members, saved queries, and work items securely; run WIQL-based reporting; and export spreadsheet-ready reports with summaries and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webspeaks](https://clawhub.ai/user/webspeaks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and delivery teams use this skill to inspect Azure DevOps projects, teams, sprints, saved queries, and work items, then generate local reporting outputs for progress and workload analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Azure DevOps work data through a personal access token.

Mitigation: Use a least-privilege PAT with only the required read scopes, store it locally, and avoid sharing generated reports without review.

Risk: Generated CSV or XLSX reports may contain untrusted work-item data.

Mitigation: Review generated files before sharing and avoid opening spreadsheet reports with formula execution enabled when data is untrusted.

Risk: Routine use depends on local tooling and report file paths.

Mitigation: Pin the Python dependency where practical and keep Excel input and output paths confined to the skill workspace.

## Reference(s):

- [Azure DevOps Reports on ClawHub](https://clawhub.ai/webspeaks/skills/azure-devops-reports)
- [API Notes](references/api-notes.md)
- [Field Mapping](references/field-mapping.md)
- [Report Types](references/report-types.md)
- [Charting](references/charting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated report artifacts may be JSON, CSV, or XLSX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AZURE_DEVOPS_ORG and AZURE_DEVOPS_PAT; reports are generated locally.]

## Skill Version(s):

1.0.6 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
