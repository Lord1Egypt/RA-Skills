## Description:

Fetch a pre-transaction risk score and advisory recommendation for tokens on Solana, Base, Ethereum, Arbitrum, BSC, and HyperEVM before the user trades, swaps, or provides liquidity. Read-only; never signs or moves funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babyscaphe](https://clawhub.ai/user/babyscaphe)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use Bitfence before token swaps, DEX trades, or liquidity actions to request advisory token risk reports and surface warnings before the user decides whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid risk checks spend USDC on Base mainnet through x402.

Mitigation: Inform the user about the cost, obtain consent before the first paid check in a session, use one check per distinct trade decision, and stop for user direction if payment fails.

Risk: Contextual analysis shares position size and total portfolio size in USD with Bitfence.

Mitigation: Use the contextual endpoint only after explicit user opt-in; use the token-risk endpoint when position-size context is not needed.

Risk: Risk reports are advisory and may reflect incomplete or degraded source data.

Mitigation: Surface the recommendation, reasoning, flags, confidence, and degraded-source details to the user, then leave the final trade decision to the user.

Risk: The external risk-check API can fail or be unreachable.

Mitigation: Tell the user the check could not complete and offer retry, proceed without the check, or abandon the action; do not silently retry more than once.

## Reference(s):

- [Bitfence ClawHub Skill Page](https://clawhub.ai/babyscaphe/skills/bitfence)
- [Bitfence Website](https://www.bitfence.ai)
- [Bitfence API Root](https://api.bitfence.ai)
- [Bitfence X Profile](https://x.com/bitfenceai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON risk reports summarized as Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only advisory output; contextual checks require explicit opt-in and paid x402 USDC requests.]

## Skill Version(s):

0.7.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
