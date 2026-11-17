## Description:

Reconciles cross-chain DeFi holdings, debt, and cash flows into sourced portfolio reports or rebalance plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Portfolio holders and treasury teams use this skill to reconcile DeFi positions, assess net equity and exposure, and plan rebalancing without executing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved account data and provider credentials may reveal sensitive financial holdings.

Mitigation: Limit account scope, keep API keys in the credential store, and review recurring-report destinations before enabling them.

Risk: A rebalance plan could be mistaken for authorization to move funds.

Mitigation: Treat plans as read-only guidance and require separate, explicit authorization for any transaction.

## Reference(s):

- [Galleon DeFi Portfolio release](https://clawhub.ai/galleonlabs/skills/galleon-defi-portfolio)
- [Accounting and performance conventions](references/accounting.md)
- [Provider interfaces](references/providers.md)
- [Reporting and rebalance workflow](references/reporting.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown portfolio report or rebalance plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes valuation time, coverage gaps, source links, assets, liabilities, and material risks; does not execute trades.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
