## Description:

Find trusted BestChange exchangers for crypto-to-fiat and e-currency exchange requests using the hosted BestChange MCP tool when users ask for current BestChange options or exchanger rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftadviser](https://clawhub.ai/user/swiftadviser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to resolve exact BestChange currency codes and retrieve ranked live exchanger options for crypto-to-fiat and e-currency routes through a hosted MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exchange search details, amounts, payout rails, and some blocked-request text are sent to the hosted BestChange MCP operator.

Mitigation: Install only when that data sharing is acceptable, and avoid sending sensitive personal or destination details through the skill.

Risk: Returned BestChange URLs are referral or tracked click links.

Mitigation: Treat links as tracked routes and independently verify exchanger reputation, exact network, payout rail, fees, limits, and destination details before sending funds.

Risk: The skill can only quote routes available through the connected hosted MCP service and current BestChange API data.

Mitigation: Use exact BestChange currency codes from the search tool, ask for clarification on ambiguous routes, and do not rely on fabricated or stale exchange information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swiftadviser/skills/bestchange)
- [BestChange MCP homepage](https://bestchange-mcp.krutovoy.me)
- [BestChange MCP endpoint](https://bestchange-mcp.krutovoy.me/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful quote responses include live BestChange route details, ranked exchanger options, referral URLs, and pre-send checks when MCP data is available.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
