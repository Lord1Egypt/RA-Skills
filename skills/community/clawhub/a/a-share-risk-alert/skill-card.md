## Description:

A Share Risk Alert helps agents screen A-share stocks for ST, delisting, and financial risk signals using cn-stock-data financial data, quote data, and web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzswk](https://clawhub.ai/user/yzswk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for concise or report-style screening of individual A-share stock risk, including profitability, cash flow, leverage, audit, pledge, related-party transaction, and delisting-warning signals. The skill is research support and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad phrases such as 'is it safe' may trigger the skill outside an A-share stock context.

Mitigation: Clarify the target stock name or code and confirm the user wants A-share risk screening before producing the report.

Risk: Financial statements, quote data, and web search results may lag current market disclosures.

Mitigation: State the reporting period and data availability, verify important conclusions against latest disclosures, and avoid fabricating unavailable data.

Risk: Risk labels and investment caution language could be mistaken for investment advice.

Mitigation: Frame outputs as research support, explain triggered signals, and keep buy, sell, or hold decisions outside the skill output.

## Reference(s):

- [A股风险预警参考指南](references/risk-alert-guide.md)
- [A Share Risk Alert on ClawHub](https://clawhub.ai/yzswk/skills/a-share-risk-alert)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown risk report or brief summary with risk labels and supporting data notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formal mode produces a detailed stock risk report; brief mode returns risk level, triggered signals, and a short conclusion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
