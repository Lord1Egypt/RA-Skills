## Description:

Normalize odds across Polymarket, Kalshi, and sportsbooks into a unified implied-probability format for comparing the same event across platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to convert market odds into implied probabilities, compare sportsbook and prediction-market prices, and identify cross-platform pricing gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled event names, categories, tickers, platform names, or odds values could be interpolated into shell or Python commands.

Mitigation: Treat those values as untrusted data and pass them via URL encoding, argv, stdin, or JSON rather than direct command interpolation.

Risk: The skill is flagged as suspicious by the authoritative security evidence because unsafe command examples could create code-execution risk.

Mitigation: Review before installing or running generated commands, and adjust command examples before deployment.

## Reference(s):

- [Cross-Market Pricer on ClawHub](https://clawhub.ai/rsquaredsolutions2026/skills/cross-market-pricer)
- [The Odds API](https://the-odds-api.com/)
- [Polymarket Gamma API markets endpoint](https://gamma-api.polymarket.com/markets)
- [Kalshi public markets endpoint](https://api.elections.kalshi.com/trade-api/v2/markets)
- [AgentBets Cross-Market Pricer guide](https://agentbets.ai/guides/openclaw-cross-market-pricer-skill/)
- [Agent Betting Stack guide](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include normalized implied probabilities, American odds equivalents, source-specific notes, API quota notes, and pricing-gap flags.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
