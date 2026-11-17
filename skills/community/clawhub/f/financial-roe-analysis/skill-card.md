## Description:

Guides agents to produce structured ROE and DuPont financial analyses for listed companies, covering profitability quality, asset efficiency, leverage risk, benchmarking, and report templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to guide an agent through listed-company financial analysis using ROE decomposition, industry benchmarking, financial quality checks, and standardized quick or deep markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad finance questions and produce analysis that could be mistaken for investment advice.

Mitigation: Confirm the user wants ROE/DuPont financial analysis, retain the non-investment-advice framing, and avoid stock recommendations or price predictions.

Risk: The skill relies on public company data, which may be incomplete, stale, or inconsistently reported across companies.

Mitigation: Use cited annual reports, quarterly reports, or market data sources, and note accounting-policy adjustments before benchmarking companies.

Risk: The artifact appears designed primarily for Chinese-language financial reports.

Mitigation: Confirm the user's preferred language and target market or company identifier before producing the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/financial-roe-analysis)
- [Industry analysis rules](references/industry-rules.md)
- [Financial report template](references/report-template.md)
- [ROE DuPont analysis framework](references/roe-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown financial analysis reports with tables, summaries, risk flags, and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports quick reports up to 3000 Chinese characters and deeper nine-module reports; outputs are financial analysis, not investment advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
