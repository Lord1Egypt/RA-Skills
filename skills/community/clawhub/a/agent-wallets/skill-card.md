## Description:

Route wallet workflows for agents that need to generate or import wallets using either a seed phrase or private key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beardkoda](https://clawhub.ai/user/beardkoda)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Agent-Wallet to route local blockchain wallet setup, recovery, balance, and transaction tasks to the correct viem-based workflow. It helps agents handle wallet addresses, key material, balances, and transaction confirmations while keeping secret material masked and stored through secure secret storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet generation and import workflows may expose seed phrases or private keys if secret material is pasted, logged, or stored incorrectly.

Mitigation: Use a real encrypted secret store, ask before reading environment-based secrets, mask secret material in outputs, and never print full seed phrases or private keys.

Risk: Send workflows can broadcast irreversible transactions with the wrong chain, recipient, amount, or fee.

Mitigation: Default to read-only behavior until the user explicitly requests a send, simulate or preflight when possible, and require confirmation of chain, recipient, amount, and estimated fee before broadcast.

## Reference(s):

- [ClawHub Agent-Wallet release](https://clawhub.ai/beardkoda/skills/agent-wallets)
- [Local wallet router](artifact/local-wallet/SKILL.md)
- [Wallet generation and import workflow](artifact/local-wallet/generate/SKILL.md)
- [Wallet balance workflow](artifact/local-wallet/balance/SKILL.md)
- [Wallet transaction send workflow](artifact/local-wallet/send/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript examples and a structured response contract]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet action summaries with action, chain, address, txHash, status, and next_step fields.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
