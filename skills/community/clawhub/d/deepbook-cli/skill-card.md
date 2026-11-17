## Description:

Operate the deepbook CLI for DeepBook reads (REST/SSE), global ~/.deepbook config/account management, on-chain spot trading, top-level swap execution, balance-manager ops, and margin trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astinz](https://clawhub.ai/user/astinz)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to operate the DeepBook CLI end to end for market reads, wallet and account setup, spot orders, swaps, balance-manager operations, and margin trading on Sui.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys and API keys can be exposed if they are placed in command arguments, chat, logs, or tool-call text.

Mitigation: Use stdin, a keychain, hardware wallet, or protected signer; never place private keys or API keys in prompts, command arguments, or logs.

Risk: Mainnet trades, deposits, withdrawals, swaps, manager creation, and margin actions can move funds or create financial exposure.

Mitigation: Require explicit human approval before live execution and verify network, pool, manager ID, amounts, and dry-run output first.

Risk: Incorrect CLI package provenance can expose users to unreviewed code before interacting with wallets or markets.

Mitigation: Review the CLI source and package provenance before installation and prefer a pinned, project-local install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/astinz/skills/deepbook-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run-first operational guidance for wallet, manager, trading, swap, and margin commands.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
