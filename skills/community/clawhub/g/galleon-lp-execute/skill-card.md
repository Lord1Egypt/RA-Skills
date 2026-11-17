## Description:

Helps execute explicitly requested Uniswap and Aerodrome liquidity actions through a user-controlled wallet, with exact confirmation and receipt-based state checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

People managing DeFi liquidity positions use this skill to review and carry out an explicitly requested add, remove, collect, rebalance, stake, or exit action, then verify the on-chain result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Liquidity actions can move funds or grant spending authority.

Mitigation: Use a trusted user-controlled wallet; inspect the exact transaction terms and confirm each action before submission.

Risk: Stale plans or ambiguous transactions can lead to unintended actions or duplicate submissions.

Mitigation: Refresh chain state and simulation before acting, submit one confirmed step at a time, and check mined receipts and resulting state before continuing or retrying.

Risk: An optional external provider may not be suitable or trustworthy for the intended action.

Mitigation: Verify any provider chosen and its capabilities before using it; do not treat provider data as wallet authorization.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/galleonlabs/skills/galleon-lp-execute)
- [Plan intake](artifact/references/plan-intake.md)
- [Confirmation contract](artifact/references/confirmation-contract.md)
- [Transaction state machine](artifact/references/transaction-state-machine.md)
- [Recovery guidance](artifact/references/recovery.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown preflight and execution reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports transaction hashes, receipt status, reconciled balances and ownership, and unresolved risks.]

## Skill Version(s):

0.6.1 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
