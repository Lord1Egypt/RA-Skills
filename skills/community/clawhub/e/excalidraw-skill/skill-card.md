## Description: <br>
Creates Excalidraw diagrams and exports them to SVG through Kroki or to PNG and SVG with a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and technical writers use this skill to create Excalidraw diagrams, flowcharts, architecture charts, and visual explanations, then export them as SVG or PNG. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default SVG export path can send diagram contents to kroki.io. <br>
Mitigation: For sensitive diagrams, use the local CLI or a local Kroki Docker endpoint instead of the public Kroki service. <br>
Risk: Optional local setup can install a global npm package and patch local CLI files on macOS. <br>
Mitigation: Review optional global npm and macOS patch commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agents365-ai/excalidraw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Excalidraw JSON files and shell commands for SVG or PNG export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce .excalidraw JSON and SVG or PNG exports; Kroki export sends diagram content to the configured endpoint unless a local endpoint is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
