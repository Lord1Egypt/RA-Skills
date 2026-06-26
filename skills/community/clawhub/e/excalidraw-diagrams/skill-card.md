## Description: <br>
Generates Excalidraw diagrams from text content in Obsidian Markdown or standard .excalidraw JSON formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ricardodpalmeida](https://clawhub.ai/user/Ricardodpalmeida) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and Obsidian users use this skill to turn architecture diagrams, flowcharts, concept maps, sequence flows, system designs, and other visual structures into Excalidraw-compatible files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite local diagram files, including files inside an Obsidian vault. <br>
Mitigation: Confirm the full save path and filename before writing, and require explicit approval before overwriting an existing file. <br>
Risk: Generated diagrams may encode an incomplete or inaccurate interpretation of the user's source material. <br>
Mitigation: Review the diagram content and Excalidraw output before relying on it or adding it to shared documentation. <br>


## Reference(s): <br>
- [Excalidraw JSON Format Reference](references/excalidraw-format.md) <br>
- [Obsidian Excalidraw Plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin) <br>
- [Excalidraw](https://excalidraw.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/Ricardodpalmeida/excalidraw-diagrams) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Configuration] <br>
**Output Format:** [Markdown wrapping Excalidraw JSON for Obsidian, or standard Excalidraw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation for output mode, save path, filename, and overwrites before writing files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
