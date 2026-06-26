## Description: <br>
AWP Wallet gives agents an EVM wallet CLI for transfers, balance checks, approvals, message signing, gas estimates, transaction status, and gasless operations across configured EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kilb](https://clawhub.ai/user/kilb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate an EVM wallet for balance queries, token transfers, approvals, signing, transaction history, and gasless transaction workflows. It is intended for wallet operations that require explicit user confirmation before high-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize wallet transfers, approvals, signatures, batch operations, API-key persistence, and EIP-7702 actions. <br>
Mitigation: Require explicit human review before every transfer, approval, signature, batch operation, API-key persistence action, and EIP-7702 operation. <br>
Risk: Using an existing or high-value wallet could expose significant funds to agent mistakes or misuse. <br>
Mitigation: Use a dedicated low-value wallet and avoid importing an existing seed phrase. <br>
Risk: Local secret-management behavior and installation choices affect wallet security. <br>
Mitigation: Avoid sudo installation, inspect ~/.openclaw-wallet storage before use, and configure recipient restrictions where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kilb/awp-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/kilb) <br>
- [Project homepage](https://github.com/awp-core/awp-wallet) <br>
- [Node package install metadata](npm:awp-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses session tokens for wallet operations and optional environment variables for wallet password, gasless providers, and wallet isolation.] <br>

## Skill Version(s): <br>
0.15.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
