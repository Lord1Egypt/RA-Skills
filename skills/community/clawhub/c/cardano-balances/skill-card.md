## Description:

Query wallet balances, addresses, and UTxOs on the Cardano blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Cardano wallet balances, addresses, native assets, and UTxOs through a configured Cardano MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a SEED_PHRASE environment variable, which can expose wallet recovery material to the MCP process.

Mitigation: Use a watch-only address or public-key based method when possible, and do not provide a recovery phrase for a wallet holding meaningful funds unless the dependency and runtime isolation have been independently reviewed.

Risk: The release installs the external @indigoprotocol/cardano-mcp package without a pinned version in the available evidence.

Mitigation: Pin and review the package version before installation, and run it in an isolated environment appropriate for wallet-related tooling.

Risk: Cardano ADA balances are returned in lovelace and can be misread if displayed without conversion.

Mitigation: Convert lovelace to ADA for user-facing summaries and label native asset amounts clearly.

## Reference(s):

- [Cardano Balances ClawHub page](https://clawhub.ai/adacapo21/skills/cardano-balances)
- [adacapo21 publisher profile](https://clawhub.ai/user/adacapo21)
- [Cardano MCP npm package](https://www.npmjs.com/package/@indigoprotocol/cardano-mcp)
- [Wallet Balances Concepts](references/concepts.md)
- [Balances MCP Tools Reference](references/mcp-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary of balances, addresses, native assets, or UTxO details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converts lovelace to ADA for display and lists native assets with names and amounts when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
