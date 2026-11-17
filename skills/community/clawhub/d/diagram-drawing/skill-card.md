## Description:

Generate high-quality SVG and PNG technical diagrams from natural language, including architecture, flowchart, sequence, UML, mind maps, and AI agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agents use this skill to turn natural-language system or process descriptions into SVG and PNG diagrams for documentation, presentations, and architecture review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may cause an agent to generate diagram files when the user intended only a conceptual explanation.

Mitigation: Be explicit about whether a diagram should be created before invoking the skill.

Risk: The skill writes local SVG and PNG files, which can overwrite or clutter shared or important directories if paths are unclear.

Mitigation: Specify the output directory and filename before generation, especially in shared workspaces.

Risk: PNG export depends on locally available conversion backends such as rsvg-convert, CairoSVG, or svglib with Pillow.

Mitigation: Confirm a supported SVG-to-PNG converter is installed or keep the SVG as the primary output.

## Reference(s):

- [Icon Reference](references/icons.md)
- [Style Reference Guide](references/styles.md)
- [Diagram Drawing ClawHub Skill Page](https://clawhub.ai/0xcjl/skills/diagram-drawing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown response with generated SVG code, PNG conversion commands, and local SVG/PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local SVG and PNG diagram files; PNG export defaults to 1920px width unless a custom output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
