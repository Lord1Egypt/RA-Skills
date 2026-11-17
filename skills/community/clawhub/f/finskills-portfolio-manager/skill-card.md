## Description:

Monitor and rebalance a multi-asset portfolio using real-time quotes, sector allocation, and risk metrics from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to analyze US equity holdings, compare portfolio performance against benchmarks, identify sector and concentration risks, and prepare rebalancing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio holdings, cost basis, and ticker symbols may reveal sensitive financial information in the agent session or to Finskills market-data endpoints.

Mitigation: Share only the portfolio details needed for the requested analysis, avoid unnecessary cost-basis data, and confirm that use of the Finskills API is acceptable for the portfolio data involved.

Risk: Market quotes can be delayed and beta values may be approximated, which can make performance, risk, and rebalance outputs imperfect.

Mitigation: Treat the report as analytical guidance, verify important figures against authoritative market data, and review any rebalance suggestion before acting.

Risk: The skill can suggest buy or sell quantities but does not connect to brokerage accounts or execute trades.

Mitigation: Keep all trade execution outside the skill and require human review before placing orders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/finskills-portfolio-manager)
- [Publisher profile](https://clawhub.ai/user/finskills)
- [Project homepage](https://github.com/finskills/portfolio-manager)
- [Finskills API](https://finskills.net)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown portfolio report with holdings, allocation, risk flags, market context, and rebalancing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-derived market data, estimated beta values, benchmark comparisons, and share-quantity suggestions when user inputs support them.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
