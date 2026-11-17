## Description:

Gate live stream and replay listing skill for finding live rooms or replays by tag, coin, sort order, and result count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Gate live-stream and replay listings for requested tags, coins, hottest/newest sorting, and bounded result counts. It returns creator content links and avoids trading advice or market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required Gate Info MCP server may be unavailable in the runtime environment.

Mitigation: Confirm MCP availability before use and return setup or availability guidance instead of fabricated results.

Risk: Users may mistake live or replay listings for trading or investment advice.

Mitigation: Keep responses limited to creator content listings and links, and avoid buy, sell, market-analysis, or investment claims.

Risk: Gate live or replay content may be unavailable in restricted regions.

Mitigation: Apply the documented region availability policy and return a concise availability message when access is restricted.

## Reference(s):

- [Gate Info Liveroom Location skill page](https://clawhub.ai/gate-exchange/skills/gate-info-liveroomlocation)
- [Gate Info Liveroom Location Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Gate Live Room Location MCP Specification](references/mcp.md)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown list of live or replay titles with Gate links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output; result count is limited to 1-10 items and restricted-region requests may return an availability message instead of listings.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
