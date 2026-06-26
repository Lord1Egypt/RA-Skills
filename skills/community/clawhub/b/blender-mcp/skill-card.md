## Description: <br>
Advanced bridge to Blender via MCP. Allows querying scene, creating objects, applying materials, and running custom BPY code in real-time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlayZz](https://clawhub.ai/user/FlayZz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and 3D artists use this skill to connect an agent to a running Blender instance for real-time scene inspection, object creation, material application, asset import, rendering, saving, and Blender Python automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over Blender, including Python execution through `execute_code`. <br>
Mitigation: Require explicit approval before Python execution, renders, saves, or other state-changing Blender actions. <br>
Risk: The bridge runs the external `blender-mcp` package through `uvx`. <br>
Mitigation: Install only from trusted sources and verify or pin the MCP server version before use. <br>
Risk: External asset search and import can download content into the working scene. <br>
Mitigation: Review asset source, licensing, and file behavior before importing Sketchfab or PolyHaven assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FlayZz/blender-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return MCP tool results, scene details, or error messages from the Blender bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
