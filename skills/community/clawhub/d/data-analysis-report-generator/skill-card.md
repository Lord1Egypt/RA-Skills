## Description: <br>
Intelligent data analysis report generator. Auto-identifies Excel/CSV data structure (dimensions, metrics, timelines), performs multi-dimensional parallel analysis, and generates professional HTML reports with ECharts interactive charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to analyze trusted Excel or CSV files and generate styled HTML data reports with summary statistics, charts, and concise insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can run unsafe JavaScript from crafted spreadsheet content. <br>
Mitigation: Use the skill only with trusted spreadsheets, review generated reports before opening or sharing them, and sanitize spreadsheet-derived text before browser rendering. <br>
Risk: Generated reports load ECharts from an external CDN by default. <br>
Mitigation: For sensitive or controlled environments, replace the CDN reference with a locally bundled and reviewed ECharts asset. <br>
Risk: Additional custom pandas analysis scripts may be added during report customization. <br>
Mitigation: Review and explicitly approve any custom analysis script before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/openlark/data-analysis-report-generator) <br>
- [Chart Type Selection Guide](artifact/references/chart_types.md) <br>
- [Report Style Reference](artifact/references/report_styles.md) <br>
- [Style Variables](artifact/references/style_variables.json) <br>
- [ECharts 5.5.0 CDN](https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [JSON analysis artifacts and a self-contained HTML report with ECharts chart configuration code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python scripts for CSV/Excel analysis and chart generation; generated reports may load ECharts from a CDN unless adapted for local bundling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
