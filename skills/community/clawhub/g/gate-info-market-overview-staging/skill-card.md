## Description:

Market overview for overall crypto market conditions, using Gate Info and Gate News MCP data only when the user's query is not asking for specific coin analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a concise, data-driven crypto market overview from read-only Gate Info and Gate News MCP sources. It summarizes market breadth, top movers, DeFi metrics, recent events, macro context, and an overall assessment without giving investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data or news feeds may be unavailable, stale, or incomplete.

Mitigation: Confirm the Gate MCP server is trusted and available, label missing or stale sections clearly, and continue only with the data returned by documented read-only tools.

Risk: A market overview may be mistaken for investment advice.

Mitigation: Keep the report data-driven, avoid buy or sell recommendations and deterministic predictions, and include a clear non-investment-advice disclaimer.

## Reference(s):

- [Gate Info Market Overview Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Gate Info MarketOverview MCP Specification](references/mcp.md)
- [Scenarios & Prompt Examples](references/scenarios.md)
- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-info-market-overview-staging)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables and concise narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only MCP data; labels unavailable sections instead of fabricating missing data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
