## Description:

从Excel/PDF文件分析财务数据，生成含趋势图的HTML分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individual investors, analysts, and automation users use this skill to extract financial data from local Excel or PDF files, calculate basic financial metrics, and produce an HTML report with trend visuals. It is intended for single-file report generation rather than real-time streams, batch analysis, or peer benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial files may be processed in the agent environment.

Mitigation: Use the skill only with financial files approved for that environment, keep generated reports in a private directory, and delete outputs when no longer needed.

Risk: The artifact mixes local report generation with broad command, API, network, and information-retrieval claims that are not clearly scoped.

Mitigation: Review the skill before installation and do not allow API or network use unless the destination, data sent, and purpose have been confirmed.

Risk: Generated financial analysis and forecast markers may be incomplete or misleading.

Mitigation: Treat reports and simple trend extrapolations as decision support only, and verify conclusions against source filings or a qualified financial review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/finance-report-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash and YAML examples; generated report output is HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free version is described as single-file, HTML-only output with basic trend forecasting.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
