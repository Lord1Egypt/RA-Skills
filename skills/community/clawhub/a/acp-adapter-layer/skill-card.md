## Description:

ACP (Agent Control Protocol) Adapter Layer for AI Native Full-Stack Software Factory provides integration between ASF multi-agent workflows and OpenClaw's ACP protocol for IDE integration, session management, and tool protocol conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alshowse-tech](https://clawhub.ai/user/alshowse-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or review an ACP adapter that bridges IDE ACP clients to OpenClaw and ASF sessions, prompts, tool calls, and streaming updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can pass prompts and session history to a local OpenClaw gateway.

Mitigation: Use it only with a trusted local OpenClaw gateway and avoid confidential workspaces until session-history retention and deletion controls are reviewed.

Risk: The server security review reports weak validation and session isolation.

Mitigation: Require stronger input validation, cryptographically secure session IDs, and caller authorization before production use.

## Reference(s):

- [ACP Specification](https://agentclientprotocol.com/)
- [ClawHub skill page](https://clawhub.ai/alshowse-tech/skills/acp-adapter-layer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include adapter design notes, JSON-RPC message handling patterns, session-management guidance, and TypeScript implementation snippets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
