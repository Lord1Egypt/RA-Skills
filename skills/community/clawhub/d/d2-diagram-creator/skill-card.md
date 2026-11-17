## Description:

D2 Diagram Creator converts natural-language diagram requests into D2 code and optional SVG, PNG, or text preview outputs for flowcharts, architecture diagrams, org charts, topology maps, state machines, swimlanes, sequences, SQL relationship diagrams, and grids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huta0kj](https://clawhub.ai/user/huta0kj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, writers, and analysts use this skill to turn natural-language structure descriptions into D2 diagrams. It supports requirement gathering, D2 code generation, validation, and optional export to SVG, PNG, or text preview formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security evidence flags remote installer instructions as unsafe.

Mitigation: Review installation steps before use and prefer official package-manager or verified release installation for D2 and Tala.

Risk: The validator behavior requires removing Tala's unlicensed watermark from SVG output.

Mitigation: Remove or disable the watermark-removal instruction and script so generated outputs preserve licensing and provenance notices.

Risk: Generated diagrams and exports may not match user intent if requirements are incomplete or validation misses a diagram-structure issue.

Mitigation: Review generated D2 code and rendered output before relying on the diagram in documentation, design, or operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huta0kj/skills/d2-diagram-creator)
- [D2 installation documentation](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md)
- [Tala layout engine](https://github.com/terrastruct/tala)
- [D2 CLI help](references/cli_help.md)
- [D2 syntax reference](references/syntax.md)
- [Architecture diagram guide](references/diagram-types/architecture.md)
- [Flowchart guide](references/diagram-types/flowchart.md)
- [Grid diagram guide](references/diagram-types/grid.md)
- [Organizational chart guide](references/diagram-types/org-chart.md)
- [Sequence diagram guide](references/diagram-types/sequence.md)
- [SQL table relationship guide](references/diagram-types/sql-table.md)
- [State machine guide](references/diagram-types/state-machine.md)
- [Swimlane diagram guide](references/diagram-types/swimlane.md)
- [Topology diagram guide](references/diagram-types/topology.md)

## Skill Output:

**Output Type(s):** [text, code, files, shell commands, configuration, guidance]

**Output Format:** [D2 code files with optional SVG, PNG, or text preview exports, plus a concise validation summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the D2 CLI for validation and export; Tala layout requires separate installation and should preserve licensing and provenance notices.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
