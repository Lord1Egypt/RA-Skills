## Description:

Monitor Polymarket prediction markets for price movements, volume spikes, and new listings. Track specific markets, check order book depth, and surface trending predictions. Use when asked about Polymarket, prediction market prices, market volume, or contract probabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Polymarket markets, prices, volume, liquidity, and new listings through public Polymarket APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned Polymarket prices, liquidity, or volume can influence financial or betting decisions.

Mitigation: Verify important prices, liquidity, and market conditions against Polymarket or another reliable source before acting on them.

Risk: The skill depends on external Polymarket API responses for market data.

Mitigation: Treat unavailable, incomplete, or unexpected API responses as a reason to retry or cross-check rather than as definitive market state.

## Reference(s):

- [Polymarket Gamma API markets endpoint](https://gamma-api.polymarket.com/markets?closed=false&active=true&order=volume24hr&ascending=false&limit=10)
- [AgentBets OpenClaw Polymarket Monitor tutorial](https://agentbets.ai/guides/openclaw-polymarket-monitor-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-formatted API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq for the documented command examples.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
