## Description:

Evaluates existing Uniswap and Aerodrome liquidity positions against a hold baseline and recommends whether to hold, collect, recenter, restake, reduce, or exit without executing transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Liquidity providers and analysts use this skill to inspect a public LP position, reconcile its performance against holding the underlying tokens, assess ownership and automation, and obtain a read-only action recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing or stale position data can make performance calculations and recommendations misleading.

Mitigation: Verify current on-chain state and cash flows; label unsupported values unknown and request the missing read rather than guessing.

Risk: Optional provider setup may expose API keys or introduce unreviewed dependencies.

Mitigation: Choose providers explicitly, verify versions and permissions, and keep API keys in a secret store.

Risk: A recommendation could be mistaken for permission to trade.

Mitigation: Keep monitoring read-only and require a separate explicit workflow before preparing or signing any transaction.

## Reference(s):

- [Galleon LP Monitor on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-lp-monitor)
- [Position accounting](references/position-accounting.md)
- [Action policy](references/action-policy.md)
- [Monitor output contract](references/output-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a verdict or state-unknown status, position and observation details, accounting versus holding, action economics, and the next required read; no transaction calldata.]

## Skill Version(s):

0.6.1 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
