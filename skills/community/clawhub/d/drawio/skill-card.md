## Description:

Generate professional draw.io diagrams (ERD/database tables, class diagrams, sequence diagrams, flowcharts, architecture diagrams) and export them as PNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanmeclazcke](https://clawhub.ai/user/romanmeclazcke)

### License/Terms of Use:


## Use Case:

Developers, analysts, and technical writers use this skill to create structured draw.io diagrams for database models, UML classes, sequences, process flows, and system architectures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local diagram artifacts and exports images automatically under ./diagrams.

Mitigation: Confirm the desired filenames and formats before generation when automatic local file creation is not wanted.

Risk: Broad diagram-related trigger terms may activate the skill for requests that only mention diagrams in passing.

Mitigation: Confirm that the user wants a draw.io diagram before creating files or running the exporter.

Risk: The skill depends on a local draw.io command-line exporter.

Mitigation: Verify the drawio binary is installed and available before attempting PNG, SVG, or PDF export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romanmeclazcke/skills/drawio)
- [Skill instructions](artifact/SKILL.md)
- [ERD diagram reference](artifact/ERD.md)
- [Class diagram reference](artifact/CLASS.md)
- [Sequence diagram reference](artifact/SEQUENCE.md)
- [Flowchart reference](artifact/FLOWCHART.md)
- [Architecture diagram reference](artifact/LAYOUT.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with draw.io XML, shell commands, and generated diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local .drawio diagram files and PNG exports under ./diagrams when the draw.io command-line exporter is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
