## Description: <br>
Feishu Cli Board helps an agent create and manage Feishu whiteboards, including precise node layouts, architecture and flow diagrams, Mermaid or PlantUML imports, image downloads, and node export or redraw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GISwilson](https://clawhub.ai/user/GISwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to turn entities, relationships, workflows, or architecture descriptions into Feishu whiteboard diagrams. It is also useful for importing Mermaid or PlantUML diagrams, exporting whiteboard images, and rebuilding existing whiteboards through documented redraw steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or change Feishu documents and whiteboards using configured app credentials. <br>
Mitigation: Use a trusted feishu-cli installation, grant least-privilege Feishu app permissions, and review proposed commands before execution. <br>
Risk: Generic drawing requests or incorrect identifiers could target the wrong Feishu document or whiteboard. <br>
Mitigation: Confirm document and whiteboard IDs before running commands, especially when creating, importing, exporting, or rebuilding boards. <br>


## Reference(s): <br>
- [Feishu whiteboard node API reference](references/node-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/GISwilson/feishu-cli-board) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Feishu documents and whiteboards when executed with valid Feishu credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
