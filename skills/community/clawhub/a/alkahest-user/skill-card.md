## Description: <br>
Interact with Alkahest escrow contracts as a buyer, seller, or oracle using the CLI <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to draft CLI workflows for creating, fulfilling, arbitrating, collecting, reclaiming, and inspecting Alkahest escrow transactions on supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains patterns for wallet secrets and fund-moving blockchain transactions. <br>
Mitigation: Use a dedicated low-balance wallet, prefer testnets first, and avoid putting private keys or mnemonics in prompts, shell history, CLI arguments, source files, logs, or shared environment variables. <br>
Risk: Approval, escrow, payment, arbitration, collection, reclaim, and slash commands can move funds or change on-chain state. <br>
Mitigation: Require explicit human approval and verify the chain, contract, token, amount, arbiter, UID, and expiration before running any transaction command. <br>


## Reference(s): <br>
- [Alkahest User ClawHub Release](https://clawhub.ai/mlegls/alkahest-user) <br>
- [Alkahest Arbiter Reference](references/arbiters.md) <br>
- [Alkahest Contract Reference](references/contracts.md) <br>
- [TypeScript SDK Reference](references/typescript-sdk.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command examples may prepare real blockchain transactions and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
