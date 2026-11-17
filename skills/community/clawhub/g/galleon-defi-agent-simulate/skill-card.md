## Description:

Guides developers through simulation of exact unsigned EVM transaction sequences and recording their observed effects and limitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi teams use this skill to preflight proposed EVM transactions, investigate failed transactions, and document fork experiments with payload-bound simulation evidence for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulation providers may receive private calldata or consume paid credits.

Mitigation: Use existing approved provider access, avoid sharing secrets or signatures, and confirm charges before use.

Risk: A successful simulation may be mistaken for proof of transaction safety or eventual settlement.

Mitigation: Treat simulation as review evidence only; independently review intent and authorization, then verify actual results after any separately authorized submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/galleonlabs/skills/galleon-defi-agent-simulate)
- [Simulation providers](references/providers.md)
- [Simulation records and recovery](references/records.md)
- [Tenderly simulation documentation](https://docs.tenderly.co/simulations-and-forks)
- [Portals Foresight API reference](https://foresight.portals.fi/docs/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Markdown decision record; optional JSON diagnostic for a supplied simulation record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records payload identity, observed effects, coverage gaps, overrides and next steps; does not sign or broadcast transactions.]

## Skill Version(s):

0.1.1 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
