## Description:

Build, backtest, and deploy algorithmic trading strategies using BotSpot's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grzesir](https://clawhub.ai/user/grzesir)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create trading strategies from plain English, backtest them on historical market data, analyze performance, and prepare broker deployment through BotSpot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live broker deployment can affect real money and may cause rapid financial loss.

Mitigation: Use paper trading or a sandbox account first, and require explicit approval of the strategy, position sizing, risk limits, and order behavior before live deployment.

Risk: OAuth broker access may grant permissions on the wrong account or with broader trading authority than intended.

Mitigation: Confirm the exact broker account and permissions granted through OAuth before using deployment tools.

Risk: Backtest results and generated performance summaries can be mistaken for future-return guarantees.

Mitigation: Show actual backtest outputs only, avoid fabricated performance numbers, and remind users that past performance does not guarantee future results.

## Reference(s):

- [BotSpot Trading on ClawHub](https://clawhub.ai/grzesir/skills/botspot-trading)
- [BotSpot Website](https://botspot.trade)
- [BotSpot Agents Setup](https://botspot.trade/agents)
- [BotSpot MCP Connector](https://mcp.botspot.trade/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated strategy code, backtest summaries, and deployment instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses BotSpot MCP tools for strategy generation, backtesting, artifact retrieval, chart data, marketplace browsing, account status checks, and deployment workflows.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
