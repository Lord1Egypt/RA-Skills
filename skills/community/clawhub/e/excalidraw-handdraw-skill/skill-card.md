## Description: <br>
Generates hand-drawn Excalidraw-style diagrams from prompts, including architecture diagrams, flowcharts, ER diagrams, PNG/SVG exports, saved image files, and optional insertion or replacement in Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenyangze](https://clawhub.ai/user/zhenyangze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to turn prompt descriptions into hand-drawn style diagrams, export them as images, save them to project paths, and insert or replace diagram references in documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start a local Docker canvas service. <br>
Mitigation: Review the referenced scripts before use, confirm Docker activity is expected, and stop the canvas container when work is complete. <br>
Risk: The skill can save image files and insert or replace image references in project files. <br>
Mitigation: Confirm destination paths and document edits before execution, then review generated or modified files before committing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhenyangze/excalidraw-handdraw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON element examples, and generated image file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create PNG or SVG files and modify Markdown files when the user requests saved or inserted diagrams.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
