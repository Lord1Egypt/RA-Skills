## Description: <br>
Build, backtest, and deploy algorithmic trading strategies using BotSpot's MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grzesir](https://clawhub.ai/user/grzesir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to describe trading strategies in plain English, generate strategy code, run historical backtests, analyze results, and deploy strategies through supported brokers when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to live broker-connected trading without enough documented confirmation, limits, or stop controls. <br>
Mitigation: Use paper trading or a limited account first, require explicit confirmation before live deployment, set strict broker-side risk limits, and verify how to stop bots and revoke BotSpot or broker OAuth access. <br>
Risk: Generated strategy code or backtest results may be treated as reliable without sufficient review. <br>
Mitigation: Inspect generated strategy code, review actual backtest artifacts and metrics, avoid fabricated performance claims, and remind users that past performance does not guarantee future results. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/grzesir/botspot-trading) <br>
- [BotSpot website](https://botspot.trade) <br>
- [BotSpot agents setup](https://botspot.trade/agents) <br>
- [BotSpot MCP connector endpoint](https://mcp.botspot.trade/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown and text with generated strategy code, backtest summaries, metrics, chart references, and connector setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require OAuth access to BotSpot or broker accounts and may consume BotSpot free-tier generation and backtesting limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
