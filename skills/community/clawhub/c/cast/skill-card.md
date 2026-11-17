## Description:

Skill for managing EVM wallets, transactions, and network helpers via cast; covers onboarding, checks, and operating procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tezatezaz](https://clawhub.ai/user/tezatezaz)

### License/Terms of Use:


## Use Case:

Developers and operators use Cast to set up and manage EVM hot wallets with Foundry cast, choose EVM network and token metadata, check balances, prepare or send transactions, and remove wallet state when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle complete wallet-control secrets and local keystore passwords.

Mitigation: Review scripts before installation, avoid wallets holding meaningful funds, prefer a hardware wallet or separate signer, and avoid importing existing seed phrases.

Risk: The skill can install Foundry through a remote installer and make local or system changes.

Mitigation: Decline unverified remote installers and sudo package changes; install dependencies through a trusted channel when possible.

Risk: Testing can leave wallet files or transaction logs on disk.

Mitigation: Delete ~/.agent-wallet and any workspace transaction logs after testing.

## Reference(s):

- [Cast ClawHub skill page](https://clawhub.ai/tezatezaz/skills/cast)
- [Foundry installer](https://foundry.paradigm.xyz)
- [EVM network metadata](artifact/assets/evm-networks.json)
- [EVM token metadata](artifact/assets/evm-network-tokens.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and interactive script prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local wallet state, keystore, password, mnemonic backup, token metadata, and transaction log files during use.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
