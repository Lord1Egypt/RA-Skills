## Description:

Use when turning presales requirements, meeting notes, or solution materials into editable business capability blueprints, swimlane flows, and application architecture diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, solution architects, and presales teams use this skill to transform requirements, meeting notes, and solution materials into canonical blueprint JSON, editable viewers, and diagram exports for business and application architecture planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted blueprint content can inject browser script into generated HTML/SVG viewers.

Mitigation: Use trusted blueprint inputs, review generated viewer/export files before opening or sharing them, and avoid opening HTML/SVG generated from untrusted external data until escaping defects are fixed.

Risk: Generated blueprint files, patch logs, viewer HTML, and export folders may contain sensitive business records.

Mitigation: Store generated artifacts in controlled workspaces, review them before external distribution, and handle patch logs and exports according to the organization's data handling rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaisersong/skills/business-blueprint)
- [README](artifact/README.md)
- [Skill routing instructions](artifact/SKILL.md)
- [Entity schema](artifact/references/entities-schema.md)
- [Systems schema](artifact/references/systems-schema.md)
- [Architecture design system](artifact/references/architecture-design-system.md)
- [Export evaluation strategy](artifact/references/test-and-eval-strategy.md)
- [Export eval inputs](artifact/evals/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON schemas, Python CLI commands, and generated blueprint/export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates canonical blueprint JSON, static HTML viewers, SVG, draw.io, Excalidraw, Mermaid, projection JSON, and validation diagnostics.]

## Skill Version(s):

0.13.0 (source: server release metadata, created 2026-04-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
