## Description:

BlockBeats Skill covers over 1,500 information sources, including AI-driven insights, Hyperliquid on-chain data, and Polymarket market analytics. It also features robust keyword-based search functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockbeatsofficial](https://clawhub.ai/user/blockbeatsofficial)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query BlockBeats crypto news, article search, RSS feeds, and read-only market data through the BlockBeats Pro API. It supports market overviews, capital-flow analysis, macro and derivatives summaries, keyword search, and category-specific news retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends crypto/news queries and the user's BlockBeats API key to BlockBeats.

Mitigation: Install only when that data sharing is acceptable, keep the API key scoped and protected, and explicitly confirm ambiguous requests before external calls.

Risk: Market summaries and signals may be interpreted as investment advice.

Mitigation: Treat generated market signals as informational, verify important data independently, and avoid relying on the skill for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockbeatsofficial/skills/blockbeats)
- [BlockBeats Pro API base URL](https://api-pro.theblockbeats.info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell command examples and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLOCKBEATS_API_KEY and curl for API requests; generated market signals are informational rather than investment advice.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
