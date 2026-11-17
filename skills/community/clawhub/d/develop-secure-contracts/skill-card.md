## Description:

Helps agents integrate OpenZeppelin Contracts components into Solidity, Cairo, Stylus, and Stellar smart contracts by reading the project and library source before proposing changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or adapt OpenZeppelin library components in existing or new smart-contract projects while preserving project context and dependency patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated smart-contract changes can introduce incorrect authorization, upgrade, or storage behavior if applied without review.

Mitigation: Review every contract diff, run the project's tests and security tooling, and require independent audit before deployment or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/develop-secure-contracts)
- [OpenZeppelin Contracts documentation](https://docs.openzeppelin.com/contracts)
- [OpenZeppelin Contracts for Cairo documentation](https://docs.openzeppelin.com/contracts-cairo)
- [OpenZeppelin Contracts for Stylus documentation](https://docs.openzeppelin.com/contracts-stylus)
- [OpenZeppelin Contracts for Stellar documentation](https://docs.openzeppelin.com/stellar-contracts)
- [OpenZeppelin Solidity contracts repository](https://github.com/OpenZeppelin/openzeppelin-contracts)
- [OpenZeppelin Cairo contracts repository](https://github.com/OpenZeppelin/cairo-contracts)
- [OpenZeppelin Stylus contracts repository](https://github.com/OpenZeppelin/rust-contracts-stylus)
- [OpenZeppelin Stellar contracts repository](https://github.com/OpenZeppelin/stellar-contracts)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code snippets, shell commands, and proposed file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review generated contract diffs before deployment.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
