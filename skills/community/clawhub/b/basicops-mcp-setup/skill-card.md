## Description:

Install, configure, authenticate, or verify a BasicOps MCP connection in an MCP-capable environment. Use when the user wants to add BasicOps MCP, when a BasicOps operator skill reports that BasicOps MCP is missing or unauthorized, or when the user asks to connect BasicOps to OpenClaw, Codex, Claude, Cursor, or another MCP client. Prefer MCP-native configuration over raw API setup, verify the connection after configuration, and hand off to the BasicOps operator skill once the MCP surface is ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjhlarsen](https://clawhub.ai/user/hjhlarsen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an MCP-capable agent client to BasicOps, verify authentication and tool visibility, and hand off to a BasicOps operator workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A BasicOps bearer key could be exposed through chat or insecure client configuration.

Mitigation: Keep the key in a secure secret store or protected configuration, avoid echoing it, and revoke or rotate it if exposed.

Risk: The connected BasicOps tools can support changes to business data.

Mitigation: Use an account with only the access the agent needs and review enabled tool permissions before operational work.

## Reference(s):

- [BasicOps agent users](https://basicops.com/agent-users)
- [Client patterns](artifact/references/client-patterns.md)
- [Setup flow](artifact/references/setup-flow.md)
- [Verification](artifact/references/verification.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with client configuration examples and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup, authentication, verification, and handoff guidance; does not perform BasicOps operational tasks.]

## Skill Version(s):

0.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
