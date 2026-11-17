## Description:

Create professional Excalidraw diagrams for flowcharts, architecture diagrams, workflows, systems, processes, and concepts, with support for DSL-based flowcharts, hand-crafted JSON diagrams, PNG rendering, and PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottgl9](https://clawhub.ai/user/scottgl9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical communicators use this skill to create, edit, render, and validate Excalidraw diagrams for processes, systems, workflows, and architecture documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses npm and uv to download and execute current third-party packages.

Mitigation: Review setup.sh before installation, avoid sudo or administrator privileges, and prefer a local-only install.

Risk: The bundled references renderer path includes a CDN import that is broader and less controlled than the primary local renderer path.

Mitigation: Avoid the references renderer path unless the CDN import is removed or explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skills/excalidraw-render)
- [Excalidraw](https://excalidraw.com)
- [Color Palette & Brand Style](references/color-palette.md)
- [Element Templates](references/element-templates.md)
- [Excalidraw JSON Schema](references/json-schema.md)
- [Layout Rules: Anti-Overlap & Text Sizing](references/layout-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Excalidraw JSON, shell commands, and rendered PNG or PDF artifacts when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams should be rendered and visually inspected before delivery.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
