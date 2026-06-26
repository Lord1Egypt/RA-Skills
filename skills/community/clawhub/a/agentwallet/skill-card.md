## Description: <br>
The agent's wallet for EVM chain transactions and raw signing, enabling agents to create wallets, transfer tokens, swap on DEXs, interact with smart contracts, and sign messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent policy-controlled wallet capabilities for EVM transfers, token swaps, smart contract interactions, balance checks, and raw message signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent wallet actions can move funds or sign messages, creating real financial exposure if policies are loose or absent. <br>
Mitigation: Claim the wallet immediately, configure spending limits, address and token allowlists, and approval requirements before funding it or executing meaningful transactions. <br>
Risk: Unclaimed wallets can operate without policy limits. <br>
Mitigation: Do not leave wallets unclaimed; revoke or relink keys if access is lost or ownership is uncertain. <br>
Risk: Stored scoped API keys and relink tokens can enable wallet operations within policy. <br>
Mitigation: Protect the credential directory, treat relink tokens as sensitive, and revoke compromised keys from the Vincent service. <br>


## Reference(s): <br>
- [Vincent homepage](https://heyvincent.ai) <br>
- [ClawHub skill listing](https://clawhub.ai/glitch003/agentwallet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands use @vincentai/cli and store scoped wallet credentials in configured paths.] <br>

## Skill Version(s): <br>
1.0.70 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
