## Description:

Dexscreener CLI helps agents query DexScreener for token prices, market data, trending pools, boosted profiles, ads, transactions, and memecoin categories through CLI commands that return structured market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuefer3](https://clawhub.ai/user/zuefer3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve DexScreener token, pool, trend, and transaction data for trading research, token discovery, liquidity analysis, and market monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install an unpinned global npm package.

Mitigation: Require explicit approval before installation or upgrade, prefer a pinned or local install, and verify the intended npm package name and publisher first.

Risk: The skill evidence notes a package-name mismatch between older text and the current installation target.

Mitigation: Confirm that @kilincarslan-enterprises/dexscreener-cli is the intended package before allowing the agent to execute install commands.

## Reference(s):

- [Dexscreener CLI Repository](https://github.com/Kilincarslan-Enterprises/dexscreener-cli)
- [Dexscreener CLI NPM Package](https://www.npmjs.com/package/@kilincarslan-enterprises/dexscreener-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or table output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses are intended to be parsed from JSON by default; human-readable table output is also supported.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
