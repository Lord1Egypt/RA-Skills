## Description:

Skill for managing EVM wallets, transactions, and network helpers via cast; covers onboarding, checks, and operating procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tezatezaz](https://clawhub.ai/user/tezatezaz)

### License/Terms of Use:


## Use Case:

Developers and crypto wallet operators use this skill to create or import EVM wallets, configure networks, inspect balances, and prepare everyday cast-based transaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet seed phrases, private keys, and keystore passwords may be stored in local plaintext helper files during onboarding.

Mitigation: Use only low-value test wallets unless the workflow is changed to avoid plaintext secret storage and to require secure secret entry at execution time.

Risk: The setup flow may run unverified installer commands and package installation with elevated privileges.

Mitigation: Review installer commands before execution, install Foundry through a trusted channel, and remove automatic sudo package installation from the workflow.

Risk: Wallet paths, balances, and transaction references may be displayed or logged locally.

Mitigation: Make balance checks and transaction logging opt-in, avoid exposing wallet metadata unnecessarily, and clear local logs when removing a wallet.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tezatezaz/skills/clawcast)
- [Foundry installer](https://foundry.paradigm.xyz)
- [EVM network list](assets/evm-networks.json)
- [EVM token metadata](assets/evm-network-tokens.json)
- [ClawAudit report](https://clawaudit.duckdns.org/audit/7737be97-edda-4cd4-9070-fa47547dd44a)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and interactive prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local wallet configuration, keystore paths, network settings, token metadata updates, and transaction log entries during guided operation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
