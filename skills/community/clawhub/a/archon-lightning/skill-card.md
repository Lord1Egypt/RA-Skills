## Description: <br>
Archon Lightning enables Lightning Network payments through Archon DIDs, including wallet creation, sending and receiving sats, payment verification, and Lightning Address zaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macterra](https://clawhub.ai/user/macterra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage DID-linked Lightning wallets, generate invoices, send Lightning payments or zaps, inspect payment history, and publish or remove Lightning endpoints in DID documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to move real Lightning funds using local wallet credentials. <br>
Mitigation: Use only a low-balance wallet, require explicit human approval, and review the invoice, recipient, and amount before any payment or zap. <br>
Risk: Local Archon wallet credentials and passphrase material in ~/.archon.env can grant wallet access. <br>
Mitigation: Protect ~/.archon.env, avoid logging secrets, and restrict access to the wallet file and passphrase. <br>
Risk: The wrapper scripts rely on @didcid/keymaster through npx for wallet and Lightning operations. <br>
Mitigation: Pin and audit @didcid/keymaster before installation or execution. <br>
Risk: Lightning payment attempts can fail, remain pending, or time out after returning a payment hash. <br>
Mitigation: Verify settlement with the provided payment scripts or lightning-check before treating a payment as complete. <br>


## Reference(s): <br>
- [Archon documentation](https://github.com/archetech/archon) <br>
- [Keymaster reference](https://github.com/archetech/archon/tree/main/keymaster) <br>
- [Lightning Network](https://lightning.network) <br>
- [BOLT specifications](https://github.com/lightning/bolts) <br>
- [Lightning Address](https://lightningaddress.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Archon wallet configuration, ARCHON_* environment variables, node, npx, and jq; payment commands can move real Lightning funds.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
