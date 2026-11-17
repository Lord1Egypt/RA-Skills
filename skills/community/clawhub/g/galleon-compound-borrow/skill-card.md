## Description:

Guides planning and verification of Compound III base-asset borrowing, repayment, and collateral withdrawals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi users use this skill to assess a Compound III position, plan a borrow, repayment, or collateral withdrawal, and record the evidence needed before authorizing a transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect market, price, or collateral assumptions can lead to unsafe borrowing or withdrawal decisions.

Mitigation: Verify the chain, Comet deployment, account, current parameters, oracle prices, and position checks; simulate the exact proposed action before authorization.

Risk: A proposed borrow can create more debt than authorized or fail the minimum borrow requirement.

Mitigation: Account for existing base supply and baseBorrowMin; do not increase a requested amount without the user's approval.

Risk: Approvals or signing authority can expose assets or permit unintended account actions.

Mitigation: Keep planning read-only, never request keys, avoid unrequested approvals or manager permissions, and verify transaction receipts and resulting balances.

## Reference(s):

- [Compound III read recipe](references/recipe.md)
- [Compound collateral and borrowing](https://docs.compound.finance/collateral-and-borrowing/)
- [Compound helper functions](https://docs.compound.finance/helper-functions/)
- [Comet specification](https://github.com/compound-finance/comet/blob/main/SPEC.md)
- [Comet deployment configurations](https://github.com/compound-finance/comet/tree/main/deployments)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown decision record with optional unsigned transaction steps and read commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment, chain, observations, assumptions, simulation status, and missing reads.]

## Skill Version(s):

0.3.1 (source: skill metadata and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
