## Description: <br>
Convert natural language to UML diagrams, export editable PPT/EMF with individually editable shapes in PowerPoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjilei123-1](https://clawhub.ai/user/zhangjilei123-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn natural-language UML requests into PlantUML source and export diagrams as PPTX, EMF, SVG, or PNG files. It is especially useful when the final diagram must be editable in PowerPoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run an external PlantUML Java JAR without user approval or integrity verification. <br>
Mitigation: Review before installing, prefer manually installed dependencies from trusted sources, verify the PlantUML JAR checksum or signature, use a virtual environment with pinned dependencies, and run only where generated files and tool execution are acceptable. <br>
Risk: Diagram export depends on local Java, Inkscape, and Python packages, so missing or untrusted dependencies can block output or add execution risk. <br>
Mitigation: Install Java, Inkscape, pillow, and python-pptx from trusted sources before use and validate the environment before running conversion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangjilei123-1/auto-plantuml-edit) <br>
- [PlantUML 1.2026.2 JAR release](https://github.com/plantuml/plantuml/releases/download/v1.2026.2/plantuml-1.2026.2.jar) <br>
- [Inkscape releases](https://inkscape.org/release/) <br>
- [Adoptium Temurin JDK 8 releases](https://adoptium.net/zh-CN/temurin/releases?version=8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PlantUML code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .puml, .pptx, .emf, .svg, and .png files in the workspace when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
