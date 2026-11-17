## Description:

Create and edit draw.io diagrams through the configured drawio MCP server, including flowcharts, architecture diagrams, ML model diagrams, Chinese labels, animated connectors, and SVG export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyq2024](https://clawhub.ai/user/yyq2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, inspect, edit, and export draw.io diagrams for process flows, architecture and deployment views, ML model diagrams, Chinese-labeled diagrams, and animated connector workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended setup uses an unpinned third-party MCP server package.

Mitigation: Review the MCP server package before installing it and prefer a pinned, reviewed version instead of @latest.

Risk: The skill may auto-activate for broad diagram requests and can create or modify exported diagram files in the workspace.

Mitigation: Run it with only the filesystem and network access needed for diagram work, and review generated or modified diagram files before relying on them.

Risk: Diagram work depends on an externally configured drawio MCP server and the live session state.

Mitigation: Confirm the MCP connection is configured and read the current diagram before editing so existing user changes are preserved.

## Reference(s):

- [Draw.io Skill on ClawHub](https://clawhub.ai/yyq2024/skills/drawio-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown responses with draw.io XML guidance, shell setup commands, and exported .drawio or .svg files when the MCP server is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on a configured drawio MCP server and the live draw.io session state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
