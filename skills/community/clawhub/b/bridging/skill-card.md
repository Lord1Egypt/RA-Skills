## Description:

Bridge assets to and from Celo. Use when transferring tokens between Celo and other chains like Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[san-npm](https://clawhub.ai/user/san-npm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to identify Celo bridge options, contract addresses, supported tokens, and integration patterns for moving assets between Celo and other chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can initiate real mainnet asset transfers.

Mitigation: Use testnets first and require explicit confirmation of chain, amount, recipient, token, and bridge provider before any wallet prompt is signed.

Risk: Incorrect or stale contract addresses can route assets to unintended contracts.

Mitigation: Verify contract addresses against official Celo, bridge provider, and block explorer sources before use.

Risk: Bridge fees, delays, approvals, and provider security models vary by route.

Mitigation: Review fees, timing, approvals, withdrawal periods, and bridge provider risk before transferring assets.

## Reference(s):

- [Bridge Contract Addresses](references/bridge-contracts.md)
- [Bridged Tokens on Celo](references/bridged-tokens.md)
- [Celo Bridges Documentation](https://docs.celo.org/tooling/bridges)
- [Celo Bridged Tokens Documentation](https://docs.celo.org/home/bridged-tokens)
- [Celo Bridge Providers](https://docs.celo.org/home/bridged-tokens/bridges)
- [Celo Cross-Chain Messaging Documentation](https://docs.celo.org/tooling/bridges/cross-chain-messaging)
- [ClawHub Skill Page](https://clawhub.ai/san-npm/skills/bridging)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with TypeScript and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bridge provider links, contract addresses, token mappings, dependency snippets, timing notes, fee considerations, and safety checks.]

## Skill Version(s):

1.0.2008 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
