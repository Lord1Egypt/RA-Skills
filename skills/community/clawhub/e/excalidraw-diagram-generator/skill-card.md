## Description: <br>
Generate Excalidraw diagrams from natural language descriptions and output .excalidraw JSON files that can be opened in Excalidraw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elihuvillaraus](https://clawhub.ai/user/elihuvillaraus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and technical teams use this skill to turn process descriptions, system relationships, data flows, class structures, sequence flows, and other concepts into editable Excalidraw diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional icon workflows can involve local helper scripts and externally downloaded icon libraries. <br>
Mitigation: Inspect helper scripts before running them and keep icon libraries inside the skill's intended libraries directory. <br>
Risk: Generated diagrams may expose sensitive architecture, workflow, or business details from the user's prompt. <br>
Mitigation: Review generated diagrams before sharing and remove sensitive details when the prompt includes confidential information. <br>
Risk: Complex requests can produce crowded or misleading diagrams. <br>
Mitigation: Review the output for accuracy and split large diagrams into focused sub-diagrams when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elihuvillaraus/excalidraw-diagram-generator) <br>
- [Excalidraw JSON Schema Reference](references/excalidraw-schema.md) <br>
- [Excalidraw Element Types Guide](references/element-types.md) <br>
- [Excalidraw](https://excalidraw.com) <br>
- [Excalidraw Libraries](https://libraries.excalidraw.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [.excalidraw JSON files with a short Markdown summary and opening or setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated diagrams should use readable text, unique element IDs, consistent colors, and reasonable element counts for clarity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
