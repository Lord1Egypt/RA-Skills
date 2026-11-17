## Description:

Use when the user wants to create, edit, or inspect an architectural floor plan / building layout as code — e.g. "draw a 2-bedroom apartment", "add a bathroom to this plan", "make the bedroom 1 m wider", "lay out an office floor". ArchLang is a tiny text language that compiles a .arch file to a professional floor-plan drawing (SVG/PNG/PDF/DXF). Drive it entirely through the `archlang` CLI; do not hand-render.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanmeng666](https://clawhub.ai/user/chanmeng666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use ArchLang to author, edit, and inspect architectural floor plans as text and compile them into drawing or plan data formats. The CLI also checks plans and reports rooms, areas, adjacency, and material quantities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious because its setup and examples repeatedly run unpinned npm packages, creating supply-chain risk; the scan found no clear malicious behavior and inspected only one Markdown file.

Mitigation: Review the package and install steps, and use a fixed package version before execution. Review how playground links handle plan data before sharing them.

## Reference(s):

- [ArchLang Intent Schema](https://archlang.uk/intent.schema.json)
- [ArchLang Plan Schema](https://archlang.uk/plan.schema.json)
- [ArchLang GBNF Grammar](https://archlang.uk/archlang.gbnf)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [ArchLang (.arch) source and SVG, DXF, TXT, PDF, PNG, or Plan JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The selected drawing or data format depends on the CLI options.]

## Skill Version(s):

1.63.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
