## Description: <br>
Develop secure smart contracts using OpenZeppelin Contracts libraries across Solidity, Cairo, Stylus, and Stellar by discovering library patterns, integrating existing components, and avoiding custom code when vetted library code exists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart contract engineers use this skill to integrate OpenZeppelin components into new or existing contracts, including token standards, access control, security primitives, governance, upgrades, and account features. It emphasizes reading the project and installed dependency source before proposing or applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated contract changes can introduce security, inheritance, initialization, or storage-layout mistakes if dependency patterns are misread or applied too broadly. <br>
Mitigation: Read the existing project and installed OpenZeppelin source first, keep changes minimal, review the resulting diff, and run the project's contract tests and security checks. <br>
Risk: Using generic advice instead of the installed library version can produce incorrect override points or obsolete integration patterns. <br>
Mitigation: Verify APIs, hooks, constructors, and required overrides against the locally installed dependency or the relevant canonical documentation before editing contracts. <br>


## Reference(s): <br>
- [OpenZeppelin Contracts documentation](https://docs.openzeppelin.com/contracts) <br>
- [OpenZeppelin Contracts for Cairo documentation](https://docs.openzeppelin.com/contracts-cairo) <br>
- [OpenZeppelin Contracts for Stylus documentation](https://docs.openzeppelin.com/contracts-stylus) <br>
- [OpenZeppelin Stellar Contracts documentation](https://docs.openzeppelin.com/stellar-contracts) <br>
- [OpenZeppelin Solidity Contracts repository](https://github.com/OpenZeppelin/openzeppelin-contracts) <br>
- [OpenZeppelin Cairo Contracts repository](https://github.com/OpenZeppelin/cairo-contracts) <br>
- [OpenZeppelin Stylus Contracts repository](https://github.com/OpenZeppelin/rust-contracts-stylus) <br>
- [OpenZeppelin Stellar Contracts repository](https://github.com/OpenZeppelin/stellar-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and direct file edits when implementation is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify existing contract files; users should review diffs and run project tests before relying on generated changes.] <br>

## Skill Version(s): <br>
98.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
