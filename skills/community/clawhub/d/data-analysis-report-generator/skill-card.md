## Description:

Intelligent data analysis report generator that auto-identifies Excel/CSV data structure, performs multi-dimensional analysis, and generates professional HTML reports with ECharts interactive charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to turn Excel or CSV files into HTML data analysis reports with statistics, interactive charts, and narrative insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can execute unsafe JavaScript from spreadsheet-derived names or labels.

Mitigation: Use trusted spreadsheets only, escape all report data before rendering, and open generated reports in a controlled browser context.

Risk: Generated reports load ECharts from an external CDN.

Mitigation: Bundle ECharts locally or use an integrity-pinned, reviewed dependency source before deployment.

Risk: The report template uses dynamic JavaScript evaluation during chart initialization.

Mitigation: Replace eval-based initialization with direct chart setup code and review generated chart options before opening reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/data-analysis-report-generator)
- [Chart Type Selection Guide](references/chart_types.md)
- [Report Style Reference](references/report_styles.md)
- [Style Variables](references/style_variables.json)
- [ECharts 5.5.0 CDN](https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML/JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a self-contained HTML report using ECharts; intermediate analysis and chart configuration are JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
