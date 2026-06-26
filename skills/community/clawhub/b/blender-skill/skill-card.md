## Description: <br>
Connect to and control Blender via the official Blender MCP Server, including built-in tools and Blender Python automation for Blender 5.1 and 5.2 LTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taosiuman](https://clawhub.ai/user/taosiuman) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and technical artists use this skill to connect an agent to a local Blender MCP Server for scene inspection, viewport navigation, rendering, documentation lookup, and Blender Python automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent execute Blender Python with broad local control over the running Blender session. <br>
Mitigation: Keep the MCP server bound to localhost, prefer scoped Blender tools over raw code execution, and review generated Python before running it. <br>
Risk: Rendering and screenshot tools can write files to caller-provided paths. <br>
Mitigation: Use dedicated output folders for generated renders and screenshots, and avoid sensitive project or system paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/taosiuman/blender-skill) <br>
- [Blender MCP Server](https://www.blender.org/lab/mcp-server/) <br>
- [Blender MCP Releases](https://projects.blender.org/lab/blender_mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON protocol examples, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Blender MCP tool calls, localhost connection settings, and generated bpy code; review generated Python before execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
