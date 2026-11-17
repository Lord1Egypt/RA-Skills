## Description:

Builds Cargo AI agents that work on GTM data: picks the model, writes the prompt, attaches docs for retrieval (RAG), connects MCP tools, manages memories, and deploys releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create and configure Cargo AI agents, attach knowledge resources, connect MCP tools, manage agent memories, and deploy releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment workflows may affect existing agent settings or live releases.

Mitigation: Review the target workspace and release payload, confirm how existing settings are preserved, and try changes on a nonproduction agent first.

Risk: The skill includes chat and document operations beyond its described agent-resource tasks.

Mitigation: Review these operations with the publisher and run only the commands needed for the intended task.

Risk: The documented install command uses an unpinned CLI version.

Mitigation: Select and verify a specific CLI version before installation.

## Reference(s):

- [Cargo skills repository](https://github.com/getcargohq/cargo-skills)
- [ClawHub cargo-ai release](https://clawhub.ai/cargo-ai/skills/cargo-ai)
- [Agent examples](artifact/references/examples/agents.md)
- [MCP server examples](artifact/references/examples/mcp-servers.md)
- [Response shapes](artifact/references/response-shapes.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown guidance, Shell commands, JSON configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural guidance and examples for agent configuration, deployments, MCP connections, memories, and troubleshooting.]

## Skill Version(s):

3.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
