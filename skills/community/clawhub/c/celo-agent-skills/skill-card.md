## Description:

Celo Agent Skills is an end-to-end Celo development playbook for building dApps, smart contracts, stablecoin fee flows, MiniPay Mini Apps, and agent payment and trust integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viral-sangani](https://clawhub.ai/user/viral-sangani)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to implement Celo applications and smart contracts with viem-first transaction handling, fee abstraction, MiniPay support, stablecoin integrations, contract verification, and agent payment and trust patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples can encourage executing remote scripts or unpinned tool versions.

Mitigation: Review install commands before use, prefer pinned and verified tool versions, and avoid curl-to-bash patterns in sensitive projects.

Risk: Wallet-key handling examples can normalize storing or passing private keys in unsafe places.

Mitigation: Use test wallets or low-value keys during development, keep production or highly funded wallet keys out of .env files and command-line arguments, and use managed secret storage where available.

Risk: Mainnet, DeFi, bridging, and x402 payment actions can move funds or call external endpoints.

Mitigation: Require explicit user confirmation and validate network, endpoint, recipient, token, and amount before proposing or running fund-moving actions.

## Reference(s):

- [Celo Fee Currency](https://docs.celo.org/developer/fee-currency)
- [Celo Token Contracts](https://docs.celo.org/tooling/contracts/token-contracts)
- [Celo Core Contracts](https://docs.celo.org/tooling/contracts/core-contracts)
- [MiniPay](https://docs.celo.org/build-with-celo/minipay)
- [viem Celo Chain Documentation](https://viem.sh/docs/chains/celo)
- [thirdweb x402 Documentation](https://portal.thirdweb.com/x402)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [x402 Whitepaper](https://www.x402.org/x402-whitepaper.pdf)
- [Celo Agent Skills on ClawHub](https://clawhub.ai/viral-sangani/skills/celo-agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include network-specific addresses, wallet compatibility notes, install/build/test/deploy commands, and implementation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
