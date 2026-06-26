## Description: <br>
Send and receive Bitcoin over Arkade, onchain, and Lightning, and swap USDC/USDT stablecoins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiero](https://clawhub.ai/user/tiero) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent initialize an Arkade wallet, inspect balances and addresses, prepare Bitcoin payments, use Lightning invoices, and perform BTC-to-stablecoin swaps. It is intended for wallet workflows where the user confirms fund-moving actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment and swap actions can move real funds immediately. <br>
Mitigation: Require explicit user approval before fund-moving commands and verify the amount, destination, network, fees, and finality before execution. <br>
Risk: Wallet configuration stores private key material locally at ~/.arkade-wallet/config.json. <br>
Mitigation: Protect the local configuration file, use only small test amounts at first, and do not paste existing private keys into prompts or shell commands. <br>
Risk: The security verdict requires review before installation. <br>
Mitigation: Review and scan the skill before deployment, then start with limited balances until expected wallet behavior is confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tiero/bitcoin-arkade-wallet) <br>
- [Arkade documentation](https://docs.arkadeos.com) <br>
- [Arkade service endpoint](https://arkade.computer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run wallet, payment, Lightning, and swap commands; fund-moving actions require explicit user review of amount, destination, network, fees, and finality.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
