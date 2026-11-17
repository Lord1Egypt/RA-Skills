## Description:

Find products and seller offers across online shops and run scoped extraction jobs on supported Amazon, Walmart US, and listed store pages using the datawebot service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wakmagpie](https://clawhub.ai/user/wakmagpie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can find products, compare sellers and prices, and request focused extraction from supported commerce pages. The skill presents linked product data and dated price snapshots, but is not for price history or guaranteed-current pricing.

### Deployment Geography for Use:

Global, with Walmart extraction limited to the US and Amazon extraction available in 10 supported countries.

## Known Risks and Mitigations:

Risk: Sign-in setup may store credentials locally or change MCP client configuration.

Mitigation: Review the linked setup guide before authorizing credential storage or configuration changes; never paste or print credentials.

Risk: Product searches and extraction inputs are sent to the datawebot service, and extraction Jobs consume credits.

Mitigation: Keep submitted searches and URLs within the user's requested scope, and confirm the Job credit budget before submitting.

Risk: Returned prices are dated snapshots and may not reflect current prices.

Mitigation: Present the retrieval time and do not describe results as guaranteed-current pricing.

## Reference(s):

- [Agent documentation](https://www.datawebot.com/docs/agents)
- [MCP server](https://mcp.datawebot.com/mcp)
- [Coding-agent setup guide](https://mcp.datawebot.com/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions]

**Output Format:** [Structured product and seller results presented as Markdown cards, plus setup and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are dated snapshots and are not guaranteed current.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
