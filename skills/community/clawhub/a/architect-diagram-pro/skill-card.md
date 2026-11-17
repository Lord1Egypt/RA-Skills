## Description:

Local-first architecture and structure diagram generation tool for architecture, system, module, flowchart, sequence, state machine, network topology, ER, data-flow, microservice/cloud-native, and Gantt diagrams; it renders locally without cloud services, Node.js, or API keys and can produce self-contained HTML, inline SVG, or Mermaid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to turn architecture or process requirements into local-first diagrams for design discussions, documentation, and reviews. It is most appropriate for Chinese-first workflows needing HTML, inline SVG, or Mermaid output without external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous diagram requests can produce an incorrect or misleading structure.

Mitigation: Ask concise clarification questions about output format, diagram type, and scope before generating when intent is unclear.

Risk: Sensitive local files may be exposed in generated diagrams if users provide unnecessary inputs.

Mitigation: Use only files explicitly needed for the diagram and avoid providing sensitive files unless they are required.

Risk: Unsupported requests such as statistical charts, 3D/maps, direct PNG/PDF export, or reverse engineering may be misrepresented as supported.

Mitigation: State the unsupported capability, explain why, offer an alternative, and wait for user confirmation before proceeding.

Risk: Generated diagrams may contain layout, overlap, or arrow/text readability errors.

Mitigation: Perform semantic planning, coordinate preflight, and the documented self-check before delivery; retry after fixes when checks fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/architect-diagram-pro)
- [README](artifact/README.md)
- [Architecture layout guidelines](artifact/references/architecture-layout.md)
- [Arrow and text clearance guidelines](artifact/references/arrow-text-clearance.md)
- [Capability matrix](artifact/references/capability-matrix.md)
- [Clarification and confirmation gates](artifact/references/clarification-gate.md)
- [Diagram type guidelines](artifact/references/diagram-types.md)
- [HTML template guide](artifact/references/html-template-guide.md)
- [Self-check and error handling](artifact/references/self-check-and-errors.md)
- [SVG efficient template](artifact/references/svg-efficient-template.md)
- [Three invariants](artifact/references/three-invariants.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown responses containing planning text plus self-contained HTML, inline SVG, or Mermaid code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first output; unsupported diagram types require explanation and user confirmation before generation.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
