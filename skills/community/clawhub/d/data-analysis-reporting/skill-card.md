## Description:

Turn raw business data (CSV, SQLite, spreadsheets, pasted tables) into clear analytical summaries, trend analysis, and actionable reports for small business operators, analysts, and decision-makers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitcanadabrett](https://clawhub.ai/user/gitcanadabrett)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as small business owners, operations managers, startup founders, consultants, and non-technical analysts use this skill to turn user-provided business data into plain-language reports, trend analysis, KPI comparisons, and recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business datasets may contain unnecessary personally identifiable information.

Mitigation: Share only the data needed for analysis, review datasets for PII before use, and follow the skill's PII flagging and exclusion workflow.

Risk: Reports may be mistaken for financial, tax, investment, or audit-grade advice.

Mitigation: Treat outputs as analytical guidance, verify material conclusions with qualified reviewers, and keep forecasts and recommendations clearly labeled as assumptions-based.

Risk: Private database access could expose data if credentials or connections are provided unintentionally.

Mitigation: Confirm any database access is intentionally configured and prefer sanitized exports or limited-scope datasets when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gitcanadabrett/skills/data-analysis-reporting)
- [Business Metrics Reference](references/business-metrics.md)
- [Data Quality Checks](references/data-quality-checks.md)
- [Report Templates](references/report-templates.md)
- [Test Prompts](references/test-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with executive summaries, data quality notes, findings, trend analysis, confidence labels, methodology notes, and recommended actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on user-provided data and should label confidence, assumptions, limitations, and data quality concerns.]

## Skill Version(s):

0.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
