## Description:

Exchange listing tracker for exchange listing, delisting, and maintenance announcements, with optional coin fundamentals and market snapshot enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query recent exchange listing, delisting, and maintenance announcements and receive a structured activity report. The skill can enrich newly listed coins with public project and market context while keeping the output informational.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake listing summaries or enriched market context for trading advice.

Mitigation: Present summaries as informational, include the not-investment-advice posture, and preserve risk warnings for newly listed assets.

Risk: The skill depends on the configured Gate MCP server and public exchange announcement data.

Mitigation: Confirm the Gate MCP server is trusted and available before use, and clearly mark unavailable or failed data instead of fabricating results.

Risk: Newly listed tokens can have extreme volatility or limited liquidity.

Mitigation: Surface volatility and liquidity warnings in listing reports and encourage additional due diligence before any trading decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-news-listing-staging)
- [Gate News Listing Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [Gate News Listing MCP Specification](references/mcp.md)
- [Gate News Listing Scenarios & Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, summaries, degraded-data markers, and risk warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public exchange announcements and optional market/token metadata; output is informational and not investment advice.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter: 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
