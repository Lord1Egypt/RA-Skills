## Description:

Interact with Alkahest escrow contracts as a buyer, seller, or oracle using the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare CLI commands and guidance for creating, fulfilling, arbitrating, reclaiming, and inspecting Alkahest escrows and payments across supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide wallet authentication and transaction execution involving real assets.

Mitigation: Use a hardware wallet or external signer where possible, avoid placing private keys or mnemonics in prompts or shell history, and test first with low-value testnet wallets.

Risk: Incorrect chain, contract, token, amount, recipient, arbiter, demand, expiration, or approval scope can cause unintended transfers or approvals.

Mitigation: Independently verify all transaction parameters and approval scope before signing any transaction.

Risk: Installing an unpinned global CLI can expose users to supply-chain or version drift risk.

Mitigation: Prefer a pinned, locally installed, provenance-verified CLI before using the skill for asset-bearing workflows.

## Reference(s):

- [Alkahest TypeScript SDK Reference](references/typescript-sdk.md)
- [Alkahest Contract Reference](references/contracts.md)
- [Alkahest Arbiter Reference](references/arbiters.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default command output is JSON; human-readable CLI output is available with the --human flag.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
