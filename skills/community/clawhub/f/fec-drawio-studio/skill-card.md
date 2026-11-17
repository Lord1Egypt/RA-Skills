## Description:

Creates, checks, and exports editable technical diagrams in draw.io / diagrams.net format, including architecture, flowchart, UML, ERD, and code-structure diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create and validate editable technical diagrams, then deliver draw.io sources and requested exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code-structure scans may inspect unintended local project files.

Mitigation: Run scanners only against the intended project directory.

Risk: Diagram URLs and CDN-rendered brand icons may expose private architecture outside the local environment.

Mitigation: For private or regulated content, deliver local .drawio files and avoid external URLs or CDN icons unless the data boundary is acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bovinphang/skills/fec-drawio-studio)
- [Data residency](references/data-residency.md)
- [Diagram patterns](references/diagram-patterns.md)
- [Flowchart quality](references/flowchart-quality.md)
- [XML and Mermaid](references/xml-and-mermaid.md)
- [Third-party notices](data/THIRD_PARTY_NOTICES.md)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Editable .drawio XML files, optional PNG/SVG/PDF/JPG exports, and a Markdown verification summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local editable source is retained; browser links and branded icons may involve external services.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
