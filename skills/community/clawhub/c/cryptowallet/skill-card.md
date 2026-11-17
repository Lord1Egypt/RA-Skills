## Description:

Complete cryptocurrency wallet management for Web3, DeFi, and blockchain applications, including encrypted EVM and Solana wallet storage, balance checks, token transfers, and smart contract interactions across multiple networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnufoo](https://clawhub.ai/user/gnufoo)

### License/Terms of Use:


## Use Case:

Developers and blockchain operators use this skill to create or import encrypted wallets, inspect balances, send tokens, and interact with EVM and Solana contracts from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real private keys and irreversible blockchain transactions.

Mitigation: Review before installing for real-fund use, start with a test wallet, and manually verify each recipient, network, amount, and contract.

Risk: Private keys or wallet passwords can be exposed if entered directly in shell commands.

Mitigation: Avoid entering private keys or wallet passwords directly in commands; use safer secret handling and prefer disposable test wallets first.

Risk: Batch transfers and contract writes can approve spending or move funds without recourse.

Mitigation: Do not use batch transfers or contract writes unless you fully understand the transaction and have tested the flow with small amounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gnufoo/skills/cryptowallet)
- [Network configuration](artifact/references/networks.json)
- [Security best practices](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create encrypted wallet files and submit irreversible blockchain transactions when scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
