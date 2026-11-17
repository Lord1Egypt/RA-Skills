## Description:

Comprehensive blockchain toolkit for Ethereum wallet management, smart contract interaction, NFT minting, token balance checks, and gas fee monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Ethereum wallets, balances, smart contracts, NFT operations, and gas fee data from a ClawHub skill release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets may be exposed through private-key printing or default serialization.

Mitigation: Use secret-storage protections, remove private-key printing and default private-key serialization, and avoid funded wallets unless these protections are added.

Risk: Deploy, mint, transfer, and other state-changing transactions can trigger irreversible on-chain actions.

Mitigation: Require explicit user confirmation before every state-changing transaction and avoid production mainnet accounts unless reviewed safeguards are in place.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin dependencies before use in sensitive or production environments.

## Reference(s):

- [Blockchain Web3 Toolkit on ClawHub](https://clawhub.ai/kaiyuelv/skills/blockchain-web3-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet addresses, transaction hashes, gas price data, contract addresses, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
