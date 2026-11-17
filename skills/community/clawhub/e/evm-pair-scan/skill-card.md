## Description:

Guides an agent through a paid scan of public EVM DEX pairs for liquidity, trading activity, routing, valuation, and volatility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check a token's DEX liquidity and trading activity before quoting, monitoring, or considering a trade on BSC, Base, or Ethereum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request can spend $0.005 USDC through an x402 payment flow.

Mitigation: Verify the endpoint and payment details before authorizing each payment.

Risk: A request sends the token address and chain to an external service.

Mitigation: Share only intended public token addresses and chains with the service.

Risk: Heuristic DEX analytics may be incomplete or misleading for trading decisions.

Mitigation: Check underlying sources and treat results as market data, not financial advice.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/perria080925-bot/skills/evm-pair-scan)
- [Pair-scan service endpoint](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell commands and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes liquidity, 24-hour volume, churn, best pair and router, FDV, and realized volatility from a paid JSON response.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
