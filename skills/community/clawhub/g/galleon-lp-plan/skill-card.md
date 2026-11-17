## Description:

Designs or backtests unsigned liquidity-position plans for a chosen Uniswap, Aerodrome, or Slipstream pool, including amounts, ranges, approvals, and preflight checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Liquidity providers and developers use this skill to draft or backtest an unsigned plan for a chosen pool, including position sizing, range selection, approvals, and transaction review. It does not select an unassessed pool or sign or submit transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect pool, chain, token, or price data can produce a misleading liquidity plan.

Mitigation: Verify pool and token identities, fees, limits, and simulation against current chain data before acting.

Risk: Overbroad approvals or an unexpected spender can expose wallet assets.

Mitigation: Review the token, spender, amount, expiry, and approval scope independently before authorizing anything.

Risk: Stale quotes, generated URLs, or unsigned transaction data may be unsafe to sign.

Mitigation: Recheck slippage, deadline, calldata, provider, and final wallet display; never treat a link or unsigned plan as authorization to sign.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/galleonlabs/skills/galleon-lp-plan)
- [Plan contract](references/plan-contract.md)
- [Approval policy](references/approval-policy.md)
- [Backtesting standards](references/backtesting.md)
- [Uniswap liquidity provisioning API guide](https://developers.uniswap.org/docs/liquidity/liquidity-provisioning-api/integration-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown planning guidance and structured JSON plan records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unsigned plans and optional review links; missing live checks make plans non-executable.]

## Skill Version(s):

0.6.1 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
