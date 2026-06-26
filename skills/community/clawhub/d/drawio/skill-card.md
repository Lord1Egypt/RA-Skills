## Description: <br>
Generate professional draw.io diagrams for ERDs, database tables, UML class diagrams, sequence diagrams, flowcharts, and architecture diagrams, then export them as PNG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romanmeclazcke](https://clawhub.ai/user/romanmeclazcke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and technical teams use this skill to turn requests for ERDs, UML class diagrams, sequence diagrams, flowcharts, and architecture overviews into draw.io XML and exported diagram images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local draw.io executable and runs export commands for generated diagrams. <br>
Mitigation: Install draw.io from an official or trusted source and review export commands before execution. <br>
Risk: The skill writes local diagram files under ./diagrams and may create PNG, SVG, or PDF outputs. <br>
Mitigation: Run it in an appropriate workspace and confirm requested output formats before generating files. <br>
Risk: Ambiguous prompts can lead to the wrong diagram type or export behavior. <br>
Mitigation: Use clear prompts that state the desired diagram type and whether an actual draw.io export is wanted. <br>


## Reference(s): <br>
- [Draw.io Professional Diagrams on ClawHub](https://clawhub.ai/romanmeclazcke/drawio) <br>
- [romanmeclazcke publisher profile](https://clawhub.ai/user/romanmeclazcke) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [ERD diagram reference](artifact/ERD.md) <br>
- [UML class diagram reference](artifact/CLASS.md) <br>
- [Sequence diagram reference](artifact/SEQUENCE.md) <br>
- [Flowchart reference](artifact/FLOWCHART.md) <br>
- [Architecture diagram reference](artifact/LAYOUT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with draw.io XML, shell commands, and local diagram files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates ./diagrams/*.drawio and exports PNG first; SVG and PDF exports are optional when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
