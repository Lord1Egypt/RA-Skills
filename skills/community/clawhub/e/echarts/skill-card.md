## Description: <br>
Create Apache ECharts option JSON, standalone HTML chart pages, and export-ready chart artifacts from CSV, TSV, JSON tables, or existing option configs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data-focused agents use this skill to turn chart ideas, table data, or existing ECharts options into reusable ECharts configuration, preview pages, and export-ready chart artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart pages load the ECharts runtime from trusted external or user-specified URLs. <br>
Mitigation: Use a trusted local or approved ECharts runtime URL for confidential work, and avoid opening generated chart.html files from untrusted sources. <br>
Risk: Local scripts read user-selected data files and write chart artifacts that may include sensitive input data. <br>
Mitigation: Keep generated chart folders private, sanitize confidential data before sharing artifacts, and review chart.data.json and chart.html before publication. <br>


## Reference(s): <br>
- [Apache ECharts](https://echarts.apache.org/) <br>
- [Chart Selection](references/chart-selection.md) <br>
- [Option Patterns](references/option-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jvy/echarts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands, plus generated JSON, HTML, PNG, or SVG chart artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifact directories can include chart.spec.json, chart.option.json, chart.data.json, chart.html, manifest.json, and optional exported image files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
