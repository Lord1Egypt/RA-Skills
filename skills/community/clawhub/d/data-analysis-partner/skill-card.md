## Description:

Data Analysis Partner analyzes CSV and Excel files from a natural-language request and produces a self-contained HTML report with interactive ECharts visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1992huanghai](https://clawhub.ai/user/1992huanghai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to inspect CSV or Excel datasets, generate statistical summaries and rule-based insights, and create browser-viewable reports with interactive charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute injected JavaScript from malicious spreadsheet or user-supplied content.

Mitigation: Review generated reports before opening or sharing them, avoid untrusted input files, and keep sensitive reports in a private folder.

Risk: Reports load ECharts from jsDelivr when opened, which can create an external network request.

Mitigation: Use a locally bundled or cached ECharts library for sensitive or offline workflows.

Risk: Python dependency resolution may rely on the local environment.

Mitigation: Use a pinned virtual environment with reviewed versions of pandas, numpy, openpyxl, and xlrd.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1992huanghai/skills/data-analysis-partner)
- [Publisher Profile](https://clawhub.ai/user/1992huanghai)
- [Artifact README](artifact/README.md)
- [ECharts CDN Dependency](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON tool result plus a self-contained HTML report with interactive ECharts charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 with pandas and numpy; Excel support uses openpyxl and xlrd; generated reports may load ECharts from jsDelivr when opened.]

## Skill Version(s):

1.0.2 (source: release evidence, manifest.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
