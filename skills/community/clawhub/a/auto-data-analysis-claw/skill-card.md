## Description:

Automates financial and business data analysis, including data profiling, cleaning, KPI calculations, trend and variance analysis, and professional report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to inspect CSV or Excel financial and operational data, calculate KPIs, identify trends and variances, and generate Markdown or HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can turn untrusted business data into executable browser content.

Mitigation: Prefer Markdown output for untrusted data, avoid opening generated HTML reports in privileged browser sessions or shared authenticated origins, and keep input and output paths limited to a working folder.

Risk: Financial and business datasets may contain sensitive information.

Mitigation: Review data handling before use, apply appropriate redaction, and avoid broad input or output paths that could expose or overwrite sensitive files.

## Reference(s):

- [Business Analysis Patterns](references/business-analysis-patterns.md)
- [Financial Metrics](references/financial-metrics.md)
- [Report Templates](references/report-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/auto-data-analysis-claw)
- [Publisher Profile](https://clawhub.ai/user/tujinsama)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands; generated reports may be Markdown or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CSV or Excel inputs and may write cleaned data, analysis output, and report files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
