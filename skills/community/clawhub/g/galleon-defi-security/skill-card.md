## Description:

Reviews DeFi transactions, typed signatures, token allowances, and smart-account policies to distinguish observed effects, unresolved risks, and actual authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Wallet users, developers, and security reviewers use this skill to assess proposed DeFi actions and ongoing spending authority before making a separate authorization decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulations or risk scores may miss hazards or reflect stale or incomplete state.

Mitigation: Check the exact payload against current chain state, disclose coverage gaps, and do not describe a simulation as proof of safety.

Risk: Optional external providers may receive sensitive transaction details.

Mitigation: Use only user-approved, narrowly scoped provider access and never send seed phrases or signatures for analysis.

Risk: A review may be mistaken for permission to sign or execute a wallet action.

Mitigation: Keep review read-only and obtain separate authorization bound to the exact transaction and authority limits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-defi-security)
- [Transaction review tools](artifact/references/providers.md)
- [Review continuing authority](artifact/references/authority.md)
- [From proposal to observed outcome](artifact/references/review.md)
- [Tenderly AI tools documentation](https://docs.tenderly.co/ai-tools/overview)
- [Safe Protocol Kit documentation](https://docs.safe.global/sdk/protocol-kit)
- [ERC-2612 specification](https://eips.ethereum.org/EIPS/eip-2612)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown transaction review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only assessment of effects, authority changes, evidence coverage, and unresolved risks; no signing or broadcasting.]

## Skill Version(s):

0.2.3 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
