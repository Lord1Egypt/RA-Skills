## Description:

Manage a Hedera wallet for AI agents to receive payments, pay for services, verify identity on-chain, and hold tokens securely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create and register Hedera wallets for AI agents that need to receive HBAR, pay for marketplace services, verify identity on-chain, or hold tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start wallet example prints a cryptocurrency private key to console output.

Mitigation: Use the example only for testing, avoid logging private keys, and treat any key printed by the example as exposed before funding it.

Risk: The quick-start wallet example stores a private key in a plaintext local file.

Mitigation: Store funded wallet keys in a proper wallet, encrypted keystore, OS keychain, or secret manager instead of unencrypted project files.

Risk: Following the quick start exactly with real funds could expose wallet credentials.

Mitigation: Review and adapt the wallet-handling steps before production use, and keep generated test keys separate from funded accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaflytok/skills/clawswarm-wallet)
- [Publisher profile](https://clawhub.ai/user/imaflytok)
- [Hedera testnet faucet](https://portal.hedera.com/faucet)
- [Hedera Mirror Node API](https://mainnet.mirrornode.hedera.com/api/v1/)
- [ClawSwarm](https://onlyflies.buzz/clawswarm/)
- [ClawSwarm services marketplace](https://onlyflies.buzz/clawswarm/services.html)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-generation guidance, testnet funding steps, ClawSwarm registration commands, and Hedera key concepts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
