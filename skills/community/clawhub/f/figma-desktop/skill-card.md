## Description:

Figma desktop MCP skill that lets an agent use Figma Desktop's local MCP server to access Figma Make, code generation, design system management, and related design-file context without OAuth setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-qin](https://clawhub.ai/user/samuel-qin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design engineers use this skill to configure and call the Figma Desktop MCP server from an agent, so they can inspect open Figma files, generate UI code, work with design variables and components, and use Figma Make workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent access to the Figma file currently open in the desktop app.

Mitigation: Open only the intended design file and avoid sensitive projects unless agent access is required.

Risk: The workflow requires installing the global npm tool mcporter.

Mitigation: Install mcporter only from a trusted source and prefer a pinned or local installation where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samuel-qin/skills/figma-desktop)
- [Figma Desktop App Downloads](https://www.figma.com/downloads/)
- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Server Announcement](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [Figma Code Connect Documentation](https://developers.figma.com/code-connect/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Figma Desktop, an open design or FigJam file, Dev Mode access where applicable, and mcporter configured against the local MCP server.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
