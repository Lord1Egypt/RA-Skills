## Description:

Clude Memory teaches AI agents how to use Clude for persistent memory with semantic search, association graphs, dream cycles, and local-first MCP runtime support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebbsssss](https://clawhub.ai/user/sebbsssss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Clude Memory to configure and operate a persistent MCP memory workflow for AI agents, including when to remember, recall, forget, and manage local or cloud memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs mutable npm code for an MCP memory server.

Mitigation: Use a pinned and reviewed clude-bot version before deployment, and review the installer behavior in the target environment.

Risk: Persistent memory can retain personal context, secrets, or sensitive data if the agent stores them.

Mitigation: Tell the agent not to store sensitive personal data or secrets unless explicitly approved, and review stored or imported memories before broad use.

Risk: Cloud mode can sync memories beyond the local machine when intentionally enabled.

Mitigation: Prefer local mode unless sync is required and the user understands the data handling implications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sebbsssss/skills/clude-memory)
- [Publisher profile](https://clawhub.ai/user/sebbsssss)
- [Clude](https://clude.io)
- [npm: clude-bot](https://www.npmjs.com/package/clude-bot)
- [Clude benchmark](https://clude.io/benchmark)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool usage guidance and installation commands for local and optional cloud modes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
