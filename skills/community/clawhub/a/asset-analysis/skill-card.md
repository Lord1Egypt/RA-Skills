## Description:

Provides a Chinese-first workflow for analyzing A-share, Hong Kong, and U.S. equities or ETFs using verified market, financial, valuation, technical, and market-regime data to produce a standardized quantitative investment research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to prepare equity and ETF research reports that combine verified market data, financial statements, valuation scenarios, technical indicators, and market-regime calibration. Outputs should be treated as research assistance, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market, financial, or valuation outputs may be incorrect or misleading if source data is stale, incomplete, or unverifiable.

Mitigation: Verify cited market and financial data against authoritative sources before relying on the report, and block report generation when key data cannot be verified.

Risk: Users may mistake research assistance for financial advice.

Mitigation: Present outputs as investment research support and require independent review before making investment decisions.

## Reference(s):

- [ClawHub skill page: asset-analysis](https://clawhub.ai/fize/skills/asset-analysis)
- [Publisher profile: fize](https://clawhub.ai/user/fize)
- [Market skill dependency](../market/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires verified market and financial data; blocks report generation when key data cannot be verified.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
