## Description:

Before a Bitcoin trade, check the derivatives picture across exchanges - funding and basis, open interest, long/short positioning, recent liquidations and where the large order-book walls are. Live data from AgentReeve; free samples, live data per request over x402 (USDC on Base).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

People considering a Bitcoin trade can use the skill to review funding and basis, open interest, positioning, recent liquidations, and nearby order-book walls across exchanges. It summarizes market conditions without recommending a trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid data calls can spend up to $0.25 per task without asking, and a low-risk scan does not mean the skill is risk-free.

Mitigation: Before paying, confirm the quote names recipient 0xDeA94ef76afa86bf1638B645F76108dF65890c0b, Base (eip155:8453), and USDC; stay within the $0.25 per-task limit and ask before exceeding it.

Risk: Market indicators may be stale, unavailable, or conflicting and could be mistaken for trading advice.

Mitigation: Report only returned data, state when fresh data is unavailable, note conflicting signals, and present the result as observational information rather than a trade recommendation.

## Reference(s):

- [Server-resolved source repository](https://github.com/shakeelamjid/agentreeve-skills/tree/main/btc-derivatives-check)
- [ClawHub skill listing](https://clawhub.ai/shakeelamjid/skills/btc-derivatives-check)
- [AgentReeve BTC derivatives endpoint](https://agentreeve.com/api/v1/btc/derivatives)
- [AgentReeve BTC positioning endpoint](https://agentreeve.com/api/v1/btc/positioning?hours=24)
- [AgentReeve BTC liquidations endpoint](https://agentreeve.com/api/v1/btc/liquidations?minutes=60)
- [AgentReeve BTC order-book walls endpoint](https://agentreeve.com/api/v1/btc/walls?hours=24)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Concise Markdown summary of market indicators and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Observational market data; report unavailable or conflicting signals and do not provide trade recommendations.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
