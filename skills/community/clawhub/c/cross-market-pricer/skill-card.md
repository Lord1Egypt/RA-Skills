## Description: <br>
Normalize odds across Polymarket, Kalshi, and sportsbooks into a unified implied-probability format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to compare sportsbook and prediction-market prices, normalize them to implied probabilities, and identify cross-platform pricing gaps for the same event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches third-party odds and prediction-market data, so outputs may depend on external API availability, rate limits, and changing market data. <br>
Mitigation: Confirm the source platform and timestamp of any fetched data, report API limitations to the user, and avoid treating stale or partial data as complete coverage. <br>
Risk: Sportsbook requests use ODDS_API_KEY, which could appear in commands, transcripts, or logs if handled carelessly. <br>
Mitigation: Use a limited The Odds API key, keep it in the environment, and review generated commands and shared logs for accidental key exposure. <br>
Risk: Cross-market price gaps can be misleading when events, settlement rules, fees, liquidity, or sportsbook lines do not match exactly. <br>
Mitigation: Compare only like-for-like events where possible, identify the sportsbook source, disclose platform differences, and present gaps as potential mispricings rather than trading advice. <br>


## Reference(s): <br>
- [Cross-Market Pricer on ClawHub](https://clawhub.ai/rsquaredsolutions2026/cross-market-pricer) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com/markets?closed=false&limit=10&tag=CATEGORY) <br>
- [Kalshi Public Market Data API](https://api.elections.kalshi.com/trade-api/v2/markets?status=open&limit=10&series_ticker=SERIES_TICKER) <br>
- [AgentBets Cross-Market Pricer Tutorial](https://agentbets.ai/guides/openclaw-cross-market-pricer-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with tables and inline bash or Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API-derived odds data, normalized implied probabilities, American odds conversions, quota notes, and rate-limit guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
