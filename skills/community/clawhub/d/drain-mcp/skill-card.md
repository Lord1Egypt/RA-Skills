## Description:

MCP server for the Handshake58 AI marketplace where agents discover providers, open USDC payment channels on Polygon, and call AI services on a pay-per-use basis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimbo128](https://clawhub.ai/user/kimbo128)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure an MCP-compatible agent for Handshake58 provider discovery, payment-channel setup, and paid AI service calls. It is intended for agents that can manage wallet-funded pay-per-use requests over Polygon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wallet private key is provided to a globally installed package that can authorize spending.

Mitigation: Use a fresh low-balance wallet only, never a main wallet, and prefer a pinned audited package version in an isolated environment.

Risk: Chat content sent through provider endpoints may be visible to third-party providers.

Mitigation: Avoid sending sensitive content unless the selected provider's handling is acceptable for the use case.

Risk: Unused funds in payment channels do not return automatically after expiry.

Mitigation: Persist channel IDs and close expired channels to reclaim unspent USDC.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kimbo128/skills/drain-mcp)
- [Handshake58 website](https://handshake58.com)
- [Handshake58 provider directory](https://handshake58.com/directory)
- [drain-mcp npm package](https://www.npmjs.com/package/drain-mcp)
- [Repository listed in skill metadata](https://github.com/kimbo128/DRAIN)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operational guidance for an MCP server that uses a wallet private key and network access.]

## Skill Version(s):

1.8.0 (source: server release metadata; frontmatter lists 1.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
