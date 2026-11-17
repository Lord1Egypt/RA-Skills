## Description:

Exchange listing tracker for exchange listing, delisting, and maintenance announcements using Gate News and Gate Info MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for recent exchange listing, delisting, and maintenance announcements. The agent retrieves public announcement data, optionally enriches listing items with coin fundamentals and market snapshots, and returns a listing-focused activity report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP announcement or enrichment data may be unavailable, incomplete, or delayed.

Mitigation: Verify the Gate News and supporting Gate Info MCP tools before use, continue only with available data, and label missing dimensions clearly.

Risk: Listing reports could be mistaken for trading or investment advice.

Mitigation: Keep outputs informational, use a neutral tone, and include the required not-investment-advice and volatility warnings.

Risk: Newly listed assets can be highly volatile or have limited liquidity.

Mitigation: Preserve announcement timestamps and exchange names, avoid listing predictions, and flag volatility, liquidity, and delisting risks when present.

## Reference(s):

- [Gate News Listing Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Gate News Listing MCP Specification](references/mcp.md)
- [Gate News Listing Scenarios](references/scenarios.md)
- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-news-listing)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown report with tables and concise narrative summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source transparency, missing-data labels, and risk warnings for volatile newly listed assets.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
