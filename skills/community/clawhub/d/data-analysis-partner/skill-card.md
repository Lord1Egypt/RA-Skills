## Description: <br>
Analyzes CSV or Excel files from natural-language requirements and produces a self-contained HTML report with interactive ECharts visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1992huanghai](https://clawhub.ai/user/1992huanghai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and analysts can use this skill to inspect CSV or Excel datasets, generate statistical summaries and visualizations, and receive a shareable HTML analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can run untrusted spreadsheet content when opened. <br>
Mitigation: Use the skill only with datasets you trust, and avoid opening reports from untrusted CSV or Excel files on sensitive machines until data-derived HTML and script content is escaped. <br>
Risk: Generated reports load chart code from jsDelivr when opened. <br>
Mitigation: Use the reports only where contacting jsDelivr is acceptable, or require a bundled or offline chart library for sensitive and offline workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1992huanghai/data-analysis-partner) <br>
- [ECharts library loaded by generated reports](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, analysis, files, shell commands] <br>
**Output Format:** [JSON result with an HTML report file path, summary, insights, chart count, and open command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an HTML report to the configured output directory; generated reports load ECharts from jsDelivr when opened.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and CHANGELOG, released 2026-03-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
