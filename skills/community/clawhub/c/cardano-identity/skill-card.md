## Description:

Resolve and list ADAHandles for the connected Cardano wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Cardano wallet users use this skill to retrieve ADAHandles owned by a connected wallet and present human-readable wallet identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Cardano wallet seed phrase for read-only ADAHandle lookup, and exposure of a recovery phrase can compromise the wallet.

Mitigation: Review the external MCP package before installing, avoid using high-value wallets, and prefer a read-only credential such as a public address or stake address when available.

Risk: The MCP dependency is referenced by package name without a pinned reviewed version in the release evidence.

Mitigation: Pin the dependency to a reviewed version and re-run security review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adacapo21/skills/cardano-identity)
- [ADAHandle Concepts](references/concepts.md)
- [Identity MCP Tools Reference](references/mcp-tools.md)
- [ADAHandle](https://handle.me/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with ADAHandle lists and wallet identity guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running @indigoprotocol/cardano-mcp server and SEED_PHRASE environment variable.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
