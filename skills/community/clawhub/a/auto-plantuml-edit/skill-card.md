## Description:

Convert natural language to UML diagrams, export editable PPT/EMF with individually editable shapes in PowerPoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjilei123-1](https://clawhub.ai/user/zhangjilei123-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to turn natural-language diagram requests into PlantUML source and export UML diagrams as PPTX, EMF, SVG, or PNG files. It is most useful when the final diagram needs to be editable in PowerPoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download and execute an external PlantUML JAR.

Mitigation: Require explicit user approval before downloading it and verify the JAR with a trusted checksum or signature before execution.

Risk: Processing untrusted .puml or SVG content through Java and Inkscape can expose the runtime to parser or converter vulnerabilities.

Mitigation: Run the workflow in a sandbox or low-privilege environment and avoid untrusted diagram inputs unless isolation is in place.

Risk: Unpinned Python dependencies may resolve to unexpected package versions.

Mitigation: Pin and review Python dependencies before installing or running the converter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangjilei123-1/skills/auto-plantuml-edit)
- [PlantUML 1.2026.2 JAR release](https://github.com/plantuml/plantuml/releases/download/v1.2026.2/plantuml-1.2026.2.jar)
- [Inkscape releases](https://inkscape.org/release/)
- [Adoptium Temurin JDK releases](https://adoptium.net/zh-CN/temurin/releases?version=8)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with PlantUML code blocks and shell commands; generated artifacts may include .puml, .pptx, .emf, .svg, or .png files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PPTX and EMF outputs are intended to be ungrouped and edited in PowerPoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
