## Description:

Helps explain Polymarket outcomes and reconcile disputed resolutions, payout eligibility, and whether an existing redemption reached a wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and market participants use this skill to compare public market rules, oracle decisions, on-chain payout records, holder balances, and redemption receipts before describing a prediction-market position as claimable or paid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An outcome display or redemption request could be mistaken for confirmed payout.

Mitigation: Check finalized resolution, recorded payout, canonical owner balance, and the recipient's collateral change before calling funds paid.

Risk: Financial actions could be taken on the basis of read-only reconciliation guidance.

Mitigation: Do not sign, trade, dispute, redeem, or transfer through this skill; use a separately authorized wallet workflow for any financial action.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/galleonlabs/skills/galleon-prediction-market-resolution)
- [Versioned resolution and receipt evidence](references/settlement.md)
- [Polymarket resolution documentation](https://docs.polymarket.com/concepts/resolution)
- [Polymarket positions and tokens](https://docs.polymarket.com/concepts/positions-tokens)
- [Polymarket on-chain position data](https://docs.polymarket.com/resources/onchain-position-data)
- [Polymarket deployed contracts](https://docs.polymarket.com/resources/contracts)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports oracle stage, payout fraction, balance and redemption evidence, and any missing verification; no wallet actions.]

## Skill Version(s):

0.1.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
