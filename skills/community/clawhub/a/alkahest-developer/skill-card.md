## Description:

Help developers write code that interacts with Alkahest escrow contracts using the TypeScript, Rust, or Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate applications, bots, and agents with Alkahest escrow contracts. It supports TypeScript, Rust, and Python SDK workflows for approving tokens, creating escrows, fulfilling obligations, collecting payments, encoding arbiter demands, and using commit-reveal or barter patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include copyable private-key and wallet transaction patterns that may approve tokens, lock funds, transfer payments, arbitrate outcomes, or slash and reclaim bonds.

Mitigation: Use testnets first, never hardcode or log private keys, verify chain IDs and contract addresses, and require explicit confirmation before signing asset-moving transactions.

Risk: The security verdict is suspicious because live-wallet usage could put assets at risk without additional safety review.

Mitigation: Review the generated code and transaction intent before installing or using the skill with live wallets or production funds.

## Reference(s):

- [Alkahest Developer Skill on ClawHub](https://clawhub.ai/mlegls/skills/alkahest-developer)
- [Alkahest TypeScript SDK API Reference](artifact/references/typescript-api.md)
- [Alkahest Rust SDK API Reference](artifact/references/rust-api.md)
- [Alkahest Python SDK API Reference](artifact/references/python-api.md)
- [Alkahest Contract Reference](artifact/references/contracts.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with language-specific code examples and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet, RPC, chain, contract-address, approval, escrow, fulfillment, arbitration, and transaction-signing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
