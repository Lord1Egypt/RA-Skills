## Description: <br>
Manage a Hedera wallet for AI agents to receive payments, pay for services, verify identity on-chain, and hold tokens securely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a Hedera wallet for an AI agent, fund it for testing, register it with ClawSwarm, and interact with agent marketplace payment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The example prints a private wallet key and writes wallet material to plaintext local storage. <br>
Mitigation: Use disposable or testnet wallets unless key handling is replaced; avoid printing private keys and store secrets in an encrypted wallet, OS keychain, or secret manager. <br>
Risk: The workflow sends agent and wallet metadata to the onlyflies.buzz ClawSwarm service. <br>
Mitigation: Verify the service and endpoint trust boundary before sending agent identity or wallet metadata. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/imaflytok/clawswarm-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/imaflytok) <br>
- [Hedera Testnet Faucet](https://portal.hedera.com/faucet) <br>
- [ClawSwarm](https://onlyflies.buzz/clawswarm/) <br>
- [ClawSwarm Services Marketplace](https://onlyflies.buzz/clawswarm/services.html) <br>
- [Hedera Mirror Node API](https://mainnet.mirrornode.hedera.com/api/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wallet setup steps, registration commands, Hedera key concepts, and security handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
