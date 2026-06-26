## Description: <br>
Generate Excalidraw diagrams from text content, with Obsidian Markdown, standard .excalidraw, and animated .excalidraw output modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axtonliu](https://clawhub.ai/user/axtonliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn structured or unstructured text into editable Excalidraw diagrams for Obsidian, excalidraw.com, or animation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger words such as diagram, flowchart, or mind map may activate the skill when a diagram file was not intended. <br>
Mitigation: Use explicit prompts for diagram generation and review whether the skill should be active in broad writing sessions. <br>
Risk: The skill creates local output files in the current working directory. <br>
Mitigation: Run it from a folder where generated diagram files are expected and review generated files before sharing or committing them. <br>
Risk: Generated diagrams may simplify or misrepresent the source text. <br>
Mitigation: Review the diagram content and layout against the original material before using it for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axtonliu/excalidraw-diagram) <br>
- [Excalidraw schema reference](references/excalidraw-schema.md) <br>
- [Excalidraw](https://excalidraw.com) <br>
- [Obsidian Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin) <br>
- [excalidraw-animate](https://dai-shi.github.io/excalidraw-animate/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Configuration, Guidance] <br>
**Output Format:** [Obsidian Markdown files or Excalidraw JSON .excalidraw files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports default Obsidian output, standard Excalidraw JSON, and animated Excalidraw JSON with animation order metadata.] <br>

## Skill Version(s): <br>
1.3.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
