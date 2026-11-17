## Description:

Verify AI agent identity and reputation via ERC-8004 on-chain registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumeetchougule](https://clawhub.ai/user/sumeetchougule)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to check whether an AI agent has an ERC-8004 identity and to review on-chain reputation signals before trusting that agent. Users can also check their own wallet identity or optionally register an agent, which requires a wallet private key and an on-chain transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional registration command can sign and broadcast an on-chain transaction when a private key is configured.

Mitigation: Use read-only commands without setting a private key unless registration is required, and prefer a dedicated low-balance wallet.

Risk: Mainnet registration can spend real gas and create a permanent on-chain action.

Mitigation: Prefer Sepolia or another testnet for registration and avoid mainnet registration until the warning and confirmation behavior has been reviewed.

Risk: The setup flow installs Python dependencies in an environment that may also contain wallet secrets.

Mitigation: Review or pin dependencies before running setup, and keep wallet secrets out of general-purpose development environments.

## Reference(s):

- [ChaosChain](https://chaoscha.in)
- [ChaosChain Documentation](https://docs.chaoscha.in)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [8004scan Agent Explorer](https://8004scan.io)
- [ClawHub Skill Page](https://clawhub.ai/sumeetchougule/skills/chaoschain)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style command responses with wallet addresses, registration status, trust scores, reputation dimensions, and explorer links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only commands depend on Python dependencies and RPC connectivity; identity checks and registration can use wallet environment variables.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
