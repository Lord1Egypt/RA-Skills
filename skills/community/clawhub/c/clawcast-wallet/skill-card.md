## Description: <br>
Skill for managing EVM wallets, transactions, and network helpers via cast; covers onboarding, checks, and operating procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tezatezaz](https://clawhub.ai/user/tezatezaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to set up and operate a local EVM hot wallet with Foundry cast for wallet checks, network selection, token awareness, and transaction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet-control secrets and stores sensitive wallet files locally, including keystores, password files, temporary private keys, and mnemonic backups. <br>
Mitigation: Use only low-value or purpose-built wallets, review files under ~/.agent-wallet, remove plaintext mnemonic and password files after setup, and run the removal script when the wallet is no longer needed. <br>
Risk: Setup can alter the host by installing Foundry/cast and, when mnemonic cleanup scheduling is needed, attempting to install or use the at scheduler. <br>
Mitigation: Review installation and sudo prompts before approving them, and install dependencies manually in a controlled environment when host changes must be audited. <br>
Risk: Transaction logs and explorer links can expose sensitive financial metadata about addresses and transfers. <br>
Mitigation: Treat logs/tx_mentions.log as sensitive, avoid sharing logs publicly, and clear wallet-specific entries during teardown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tezatezaz/clawcast-wallet) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local wallet state, keystore, password, mnemonic, network, token, and transaction-log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
