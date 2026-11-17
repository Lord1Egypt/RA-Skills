## Description:

Search and analyse Swedish real estate on booli.se, including active listings, sold prices, area resolution, and market statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask about Swedish homes for sale, recent sale prices, and local market statistics. The skill searches Booli by area and summarizes matching property data.

### Deployment Geography for Use:

Sweden (property data scope)

## Known Risks and Mitigations:

Risk: Searches may use a separately installed browser bridge that operates through the user's Booli browser context; the security verdict covers the supplied skill instructions, not the bridge or MCP server.

Mitigation: Verify the bridge release before pairing, approve only www.booli.se and capabilities needed for property lookups, and revoke access when it is no longer needed.

## Reference(s):

- [Booli property portal](https://www.booli.se)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Markdown text with property search summaries and market statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Swedish property results; prices are in SEK and areas in m².]

## Skill Version(s):

2.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
