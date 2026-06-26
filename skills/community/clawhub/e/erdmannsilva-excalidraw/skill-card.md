## Description: <br>
Generate hand-drawn style diagrams, flowcharts, and architecture diagrams as PNG images from Excalidraw JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erdmannsilva](https://clawhub.ai/user/erdmannsilva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to create diagram JSON and render it into PNG images for flowcharts, architecture diagrams, and other hand-drawn style visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup downloads npm packages and font assets from external registries and CDNs. <br>
Mitigation: Review package-lock.json and run setup in an environment with appropriate network controls before using the renderer. <br>
Risk: Diagram text and generated JSON may contain sensitive information if supplied by the user. <br>
Mitigation: Review diagram content before rendering or sharing PNG outputs, and avoid including secrets unless the workflow explicitly requires them. <br>


## Reference(s): <br>
- [Excalidraw Element Schema Reference](references/element-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands; rendered diagram output is a PNG file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects Excalidraw element JSON as input to a local Node.js renderer and produces a PNG image file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact _meta.json, and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
