## Description: <br>
Skill for managing EVM wallets, transactions, and network helpers via cast; covers onboarding, checks, and operating procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tezatezaz](https://clawhub.ai/user/tezatezaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to set up and operate a local hot wallet for EVM networks with Foundry cast. It supports wallet creation or import, network selection, balance checks, token metadata, transaction command guidance, and wallet removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles local hot-wallet secrets and stores sensitive wallet material on disk. <br>
Mitigation: Use only limited funds, avoid importing valuable seed phrases or private keys, and remove wallet material when it is no longer needed. <br>
Risk: Installation and setup commands may change the local environment. <br>
Mitigation: Review installation commands before running them and avoid granting sudo during wallet setup. <br>
Risk: Transaction signing or broadcasting can move real assets irreversibly. <br>
Mitigation: Require explicit human confirmation before any transaction is signed or broadcast. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tezatezaz/clawcast) <br>
- [ClawAudit report](https://clawaudit.duckdns.org/audit/7737be97-edda-4cd4-9070-fa47547dd44a) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>
- [EVM network list](artifact/assets/evm-networks.json) <br>
- [EVM token metadata](artifact/assets/evm-network-tokens.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide scripts that create local wallet state, keystore files, password files, and transaction mention logs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
