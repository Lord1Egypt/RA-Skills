## Description:

Analyzes A-share portfolio holdings for concentration, industry and style exposure, risk indicators, return attribution, and rebalancing suggestions using cn-stock-data market and financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzswk](https://clawhub.ai/user/yzswk)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agents use this skill to review A-share portfolios, compare holdings against benchmarks such as the CSI 300, identify concentration and exposure risks, and prepare formal or brief rebalancing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio holdings can reveal sensitive financial information, including stock codes, position sizes, cost basis, and purchase dates.

Mitigation: Share only the minimum holdings information needed for analysis and avoid account identifiers, brokerage credentials, or unrelated personal data.

Risk: Portfolio recommendations depend on supplied holdings and market or financial data and may be incomplete or stale.

Mitigation: Verify key data points before acting and treat the output as decision support rather than a precise return forecast.

## Reference(s):

- [Portfolio Guide](references/portfolio-guide.md)
- [A Share Portfolio on ClawHub](https://clawhub.ai/yzswk/skills/a-share-portfolio)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown portfolio analysis with tables and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports formal institutional-style reports and brief personal portfolio reviews.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
