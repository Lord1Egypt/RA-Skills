## Description:

Execute irreversible on-chain DeFi operations through ChainStream CLI and MCP tools, including token swaps, launchpad token creation, transaction signing, broadcasting, and trading workflows with explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harry5556](https://clawhub.ai/user/harry5556)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through wallet-backed DeFi execution on supported chains, including route building, token creation, transaction signing, broadcast, and post-transaction status reporting. It is intended for workflows where the user can review every transaction and explicitly confirm before funds move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports real, irreversible DeFi transactions and signing workflows.

Mitigation: Use dedicated low-balance wallets, show transaction details before signing, and require explicit user confirmation for every destructive action.

Risk: The release relies on mutable or unpinned external tools and setup paths.

Mitigation: Prefer pinned, reviewed CLI and wallet tooling before operational use, and review external setup commands before running them.

Risk: Raw private-key import paths can expose valuable wallets if misused.

Mitigation: Avoid importing valuable raw private keys; use isolated test or low-balance wallets for agent-driven workflows.

## Reference(s):

- [Swap Protocol Reference](artifact/references/swap-protocol.md)
- [Launchpad Reference](artifact/references/launchpad.md)
- [Currency Resolution](artifact/references/currency-resolution.md)
- [Authentication](artifact/shared/authentication.md)
- [Payment Protocols](artifact/shared/x402-payment.md)
- [Supported Chains](artifact/shared/chains.md)
- [ClawHub skill page](https://clawhub.ai/harry5556/skills/chainstream-defi)
- [ChainStream MCP server](https://mcp.chainstream.io/mcp)
- [ChainStream documentation](https://docs.chainstream.io)
- [ChainStream API reference](https://docs.chainstream.io/api-reference)
- [ChainStream CLI README](https://github.com/chainstream-io/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands, transaction summaries, confirmations, JSON snippets, and explorer links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before destructive on-chain signing or broadcast; outputs may include transaction hashes, job IDs, and block explorer links.]

## Skill Version(s):

1.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
