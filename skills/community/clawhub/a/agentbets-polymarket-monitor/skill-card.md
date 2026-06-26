## Description: <br>
Monitor Polymarket prediction markets for price movements, volume spikes, new listings, order book depth, and trending contract probabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect public Polymarket market data, including trending markets, current probabilities, volume, liquidity, and order book depth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public web requests to Polymarket APIs, which may be inappropriate in restricted network environments. <br>
Mitigation: Install and run it only where outbound public API requests to Polymarket are acceptable. <br>
Risk: Market data and probabilities may be incomplete, stale, or mistaken for financial advice. <br>
Mitigation: Treat results as informational market data and verify important values directly before making decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rsquaredsolutions2026/agentbets-polymarket-monitor) <br>
- [AgentBets Polymarket Monitor tutorial](https://agentbets.ai/guides/openclaw-polymarket-monitor-skill/) <br>
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>
- [Polymarket Gamma API market query](https://gamma-api.polymarket.com/markets?closed=false&active=true&order=volume24hr&ascending=false&limit=10) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; makes read-only public web requests to Polymarket APIs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
