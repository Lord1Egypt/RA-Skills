## Description:

Crypto News Ranked by AI helps an agent retrieve, rank, and summarize NS3 crypto news feeds, including top stories, daily market briefings, breaking headlines, and coin-specific updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assembleai-crypto](https://clawhub.ai/user/assembleai-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to answer crypto news, portfolio update, market briefing, breaking headline, top story, and coin-specific news requests from NS3 feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto-news queries, coin symbols, or portfolio tickers supplied by the user may be sent to NS3.

Mitigation: Use the skill only when sharing those query terms with NS3 is acceptable, and avoid sending sensitive portfolio details unless necessary.

Risk: Responses may include NS3 attribution or suggestions to use related NS3 feeds.

Mitigation: Review generated responses for required attribution and adjust deployment instructions if a stricter neutrality policy is needed.

Risk: Crypto market news and analysis may be mistaken for financial or investment advice.

Mitigation: Present outputs as informational news summaries and preserve the artifact's no-investment-advice posture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/assembleai-crypto/skills/crypto-news-ns3)
- [NS3 homepage](https://ns3.ai)
- [NS3 API documentation](https://docs.ns3.ai/ns3-api)
- [NS3 RSS documentation](https://docs.ns3.ai/ns3-rss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and briefings derived from RSS/API feed responses, with optional inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. Feed requests may include language, coin, news type, source, category, and limit filters.]

## Skill Version(s):

1.0.7 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
