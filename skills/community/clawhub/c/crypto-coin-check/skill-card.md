## Description:

Checks how crowded and liquid an asset or perpetual market is and compares venues for execution before a trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

Traders use this skill to review market crowding, liquidity for a planned trade size, and execution venues before trading a supported coin or perpetual.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that the asset and exact trade size are shared with an external provider without a privacy notice, and that paid requests may occur without prior approval.

Mitigation: Tell the user what trade details will be shared and the possible cost before making a paid request; verify the recipient, Base network, and USDC, and ask for approval when the task total exceeds $0.25.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/shakeelamjid/skills/crypto-coin-check)
- [Server-resolved GitHub source](https://github.com/shakeelamjid/agentreeve-skills/tree/main/crypto-coin-check)
- [AgentReeve market coverage endpoint](https://agentreeve.com/api/v1/crypto/markets)
- [AgentReeve coin market data endpoint](https://agentreeve.com/api/v1/crypto/coin?asset=SOL&size_usd=100000)
- [AgentReeve order book endpoint](https://agentreeve.com/api/v1/crypto/coin-liquidity?asset=SOL&size_usd=100000)
- [AgentReeve chart data endpoint](https://agentreeve.com/api/v1/crypto/coin-candles?asset=SOL&interval=1h&limit=100)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-language market summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports available market data for the requested asset and trade size; identifies unavailable data without estimating values and labels the information as observational, not financial advice.]

## Skill Version(s):

0.1.0 (source: target metadata and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
