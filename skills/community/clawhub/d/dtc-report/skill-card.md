## Description:

Generates DTC monthly, quarterly, or annual business analysis reports with operating summaries, budget-versus-actual comparisons, trend analysis, customer and sales views, warehouse analysis, AI-assisted findings, and HTML output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangliangliang909-oss](https://clawhub.ai/user/zhangliangliang909-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Business, finance, operations, and logistics teams use this skill to generate DTC operating reports from local management, business, warehouse, customer, sales, and budget data. It helps compare actuals against budgets, identify revenue and margin anomalies, and produce management-ready report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local DTC business data and may generate reports containing confidential customer, sales, warehouse, revenue, profit, and budget information.

Mitigation: Install only in trusted workspaces, require explicit input and output paths, and review generated reports before sharing.

Risk: Generated HTML may expose unsafe script or spreadsheet-derived text injection risks.

Mitigation: Escape spreadsheet-derived text in HTML and review the generated HTML before opening or distributing it.

Risk: The report output may depend on an external Chart.js CDN and may overwrite existing report files.

Mitigation: Pin or remove the CDN dependency with integrity protection and require confirmation before writing or overwriting reports.

## Reference(s):

- [DTC data rules](artifact/references/data_rules.md)
- [AI analysis guide](artifact/AI_ANALYSIS_GUIDE.md)
- [Revenue analysis prompt](artifact/prompts/revenue_analysis.txt)

## Skill Output:

**Output Type(s):** [Files, Analysis, HTML, Markdown, Spreadsheet]

**Output Format:** [HTML report, with documented Markdown and Excel output options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local DTC business data and writes report files for the requested period.]

## Skill Version(s):

1.6.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
