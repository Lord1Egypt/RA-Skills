## Description:

Analyzes source code logic and produces Mermaid flowcharts or SVG architecture diagrams, with optional PNG rendering, themes, visual styles, semantic shapes, and product icons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to turn source-code structure, control flow, data flow, and architecture into readable diagrams and supporting explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer can automatically run an unpinned npm command when Mermaid CLI is not already available.

Mitigation: Preinstall and pin a trusted Mermaid CLI, and avoid relying on the npx fallback.

Risk: The render script may delete .mmd input files after rendering.

Mitigation: Use disposable intermediate .mmd files or keep backups of important diagram sources before rendering.

Risk: PNG rendering may use a browser configuration with sandbox protections disabled.

Mitigation: Run the skill in an isolated workspace without secrets and limit inputs to trusted repository content.

## Reference(s):

- [README](README.md)
- [Style Diagram Matrix](references/style-diagram-matrix.md)
- [Icon Reference](references/icons.md)
- [Optimization Plan](docs/optimization-plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown explanations with Mermaid or SVG source, optional PNG image files, and terminal JSON path output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mermaid rendering depends on mmdc or an npx fallback; SVG rendering depends on rsvg-convert.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
