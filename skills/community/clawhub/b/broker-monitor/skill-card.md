## Description:

Generates a weekly monitoring report for US retail brokerage stocks and the broader trading ecosystem, including equity and options volume, crypto markets, exchange market share, and prediction market activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarahwang94712](https://clawhub.ai/user/sarahwang94712)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and finance-focused agents use this skill to refresh weekly monitoring of IBKR, SCHW, HOOD, FUTU, and related market-structure metrics. It produces a Chinese-format Markdown report and updates a structured Excel workbook for recurring broker and trading-ecosystem analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial reports can become stale or misleading if public market data, valuation inputs, or source dates are not refreshed correctly.

Mitigation: Review source dates and citations in the generated report before relying on analysis, especially for real-time market, valuation, and EPS-revision fields.

Risk: The skill may read an uploaded Excel workbook and create updated workbook and report files locally.

Mitigation: Use only the intended workbook, inspect generated files before sharing them, and manage local outputs according to data-retention expectations.

Risk: Dashboard entries may persist locally until cleared.

Mitigation: Clear the dashboard storage when data should no longer be retained or when switching contexts.

Risk: Hardcoded dashboard valuation constants can lag the generated report.

Mitigation: Update valuation constants and flags whenever the dashboard artifact is regenerated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarahwang94712/skills/broker-monitor)
- [Skill workflow](artifact/SKILL.md)
- [Report template](artifact/report-template.md)
- [Excel database structure](artifact/excel-structure.md)
- [Metrics by broker](artifact/metrics-by-broker.md)
- [Dashboard data schema](artifact/dashboard-schema.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown report plus Excel workbook updates, with supporting code or commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local report and workbook outputs; dashboard data may persist locally until cleared.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
