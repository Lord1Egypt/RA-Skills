## Description:

Check USDC balances across Base and Solana networks, including mainnet and testnet/devnet options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check available USDC funds across supported Base and Solana wallets. It is intended for balance verification, fund visibility, and network-specific balance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the latest external agnic npm CLI in a wallet-related workflow.

Mitigation: Use a reviewed, version-pinned CLI package before deployment and review proposed shell commands before execution.

Risk: Balance checks may expose wallet addresses, balances, or wallet-related tokens in logs or shared environments.

Mitigation: Run in private sessions, avoid logging command output or tokens, and pass AGNIC_TOKEN through a secret-management mechanism.

Risk: Broad balance-related triggers may cause wallet checks from vague user requests.

Mitigation: Confirm user intent before running balance commands, especially in shared, logged, or production environments.

## Reference(s):

- [Agnic Check Balance on ClawHub](https://clawhub.ai/agnicpay-prog/skills/check-balance)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return wallet addresses and USDC balances for supported networks.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
