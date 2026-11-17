## Description:

Implement secure Solidity smart contracts with tests and safety patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design Solidity smart contracts, generate tests, and produce validation commands with explicit security controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated contracts or tests may contain security defects if requirements, roles, invariants, or external-call behavior are underspecified.

Mitigation: Review generated contracts, tests, deployment parameters, and security assumptions before using the output.

Risk: Validation commands may use ambient or unpinned Hardhat or Foundry dependencies.

Mitigation: Prefer project-local or pinned dependencies when compiling, testing, and running static checks.

Risk: Mainnet deployment can cause irreversible financial or operational impact.

Mitigation: Require explicit user approval and complete a dry-run on local or testnet infrastructure before mainnet deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mzfshark/skills/axodus-solidity-dev)
- [Publisher Profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Solidity source paths, test paths, validation commands, and security notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mainnet deployment requires explicit user confirmation and prior local or testnet dry-run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
