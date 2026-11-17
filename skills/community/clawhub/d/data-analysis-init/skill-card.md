## Description:

Initializes long-term PMO Agent data-analysis workflows for Feishu Sheets or local CSV/Excel data, external information enrichment, and standardized analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winsaney](https://clawhub.ai/user/winsaney)

### License/Terms of Use:

MIT-0

## Use Case:

PMO agents and business operations teams use this skill to set up recurring data monitoring, KPI review, anomaly attribution, and decision reports from spreadsheet or local tabular data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business datasets may include confidential metrics, customer data, employee data, or financial information.

Mitigation: Use sanitized sample files where possible and review generated ./user-data files before sharing.

Risk: External search for industry, competitor, or policy context may expose sensitive names, KPIs, or business priorities.

Mitigation: Avoid sensitive identifiers and internal metrics in search queries, and limit searches to necessary public context.

## Reference(s):

- [Schema format example](references/schema-format-example.json)
- [Analysis report template](assets/analysis-report-template.md)
- [ClawHub skill page](https://clawhub.ai/winsaney/skills/data-analysis-init)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create ./user-data/data_schema_config.json, ./user-data/search strategy notes, and recurring analysis reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
