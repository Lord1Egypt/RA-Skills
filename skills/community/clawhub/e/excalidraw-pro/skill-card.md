## Description: <br>
Generate Excalidraw diagrams (.excalidraw files) from natural language descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jannik689](https://clawhub.ai/user/jannik689) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and other agent users use this skill to turn natural language diagram requests into Excalidraw flowcharts, architecture diagrams, mind maps, and sequence diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script that creates or overwrites JSON and .excalidraw files. <br>
Mitigation: Use deliberate output names and check for existing files before generation. <br>
Risk: Diagram labels and descriptions are saved into generated files. <br>
Mitigation: Avoid including secrets, credentials, or sensitive internal data in diagram text. <br>
Risk: Invalid diagram JSON or mismatched node references can cause generation to fail. <br>
Mitigation: Validate JSON syntax and ensure edges, actors, and node IDs reference declared items. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/jannik689/excalidraw-pro) <br>
- [Excalidraw](https://excalidraw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, shell commands, guidance] <br>
**Output Format:** [Structured JSON input, .excalidraw files, and concise Markdown status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates diagram_input.json and .excalidraw files in the workspace when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
