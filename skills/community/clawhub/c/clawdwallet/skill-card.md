## Description: <br>
Install and control ClawdWallet - a multi-chain Web3 wallet Chrome extension controlled by Clawdbot agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeOMakinG](https://clawhub.ai/user/NeOMakinG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up an agent-controlled multi-chain wallet, connect to dApps, review wallet requests, and approve or reject signing actions across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose wallet mnemonics and transaction-signing authority to an agent. <br>
Mitigation: Use a new low-value wallet only, never provide a primary wallet mnemonic, and require manual human confirmation for every signature or transaction. <br>
Risk: The WebSocket wallet-control interface could be misused if exposed beyond the trusted local environment. <br>
Mitigation: Keep the WebSocket bound to localhost on a trusted machine and do not expose the WebSocket URL publicly. <br>
Risk: Prebuilt wallet code may not match a user's security expectations. <br>
Mitigation: Review and build the referenced wallet code before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NeOMakinG/clawdwallet) <br>
- [Publisher profile](https://clawhub.ai/user/NeOMakinG) <br>
- [ClawdWallet source repository](https://github.com/NeOMakinG/clawdwallet.git) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON commands, Guidance] <br>
**Output Format:** [Markdown with bash, YAML, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wallet setup instructions, gateway configuration, and agent command examples for wallet initialization, status checks, dApp request handling, and signing decisions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
