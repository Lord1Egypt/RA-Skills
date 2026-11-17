## Description:

Trade on CSPR.trade DEX (Casper Network) for swaps, liquidity, and portfolio queries through the cspr-trade MCP server, with non-custodial transactions built remotely and signed locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mssteuer](https://clawhub.ai/user/mssteuer)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect CSPR.trade market data, prepare Casper DEX swaps or liquidity actions, and guide confirmed signing and submission workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may sign remotely built blockchain transactions without enough local validation.

Mitigation: Verify transaction details with a trusted wallet or local decoder before signing, and require explicit user confirmation before every signing operation.

Risk: The local signer can use sensitive key material from environment variables.

Mitigation: Prefer key-file based signer configuration, avoid inline private keys or mnemonics when possible, and keep signer environment variables isolated from unrelated processes.

Risk: Self-hosted setup may run unpinned npm package code.

Mitigation: Pin the npm package version before using local signer or self-hosted workflows.

## Reference(s):

- [CSPR.trade MCP homepage](https://mcp.cspr.trade)
- [cspr-trade MCP repository](https://github.com/make-software/cspr-trade-mcp)
- [ClawHub skill page](https://clawhub.ai/mssteuer/skills/cspr-trade-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, API Calls]

**Output Format:** [Markdown with JSON configuration snippets and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction summaries, quote tables, warnings, and user-confirmation prompts before signing or submission.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
