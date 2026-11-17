## Description:

Core Skill gives an AI agent a verifiable Agent Passport System identity, scoped delegated authority, signed action receipts, and approval-gated connection and continuity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeoess](https://clawhub.ai/user/aeoess)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents accountable identity, scoped authority, signed receipts, continuity across work boundaries, and approval-gated connection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables identity, delegation, network, and commerce-related capabilities.

Mitigation: Install only after review, set narrow delegation scopes and low spend limits, and require explicit principal approval for publishing, search, introductions, identity sharing, financial actions, and security-sensitive actions.

Risk: The skill depends on external MCP and API services and includes a quiet session-start network check.

Mitigation: Restrict MCP/server environment access and disable or avoid quiet startup checks unless external service contact is acceptable for the deployment.

Risk: The skill uses Ed25519 private keys and unpinned runtime package execution.

Mitigation: Protect private keys, use pinned and reviewed package versions, and run the skill in accounts without unnecessary valuable credentials or sensitive data.

## Reference(s):

- [APS protocol surface](references/aps.md)
- [Durable accountable continuity](references/continuity.md)
- [Connection layer](references/connect.md)
- [Agent Passport System on npm](https://www.npmjs.com/package/agent-passport-system)
- [Agent Passport System MCP on npm](https://www.npmjs.com/package/agent-passport-system-mcp)
- [Agent Passport System on PyPI](https://pypi.org/project/agent-passport-system/)
- [Agent Passport System GitHub repository](https://github.com/aeoess/agent-passport-system)
- [Remote MCP endpoint](https://mcp.aeoess.com/sse)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require npx, optional GITHUB_TOKEN for public Agora registration, remote MCP access, and principal approval for identity, connection, and delegation actions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
