## Description:

Implements and reviews liquidity-provision software for Uniswap v2–v4 and Aerodrome/Slipstream with explicit wallet and transaction boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to build or review protocol-aware LP integrations, unsigned transaction plans, simulations, position accounting, and tests. It does not choose investments or execute wallet actions on the user's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed transaction code or automation could cause unintended wallet actions.

Mitigation: Require explicit approval and review before signing, submission, live automation, or production deployment; keep plans unsigned by default.

Risk: Stale chain data or mismatched protocol contracts can make LP plans unsafe.

Mitigation: Verify current protocol documentation and deployed contracts, check data freshness, simulate independently, and confirm outcomes against receipts and refreshed state.

Risk: Optional upstream integrations may require credentials or access beyond the user's intent.

Mitigation: Verify optional tools before use, keep credentials in a secret store, and do not register providers without explicit user approval.

## Reference(s):

- [ClawHub release](https://clawhub.ai/galleonlabs/skills/galleon-lp-engineer)
- [Adapter architecture](references/adapter-architecture.md)
- [Security invariants](references/security-invariants.md)
- [Protocol matrix](references/protocol-matrix.md)
- [Test matrix](references/test-matrix.md)
- [Uniswap liquidity provisioning integration guide](https://developers.uniswap.org/docs/liquidity/liquidity-provisioning-api/integration-guide)

## Skill Output:

**Output Type(s):** [Code, Markdown, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Code and Markdown with commands and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports supported capabilities, assumptions, test evidence, and unsupported paths; transaction plans remain unsigned.]

## Skill Version(s):

0.6.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
