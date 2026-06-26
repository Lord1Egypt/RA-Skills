## Description: <br>
Analyzes source-code logic, generates Mermaid flowcharts or SVG architecture diagrams, and renders high-resolution PNG images with themes, visual styles, semantic shapes, and product icons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a source file or codebase and produce Chinese Markdown explanations, Mermaid or SVG diagram source, and rendered PNG diagrams for documentation, architecture review, and onboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the code selected for diagramming, which may include proprietary or sensitive implementation details. <br>
Mitigation: Run it only on code the user intends to analyze and review generated Markdown and diagrams before sharing them. <br>
Risk: Rendering depends on local Node and system tools, including beautiful-mermaid, rsvg-convert, and an optional mmdc fallback that may use npx. <br>
Mitigation: Review and pin dependencies in the deployment environment, and install mmdc explicitly if automatic npx fallback is not acceptable. <br>
Risk: Generated Markdown and PNG files may preserve sensitive names, flows, or architecture details from the input code. <br>
Mitigation: Write outputs to a controlled directory and inspect them for sensitive content before publication. <br>


## Reference(s): <br>
- [code-to-diagram README](README.md) <br>
- [Style Diagram Matrix](references/style-diagram-matrix.md) <br>
- [Semantic Shapes and Product Icons](references/icons.md) <br>
- [Optimization Plan](docs/optimization-plan.md) <br>
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhouchang1988/code-to-diagram) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown explanation with Mermaid or SVG source, rendered PNG files, and renderer path metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally from user-selected source files and diagram inputs.] <br>

## Skill Version(s): <br>
2.2.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
