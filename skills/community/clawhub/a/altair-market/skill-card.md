## Description:

Retrieves public market breadth and factor indicator readings for major indices, sectors, and an individual Yahoo Finance symbol, with the associated rules and sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altair-world](https://clawhub.ai/user/altair-world)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review market breadth and factor indicator readings for indices, sectors, or one ticker. The readings are informational and do not provide live quotes, brokerage actions, personal position sizing, or buy/sell advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market readings may be delayed or incomplete and could be mistaken for live quotes or personalized investment advice.

Mitigation: State the reading date and that readings are based on available market data; present them as information only, not financial or investment advice.

Risk: Changing ALTAIR_MCP_URL sends the requested ticker or history length and normal connection information to the configured endpoint.

Mitigation: Use a trusted endpoint; remote endpoints must use HTTPS.

## Reference(s):

- [Altair market indicators](https://altairworld.com/indicators)
- [Altair public MCP endpoint](https://altairworld.com/mcp/free)
- [ClawHub release page](https://clawhub.ai/altair-world/skills/altair-market)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current market readings with dates, rules, sources, and unavailable values identified explicitly.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
