## Description:

Self-sovereign EVM wallet for AI agents that can create wallets, check balances, send ETH or ERC20 tokens, swap tokens, and interact with smart contracts across Base, Ethereum, Polygon, Arbitrum, and Optimism while storing private keys locally with no cloud custody or API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfer77](https://clawhub.ai/user/surfer77)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent create and operate a self-custodied EVM wallet: checking balances, sending ETH or ERC20 tokens, swapping assets, and interacting with smart contracts after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unpinned remote code before performing high-impact wallet actions.

Mitigation: Use only a reviewed, pinned implementation or a bundled artifact, and verify locked dependencies before installation.

Risk: A token-address error could cause incorrect token handling or misleading transaction guidance.

Mitigation: Verify token addresses against authoritative chain sources before funding wallets, transferring tokens, or approving swaps.

Risk: The wallet private key is stored locally and can be used to move funds if exposed.

Mitigation: Protect ~/.evm-wallet.json as a real private key, keep file access restricted, and avoid funding the wallet with meaningful value until the implementation has been reviewed.

Risk: Transfers, swaps, approvals, and contract writes can move funds or grant spending permissions.

Mitigation: Require clear per-transaction user confirmation that includes recipient, token, amount, chain, gas estimate, and contract action before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/surfer77/skills/evm-wallet)
- [Project homepage](https://github.com/surfer77/evm-wallet-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and git; wallet command results are requested with --json for agent parsing.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
