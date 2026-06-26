## Description: <br>
Create hand-drawn style Excalidraw diagrams, flowcharts, and architecture visuals as PNG images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and technical communicators use this skill to generate Excalidraw-style diagrams, flowcharts, and architecture visuals from JSON element definitions and render them as PNG files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local Node.js execution and setup downloads. <br>
Mitigation: Review setup.sh in restricted environments and run setup or rendering without privileged permissions. <br>
Risk: Rendering workflows that use arbitrary filenames can create avoidable file-handling risk. <br>
Mitigation: Use fixed, simple temporary filenames rather than user-supplied names. <br>


## Reference(s): <br>
- [Excalidraw Element Schema Reference](references/element-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/plgonzalezrx8/excalidraw-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands] <br>
**Output Format:** [Excalidraw JSON and PNG image files with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Node.js renderer to convert Excalidraw element arrays into PNG images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
