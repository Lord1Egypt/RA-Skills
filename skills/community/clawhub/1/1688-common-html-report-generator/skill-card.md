## Description: <br>
Converts text data reports into interactive HTML dashboards by guiding agents to extract source data, plan chart structure, and generate Python ReportBuilder scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and reporting teams use this skill to turn market analysis, operations reviews, industry research, and sales summaries into interactive HTML data dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include raw HTML from report content. <br>
Mitigation: Sanitize untrusted report text before generating or sharing the HTML output. <br>
Risk: Generated reports load a public charting library from a CDN. <br>
Mitigation: Use a local pinned ECharts copy when reports need offline use or broader distribution. <br>


## Reference(s): <br>
- [Chart Bindbook](references/chart-bindbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-common-html-report-generator) <br>
- [ECharts CDN asset](https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code and shell commands that produce local HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports use a Python template workflow and may load ECharts from a public CDN.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
