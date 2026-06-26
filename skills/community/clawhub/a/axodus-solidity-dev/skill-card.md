## Description: <br>
Implement secure Solidity smart contracts with tests and safety patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft Solidity contracts, tests, validation commands, and security notes for ERC-20, ERC-721, ERC-1155, or custom smart contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated smart contracts may contain exploitable logic or security mistakes. <br>
Mitigation: Treat generated contracts as draft code, run tests and static analysis, and obtain an independent audit before using contracts that control real assets. <br>
Risk: Deployment commands may affect live networks or assets if used without review. <br>
Mitigation: Review deployment commands manually and require a local or testnet dry run plus explicit user confirmation before mainnet deployment. <br>
Risk: Private keys, mnemonics, or RPC secrets could be exposed if supplied during contract work. <br>
Mitigation: Do not provide secrets to the skill or embed them in generated code, tests, configuration, or commands. <br>
Risk: Trigger metadata is not explicit in the packaged manifest. <br>
Mitigation: Fix the trigger metadata before installation so activation behavior is clear and intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-solidity-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with contract file paths, test file paths, validation commands, and security notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated smart contract outputs include assumptions and risk areas for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
