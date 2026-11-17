## Description:

Financial Edu David guides agents through A-share listed-company financial analysis, from annual report collection and financial statement extraction to metrics, data cross-checking, and HTML dashboard generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidyin1976](https://clawhub.ai/user/davidyin1976)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and education users use this skill to analyze public A-share company financial reports over a 3-5 year period and produce structured data, metric calculations, validation checks, and local visualization dashboards. Outputs should support financial education and analysis workflows, not replace independent investment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial dashboards may include unescaped or unsafely embedded data and external chart libraries.

Mitigation: Treat dashboards as local analysis artifacts unless the HTML is hardened with escaping, safer JSON embedding, and trusted or bundled chart libraries.

Risk: Downloaded reports, extracted statements, and computed metrics can contain parsing errors or source-data mismatches.

Mitigation: Cross-check key financial data against official public sources and independently verify results before relying on the analysis.

Risk: Running collection and extraction scripts in a shared environment can mix generated files with unrelated data.

Mitigation: Install dependencies in a virtual environment and run the workflow in a dedicated output folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidyin1976/skills/financial-edu-david)
- [CNInfo API reference](references/cninfo_api.md)
- [Eastmoney F10 API reference](references/eastmoney_api.md)
- [Financial metrics guide](references/metrics_guide.md)
- [CNInfo annual report query](https://www.cninfo.com.cn/new/hisAnnouncement/query)
- [Eastmoney F10 data API](https://datacenter-web.eastmoney.com/api/data/v1/get)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, Python scripts, Excel workbooks, JSON data files, and local HTML dashboards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local analysis artifacts including downloaded PDFs, collection logs, extracted XLSX statements, core-data JSON, metrics JSON, and an ECharts-based HTML dashboard.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
