## Description:

Check any coin or perpetual before a trade - funding and open interest on every exchange that lists it, long/short positioning, live order-book liquidity with slippage for your size and the best exchange to buy or sell. Covers 900+ coins plus stock, forex and commodity perpetuals on Binance, Bybit, OKX and Hyperliquid. Live data from AgentReeve per request over x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

External traders use this skill before trading a coin or a stock, forex, or commodity perpetual to review funding, positioning, liquidity, expected slippage for their trade size, and possible execution venues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags that paid requests may spend up to $0.25 per task without prior approval and that trade size is sent to an external provider without a privacy warning.

Mitigation: Before use, decide whether you are comfortable sharing the asset and intended trade size with the provider and allowing paid requests up to $0.25 per task; verify the payment quote details and seek approval before spending more.

## Reference(s):

- [Source skill on GitHub (server-resolved provenance)](https://github.com/shakeelamjid/agentreeve-skills/tree/main/crypto-coin-check)
- [ClawHub skill release](https://clawhub.ai/shakeelamjid/skills/crypto-coin-check)
- [AgentReeve market coverage API](https://agentreeve.com/api/v1/markets)
- [AgentReeve market snapshot API](https://agentreeve.com/api/v1/snapshot?asset=SOL&size_usd=100000)
- [AgentReeve liquidity API](https://agentreeve.com/api/v1/liquidity?asset=SOL&size_usd=100000)
- [AgentReeve candles API](https://agentreeve.com/api/v1/candles?asset=SOL&interval=1h&limit=100)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain-language market summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asset and trade-size specific live market observations; includes funding, positioning, liquidity, slippage, and execution venue comparisons when data is available.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
