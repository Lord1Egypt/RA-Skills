## Description:

Scan funding rates across USDT and USDC perpetual markets on Binance, Bybit, OKX, and Hyperliquid to identify extreme funding, cross-exchange spreads, and changes in open interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shakeelamjid](https://clawhub.ai/user/shakeelamjid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to review current perpetual-market funding, compare funding across exchanges, and track leverage building or unwinding. It provides observational market data and cautions that funding spreads carry trading risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid data requests may incur repeated charges when the skill is invoked repeatedly, even with a per-task spending cap.

Mitigation: Check each payment quote against the specified recipient, Base network, and USDC asset; enforce a user-approved payment policy and spending limit, and ask before spending more than $0.25 per task.

## Reference(s):

- [Source repository](https://github.com/shakeelamjid/agentreeve-skills/tree/main/crypto-funding-scanner)
- [ClawHub release](https://clawhub.ai/shakeelamjid/skills/crypto-funding-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries of funding rates, cross-exchange spreads, and open-interest changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports returned market data with relevant risk context; does not invent values or provide financial advice.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
