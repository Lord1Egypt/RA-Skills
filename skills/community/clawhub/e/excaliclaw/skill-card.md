## Description: <br>
Creates reliable Excalidraw diagrams in OpenClaw using the Excalidraw MCP, export-safe labels, Excalifont text, and clear system-diagram structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickytonline](https://clawhub.ai/user/nickytonline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and other OpenClaw users use this skill to create editable Excalidraw architecture diagrams, system diagrams, flowcharts, and hand-drawn diagrams with preview and export checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require Excalidraw MCP installation, configuration changes, or saved preferences. <br>
Mitigation: Require explicit user approval before MCP installation or configuration changes and verify availability with a minimal Excalidraw scene. <br>
Risk: Exported excalidraw.com links can be empty, simplified, or different from the previewed scene. <br>
Mitigation: Preview first, export the same full native Excalidraw scene, verify the link is non-empty, and disclose any simplified fallback. <br>
Risk: Diagram labels or arrows may lose editability if Excalidraw metadata is flattened during export. <br>
Mitigation: Use explicit text elements, preserve container and binding metadata, and audit semantic connectors before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickytonline/excaliclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, text, markdown] <br>
**Output Format:** [Markdown replies with Excalidraw scene JSON guidance, MCP workflow steps, and editable excalidraw.com links when export succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal output includes preview-before-export checks, non-empty link verification, and disclosed fallbacks such as Excalidraw JSON, SVG/PNG, Mermaid, or another diagram format when MCP export is unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
