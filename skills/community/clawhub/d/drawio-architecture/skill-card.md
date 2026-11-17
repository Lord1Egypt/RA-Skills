## Description:

Use when generating or editing draw.io/diagrams.net architecture diagrams via MCP or native XML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, edit, validate, and deliver editable draw.io/diagrams.net architecture, network, cloud, flowchart, ER, UML, and C4-style diagrams. It supports MCP-driven editor opening, native draw.io XML authoring, local CLI export, and platform-specific MCP configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled setup helper can persist an unpinned remote draw.io MCP server command into agent configuration files.

Mitigation: Review configuration changes before applying them and pin @drawio/mcp to an explicit verified version.

Risk: Using the hosted draw.io MCP endpoint can send diagram XML to the draw.io vendor service.

Mitigation: Use local stdio MCP or a trusted self-hosted draw.io instance for sensitive architecture diagrams.

Risk: Bare npx execution can download and run the latest remote package at runtime.

Mitigation: Avoid bare npx -y @drawio/mcp and use npx -y @drawio/mcp@<VERSION> after checking the package and publisher.

## Reference(s):

- [Draw.io MCP Server Documentation](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/)
- [drawio-mcp GitHub Repository](https://github.com/jgraph/drawio-mcp)
- [@drawio/mcp npm Package](https://www.npmjs.com/package/@drawio/mcp)
- [Afonsoft Skills Repository](https://github.com/afonsoft/skills)
- [Agents365 drawio-skill Source](https://github.com/Agents365-ai/drawio-skill)
- [scarr05 claude-skills-pub Source](https://github.com/scarr05/claude-skills-pub)
- [MCP Server Configuration](references/mcp-config.md)
- [MCP Tools Reference](references/mcp-tools-reference.md)
- [Architecture Diagram Patterns](references/architecture-patterns.md)
- [Cloud Provider Icons](references/cloud-icons.md)
- [Usage Guide](references/usage-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with draw.io XML, Mermaid, CSV, JSON configuration snippets, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open diagrams through draw.io MCP tools or produce local .drawio, PNG, SVG, or PDF delivery guidance when supported by the agent environment.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
