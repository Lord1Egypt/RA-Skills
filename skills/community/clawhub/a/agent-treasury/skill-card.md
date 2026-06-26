## Description: <br>
Manage your agent's crypto wallet. Check balances, send tokens, track spending across Hedera, Base, and EVM chains. Built for agents who earn and spend on-chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to check crypto wallet balances, track bounty income and spending, inspect gas prices, and prepare HBAR transfer code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes live crypto-transfer code and examples that can move funds if credentials, account IDs, recipient IDs, and amounts are filled in. <br>
Mitigation: Use a dedicated low-balance wallet, require manual approval for every transfer, and verify recipient and amount outside the agent before execution. <br>
Risk: The transfer snippet places an operator private key directly in code. <br>
Mitigation: Do not paste production private keys into generated scripts; use safer secret handling and restrict wallet permissions before testing. <br>
Risk: The artifact contains an unexplained onlyflies.buzz registration and ping marker. <br>
Mitigation: Review the hidden endpoint marker and network behavior before trusting or deploying the skill. <br>
Risk: The skill writes a local treasury ledger that may expose financial activity. <br>
Mitigation: Protect the ledger file and limit access to the local configuration directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaflytok/agent-treasury) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and checklist snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live wallet balance queries, local ledger commands, gas price checks, and crypto transfer snippets requiring manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
