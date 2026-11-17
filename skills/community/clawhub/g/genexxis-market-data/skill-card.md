## Description:

Live market data for agents, paid per call via x402 (USDC on Base, no API key): median crypto spot prices, DEX price and liquidity by contract address, OHLCV candles, top movers, perpetual funding rates and open interest, order-book slippage, Korea premium, DeFi yields, pools and protocol TVL, gas fees and the cheapest chain for a transfer, Polymarket and Kalshi odds, crypto news, government bond yields and curves, central bank policy rates, official FX rates, currency conversion and carry. Use when a task needs current prices, rates or odds rather than training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montassirbbk-dot](https://clawhub.ai/user/montassirbbk-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents that need current crypto, DeFi, prediction-market, macroeconomic, or FX data can query the service and use its sources and timestamps when reporting time-sensitive figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented AgentCash command uses an unpinned package version, so the installed CLI could change without review.

Mitigation: Wait to install until the CLI dependency is pinned to a reviewed version and its installation is integrity-checked.

Risk: Each data request can incur a USDC payment.

Mitigation: Review the listed price and cap each payment at the approved amount before making a paid request.

## Reference(s):

- [Genexxis service homepage](https://skills.genexxis.com)
- [Genexxis MCP endpoint](https://mcp.genexxis.com/mcp)
- [ClawHub release page](https://clawhub.ai/montassirbbk-dot/skills/genexxis-market-data)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text]

**Output Format:** [Current market data and concise text summaries with sources and timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retain the returned source and timestamp when reporting figures.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
