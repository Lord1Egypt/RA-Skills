## Description:

47 Bitcoin tools for AI agents, including fee intelligence, mempool analysis, address lookups, transaction decoding, and access to an MCP server backed by the Satoshi API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bortlesboat](https://clawhub.ai/user/bortlesboat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users install this MCP server to give agents Bitcoin blockchain, mempool, fee, transaction, address, PSBT, Lightning, mining, and market lookup capabilities. The skill is useful when an agent needs Bitcoin context without operating a local Bitcoin node or managing an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party bitcoin-mcp package under the user's account.

Mitigation: Install in an isolated environment and prefer a pinned, reviewed package version before production use.

Risk: Bitcoin lookup metadata, wallet addresses, transactions, or PSBT data may be sent to the Satoshi API.

Mitigation: Avoid submitting sensitive wallet, transaction, or PSBT data unless third-party API exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bortlesboat/skills/bitcoin-mcp)
- [bitcoin-mcp PyPI package](https://pypi.org/project/bitcoin-mcp/)
- [bitcoin-mcp GitHub project](https://github.com/Bortlesboat/bitcoin-mcp)
- [Satoshi API documentation](https://bitcoinsapi.com)
- [uv installer](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs installation snippets and setup guidance; MCP tool responses depend on the bitcoin-mcp package and Satoshi API.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
