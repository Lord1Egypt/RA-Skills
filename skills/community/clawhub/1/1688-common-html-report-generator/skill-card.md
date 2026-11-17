## Description:

Converts text-based data reports into interactive HTML dashboards through a Python ReportBuilder template and chart component workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn market analysis, operations reviews, industry research, and sales summaries into interactive HTML dashboards while preserving source sections, tables, key figures, and written insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can execute unsanitized HTML or JavaScript from input data.

Mitigation: Use trusted data or review and sanitize text fields before sharing generated reports, especially on authenticated or sensitive origins.

Risk: Generated reports load ECharts from a remote CDN script.

Mitigation: Bundle ECharts locally or use an integrity-pinned trusted script before distributing or hosting reports.

## Reference(s):

- [Chart Bindbook](references/chart-bindbook.md)
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-common-html-report-generator)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with Python code and shell commands; generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local HTML dashboards using a bundled template and ECharts-based chart components.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
