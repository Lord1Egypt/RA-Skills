## Description:

Crypto Market analyzes spot cryptocurrency pairs by fetching Binance public market data, calculating technical indicators, and combining fetched news context with risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to generate cryptocurrency market snapshots, technical-indicator summaries, and news-informed analysis for spot symbols such as BTCUSDT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Binance public APIs and news websites, so analysis can be incomplete or unavailable if those services are blocked, down, or return limited data.

Mitigation: Check returned status and source availability before relying on the analysis, and clearly state when market data or fetched news could not be retrieved.

Risk: Cryptocurrency analysis may be mistaken for investment advice.

Mitigation: Present outputs as informational market analysis only and retain explicit risk notes for users.

## Reference(s):

- [Crypto Market on ClawHub](https://clawhub.ai/luyao-inc/skills/crypto-market)
- [luyao-inc ClawHub Profile](https://clawhub.ai/user/luyao-inc)
- [Binance Public REST API](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with optional shell-command examples and JSON market snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 or Python and Binance public REST data; no API key is required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
