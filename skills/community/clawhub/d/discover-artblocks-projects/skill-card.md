## Description:

Browse, search, and explore Art Blocks projects, collections, and collector portfolios using artblocks-mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryley-o](https://clawhub.ai/user/ryley-o)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents in finding Art Blocks projects, live mints, upcoming drops, artist portfolios, and collector wallet summaries across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may move from discovery into broader GraphQL or purchase-related tool references outside the stated discovery tool set.

Mitigation: Keep use informational by default and require explicit user direction before following purchase-related or broader data-query paths.

Risk: Collector username lookups can aggregate holdings across linked wallets.

Mitigation: Only request or summarize wallet and username portfolio data when the user has clearly asked for that collector view.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryley-o/skills/discover-artblocks-projects)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance with tool names and parameter descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Art Blocks project metadata, artist details, mint status, floor prices, links, token details, and wallet portfolio summaries when the underlying tools are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
