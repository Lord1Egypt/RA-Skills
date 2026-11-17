## Description:

Compares LI.FI cross-chain quotes, prepares unsigned transfer terms, and reconciles transfers against actual destination or refund evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and cross-chain users compare LI.FI routes and minimum destination amounts, prepare unsigned transactions, and track submitted transfers through completion, partial delivery, or refund.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect chain, token, recipient, slippage, or approval terms could cause unintended transfers or losses.

Mitigation: Verify transaction terms, approvals, and current LI.FI documentation before acting through an authorized wallet; the skill does not sign or send transactions.

Risk: A source receipt or provider completion label may be mistaken for delivery of the intended destination asset.

Mitigation: Confirm the destination receipt, recipient, token, and received amount against the saved minimum; report partial delivery and refunds as distinct outcomes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-lifi-cross-chain)
- [LI.FI API recipes](references/recipes.md)
- [LI.FI quote endpoint](https://docs.li.fi/li.fi-api/li.fi-api/requesting-a-quote)
- [LI.FI status tracking](https://docs.li.fi/introduction/user-flows-and-examples/status-tracking)
- [LI.FI quotes, routes, and transaction steps](https://docs.li.fi/introduction/user-flows-and-examples/difference-between-quote-and-route)
- [LI.FI contract deployments](https://docs.li.fi/introduction/lifi-architecture/smart-contract-addresses)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown quote comparisons and settlement evidence, with optional JSON classifications and read-only API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unsigned transfer terms only; delivery requires independent destination verification.]

## Skill Version(s):

0.3.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
