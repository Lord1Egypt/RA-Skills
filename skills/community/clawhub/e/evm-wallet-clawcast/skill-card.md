## Description: <br>
This skill is focused on crypto/EVM wallet operations and transaction workflows using cast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tezatezaz](https://clawhub.ai/user/tezatezaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to set up and operate an EVM hot wallet with Foundry cast, including key creation or import, network selection, balance checks, token awareness, transaction preparation, and wallet removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages a real EVM hot wallet and can support value-bearing transactions. <br>
Mitigation: Use a fresh low-balance wallet and manually confirm network, recipient, value, calldata, gas, and broadcast intent before every transaction. <br>
Risk: Wallet secrets, a keystore, and the keystore password can be stored locally under ~/.agent-wallet during onboarding. <br>
Mitigation: Protect ~/.agent-wallet, do not import valuable existing seed phrases or private keys, and run the wallet removal script when the workflow is complete. <br>
Risk: Setup can install Foundry/cast and may request installer, package manager, or sudo approval. <br>
Mitigation: Review every installer or sudo prompt before approval, and install dependencies manually in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tezatezaz/evm-wallet-clawcast) <br>
- [Foundry installer and cast tooling](https://foundry.paradigm.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and interactive prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local wallet state, keystore, password, token, network, and transaction log files during guided wallet workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
