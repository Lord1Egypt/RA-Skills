## Description:

ClawCast guides agents through EVM wallet setup and transaction workflows with Foundry cast, including key creation or import, network selection, balance checks, token handling, and transaction preparation or submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tezatezaz](https://clawhub.ai/user/tezatezaz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to set up and operate a local EVM hot wallet through an agent-assisted Foundry cast workflow. It helps create or import wallet keys, configure networks and tokens, check balances, and prepare or send transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or import a local hot wallet and store wallet secrets or passwords on disk.

Mitigation: Review the scripts before installation, use a low-value test wallet, avoid importing funded seed phrases or private keys, and prefer hardware or external signing for real funds.

Risk: The setup flow can modify local toolchain and package state while installing Foundry/cast.

Mitigation: Install only in an environment where toolchain changes are acceptable and inspect the installation script before execution.

Risk: Wallet metadata such as addresses, keystore paths, network configuration, balances, RPC URLs, or transaction references may be displayed or logged during normal operation.

Mitigation: Treat wallet metadata as sensitive, avoid sharing logs publicly, and remove wallet state when the skill is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tezatezaz/skills/evm-wallet-clawcast)
- [EVM network list](assets/evm-networks.json)
- [EVM token metadata](assets/evm-network-tokens.json)
- [Foundry installer](https://foundry.paradigm.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown/plain text guidance with shell commands and local configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local wallet state, keystore files, password files, token metadata updates, and transaction mention logs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
