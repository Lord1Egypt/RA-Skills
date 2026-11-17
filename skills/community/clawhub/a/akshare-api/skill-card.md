## Description:

This skill helps agents answer Chinese-language market-data questions for A-shares, Hong Kong stocks, U.S. stocks, indexes, sectors, funds, convertible bonds, news, and research reports by normalizing the query and calling a hosted AkShare service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize Chinese-language securities market data and basic analysis for A-shares, Hong Kong stocks, U.S. stocks, indexes, sectors, funds, convertible bonds, news, and research reports. It is not intended for order placement, trading execution, guaranteed returns, or personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data queries are sent to the hosted service at akshare.devtool.uk.

Mitigation: Use the skill only when users are comfortable sending query text to that service, and avoid including sensitive portfolio or holdings details.

Risk: Portfolio-related prompts can trigger local operations that run an unbundled sibling script and may change local holdings data.

Mitigation: Do not expose portfolio-management use unless the feature has been removed or separately reviewed with clear confirmation and script-integrity controls.

Risk: Market data may be delayed, incomplete, or unavailable for some interfaces or time periods.

Mitigation: Present outputs as informational market data, include freshness and mapping caveats when relevant, and avoid personalized investment recommendations or return promises.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/akshare-api)
- [AkShare stock data documentation](https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt)
- [Hosted AkShare service](https://akshare.devtool.uk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summaries with optional shell command snippets and structured data highlights]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should summarize query results concisely, preserve key numeric values, and include data freshness or mapping caveats when relevant.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
