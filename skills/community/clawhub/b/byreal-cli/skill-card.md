## Description:

Byreal DEX (Solana) data & analytics CLI: query pools, tokens, TVL, APR, k-line charts, farmer rankings, launchpad projects, and DeFi position stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggg223399](https://clawhub.ai/user/ggg223399)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Byreal DEX analytics, inspect Solana pool and token data, and prepare wallet-backed actions through the Byreal CLI when explicitly needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and updates an unpinned global CLI package.

Mitigation: Install only from a trusted @byreal-io/byreal-cli release channel, prefer pinning or reviewing the CLI version, and avoid running self-updates blindly.

Risk: The CLI can perform wallet-backed write operations.

Mitigation: Use dry-run previews before confirmation and verify every wallet operation, recipient, amount, and slippage before execution.

Risk: Wallet credentials may be mishandled if collected outside the CLI flow.

Mitigation: Do not ask users to paste private keys in chat; direct wallet setup through the interactive byreal-cli setup flow.

## Reference(s):

- [Byreal CLI GitHub repository](https://github.com/byreal-git/byreal-cli)
- [Byreal CLI package](npm:@byreal-io/byreal-cli)
- [ClawHub skill page](https://clawhub.ai/ggg223399/skills/byreal-cli)
- [Publisher profile](https://clawhub.ai/user/ggg223399)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves full on-chain identifiers and relies on the CLI's native tables and charts for user-facing output.]

## Skill Version(s):

0.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
