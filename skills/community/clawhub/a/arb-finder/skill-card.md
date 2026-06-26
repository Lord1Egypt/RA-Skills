## Description: <br>
Detect guaranteed-profit arbitrage opportunities across sportsbooks and prediction markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan sportsbook and prediction-market prices, compare implied probabilities, and calculate stake allocations for potential arbitrage opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market odds and prediction-market prices can change before a user acts on an arbitrage calculation. <br>
Mitigation: Treat results as informational and verify current odds, fees, liquidity, limits, and market rules before wagering or trading. <br>
Risk: The skill requires an Odds API key and makes external market-data requests. <br>
Mitigation: Install and run it only when external API access and the use of the configured ODDS_API_KEY are acceptable. <br>
Risk: Sports betting and prediction-market activity can be subject to local legal restrictions. <br>
Mitigation: Confirm applicable local requirements before using any calculated opportunity for wagering or trading. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/arb-finder) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [Polymarket Gamma Events API](https://gamma-api.polymarket.com/events?closed=false&limit=50&order=volume24hr&ascending=false) <br>
- [Polymarket Gamma Markets API](https://gamma-api.polymarket.com/markets?id=MARKET_ID) <br>
- [Kalshi Events API](https://api.elections.kalshi.com/trade-api/v2/events?status=open&limit=50&with_nested_markets=true) <br>
- [AgentBets Arbitrage Finder Tutorial](https://agentbets.ai/guides/openclaw-arb-finder-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, jq filters, Python snippets, and arbitrage analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports event names, best prices by platform, arb margin, stake amounts, guaranteed profit, near-arbs, API quota, and time-sensitivity notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, released 2026-03-24T23:11:08Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
