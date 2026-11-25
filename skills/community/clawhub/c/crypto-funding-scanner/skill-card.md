## Description:

Scan funding rates across every USDT/USDC perpetual on Binance, Bybit, OKX and Hyperliquid - the most extreme funding right now, the widest cross-exchange funding spreads for the same coin, and where open interest is building or unwinding. Real multi-exchange data from AgentReeve, every 5 minutes; free market list, live data per request over x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and market analysts use this skill to inspect funding extremes, cross-exchange spreads, open-interest changes, and crowded positions across perpetual markets. It provides observational market data rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags paid requests without a prompt as a consent risk; spend can reach $0.25 per task.

Mitigation: If that spend is not acceptable, use the skill only where paid calls can be prevented or require approval first.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/shakeelamjid/agentreeve-skills/tree/main/crypto-funding-scanner)
- [ClawHub skill release](https://clawhub.ai/shakeelamjid/skills/crypto-funding-scanner)
- [AgentReeve markets endpoint](https://agentreeve.com/api/v1/markets)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Concise Markdown market summaries with reported funding, spreads, open interest, and crowded-position measures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses available live market data; reports when fresh data is unavailable, cautions that funding spreads are not risk-free, and identifies the results as observational rather than financial advice.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata; artifact frontmatter declares 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
