## Description:

Deploy ERC20 tokens on Base using Clanker SDK. Create tokens with built-in Uniswap V4 liquidity pools. Supports Base mainnet and Sepolia testnet. Requires PRIVATE_KEY in config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spirosrap](https://clawhub.ai/user/spirosrap)

### License/Terms of Use:


## Use Case:

External developers and crypto operators use this skill to configure wallets, inspect Base token data, and deploy ERC20 tokens through the Clanker protocol with optional Uniswap V4 liquidity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys may be exposed or mishandled during configuration and deployment.

Mitigation: Use only throwaway testnet keys until key handling and file permissions are reviewed and fixed.

Risk: Mainnet deployment can spend ETH through irreversible blockchain transactions.

Mitigation: Avoid funded mainnet wallets unless the operator has reviewed the exact transaction path, contract addresses, dependency versions, and spending amount.

Risk: Contract addresses and deployment dependencies may be unsafe or stale.

Mitigation: Verify Clanker contract addresses against official documentation and pin deployment dependencies before using the skill for production funds.

## Reference(s):

- [Clanker SDK Reference](references/clanker-sdk.md)
- [Clanker homepage](https://clanker.world)
- [Clanker documentation](https://docs.clanker.world)
- [Clanker GitHub](https://github.com/clanker-world)
- [ClawHub skill page](https://clawhub.ai/spirosrap/skills/clanker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON snippets plus terminal command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit irreversible Base mainnet or Sepolia transactions when run with a funded private key and deployment dependencies.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
