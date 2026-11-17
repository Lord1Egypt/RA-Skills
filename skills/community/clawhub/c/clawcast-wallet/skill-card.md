## Description:

Skill for managing EVM wallets, transactions, and network helpers via cast; covers onboarding, checks, and operating procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tezatezaz](https://clawhub.ai/user/tezatezaz)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to onboard and operate an EVM wallet with Foundry cast, including wallet creation or import, network selection, balance checks, token metadata lookup, transaction command guidance, and wallet removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets may be exposed because the skill handles mnemonics, private keys, and keystore passwords during onboarding.

Mitigation: Do not use valuable wallets with this release; prefer a hardware wallet or external signer and avoid entering secrets into chat.

Risk: Local plaintext wallet support files may expose funds if the host or workspace is compromised.

Mitigation: Review and change the secret-handling flow before installation; remove password, mnemonic, and temporary key files after use.

Risk: Installation and setup can make broad local or system changes, including Foundry installation and optional package-manager use.

Mitigation: Verify Foundry installation separately and do not allow sudo, package-manager commands, or automatic balance checks unless the exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tezatezaz/skills/clawcast-wallet)
- [Foundry cast installer](https://foundry.paradigm.xyz)
- [EVM network list](artifact/assets/evm-networks.json)
- [EVM token metadata](artifact/assets/evm-network-tokens.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local wallet state, keystore files, password files, token metadata, and transaction mention logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
