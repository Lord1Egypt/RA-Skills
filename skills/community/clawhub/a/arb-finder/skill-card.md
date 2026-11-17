## Description:

Detects guaranteed-profit arbitrage opportunities across sportsbooks and prediction markets, including odds comparison, market-price checks, and optimal stake distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan sportsbook, Polymarket, and Kalshi market data for arbitrage opportunities and calculate stake splits for equal-profit outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market lines and prediction-market prices can change quickly, so an identified arbitrage may disappear before execution.

Mitigation: Verify current prices directly on each platform before risking money and include a time-sensitivity note in results.

Risk: The skill sends market queries to third-party APIs and requires an Odds API key in the environment.

Mitigation: Install only if third-party API use is acceptable, store ODDS_API_KEY as an environment variable, and avoid exposing the key in shared logs.

Risk: Betting and prediction-market activity may be legally or contractually restricted by location or platform terms.

Mitigation: Follow applicable laws and platform rules before acting on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/skills/arb-finder)
- [The Odds API](https://the-odds-api.com/)
- [Polymarket Gamma API events endpoint](https://gamma-api.polymarket.com/events?closed=false&limit=50&order=volume24hr&ascending=false)
- [Kalshi events API endpoint](https://api.elections.kalshi.com/trade-api/v2/events?status=open&limit=50&with_nested_markets=true)
- [AgentBets Arbitrage Finder guide](https://agentbets.ai/guides/openclaw-arb-finder-skill/)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with odds summaries, stake calculations, and inline shell or Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports arbitrage margins, exact stake amounts, guaranteed profit, near-arbs, time-sensitivity notes, and remaining Odds API quota when available.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
