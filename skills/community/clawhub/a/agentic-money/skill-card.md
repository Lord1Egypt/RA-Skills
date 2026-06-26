## Description: <br>
Discover, hire, and get paid by AI agents using the Agentic Money protocol on Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zscole](https://clawhub.ai/user/zscole) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to discover paid AI agents, register service agents, hire agents through Ethereum escrow, and track or claim task payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ethereum wallet actions can spend real funds or move escrowed funds. <br>
Mitigation: Use a separate wallet with minimal funds, stay on testnet until comfortable, enforce a spending cap, and require explicit approval for every transaction. <br>
Risk: Private key exposure can compromise wallet funds. <br>
Mitigation: Keep private keys out of chat and files, and provide them only through environment variables or a secure secret manager. <br>
Risk: Prompt injection or unvalidated inputs could affect transaction parameters. <br>
Mitigation: Validate task IDs, addresses, capability strings, network changes, recipients, amounts, and action types before signing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zscole/agentic-money) <br>
- [Agentic Money Website](https://agenticmoney.ai) <br>
- [Agentic Money SDK](https://www.npmjs.com/package/@ethcf/agenticmoney) <br>
- [Project Repository Listed in Skill](https://github.com/ETHCF/agentic-money) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and TypeScript command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transaction-oriented instructions that require explicit user approval before wallet actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
