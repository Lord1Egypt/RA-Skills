## Description:

Integrate DeFi protocols on Celo. Use when building swaps, lending, or liquidity applications with Uniswap, Aave, Ubeswap, or other DeFi protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[san-npm](https://clawhub.ai/user/san-npm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Celo DeFi integrations for swaps, liquidity provisioning, lending, borrowing, and protocol address lookups across Uniswap, Ubeswap, Aave, and related protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated transaction examples can cause financial loss if users submit swaps, lending, borrowing, or approvals without reviewing exact transaction details.

Mitigation: Require explicit user confirmation, display transaction details before signing, use conservative slippage and deadline settings, and test integrations on Alfajores before mainnet use.

Risk: Outdated or incorrect contract addresses can route transactions to unintended contracts.

Mitigation: Verify contract addresses against official protocol documentation or Celoscan before deployment, and prefer authoritative address packages where available.

Risk: Unlimited or overly broad token approvals can expose funds if an integration or spender contract is compromised.

Mitigation: Avoid unlimited approvals and request only the minimum token allowance needed for the intended transaction.

## Reference(s):

- [Celo DeFi Contract Addresses](references/contract-addresses.md)
- [ClawHub skill release](https://clawhub.ai/san-npm/skills/celo-defi)
- [Uniswap Celo deployments](https://docs.uniswap.org/contracts/v3/reference/deployments/celo-deployments)
- [Celo Uniswap contracts](https://docs.celo.org/tooling/contracts/uniswap-contracts)
- [Ubeswap contract addresses](https://docs.ubeswap.org/code-contracts/contract-addresses)
- [Aave address book](https://github.com/bgd-labs/aave-address-book)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with TypeScript examples, JSON dependency snippets, and contract-address tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mainnet and Alfajores contract addresses for supported Celo DeFi protocols.]

## Skill Version(s):

1.0.2011 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
