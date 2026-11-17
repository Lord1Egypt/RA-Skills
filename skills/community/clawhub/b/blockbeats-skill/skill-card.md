## Description:

BlockBeats Skill covers over 1,500 information sources, including AI-driven insights, Hyperliquid on-chain data, and Polymarket market analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockbeatsofficial](https://clawhub.ai/user/blockbeatsofficial)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query BlockBeats Pro API news, article, search, RSS, and crypto market-data endpoints. It supports market overview, capital flow, macro, derivatives, keyword search, and news-list workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends market, news, and keyword-search queries to BlockBeats using a user-provided API key.

Mitigation: Install only when that data sharing is acceptable, keep BLOCKBEATS_API_KEY in environment configuration, and avoid sensitive keyword searches.

Risk: Market interpretation rules may produce buy, sell, bullish, or bearish commentary.

Mitigation: Present those outputs as informational market commentary rather than financial advice.

Risk: Broad trigger phrases such as market overview or search terms may invoke external API calls unexpectedly.

Mitigation: Prefer explicit prompts such as 'search BlockBeats for ...' and confirm intent before sending ambiguous queries.

Risk: Results depend on BlockBeats API availability, subscription status, and endpoint data-refresh frequency.

Mitigation: Surface API status messages clearly, tolerate partial request failures, and note data delays where endpoint behavior indicates daily or monthly refreshes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockbeatsofficial/skills/blockbeats-skill)
- [Publisher profile](https://clawhub.ai/user/blockbeatsofficial)
- [BlockBeats Pro API base URL](https://api-pro.theblockbeats.info)
- [BlockBeats API access page](https://www.theblockbeats.info/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and API response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and BLOCKBEATS_API_KEY; sends selected market, news, and keyword queries to BlockBeats.]

## Skill Version(s):

1.0.3 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
