## Description: <br>
Generate and edit diagrams with the mcp-diagram-generator MCP server for Draw.io, Mermaid, and Excalidraw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewyin](https://clawhub.ai/user/matthewyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical writers use this skill to turn diagram requirements into structured specifications and generated diagram files for architecture, network topology, flowchart, swimlane, UML, Mermaid, Draw.io, and Excalidraw use cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create configuration files, output directories, and diagram files, including at custom paths. <br>
Mitigation: Review requested target paths before generation, especially when editing existing files or using non-default output locations. <br>
Risk: Generated diagrams may be incorrect or misleading if the user's requirements are incomplete. <br>
Mitigation: Use the intake guide, select the appropriate playbook, and inspect generated files for expected format-specific properties before relying on the diagram. <br>


## Reference(s): <br>
- [Diagram Generator Skill Page](https://clawhub.ai/matthewyin/diagram-generator) <br>
- [Interactive Intake Guide](references/interaction-intake-guide.md) <br>
- [Format Selection Guide](references/format-selection-guide.md) <br>
- [JSON Schema Guide](references/json-schema-guide.md) <br>
- [Layout And Quality Guide](references/layout-quality-guide.md) <br>
- [Network Topology Examples](references/network-topology-examples.md) <br>
- [Architecture Diagram Playbook](references/playbook-architecture.md) <br>
- [Excalidraw Playbook](references/playbook-excalidraw.md) <br>
- [Flowchart Playbook](references/playbook-flowchart.md) <br>
- [Network Topology Playbook](references/playbook-network-topology.md) <br>
- [Swimlane Playbook](references/playbook-swimlane.md) <br>
- [UML And Data Model Playbook](references/playbook-uml.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON diagram specifications, MCP tool calls, configuration snippets, and generated diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include .drawio, .mmd, or .excalidraw outputs, with custom filenames and output paths when requested.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
