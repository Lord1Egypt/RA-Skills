## Description:

Arch Diagrammer helps agents create architecture, flow, sequence, and deployment diagrams as offline SVG files or browser-previewable HTML using pure SVG templates or Mermaid, PlantUML, and Graphviz through Kroki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[footya](https://clawhub.ai/user/footya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and technical teams use this skill to turn system structure, workflows, service dependencies, and deployment designs into reusable visual deliverables for design reviews and technical communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Kroki rendering can disclose diagram source to the configured rendering endpoint.

Mitigation: Use pure SVG/offline mode for confidential diagrams, verify KROKI_URL before rendering, and prefer a trusted private Kroki instance.

Risk: Generated HTML previews and CDN-based Mermaid rendering can execute mutable remote code or render untrusted diagram text.

Mitigation: Avoid opening generated HTML from untrusted diagram text or untrusted rendering endpoints, and review the preview source before sharing.

Risk: The documented npx Mermaid CLI fallback is unpinned.

Mitigation: Pin and review the Mermaid CLI version before using it in controlled or production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/footya/skills/arch-diagrammer)
- [Publisher Profile](https://clawhub.ai/user/footya)
- [Architecture Checklist](references/architecture-checklist.md)
- [Diagram Quickstart](references/diagram-quickstart.md)
- [SVG Layered Specification](references/svg-layered-spec.md)
- [Kroki](https://kroki.io)
- [Mermaid ESM CDN](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with SVG, HTML, and diagram DSL code or generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Common deliverables are .svg files for offline viewing and .html files for browser preview.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, CHANGELOG.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
