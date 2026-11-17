## Description:

Generates draw.io diagrams from natural-language requirements, writes editable draw.io XML, self-reviews layout, and exports PNG, SVG, or PDF through the local draw.io CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bruc3van](https://clawhub.ai/user/bruc3van)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to create flowcharts, architecture diagrams, UML diagrams, ER diagrams, mindmaps, and network topology diagrams as editable draw.io files and exported images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite diagram and export files in the workspace.

Mitigation: Confirm output filenames and paths before generation, especially when modifying an existing diagram.

Risk: Exporting diagrams requires running the local draw.io desktop CLI.

Mitigation: Run exports only when draw.io is already trusted in the local environment, and approve any draw.io installation separately.

Risk: Generated diagrams may contain layout, XML, or labeling mistakes.

Mitigation: Review the editable .drawio file and exported image before sharing or using the diagram in documentation.

## Reference(s):

- [Draw.io XML Best Practices](references/best-practices.md)
- [Draw.io XML Examples](references/examples.md)
- [Draw.io Desktop Releases](https://github.com/jgraph/drawio-desktop/releases)
- [Diagrams.net](https://app.diagrams.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with draw.io XML snippets and local .drawio files plus PNG, SVG, or PDF exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local draw.io desktop CLI for exports; generated diagrams should be reviewed before use.]

## Skill Version(s):

3.1.0 (source: server release metadata; artifact skill.json reports 3.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
