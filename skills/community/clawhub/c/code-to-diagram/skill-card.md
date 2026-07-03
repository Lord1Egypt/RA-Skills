## Description: <br>
Analyzes source code logic, generates Mermaid flowcharts or SVG architecture diagrams, and renders them as PNG images with multiple themes, visual styles, semantic shapes, and product icons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect code structure and produce human-readable diagrams, Markdown documentation, and rendered PNG assets for flows, architectures, classes, states, and data models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill can automatically run external npm tooling during rendering. <br>
Mitigation: Review before installing, run npm install from the included lockfile, pin or preinstall mmdc instead of relying on npx fallback, and use the skill only on code intended for diagramming. <br>
Risk: Generated diagrams and explanations may omit or misstate code behavior if the analyzed code path is incomplete. <br>
Mitigation: Review generated Markdown, Mermaid or SVG source, and PNG output against the source code before using the diagrams for design or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/code-to-diagram) <br>
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) <br>
- [icons.md](references/icons.md) <br>
- [style-diagram-matrix.md](references/style-diagram-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with Mermaid or SVG code blocks, rendered PNG files, and terminal JSON containing generated file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Mermaid or SVG rendering paths and may invoke local npm-based tooling and rsvg-convert during diagram rendering.] <br>

## Skill Version(s): <br>
2.2.1 (source: ClawHub release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
