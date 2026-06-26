## Description: <br>
Create professional, dark-themed SVG diagrams across architecture, flowchart, sequence, structural, mind map, timeline, state machine, data flow, and conceptual diagram types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and product teams use this skill to turn system designs, workflows, relationships, timelines, and conceptual material into standalone SVG diagrams for documentation, articles, and presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates diagram files in the workspace. <br>
Mitigation: Confirm the intended output directory before use and run it only where generated SVG and PNG files are acceptable. <br>
Risk: The skill may run Bun or `npx -y bun` to create a PNG in addition to the SVG. <br>
Mitigation: Review the conversion step before execution, especially in restricted environments or workspaces where package execution is not allowed. <br>
Risk: Generated diagrams can misrepresent complex systems if the source description is incomplete or ambiguous. <br>
Mitigation: Review the generated diagram for correct labels, relationships, and layout before publishing or sharing it. <br>


## Reference(s): <br>
- [Baoyu Diagram on ClawHub](https://clawhub.ai/jimliu/baoyu-diagram) <br>
- [Architecture Diagram Layout](artifact/references/architecture.md) <br>
- [Flowchart Layout](artifact/references/flowchart.md) <br>
- [Sequence Diagram Layout](artifact/references/sequence.md) <br>
- [Structural Diagram Layout](artifact/references/structural.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with standalone SVG file output and optional PNG conversion command or status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates diagram files in the workspace; may also run Bun or npx to generate an @2x PNG from the SVG.] <br>

## Skill Version(s): <br>
1.117.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
