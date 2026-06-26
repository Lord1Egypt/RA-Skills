## Description: <br>
Create and edit draw.io diagrams through the configured drawio MCP server, including flowcharts, architecture diagrams, ML model diagrams, Chinese labels, animated connectors, and svg export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyq2024](https://clawhub.ai/user/yyq2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, edit, and export draw.io diagrams through a configured drawio MCP server, including architecture diagrams, flowcharts, ML model diagrams, and Chinese-labeled diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram contents may include sensitive architecture, deployment, or business details handled through the configured drawio MCP server. <br>
Mitigation: Use only a trusted and approved drawio MCP server, and avoid sending sensitive details unless that server is approved for the data. <br>
Risk: Installing the MCP server with an unpinned package version can introduce unreviewed server behavior over time. <br>
Mitigation: Pin the drawio MCP server package version and review or scan updates before deployment. <br>
Risk: The skill cannot create, inspect, edit, or export diagrams when the drawio MCP connection is unavailable or misconfigured. <br>
Mitigation: Configure or reconnect the drawio MCP server before use, then restart Codex or reload the IDE window if tools do not appear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yyq2024/drawio-skill) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown responses with draw.io XML, MCP tool actions, shell commands when needed, and exported .drawio or .svg files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on a configured drawio MCP server and live draw.io session state] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
