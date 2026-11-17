## Description:

Provides X/Twitter-first community sentiment scans for crypto coins or topics using Gate-News MCP discussion search and social sentiment tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize crypto community discussion, KOL themes, and social sentiment for a coin or topic. It helps produce neutral community insight reports without treating sentiment as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community sentiment summaries may be mistaken for trading or investment advice.

Mitigation: Present outputs as social-sentiment summaries, keep the tone neutral, and include the skill's investment-advice limitation.

Risk: Coverage may omit Reddit, Discord, and Telegram when upstream UGC support is unavailable.

Mitigation: Label reports as X/Twitter-only unless the upstream UGC API is available.

Risk: Required Gate-News MCP tools may be unavailable or return partial data.

Mitigation: Check MCP availability before use and degrade gracefully with clear limitations when a tool fails.

## Reference(s):

- [Gate News Community Scan Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with sentiment metrics, narrative summary, and risk disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output synthesized from Gate-News MCP tool results; coverage should be labeled X/Twitter-only unless upstream UGC support is available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
