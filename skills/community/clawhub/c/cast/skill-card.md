## Description: <br>
Skill for managing EVM wallets, transactions, and network helpers via cast; covers onboarding, checks, and operating procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tezatezaz](https://clawhub.ai/user/tezatezaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to set up and operate a local EVM hot-wallet workflow with Foundry cast, including wallet onboarding, network and token selection, balance checks, and transaction preparation or inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a local hot wallet and may store wallet secrets, keystore passwords, RPC URLs, and transaction metadata on disk. <br>
Mitigation: Use it only with a low-value wallet, avoid importing valuable seed phrases, avoid reusing passwords, and review the scripts before installation or use. <br>
Risk: Wallet and transaction actions can affect real EVM assets if used with funded accounts. <br>
Mitigation: Prefer manual or hardware-wallet workflows for significant funds, and require explicit user confirmation before sending or publishing transactions. <br>
Risk: The setup flow can install Foundry/cast and modify local wallet-related files. <br>
Mitigation: Run it in a trusted local environment, inspect the planned changes, and use the removal workflow when the wallet helper is no longer needed. <br>


## Reference(s): <br>
- [Cast release page](https://clawhub.ai/tezatezaz/cast) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>
- [EVM network metadata](artifact/assets/evm-networks.json) <br>
- [EVM token metadata](artifact/assets/evm-network-tokens.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local wallet state, RPC configuration, token metadata, and transaction mention logs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
