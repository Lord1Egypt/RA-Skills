## Description: <br>
Excel/CSV data quality diagnosis and interactive charting for supported spreadsheet files, with local profiling, quality scanning, scoring, and ECharts visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect CSV, TSV, XLSX, and XLS files, identify data quality problems, score spreadsheet readiness, and generate basic chart images. It is useful for data review workflows where the agent should ask for an explicit action before processing a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent reads spreadsheet contents and may show representative cell values in the conversation. <br>
Mitigation: Use the skill only with files the user is permitted to disclose, and avoid sharing outputs that expose sensitive cell values. <br>
Risk: The advanced chart route can leave the local-only workflow by delegating to ChartGen. <br>
Mitigation: Use local quality checks and basic charts by default; choose Advanced Chart/ChartGen only after separately reviewing that skill and confirming external processing is allowed. <br>


## Reference(s): <br>
- [Excel Data Quality Check on ClawHub](https://clawhub.ai/chartgen-ai/excel-data-quality) <br>
- [Quality Check Reference](references/quality-check.md) <br>
- [Chart Reference](references/chart.md) <br>
- [Advanced Chart Reference](references/advanced-chart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON chart configurations, and generated PNG chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local quality and basic chart paths use spreadsheet contents and may surface representative cell values; the advanced chart route can delegate to ChartGen when separately installed and configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
