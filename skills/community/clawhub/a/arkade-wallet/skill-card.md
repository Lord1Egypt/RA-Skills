## Description: <br>
Send and receive Bitcoin over Arkade (offchain), onchain (via onboard/offboard), and Lightning. Swap USDC/USDT stablecoins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiero](https://clawhub.ai/user/tiero) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let agents operate an Arkade wallet for Bitcoin payments across Arkade, onchain, and Lightning, and to request stablecoin swap quotes or swaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents direct ability to create wallets and move cryptocurrency funds. <br>
Mitigation: Treat it as a hot-wallet integration: keep only small balances available and require explicit human approval for every payment, offboard, Lightning payment, or swap. <br>
Risk: Payment destinations and amounts may be irreversible or difficult to recover once executed. <br>
Mitigation: Verify the destination, chain, token, and amount out of band before authorizing any fund movement. <br>
Risk: Wallet data and private keys are stored locally and stale examples may still show private-key command usage. <br>
Mitigation: Back up wallet data carefully and do not paste existing private keys into command lines. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tiero/arkade-wallet) <br>
- [Arkade documentation](https://docs.arkadeos.com) <br>
- [Arkade skill source reference](https://github.com/arkade-os/skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet addresses, balances, invoices, transaction identifiers, swap quotes, and payment status when the described commands or SDK calls are executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; package.json reports 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
