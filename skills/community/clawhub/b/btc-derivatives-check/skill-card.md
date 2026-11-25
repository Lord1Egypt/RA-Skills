## Description:

Before a Bitcoin trade, check the derivatives picture across exchanges - funding and basis, open interest, long/short positioning, recent liquidations and where the large order-book walls are. Live data from AgentReeve; free samples, live data per request over x402 (USDC on Base).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and market analysts use the skill to review derivatives positioning, liquidations, and order-book liquidity before considering a Bitcoin trade. It presents market observations for context, not trade recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid data calls can incur charges of up to $0.25 per task without asking first.

Mitigation: Check that the quote specifies the expected recipient, Base network, and USDC asset; stay within the $0.25 per-task limit and ask before exceeding it.

Risk: Market indicators could be mistaken for financial advice.

Mitigation: Present the observations and any conflicting signals without recommending a trade, and state that the data is not financial advice.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/shakeelamjid/agentreeve-skills/tree/main/btc-derivatives-check)
- [ClawHub skill page](https://clawhub.ai/shakeelamjid/skills/btc-derivatives-check)
- [AgentReeve derivatives data](https://agentreeve.com/api/v1/derivatives?asset=BTC)
- [AgentReeve positioning data](https://agentreeve.com/api/v1/positioning?asset=BTC&hours=24)
- [AgentReeve liquidation data](https://agentreeve.com/api/v1/liquidations?minutes=60)
- [AgentReeve liquidity data](https://agentreeve.com/api/v1/liquidity?asset=BTC&size_usd=100000)

## Skill Output:

**Output Type(s):** [Text, Markdown, Market analysis, Guidance]

**Output Format:** [Concise market summary in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed market data and conflicting signals; does not recommend trades or invent values when data is unavailable.]

## Skill Version(s):

0.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
