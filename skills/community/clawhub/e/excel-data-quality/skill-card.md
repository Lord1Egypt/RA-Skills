## Description:

Helps agents profile CSV, TSV, XLSX, and XLS spreadsheet data, run data quality checks, and generate charts from selected datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agent users use this skill to inspect spreadsheet structure, diagnose data quality issues, score datasets, and create basic visualizations before downstream analysis or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced Chart delegates work to ChartGen and may use an external API despite local-only language elsewhere in the skill.

Mitigation: Use Advanced Chart only after confirming ChartGen is installed, configured, and trusted for the spreadsheet contents being processed.

Risk: Chart commands can write generated image files.

Mitigation: Direct chart outputs to a controlled directory and review generated file paths before sharing or reusing them.

Risk: Spreadsheet previews, analysis summaries, and generated charts may expose sensitive data.

Mitigation: Avoid using sensitive spreadsheets unless local previews and chart outputs are acceptable for the intended audience.

## Reference(s):

- [Excel Data Quality Check](https://clawhub.ai/chartgen-ai/skills/excel-data-quality)
- [Publisher Profile](https://clawhub.ai/user/chartgen-ai)
- [OpenClaw](https://openclaw.com)
- [Quality Check Reference](references/quality-check.md)
- [Chart Reference](references/chart.md)
- [Advanced Chart Reference](references/advanced-chart.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command examples, parsed quality summaries, chart configuration JSON, and generated file paths for chart images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG chart files when chart rendering is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
