## Description:

Deploy smart contracts and bridge assets to Abstract (ZK Stack L2), including contract deployment, ETH and token bridging, swaps, balance checks, transfers, Abstract mainnet contract calls, zksolc compilation, Hardhat deployment, Relay bridging, DEX trading, and key contract addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masoncags-tech](https://clawhub.ai/user/masoncags-tech)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to prepare and execute Abstract network workflows, including wallet setup, balance checks, bridging, swaps, transfers, contract deployment, and contract calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move Abstract mainnet funds using raw private keys.

Mitigation: Use only a dedicated low-value wallet and never use a primary or treasury private key.

Risk: Bridge, swap, transfer, deployment, and contract-call transactions are irreversible once signed.

Mitigation: Test on testnet or with tiny amounts first, then manually verify each destination, router, bridge route, contract function, value, and transaction before signing.

Risk: Unpinned or changed dependencies and external routes can alter transaction behavior.

Mitigation: Pin dependencies and review the installed packages and route outputs before running fund-moving scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/masoncags-tech/skills/abstract-toolkit)
- [Abstract Contract Addresses](artifact/references/addresses.md)
- [Abstract Global Wallet Guide](artifact/references/agw.md)
- [Hardhat Abstract Configuration](artifact/references/hardhat.config.js)
- [Abstract Troubleshooting Guide](artifact/references/troubleshooting.md)
- [Abstract Docs](https://docs.abs.xyz)
- [Abstract Global Wallet Docs](https://docs.abs.xyz/abstract-global-wallet/overview)
- [AGW SDK](https://github.com/Abstract-Foundation/agw-sdk)
- [Relay Abstract Bridge](https://relay.link/bridge/abstract)
- [Abscan Explorer](https://abscan.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for blockchain transactions; users must review commands and transaction details before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
