## Description:

Register your AI agent onchain with ERC-8004 on Base. Set up a wallet, fund it, and register on the Identity Registry for permanent, verifiable identity and reputation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squirt11e](https://clawhub.ai/user/squirt11e)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create a Base mainnet wallet, fund it for gas, and register an AI agent with ERC-8004 identity metadata. It also guides updates to the agent registration after creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys can be exposed if printed, logged, committed, or copied into insecure storage.

Mitigation: Generate and store keys in a secure wallet, encrypted keystore, or secret manager; avoid printing private keys and rotate any key that appears in logs.

Risk: Agent names, descriptions, images, service endpoints, and reputation data published onchain are public and persistent.

Mitigation: Publish only intentionally public metadata and review service endpoints before registration or update transactions.

Risk: Running dependency installation and blockchain examples without dependency controls can introduce supply-chain or execution risk.

Mitigation: Use pinned dependencies or a trusted lockfile and review commands before running them.

## Reference(s):

- [ERC-8004 protocol homepage](https://8004.org)
- [ERC-8004 registration schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)
- [Base](https://base.org)
- [viem](https://viem.sh)
- [Identity Registry on BaseScan](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432)
- [Reputation Registry on BaseScan](https://basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63)
- [Relay bridge](https://relay.link/bridge)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet setup, funding checks, registry transactions, and metadata update examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
